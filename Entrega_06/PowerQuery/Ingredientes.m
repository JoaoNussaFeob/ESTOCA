let
    Fonte = FonteExcel{[Item="tb_Ingredientes", Kind="Table"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"receita", "produto", "quantidade_base_por_M"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"receita", type text}, {"produto", type text}, {"quantidade_base_por_M", type number}}, "pt-BR"),
    Textos = Table.TransformColumns(Tipos, {{"receita", each if _ = null then null else Text.Trim(_), type text}, {"produto", each if _ = null then null else Text.Trim(_), type text}}),
    SemDuplicatas = Table.Distinct(Textos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [receita] = null or [receita] = "" or [produto] = null or [produto] = "")) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"receita", "produto"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Resultado = Unicidade
in
    Resultado