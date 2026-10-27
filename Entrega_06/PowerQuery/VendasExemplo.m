let
    Fonte = FonteExcel{[Item="tb_VendasExemplo", Kind="Table"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"id", "data", "valor_centavos"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"id", Int64.Type}, {"data", type date}, {"valor_centavos", Int64.Type}}, "pt-BR"),
    SemDuplicatas = Table.Distinct(Tipos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [id] = null)) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"id"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Resultado = Unicidade
in
    Resultado