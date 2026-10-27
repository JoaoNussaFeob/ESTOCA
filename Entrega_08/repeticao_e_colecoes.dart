void analisarVendas(List<double> vendas) {
  if (vendas.isEmpty) {
    print('Não há vendas para calcular.');
    return;
  }

  double soma = 0;
  for (double valor in vendas) {
    if (!valor.isFinite || valor < 0) {
      throw ArgumentError('A venda deve ter um valor válido e não negativo.');
    }
    soma += valor;
  }

  double maior = vendas[0];
  double menor = vendas[0];
  int indice = 0;
  while (indice < vendas.length) {
    if (vendas[indice] > maior) {
      maior = vendas[indice];
    }
    if (vendas[indice] < menor) {
      menor = vendas[indice];
    }
    indice++;
  }

  double media = soma / vendas.length;
  print('Quantidade de vendas: ${vendas.length}');
  print('Soma: R\$ ${soma.toStringAsFixed(2)}');
  print('Média: R\$ ${media.toStringAsFixed(2)}');
  print('Maior venda: R\$ ${maior.toStringAsFixed(2)}');
  print('Menor venda: R\$ ${menor.toStringAsFixed(2)}');
}

void main() {
  List<double> vendas = [22.00, 24.00, 27.00, 27.00, 22.00];
  analisarVendas(vendas);
}
