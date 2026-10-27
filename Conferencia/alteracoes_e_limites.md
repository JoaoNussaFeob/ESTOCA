# Alterações e limites da revisão

## Organização e conteúdo

Foram criadas as pastas Entrega_01 a Entrega_10. Cada documento, diagrama, código e conjunto de fontes está associado à atividade correspondente. A Entrega 10 foi incorporada com seu prazo de 03/11/2026 e com exigência explícita de MySQL.

Foram concluídos os documentos de planejamento funcional, requisitos, modelo conceitual, modelo lógico, normalização e implementação física. Os diagramas foram revisados em tamanho de leitura. A identidade visual usa azul escuro, verde e fundo claro, mantendo tabelas e paginação consistentes.

## Correções estruturais

- O banco definitivo passou a ser MySQL, alinhando as entregas 04, 07 e 10.
- Categoria foi separada de produto. Campos derivados, como total da demanda e dia repetido nos fatos, foram retirados das tabelas físicas e recompostos em visões.
- A projeção de saldo passou a ser atualizada por gatilhos no MySQL e pode ser conciliada com o histórico. A aplicação deve restringir sua alteração manual.
- O Excel passou a conter as dez tabelas necessárias ao modelo analítico, incluindo calendário e vendas do exercício.
- Os problemas deliberados do Excel ficaram identificados: uma duplicata exata, espaços, unidade em maiúsculas e origem ausente. Não foram introduzidas inconsistências no banco carregado.
- Os exemplos Dart foram separados por atividade e mantidos sem comentários ou docstrings.
- Previsão de receita, vendas de exemplo e movimentações de estoque foram distinguidas para evitar indicadores enganosos.

## Evidências de teste

- Dart 3.9.4: análise estática sem problemas e 30 verificações aprovadas.
- MySQL 8.0.36: estrutura e dados executados; 14 verificações aprovadas.
- Power Query: 37 expressões analisadas pelo parser da Microsoft, com sintaxe válida.
- Definições de relatório Power BI: 29 arquivos JSON validados contra esquemas e referências de colunas/medidas conferidas.
- Excel: dez tabelas nomeadas, datas tipadas e demanda total de 2.760 refeições conferidas. A aba de orientação é adicional às dez tabelas de dados.
- PDF: sete documentos, totalizando 30 páginas, renderizados e inspecionados.

## Pendências que impedem declarar as dez entregas completas

Faltam os arquivos nativos PBIX das entregas 03, 06 e 10. Não houve execução do Power BI Desktop, atualização de dados, cálculo pelo motor DAX ou conexão do Power BI ao MySQL. Os projetos PBIP, consultas, medidas e definições de visuais estão preparados, mas não foram validados no aplicativo, inclusive na versão 2.138 da faculdade.

A prévia PNG do dashboard foi calculada fora do Power BI e está identificada como tal. Ela não serve como evidência de execução do aplicativo. Não foi feita conversão artificial de extensão.

A publicação do GitHub depende do acesso à conta e não foi realizada. O protótipo local não inclui autenticação, controle de lotes/validade nem uma aplicação web de produção. Esses recursos não são requisitos dos exercícios isolados já entregues, mas continuam como evolução do projeto.

Os testes cobrem os casos descritos, não uma garantia de ausência absoluta de defeitos em qualquer ambiente.

## Identificação do grupo

Incluídos os quatro integrantes, na ordem solicitada, nas capas e metadados dos PDFs, nos arquivos de identificação das dez entregas e na documentação principal. O bloco de identificação foi ampliado para reconhecer todos os autores. Os códigos continuam sem comentários.
