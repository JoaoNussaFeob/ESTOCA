let
    Fonte = FonteExcel{[Item="tb_Recebimentos", Kind="Table"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"id", "data", "dia", "produto", "quantidade_base", "pacotes", "estado"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"id", Int64.Type}, {"data", type date}, {"dia", Int64.Type}, {"produto", type text}, {"quantidade_base", Int64.Type}, {"pacotes", Int64.Type}, {"estado", type text}}, "pt-BR"),
    Textos = Table.TransformColumns(Tipos, {{"produto", each if _ = null then null else Text.Trim(_), type text}, {"estado", each if _ = null then null else Text.Trim(_), type text}}),
    SemDuplicatas = Table.Distinct(Textos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [id] = null)) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"id"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Resultado = Unicidade
in
    Resultado