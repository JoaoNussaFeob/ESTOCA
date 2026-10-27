import 'dart:async';
import '../Entrega_05/classes_e_objetos.dart' as e05;
import '../Entrega_08/repeticao_e_colecoes.dart' as e08;
import '../Entrega_09/encapsulamento_e_validacao.dart' as e09;

int testes = 0;

void conferir(bool resultado, String nome) {
  if (!resultado) {
    throw StateError('Falhou: $nome');
  }
  testes++;
}

void rejeitar(void Function() acao, String nome) {
  bool rejeitou = false;
  try {
    acao();
  } on ArgumentError {
    rejeitou = true;
  } on StateError {
    rejeitou = true;
  }
  conferir(rejeitou, nome);
}

List<String> capturar(void Function() acao) {
  List<String> mensagens = [];
  runZoned(
    acao,
    zoneSpecification: ZoneSpecification(
      print: (self, parent, zone, mensagem) {
        mensagens.add(mensagem);
      },
    ),
  );
  return mensagens;
}

void main() {
  e05.Produto produto = e05.Produto('arroz', 'Arroz', 'g', 1000);
  e05.Receita receita = e05.Receita('base', 'Arroz', [
    e05.Ingrediente(produto, 60),
  ]);
  conferir(
    receita.ingredientes[0].produto.codigo == 'arroz',
    'associação de objetos',
  );
  conferir(capturar(e05.main).length == 5, 'execução da entrega 05');

  List<String> saida = capturar(e08.main);
  conferir(saida.contains('Soma: R\$ 122.00'), 'soma');
  conferir(saida.contains('Média: R\$ 24.40'), 'média');
  conferir(saida.contains('Maior venda: R\$ 27.00'), 'maior');
  conferir(saida.contains('Menor venda: R\$ 22.00'), 'menor');
  conferir(
    capturar(() => e08.analisarVendas([])).single ==
        'Não há vendas para calcular.',
    'lista vazia',
  );
  conferir(
    capturar(() => e08.analisarVendas([24])).contains('Média: R\$ 24.00'),
    'venda única',
  );
  conferir(
    capturar(() => e08.analisarVendas([0, 0])).contains('Soma: R\$ 0.00'),
    'vendas de valor zero',
  );
  rejeitar(() => e08.analisarVendas([-1]), 'venda negativa');
  rejeitar(() => e08.analisarVendas([double.nan]), 'venda NaN');
  rejeitar(() => e08.analisarVendas([double.infinity]), 'venda infinita');

  e09.Produto frango = e09.Produto(' frango ', ' Frango ', 'g', 1000, 500);
  conferir(
    frango.codigo == 'frango' && frango.nome == 'Frango',
    'espaços do cadastro',
  );
  frango.registrarEntrada(1000);
  frango.registrarSaida(1760);
  conferir(frango.quantidade == 240, 'entrada e saída');
  conferir(frango.precisaRepor(), 'alerta abaixo do mínimo');
  conferir(frango.calcularReposicao() == 260, 'quantidade de reposição');
  conferir(frango.calcularPorcoes(220) == 1, 'porções inteiras');
  rejeitar(() => frango.registrarSaida(241), 'saída acima do saldo');
  conferir(frango.quantidade == 240, 'rejeição preserva saldo');
  frango.registrarSaida(240);
  conferir(frango.quantidade == 0, 'saída igual ao saldo');
  rejeitar(() => frango.registrarEntrada(0), 'entrada zero');
  rejeitar(() => frango.registrarSaida(-1), 'saída negativa');
  rejeitar(() => frango.nome = ' ', 'nome vazio');
  rejeitar(() => frango.estoqueMinimo = -1, 'mínimo negativo');
  rejeitar(() => frango.calcularPorcoes(0), 'divisão por zero');
  rejeitar(() => e09.Produto('', 'A', 'g', 0, 0), 'código vazio');
  rejeitar(() => e09.Produto('A', 'A', 'kg', 0, 0), 'unidade inválida');
  rejeitar(() => e09.Produto('A', 'A', 'g', -1, 0), 'saldo inicial negativo');
  e09.Produto limite = e09.Produto('A', 'A', 'un', 10, 10);
  conferir(
    !limite.precisaRepor() && limite.calcularReposicao() == 0,
    'saldo igual ao mínimo',
  );
  conferir(
    capturar(e09.main).last == 'Saldo após a tentativa: 240 g',
    'execução da entrega 09',
  );
  print('$testes verificações Dart aprovadas.');
}
