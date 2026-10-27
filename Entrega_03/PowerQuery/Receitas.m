let
    Fonte = FonteExcel{[Item="tb_Receitas", Kind="Table"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"codigo", "nome", "tipo"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"codigo", type text}, {"nome", type text}, {"tipo", type text}}, "pt-BR"),
    Textos = Table.TransformColumns(Tipos, {{"codigo", each if _ = null then null else Text.Trim(_), type text}, {"nome", each if _ = null then null else Text.Trim(_), type text}, {"tipo", each if _ = null then null else Text.Trim(_), type text}}),
    SemDuplicatas = Table.Distinct(Textos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [codigo] = null or [codigo] = "")) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"codigo"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Resultado = Unicidade
in
    Resultado