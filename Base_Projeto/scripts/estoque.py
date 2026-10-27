import argparse,sqlite3
from pathlib import Path
p=argparse.ArgumentParser(description='Estoca JK - quantidades inteiras em g/ml/un')
p.add_argument('--banco',default=str(Path(__file__).resolve().parents[1]/'banco/estoca_jk.sqlite'))
p.add_argument('acao',choices=['listar','entrada','saida'])
p.add_argument('--produto');p.add_argument('--quantidade',type=int);p.add_argument('--motivo')
a=p.parse_args()
if not Path(a.banco).is_file():p.error('Banco não encontrado. Gere a base primeiro.')
db=sqlite3.connect(a.banco);db.execute('PRAGMA foreign_keys=ON')
if a.acao=='listar':
    for code,name,unit,balance in db.execute('SELECT * FROM saldo_atual ORDER BY nome'):
        print(f'{code:18} {name:38} {balance:9} {unit}')
else:
    if not a.produto or not a.quantidade or a.quantidade<=0 or not a.motivo or not a.motivo.strip():p.error('Informe produto, quantidade positiva e motivo.')
    try:
        with db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('INSERT INTO movimento(produto,tipo,delta,motivo) VALUES(?,?,?,?)',(a.produto,a.acao.upper(),a.quantidade*(1 if a.acao=='entrada' else -1),a.motivo.strip()))
        print('Operação registrada. Saldo:',db.execute('SELECT saldo,unidade FROM saldo_atual WHERE codigo=?',(a.produto,)).fetchone())
    except sqlite3.Error as e:p.exit(1,f'Operação rejeitada: {e}\n')
db.close()
