let
    Fonte = FonteMySQL{[Schema=BancoMySQL, Item="vw_pedidos"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"id", "data", "linha", "principal", "tamanho", "quantidade", "variante"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"id", Int64.Type}, {"data", type date}, {"linha", type text}, {"principal", type text}, {"tamanho", type text}, {"quantidade", Int64.Type}, {"variante", type text}}, "pt-BR"),
    Textos = Table.TransformColumns(Tipos, {{"linha", each if _ = null then null else Text.Trim(_), type text}, {"principal", each if _ = null then null else Text.Trim(_), type text}, {"tamanho", each if _ = null then null else Text.Trim(_), type text}, {"variante", each if _ = null then null else Text.Trim(_), type text}}),
    SemDuplicatas = Table.Distinct(Textos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [id] = null)) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"id"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Preco = Table.AddColumn(Unicidade, "preco_unitario_centavos", each if [linha] = "fit" then (if [principal] = "tilapia_g" then 2700 else 2200) else if [tamanho] = "P" then 2200 else if [tamanho] = "M" then 2400 else 2700, Int64.Type),
    Valor = Table.AddColumn(Preco, "valor_previsto_centavos", each [quantidade] * [preco_unitario_centavos], Int64.Type),
    Resultado = Valor
in
    Resultado