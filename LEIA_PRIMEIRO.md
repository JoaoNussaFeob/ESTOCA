# Estoca - entregas 01 a 10

Projeto Integrado de Ciência da Computação, UNIFEOB. Caso de estudo: JK Bar e Restaurante. Os dados são fictícios e representam o cenário de 2.760 refeições em 14 dias.

## Conferência de entrega

| Pasta | Arquivos principais | Situação |
| --- | --- | --- |
| Entrega_01 | planejamento_funcional.pdf; mapa_funcional.png | Documento e mapa concluídos. |
| Entrega_02 | requisitos_e_modelo_conceitual.pdf; der_operacional.png; der_planejamento.png | Documento, requisitos e DER concluídos. |
| Entrega_03 | Base_Estoca.xlsx; tratamento_e_modelagem.pdf; fluxo_dados.png; Projeto_PowerBI; PowerQuery | PBIX recebido após carga e exibição da tabela no Desktop do usuário; integridade conferida. |
| Entrega_04 | modelo_logico_e_normalizacao.pdf | Modelo lógico, chaves, integridade e normalização concluídos. |
| Entrega_05 | classes_e_objetos.dart | Código sem comentários, analisado e executado. |
| Entrega_06 | Base_Estoca.xlsx; indicadores_e_visualizacoes.pdf; fluxo_dados.png; medidas.dax; Projeto_PowerBI | Modelo, medidas, visuais e prévia preparados. Falta atualizar e validar no Power BI e salvar o PBIX obrigatório. |
| Entrega_07 | estrutura_mysql.sql; implementacao_fisica.pdf | Estrutura MySQL executada e validada. |
| Entrega_08 | repeticao_e_colecoes.dart | Código sem comentários, analisado e executado. |
| Entrega_09 | encapsulamento_e_validacao.dart | Código sem comentários, analisado e executado. |
| Entrega_10 | banco_completo_mysql.sql; consultas_extracao.sql; migracao_mysql_e_extracao.pdf; fluxo_dados.png; Projeto_PowerBI; Estoca_Entrega_10.pbix | PBIX recebido após atualização local e renderização demonstrada por captura. Versão visual revisada recebida; 53 produtos sem seleção confirmados pelo usuário. |

**O conjunto ainda não está 100% pronto para envio das dez atividades:** falta o PBIX da Entrega 06. O PBIX da Entrega 03 foi recebido e incluído. O PBIX da Entrega 10 foi recebido e incluído. Os PBIP são projetos editáveis, não arquivos PBIX e não substituem o formato solicitado pelo professor. A existência das pastas não indica que essa etapa foi executada.

## Finalização dos três arquivos Power BI

1. No computador que tem Power BI Desktop, extraia a pasta inteira.
2. Execute `python configurar_powerbi.py`. Isso ajusta os caminhos dos Excel para a pasta extraída. Para a Entrega 10, use também `--servidor host:3306 --banco estoca_jk`, com os valores da instalação.
3. Abra `Projeto_PowerBI/Estoca.pbip` da entrega correspondente. Se o recurso de projetos precisar ser habilitado no Desktop, faça essa configuração no ambiente autorizado.
4. Atualize os dados. Nas entregas 03 e 06, a fonte deve ser o respectivo Excel. Na 10, a fonte deve ser MySQL, com credenciais informadas no próprio Power BI.
5. Confira os tipos, relacionamentos, filtros e resultados. Os valores de referência e as consultas estão nos documentos de cada atividade.
6. Salve como `Estoca_Entrega_03.pbix`, `Estoca_Entrega_06.pbix` e `Estoca_Entrega_10.pbix`, dentro das pastas correspondentes. Feche e reabra cada PBIX para verificar o arquivo final.

Não foi comprovada compatibilidade dos projetos com Power BI Desktop 2.138.1452.0 (novembro de 2024). Foram usados esquemas PBIR mais antigos para reduzir a dependência de formatos recentes, mas isso não substitui a abertura nessa versão. Não há arquivo renomeado artificialmente para `.pbix` no pacote.

## Execução dos códigos Dart

```sh
dart run Entrega_05/classes_e_objetos.dart
dart run Entrega_08/repeticao_e_colecoes.dart
dart run Entrega_09/encapsulamento_e_validacao.dart
dart run Conferencia/testes_dart.dart
```

Validação realizada com Dart 3.9.4: análise estática sem problemas e 30 verificações de comportamento aprovadas. As quantidades são inteiras em g, ml ou un. A venda simulada da atividade 08 usa reais e é independente do planejamento de 2.760 refeições.

## Execução MySQL

O banco definitivo das entregas 04, 07 e 10 é MySQL. Use 8.0.16 ou superior; a validação foi feita em 8.0.36. Em um banco vazio, execute **apenas uma** destas opções:

- `Entrega_07/estrutura_mysql.sql`: somente estrutura.
- `Entrega_10/banco_completo_mysql.sql`: estrutura e dados. É a opção para a atividade 10.

Não execute os dois scripts de criação sobre o mesmo banco. Eles não apagam tabelas existentes. `consultas_extracao.sql` pode ser executado após a carga. O arquivo `Conferencia/testes_mysql.json` registra as 14 verificações realizadas.

## Pastas de apoio

- `Conferencia`: resultados e testes, separados dos arquivos principais a enviar ao professor.
- `Base_Projeto`: memória de cálculo, CSV e protótipo local anterior em SQLite. É apoio ao cálculo e à demonstração; não é o banco definitivo da Entrega 10. Seus documentos antigos descrevem aquela versão e não substituem os novos documentos numerados.
- `docs/gestao`: cronograma das entregas e modelos de Sprint Report e de ata de reunião.

As prévias de dashboard foram calculadas em Python e estão identificadas dessa forma. Não são capturas de uma execução no Power BI. A validação dos projetos inclui sintaxe M, esquemas JSON e referências de campos; na Entrega 10, a captura enviada pelo usuário comprova renderização e resultados de 2.760 refeições, R$ 66.490 de receita prevista e 1.794 deliveries. Não houve execução independente do PBIX neste ambiente.

## Integrantes

- Kauê de Oliveira Silva - RA: 26001417
- João Victor Rodrigues Nussa - RA: 26000516
- Pedro Joaquim Boletta de Piza - RA: 26001534
- Kauã Marques de Carvalho - RA: 26001550
