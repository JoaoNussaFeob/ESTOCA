class Produto {
  final String _codigo;
  String _nome = '';
  final String _unidade;
  int _quantidade;
  int _estoqueMinimo = 0;

  Produto(
    String codigo,
    String nome,
    String unidade,
    int quantidade,
    int minimo,
  ) : _codigo = codigo.trim(),
      _unidade = unidade.trim(),
      _quantidade = quantidade {
    if (_codigo.isEmpty) {
      throw ArgumentError('O código não pode ficar vazio.');
    }
    if (!['g', 'ml', 'un'].contains(_unidade)) {
      throw ArgumentError('A unidade deve ser g, ml ou un.');
    }
    if (quantidade < 0) {
      throw ArgumentError('A quantidade não pode ser negativa.');
    }
    this.nome = nome;
    estoqueMinimo = minimo;
  }

  String get codigo => _codigo;
  String get nome => _nome;
  String get unidade => _unidade;
  int get quantidade => _quantidade;
  int get estoqueMinimo => _estoqueMinimo;

  set nome(String valor) {
    if (valor.trim().isEmpty) {
      throw ArgumentError('O nome não pode ficar vazio.');
    }
    _nome = valor.trim();
  }

  set estoqueMinimo(int valor) {
    if (valor < 0) {
      throw ArgumentError('O estoque mínimo não pode ser negativo.');
    }
    _estoqueMinimo = valor;
  }

  void registrarEntrada(int quantidade) {
    if (quantidade <= 0) {
      throw ArgumentError('A entrada deve ser positiva.');
    }
    _quantidade += quantidade;
  }

  void registrarSaida(int quantidade) {
    if (quantidade <= 0) {
      throw ArgumentError('A saída deve ser positiva.');
    }
    if (quantidade > _quantidade) {
      throw StateError('Estoque insuficiente.');
    }
    _quantidade -= quantidade;
  }

  bool precisaRepor() {
    return _quantidade < _estoqueMinimo;
  }

  int calcularReposicao() {
    if (precisaRepor()) {
      return _estoqueMinimo - _quantidade;
    }
    return 0;
  }

  int calcularPorcoes(int consumoPorPorcao) {
    if (consumoPorPorcao <= 0) {
      throw ArgumentError('O consumo por porção deve ser positivo.');
    }
    return _quantidade ~/ consumoPorPorcao;
  }
}

void main() {
  Produto frango = Produto('frango', 'Filé de frango', 'g', 1000, 500);
  frango.nome = 'Filé de peito de frango';
  frango.registrarEntrada(1000);
  frango.registrarSaida(1760);

  print('${frango.nome}: ${frango.quantidade} ${frango.unidade}');
  print('Estoque mínimo: ${frango.estoqueMinimo} ${frango.unidade}');
  print('Precisa repor: ${frango.precisaRepor()}');
  print(
    'Reposição necessária: ${frango.calcularReposicao()} ${frango.unidade}',
  );
  print('Porções de 220 g disponíveis: ${frango.calcularPorcoes(220)}');

  try {
    frango.registrarSaida(300);
  } on StateError catch (erro) {
    print(erro.message);
  }
  print('Saldo após a tentativa: ${frango.quantidade} ${frango.unidade}');
}
