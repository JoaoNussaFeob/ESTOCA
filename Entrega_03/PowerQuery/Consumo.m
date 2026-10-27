let
    Fonte = FonteExcel{[Item="tb_Consumo", Kind="Table"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"data", "dia", "produto", "quantidade_base"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"data", type date}, {"dia", Int64.Type}, {"produto", type text}, {"quantidade_base", Int64.Type}}, "pt-BR"),
    Textos = Table.TransformColumns(Tipos, {{"produto", each if _ = null then null else Text.Trim(_), type text}}),
    SemDuplicatas = Table.Distinct(Textos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [data] = null or [produto] = null or [produto] = "")) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"data", "produto"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Resultado = Unicidade
in
    Resultado