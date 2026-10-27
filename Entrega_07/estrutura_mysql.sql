CREATE DATABASE IF NOT EXISTS estoca_jk CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE estoca_jk;
CREATE TABLE categoria (
  id INT PRIMARY KEY,
  nome VARCHAR(60) NOT NULL UNIQUE
);
CREATE TABLE produto (
  codigo VARCHAR(40) PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  categoria_id INT NOT NULL,
  unidade ENUM('g','ml','un') NOT NULL,
  embalagem INT NOT NULL CHECK (embalagem > 0),
  ciclo_dias INT NOT NULL CHECK (ciclo_dias > 0),
  origem VARCHAR(255) NOT NULL,
  FOREIGN KEY (categoria_id) REFERENCES categoria(id)
);
CREATE TABLE saldo_produto (
  produto VARCHAR(40) PRIMARY KEY,
  saldo BIGINT NOT NULL DEFAULT 0 CHECK (saldo >= 0),
  FOREIGN KEY (produto) REFERENCES produto(codigo)
);
CREATE TABLE receita (
  codigo VARCHAR(40) PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  tipo ENUM('Principal','Base','Acompanhamento') NOT NULL
);
CREATE TABLE receita_ingrediente (
  receita VARCHAR(40) NOT NULL,
  produto VARCHAR(40) NOT NULL,
  quantidade_base_por_M DECIMAL(12,4) NOT NULL CHECK (quantidade_base_por_M > 0),
  PRIMARY KEY (receita,produto),
  FOREIGN KEY (receita) REFERENCES receita(codigo),
  FOREIGN KEY (produto) REFERENCES produto(codigo)
);
CREATE TABLE demanda_diaria (
  data DATE PRIMARY KEY,
  dia INT NOT NULL UNIQUE CHECK (dia BETWEEN 1 AND 14),
  tradicional INT NOT NULL CHECK (tradicional >= 0),
  fitness INT NOT NULL CHECK (fitness >= 0),
  delivery INT NOT NULL CHECK (delivery >= 0),
  variante ENUM('A','B','C','D') NOT NULL,
  CHECK (delivery <= tradicional+fitness)
);
CREATE TABLE pedido_planejado (
  id INT PRIMARY KEY,
  data DATE NOT NULL,
  linha ENUM('trad','fit') NOT NULL,
  principal VARCHAR(40) NOT NULL,
  tamanho ENUM('P','M','G','U') NOT NULL,
  quantidade INT NOT NULL CHECK (quantidade > 0),
  CHECK ((linha='fit' AND tamanho='U') OR (linha='trad' AND tamanho IN ('P','M','G'))),
  FOREIGN KEY (data) REFERENCES demanda_diaria(data),
  FOREIGN KEY (principal) REFERENCES receita(codigo)
);
CREATE TABLE consumo_planejado (
  data DATE NOT NULL,
  produto VARCHAR(40) NOT NULL,
  quantidade_base BIGINT NOT NULL CHECK (quantidade_base >= 0),
  PRIMARY KEY (data,produto),
  FOREIGN KEY (data) REFERENCES demanda_diaria(data),
  FOREIGN KEY (produto) REFERENCES produto(codigo)
);
CREATE TABLE recebimento_planejado (
  id INT PRIMARY KEY,
  data DATE NOT NULL,
  produto VARCHAR(40) NOT NULL,
  quantidade_base BIGINT NOT NULL CHECK (quantidade_base > 0),
  FOREIGN KEY (data) REFERENCES demanda_diaria(data),
  FOREIGN KEY (produto) REFERENCES produto(codigo)
);
CREATE TABLE movimento (
  id INT PRIMARY KEY AUTO_INCREMENT,
  produto VARCHAR(40) NOT NULL,
  tipo ENUM('SALDO_INICIAL','ENTRADA','SAIDA') NOT NULL,
  delta BIGINT NOT NULL,
  motivo VARCHAR(255) NOT NULL CHECK (CHAR_LENGTH(TRIM(motivo)) > 0),
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  abertura_produto VARCHAR(40) GENERATED ALWAYS AS (CASE WHEN tipo='SALDO_INICIAL' THEN produto ELSE NULL END) STORED,
  UNIQUE (abertura_produto),
  CHECK ((tipo IN ('SALDO_INICIAL','ENTRADA') AND delta > 0) OR (tipo='SAIDA' AND delta < 0)),
  FOREIGN KEY (produto) REFERENCES produto(codigo)
);
CREATE TABLE calendario (
  data DATE PRIMARY KEY
);
CREATE TABLE venda_exemplo (
  id INT PRIMARY KEY,
  data DATE NOT NULL,
  valor_centavos INT NOT NULL CHECK (valor_centavos >= 0),
  FOREIGN KEY (data) REFERENCES calendario(data)
);
DELIMITER $$
CREATE TRIGGER criar_saldo AFTER INSERT ON produto FOR EACH ROW
BEGIN
  INSERT INTO saldo_produto(produto,saldo) VALUES(NEW.codigo,0);
