let
    Fonte = FonteExcel{[Item="tb_Movimentos", Kind="Table"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"id", "produto", "tipo", "delta", "motivo", "criado_em"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"id", Int64.Type}, {"produto", type text}, {"tipo", type text}, {"delta", Int64.Type}, {"motivo", type text}, {"criado_em", type datetime}}, "pt-BR"),
    Textos = Table.TransformColumns(Tipos, {{"produto", each if _ = null then null else Text.Trim(_), type text}, {"tipo", each if _ = null then null else Text.Trim(_), type text}, {"motivo", each if _ = null then null else Text.Trim(_), type text}}),
    SemDuplicatas = Table.Distinct(Textos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [id] = null)) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"id"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    DataMovimento = Table.AddColumn(Unicidade, "data_movimento", each Date.From([criado_em]), type date),
    Resultado = DataMovimento
in
    Resultado