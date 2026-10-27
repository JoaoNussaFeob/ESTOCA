let
    Fonte = FonteMySQL{[Schema=BancoMySQL, Item="vw_produtos"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"codigo", "nome", "categoria", "unidade", "embalagem", "ciclo_dias", "origem"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"codigo", type text}, {"nome", type text}, {"categoria", type text}, {"unidade", type text}, {"embalagem", Int64.Type}, {"ciclo_dias", Int64.Type}, {"origem", type text}}, "pt-BR"),
    Textos = Table.TransformColumns(Tipos, {{"codigo", each if _ = null then null else Text.Trim(_), type text}, {"nome", each if _ = null then null else Text.Trim(_), type text}, {"categoria", each if _ = null then null else Text.Trim(_), type text}, {"unidade", each if _ = null then null else Text.Trim(_), type text}, {"origem", each if _ = null then null else Text.Trim(_), type text}}),
    Unidades = Table.TransformColumns(Textos, {{"unidade", Text.Lower, type text}}),
    Origem = Table.ReplaceValue(Unidades, null, "Não informado", Replacer.ReplaceValue, {"origem"}),
    SemDuplicatas = Table.Distinct(Origem),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [codigo] = null or [codigo] = "")) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"codigo"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Resultado = Unicidade
in
    Resultado