END$$
CREATE TRIGGER validar_abertura BEFORE INSERT ON movimento FOR EACH ROW
BEGIN
  IF NEW.tipo='SALDO_INICIAL' AND EXISTS(SELECT 1 FROM movimento WHERE produto=NEW.produto) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='A abertura deve ser o primeiro movimento';
  END IF;
END$$
CREATE TRIGGER atualizar_saldo AFTER INSERT ON movimento FOR EACH ROW
BEGIN
  UPDATE saldo_produto SET saldo=saldo+NEW.delta
  WHERE produto=NEW.produto AND saldo+NEW.delta>=0;
  IF ROW_COUNT()<>1 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Estoque insuficiente';
  END IF;
END$$
CREATE TRIGGER impedir_edicao_movimento BEFORE UPDATE ON movimento FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Historico de movimentos imutavel';
END$$
CREATE TRIGGER impedir_exclusao_movimento BEFORE DELETE ON movimento FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Historico de movimentos imutavel';
END$$
DELIMITER ;
CREATE VIEW vw_produtos AS
SELECT p.codigo,p.nome,c.nome AS categoria,p.unidade,p.embalagem,p.ciclo_dias,p.origem
FROM produto p JOIN categoria c ON c.id=p.categoria_id;
CREATE VIEW vw_receitas AS SELECT codigo,nome,tipo FROM receita;
CREATE VIEW vw_ingredientes AS SELECT receita,produto,quantidade_base_por_M FROM receita_ingrediente;
CREATE VIEW vw_demanda AS
SELECT data,dia,tradicional+fitness AS total,tradicional,fitness,delivery,variante FROM demanda_diaria;
CREATE VIEW vw_pedidos AS
SELECT p.id,p.data,p.linha,p.principal,p.tamanho,p.quantidade,d.variante
FROM pedido_planejado p JOIN demanda_diaria d ON d.data=p.data;
CREATE VIEW vw_consumo AS
SELECT c.data,d.dia,c.produto,c.quantidade_base FROM consumo_planejado c JOIN demanda_diaria d ON d.data=c.data;
CREATE VIEW vw_recebimentos AS
SELECT r.id,r.data,d.dia,r.produto,r.quantidade_base,
CAST(r.quantidade_base/p.embalagem AS UNSIGNED) AS pacotes,
CASE WHEN d.dia=1 THEN 'INICIAL' ELSE 'PREVISTO' END AS estado
FROM recebimento_planejado r JOIN demanda_diaria d ON d.data=r.data JOIN produto p ON p.codigo=r.produto;
CREATE VIEW vw_movimentos AS SELECT id,produto,tipo,delta,motivo,criado_em FROM movimento;
CREATE VIEW vw_calendario AS SELECT data,WEEKDAY(data)+1 AS dia_semana,CASE WHEN WEEKDAY(data)>=5 THEN 1 ELSE 0 END AS fim_semana FROM calendario;
CREATE VIEW vw_vendasexemplo AS SELECT id,data,valor_centavos FROM venda_exemplo;
CREATE VIEW vw_saldo_atual AS SELECT p.codigo,p.nome,p.unidade,s.saldo FROM produto p JOIN saldo_produto s ON s.produto=p.codigo;
CREATE VIEW vw_conferencia_saldo AS
SELECT s.produto,s.saldo,COALESCE(SUM(m.delta),0) AS saldo_historico,
s.saldo-COALESCE(SUM(m.delta),0) AS diferenca FROM saldo_produto s LEFT JOIN movimento m ON m.produto=s.produto
GROUP BY s.produto,s.saldo;
