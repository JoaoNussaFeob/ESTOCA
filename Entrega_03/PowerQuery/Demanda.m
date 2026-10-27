let
    Fonte = FonteExcel{[Item="tb_Demanda", Kind="Table"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"data", "dia", "total", "tradicional", "fitness", "delivery", "variante"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"data", type date}, {"dia", Int64.Type}, {"total", Int64.Type}, {"tradicional", Int64.Type}, {"fitness", Int64.Type}, {"delivery", Int64.Type}, {"variante", type text}}, "pt-BR"),
    Textos = Table.TransformColumns(Tipos, {{"variante", each if _ = null then null else Text.Trim(_), type text}}),
    SemDuplicatas = Table.Distinct(Textos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [data] = null)) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"data"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Resultado = Unicidade
in
    Resultado