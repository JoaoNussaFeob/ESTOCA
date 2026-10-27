import csv,sqlite3,json
from pathlib import Path
from collections import Counter
from math import ceil
R=Path(__file__).resolve().parents[1]
def read(name):
    return list(csv.DictReader((R/'dados'/name).open(encoding='utf-8-sig'),delimiter=';'))
db=sqlite3.connect(':memory:');db.executescript((R/'banco/base_completa_sqlite.sql').read_text())
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name)
check('SQLite: integridade estrutural',db.execute('PRAGMA integrity_check').fetchone()[0]=='ok')
check('SQLite: referências válidas',not db.execute('PRAGMA foreign_key_check').fetchall())
days=read('demanda_diaria.csv');orders=read('pedidos_planejados.csv');stocks=read('estoque_14_dias.csv');projection=read('saldos_projetados.csv')
check('14 dias de planejamento',len(days)==14)
byday=Counter()
for r in orders:byday[r['data']]+=int(r['quantidade'])
check('Pedidos coincidem com demanda em todos os dias',all(byday[d['data']]==int(d['total']) for d in days))
check('Saldo não negativo nos 742 pares produto/dia',all(int(x['saldo_projetado'])>=0 for x in projection))
check('Compra total cobre consumo mais margem global',all(int(x['total_compras'])>=int(x['meta_global_15pct']) for x in stocks))
check('Abertura mais reposições equivale a compra total',all(int(x['estoque_inicial'])+int(x['reposicao_14d'])==int(x['total_compras']) for x in stocks))
check('Saldo final reconciliado',all(int(x['total_compras'])-int(x['consumo_14d'])==int(x['saldo_final']) for x in stocks))
check('Somente abertura foi efetivada no banco',db.execute("SELECT COUNT(*) FROM movimento WHERE tipo<>'SALDO_INICIAL'").fetchone()[0]==0)
for x in stocks:
    assert db.execute('SELECT saldo FROM saldo_atual WHERE codigo=?',(x['produto'],)).fetchone()[0]==int(x['estoque_inicial'])
check('Todos os saldos iniciais coincidem com CSV',True)
backup=Counter();margin=json.loads((R/'dados/premissas.json').read_text())['margem_seguranca']
for r in projection:
    backup[r['produto']]+=int(r['entrada_planejada'])-ceil(int(r['consumo_planejado'])*(1+margin))
    assert backup[r['produto']]>=0,(r,backup[r['produto']])
check('Cenário de consumo 15% maior sem ruptura diária',True)
def rejected(label,sql,args=()):
    db.execute('SAVEPOINT negative_test')
    try:
        db.execute(sql,args)
    except sqlite3.IntegrityError:
        db.execute('ROLLBACK TO negative_test');db.execute('RELEASE negative_test');checks.append(label);return
    raise AssertionError(label)
rejected('Saída acima do saldo bloqueada',"INSERT INTO movimento(produto,tipo,delta,motivo) VALUES('frango','SAIDA',-99999999,'teste')")
rejected('Produto inexistente bloqueado',"INSERT INTO movimento(produto,tipo,delta,motivo) VALUES('ausente','ENTRADA',1,'teste')")
rejected('Quantidade zero bloqueada',"INSERT INTO movimento(produto,tipo,delta,motivo) VALUES('frango','ENTRADA',0,'teste')")
rejected('Quantidade fracionária na unidade-base bloqueada',"INSERT INTO movimento(produto,tipo,delta,motivo) VALUES('frango','ENTRADA',0.5,'teste')")
rejected('Exclusão de histórico bloqueada','DELETE FROM movimento WHERE id=1')
rejected('Edição de histórico bloqueada','UPDATE movimento SET delta=100 WHERE id=1')
rejected('Segundo saldo inicial bloqueado',"INSERT INTO movimento(produto,tipo,delta,motivo) VALUES('frango','SALDO_INICIAL',1,'teste')")
before=db.execute("SELECT saldo FROM saldo_atual WHERE codigo='frango'").fetchone()[0]
db.execute("INSERT INTO movimento(produto,tipo,delta,motivo) VALUES('frango','ENTRADA',1000,'teste')")
db.execute("INSERT INTO movimento(produto,tipo,delta,motivo) VALUES('frango','SAIDA',-500,'teste')")
check('Entrada e saída válidas alteram saldo corretamente',db.execute("SELECT saldo FROM saldo_atual WHERE codigo='frango'").fetchone()[0]==before+500)
(R/'documentacao/validacao.json').write_text(json.dumps({'resultado':'APROVADO','verificacoes':checks,'limite':'Testes locais de dados e SQLite; não validam receitas reais, conservação, capacidade física, aplicação web ou integração MySQL.'},ensure_ascii=False,indent=2))
print(f'{len(checks)} verificações aprovadas. Banco de entrega preservado.')
