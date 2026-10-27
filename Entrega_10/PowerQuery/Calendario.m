let
    Fonte = FonteMySQL{[Schema=BancoMySQL, Item="vw_calendario"]}[Data],
    Colunas = Table.SelectColumns(Fonte, {"data", "dia_semana", "fim_semana"}),
    Tipos = Table.TransformColumnTypes(Colunas, {{"data", type date}, {"dia_semana", Int64.Type}, {"fim_semana", Int64.Type}}, "pt-BR"),
    SemDuplicatas = Table.Distinct(Tipos),
    ChavesValidas = if Table.RowCount(Table.SelectRows(SemDuplicatas, each [data] = null)) > 0 then error "Chave obrigatória ausente" else SemDuplicatas,
    Unicidade = if Table.RowCount(Table.Distinct(ChavesValidas, {"data"})) <> Table.RowCount(ChavesValidas) then error "Chaves duplicadas conflitantes" else ChavesValidas,
    Resultado = Unicidade
in
    Resultado