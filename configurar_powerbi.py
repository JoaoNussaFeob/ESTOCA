import argparse,json
from pathlib import Path

p=argparse.ArgumentParser(description='Configura caminhos e parâmetros dos projetos Power BI.')
p.add_argument('--servidor',default='localhost:3306')
p.add_argument('--banco',default='estoca_jk')
a=p.parse_args()
r=Path(__file__).resolve().parent

def parametro(valor):
    return '"'+valor.replace('"','""')+'" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'

for numero in [3,6,10]:
    pasta=r/f'Entrega_{numero:02}'
    modelo=pasta/'Projeto_PowerBI/Estoca.SemanticModel/model.bim'
    dados=json.loads(modelo.read_text(encoding='utf-8'))
    for expressao in dados['model']['expressions']:
        nome=expressao['name']
        if nome=='ArquivoExcel':expressao['expression']=parametro(str((pasta/'Base_Estoca.xlsx').resolve()))
        if nome=='ServidorMySQL':expressao['expression']=parametro(a.servidor)
        if nome=='BancoMySQL':expressao['expression']=parametro(a.banco)
    modelo.write_text(json.dumps(dados,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Entrega {numero:02}: parâmetros configurados.')

print('Abra Estoca.pbip no Power BI Desktop. Atualize os dados e valide o resultado antes de salvar como PBIX.')
