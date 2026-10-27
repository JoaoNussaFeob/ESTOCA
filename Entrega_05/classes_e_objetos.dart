class Produto {
  String codigo;
  String nome;
  String unidade;
  int quantidade;

  Produto(this.codigo, this.nome, this.unidade, this.quantidade);
}

class Receita {
  String codigo;
  String nome;
  List<Ingrediente> ingredientes;

  Receita(this.codigo, this.nome, this.ingredientes);
}

class Ingrediente {
  Produto produto;
  double quantidadePorPorcao;

  Ingrediente(this.produto, this.quantidadePorPorcao);
}

class Movimentacao {
  int id;
  Produto produto;
  String tipo;
  int quantidade;
  String motivo;

  Movimentacao(this.id, this.produto, this.tipo, this.quantidade, this.motivo);
}

void main() {
  Produto frango = Produto('frango', 'Filé de frango', 'g', 202000);
  Produto arroz = Produto('arroz', 'Arroz branco', 'g', 155000);
  Ingrediente ingrediente = Ingrediente(frango, 220);
  Receita receita = Receita('frango_g', 'Frango grelhado', [ingrediente]);
  Movimentacao abertura = Movimentacao(
    1,
    frango,
    'SALDO_INICIAL',
    202000,
    'Estoque inicial fictício',
  );

  print('${frango.nome}: ${frango.quantidade} ${frango.unidade}');
  print('${arroz.nome}: ${arroz.quantidade} ${arroz.unidade}');
  print('Receita: ${receita.nome}');
  for (Ingrediente item in receita.ingredientes) {
    print(
      '${item.produto.nome}: ${item.quantidadePorPorcao} ${item.produto.unidade} por porção',
    );
  }
  print('${abertura.tipo}: ${abertura.quantidade} ${abertura.produto.unidade}');
}
