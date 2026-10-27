import csv, json, sqlite3, math
from pathlib import Path
from datetime import date, timedelta
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT/'dados/premissas.json').read_text())
dbpath=ROOT/'banco/estoca_jk.sqlite'
if dbpath.exists():
    old=sqlite3.connect(dbpath)
    operational=old.execute("SELECT COUNT(*) FROM movimento WHERE tipo<>'SALDO_INICIAL'").fetchone()[0]
    old.close()
    if operational:
        raise SystemExit('Banco contém operações: nada foi regenerado. Copie o projeto antes de regenerar.')
assert P['dias'] == 14, 'Este cenário foi desenhado para 14 dias.'
assert 0 <= P['fracao_fitness'] <= 1 and 0 <= P['fracao_delivery'] <= 1
assert P['margem_seguranca'] >= 0
assert all(isinstance(P[k],int) and P[k]>0 for k in ['refeicoes_dia_util','refeicoes_fim_semana'])


raw = [
('frango','Filé de peito de frango','Proteínas','g',1000,7,'Citado'),
('tilapia','Filé de tilápia','Proteínas','g',1000,7,'Citado'),
('peito_bovino','Ponta de peito bovina','Proteínas','g',1000,7,'Citado'),
('bovino_assar','Carne bovina para assar','Proteínas','g',1000,7,'Citado; corte presumido'),
('bovino_panela','Carne bovina para panela','Proteínas','g',1000,7,'Citado; corte presumido'),
('carne_moida','Carne bovina moída','Proteínas','g',1000,7,'Inferido da bolonhesa'),
('sobrecoxa','Sobrecoxa de frango com osso','Proteínas','g',1000,7,'Citado; com osso presumido'),
('bacon','Bacon','Proteínas','g',1000,7,'Citado'),
('ovos','Ovos','Ovos e laticínios','un',30,7,'Inferido da omelete e empanados'),
('queijo','Queijo muçarela','Ovos e laticínios','g',1000,7,'Queijo citado; tipo presumido'),
('leite','Leite','Ovos e laticínios','ml',1000,7,'Inferido do creme e molho'),
('manteiga','Manteiga','Ovos e laticínios','g',500,7,'Citado'),
('arroz','Arroz branco cru','Secos','g',5000,14,'Citado'),
('integral','Arroz integral cru','Secos','g',1000,14,'Citado'),
('feijao','Feijão carioca seco','Secos','g',1000,14,'Feijão citado; tipo presumido'),
('lasanha','Massa seca para lasanha','Secos','g',500,14,'Inferido da lasanha'),
('macarrao','Macarrão seco para macarronese','Secos','g',500,14,'Inferido da macarronese'),
('trigo','Farinha de trigo','Secos','g',1000,14,'Inferido'),
('rosca','Farinha de rosca','Secos','g',1000,14,'Inferido dos empanados'),
('oleo','Óleo vegetal','Óleos e temperos','ml',900,14,'Inferido'),
('azeite','Azeite','Óleos e temperos','ml',500,14,'Inferido'),
('sal','Sal','Óleos e temperos','g',1000,14,'Inferido'),
('pimenta','Pimenta-do-reino','Óleos e temperos','g',100,14,'Inferido'),
('vinagre','Vinagre','Óleos e temperos','ml',750,14,'Inferido'),
('molho','Molho de tomate','Conservas','g',1000,14,'Inferido da bolonhesa'),
('maionese','Maionese industrializada','Conservas','g',1000,14,'Inferido da macarronese'),
('milho','Milho verde drenado','Conservas','g',170,14,'Citado; embalagem em peso drenado'),
('ervilha','Ervilha drenada','Conservas','g',170,14,'Citado; embalagem em peso drenado'),
('palmito','Palmito drenado','Conservas','g',300,14,'Citado; embalagem em peso drenado'),
('azeitona','Azeitona sem caroço drenada','Conservas','g',500,14,'Inferido da caponata'),
('alface','Alface','Hortifruti','g',500,2,'Folhas citadas; tipo presumido'),
('rucula','Rúcula','Hortifruti','g',250,2,'Folhas citadas; tipo presumido'),
('couve','Couve','Hortifruti','g',500,2,'Citado'),
('tomate','Tomate','Hortifruti','g',1000,2,'Citado'),
('laranja','Laranja','Hortifruti','g',1000,2,'Citado'),
('pepino','Pepino','Hortifruti','g',1000,2,'Citado'),
('cabotia','Abóbora cabotiá inteira','Hortifruti','g',1000,2,'Citado'),
('batata_doce','Batata-doce','Hortifruti','g',1000,2,'Citado'),
('batata','Batata inglesa','Hortifruti','g',1000,2,'Inferido da batata canoa'),
('cenoura','Cenoura','Hortifruti','g',1000,2,'Citado'),
('brocolis','Brócolis','Hortifruti','g',1000,2,'Citado'),
('abobrinha','Abobrinha','Hortifruti','g',1000,2,'Citado'),
('repolho','Repolho','Hortifruti','g',1000,2,'Citado'),
('beterraba','Beterraba','Hortifruti','g',1000,2,'Citado'),
('berinjela','Berinjela','Hortifruti','g',1000,2,'Citado'),
('pimentao','Pimentão','Hortifruti','g',1000,2,'Inferido dos legumes e caponata'),
('cebola','Cebola','Hortifruti','g',1000,2,'Inferido'),
('alho','Alho descascado','Hortifruti','g',500,2,'Inferido'),
('limao','Limão','Hortifruti','g',1000,2,'Inferido do tempero'),
('cheiro','Cheiro-verde','Hortifruti','g',100,2,'Inferido'),
('marmita','Conjunto marmita com tampa','Embalagens','un',100,14,'Inferido; modelo universal fictício'),
('sacola','Sacola para entrega','Embalagens','un',100,14,'Inferido; uma por refeição delivery'),
('talher','Kit de talheres e guardanapo','Embalagens','un',100,14,'Inferido; um por refeição delivery')]
products = {x[0]:dict(zip(['codigo','nome','categoria','unidade','embalagem','ciclo_dias','origem'],x)) for x in raw}


recipes = {}
def recipe(code,name,kind,**items):
    recipes[code]={'codigo':code,'nome':name,'tipo':kind,'itens':items}
recipe('frango_g','Filé de frango grelhado','Principal',frango=220,oleo=8,alho=3,sal=2,pimenta=1,limao=15)
recipe('frango_e','Filé de frango empanado','Principal',frango=220,trigo=20,rosca=30,ovos=.25,oleo=30,alho=3,sal=2,pimenta=1)
recipe('tilapia_g','Filé de tilápia grelhado','Principal',tilapia=220,oleo=8,alho=3,sal=2,pimenta=1,limao=25)
recipe('tilapia_e','Iscas de tilápia empanadas','Principal',tilapia=220,trigo=20,rosca=30,ovos=.25,oleo=30,limao=25,sal=2,pimenta=1)
recipe('omelete','Omelete com queijo','Principal',ovos=3,queijo=50,oleo=8,cheiro=3,sal=2)
recipe('peito','Ponta de peito na pressão','Principal',peito_bovino=260,cebola=30,alho=4,molho=30,oleo=8,sal=2,pimenta=1)
recipe('assado','Carne bovina assada','Principal',bovino_assar=260,cebola=25,alho=4,oleo=8,sal=2,pimenta=1)
recipe('panela','Carne de panela','Principal',bovino_panela=250,cenoura=40,cebola=30,alho=4,molho=30,oleo=8,sal=2,pimenta=1)
recipe('lasanha','Lasanha à bolonhesa','Principal',carne_moida=100,lasanha=60,queijo=50,molho=100,leite=60,trigo=8,manteiga=5,cebola=20,alho=3,sal=2)
recipe('sobrecoxa','Sobrecoxa assada com bacon','Principal',sobrecoxa=320,bacon=30,cebola=20,alho=4,oleo=5,sal=2,pimenta=1)
recipe('trad_base','Arroz branco e feijão','Base',arroz=60,feijao=40,cebola=8,alho=3,oleo=5,sal=2)
recipe('trad_A','Batata-doce e legumes na manteiga','Acompanhamento',batata_doce=100,cenoura=30,brocolis=35,abobrinha=25,pimentao=10,manteiga=5,oleo=15,sal=1)
recipe('trad_B','Batata canoa e creme de milho','Acompanhamento',batata=100,milho=45,leite=40,manteiga=4,trigo=4,oleo=15,sal=1)
recipe('trad_C','Brócolis com bacon e macarronese','Acompanhamento',brocolis=90,bacon=12,macarrao=35,maionese=20,cenoura=15,milho=10,ervilha=10,sal=1)
recipe('trad_D','Abobrinha empanada e repolho com bacon','Acompanhamento',abobrinha=100,trigo=15,rosca=20,ovos=.15,oleo=20,repolho=90,bacon=12,sal=1)
recipe('fit_base','Arroz integral, folhas e tomate','Base',integral=60,alface=25,rucula=10,tomate=50,alho=2,azeite=5,vinagre=3,sal=1)
recipe('fit_A','Couve, palmito, laranja e pepino','Acompanhamento',couve=50,palmito=30,laranja=100,pepino=40,oleo=3)
recipe('fit_B','Couve, cabotiá e laranja','Acompanhamento',couve=50,cabotia=100,laranja=100,oleo=3)
recipe('fit_C','Milho e ervilha','Acompanhamento',milho=40,ervilha=40)
recipe('fit_D','Repolho, cenoura, beterraba e caponata','Acompanhamento',repolho=40,cenoura=30,beterraba=30,berinjela=40,pimentao=10,cebola=8,azeitona=5,azeite=5,vinagre=3)

def allocation(n,weights):
    exact=[n*w/sum(weights) for w in weights]; out=[int(v) for v in exact]
    for i in sorted(range(len(out)),key=lambda i:exact[i]-out[i],reverse=True)[:n-sum(out)]:out[i]+=1
    return out

orders=[]; daily=[]; consumption=[]; details=[]
start=date.fromisoformat(P['inicio'])
specials=[['peito'],['lasanha','sobrecoxa'],['assado','tilapia_e'],['panela']]
for d in range(14):
    dt=(start+timedelta(days=d)).isoformat(); variant='ABCD'[d%4]
    n=P['refeicoes_fim_semana'] if (start+timedelta(days=d)).weekday()>=5 else P['refeicoes_dia_util']
    fit,trad=allocation(n,[P['fracao_fitness'],1-P['fracao_fitness']])
    delivery=round(n*P['fracao_delivery']); used=Counter()
    daily.append({'data':dt,'dia':d+1,'total':n,'tradicional':trad,'fitness':fit,'delivery':delivery,'variante':variant})
    mains=['frango_g','frango_e','omelete']+specials[d%4]
    tradmix=allocation(trad,[35,25,10]+[30/len(specials[d%4])]*len(specials[d%4]))
    fitmix=allocation(fit,[50,30,20])
    for line,mainlist,counts in [('trad',mains,tradmix),('fit',['frango_g','tilapia_g','omelete'],fitmix)]:
        for main,count in zip(mainlist,counts):
            sizes=[('P',.85,count//4),('M',1,count-2*(count//4)),('G',1.15,count//4)] if line=='trad' else [('U',1,count)]
            for size,factor,q in sizes:
                if not q:continue
                oid=len(orders)+1
                orders.append({'id':oid,'data':dt,'linha':line,'principal':main,'tamanho':size,'quantidade':q,'variante':variant})
                for rc in [main,line+'_base',line+'_'+variant]:
                    for product,amount in recipes[rc]['itens'].items():

                        amount_scaled=({'P':2,'M':3,'G':4,'U':3}[size] if product=='ovos' and rc=='omelete' else amount*factor)
                        gross=amount_scaled*q;used[product]+=gross
                        details.append({'pedido_grupo_id':oid,'receita':rc,'produto':product,'quantidade_base':round(gross,4)})
    for k in ['marmita','sacola','talher']:used[k]+=delivery
    for k in products:

        consumption.append({'data':dt,'dia':d+1,'produto':k,'quantidade_base':math.ceil(round(used[k],6))})

receipts=[]; stock=[]; balance_rows=[]
for k,p in products.items():
    needs=[r['quantidade_base'] for r in consumption if r['produto']==k]
    balance=0; total_bought=0; opening=0
    for d in range(14):
        received=0
        if d%p['ciclo_dias']==0:
            block=sum(needs[d:min(14,d+p['ciclo_dias'])]);target=math.ceil(block*(1+P['margem_seguranca']))
            received=math.ceil(target/p['embalagem'])*p['embalagem']
            if received:
                receipts.append({'data':(start+timedelta(days=d)).isoformat(),'dia':d+1,'produto':k,'quantidade_base':received,'pacotes':received//p['embalagem'],'estado':'INICIAL' if d==0 else 'PREVISTO'})
            if d==0:opening=received
            total_bought+=received;balance+=received
        balance-=needs[d]
        assert balance>=0,(k,d,balance)
        balance_rows.append({'dia':d+1,'produto':k,'entrada_planejada':received,'consumo_planejado':needs[d],'saldo_projetado':balance})
    stock.append(dict(produto=k,nome=p['nome'],categoria=p['categoria'],unidade=p['unidade'],consumo_14d=sum(needs),meta_global_15pct=math.ceil(sum(needs)*(1+P['margem_seguranca'])),estoque_inicial=opening,reposicao_14d=total_bought-opening,total_compras=total_bought,saldo_final=balance,ciclo_dias=p['ciclo_dias'],embalagem=p['embalagem']))

def csvwrite(name,rows):
    with (ROOT/'dados'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
csvwrite('produtos.csv',list(products.values()))
csvwrite('receitas.csv',[{k:v for k,v in r.items() if k!='itens'} for r in recipes.values()])
csvwrite('receita_ingredientes.csv',[{'receita':r['codigo'],'produto':p,'quantidade_base_por_M':v} for r in recipes.values() for p,v in r['itens'].items()])
csvwrite('demanda_diaria.csv',daily);csvwrite('pedidos_planejados.csv',orders)
csvwrite('consumo_por_pedido.csv',details);csvwrite('consumo_diario.csv',consumption)
csvwrite('estoque_14_dias.csv',stock);csvwrite('recebimentos_planejados.csv',receipts);csvwrite('saldos_projetados.csv',balance_rows)

schema='''PRAGMA foreign_keys=ON;
CREATE TABLE produto(codigo TEXT PRIMARY KEY,nome TEXT NOT NULL,categoria TEXT NOT NULL,unidade TEXT NOT NULL CHECK(unidade IN ('g','ml','un')),embalagem INTEGER NOT NULL CHECK(embalagem>0),ciclo_dias INTEGER NOT NULL CHECK(ciclo_dias>0),origem TEXT NOT NULL);
CREATE TABLE receita(codigo TEXT PRIMARY KEY,nome TEXT NOT NULL,tipo TEXT NOT NULL);
CREATE TABLE receita_ingrediente(receita TEXT NOT NULL REFERENCES receita(codigo),produto TEXT NOT NULL REFERENCES produto(codigo),quantidade_base_por_M REAL NOT NULL CHECK(quantidade_base_por_M>0),PRIMARY KEY(receita,produto));
CREATE TABLE demanda_diaria(data TEXT PRIMARY KEY,dia INTEGER UNIQUE NOT NULL,total INTEGER NOT NULL,tradicional INTEGER NOT NULL,fitness INTEGER NOT NULL,delivery INTEGER NOT NULL,variante TEXT NOT NULL,CHECK(total=tradicional+fitness),CHECK(delivery BETWEEN 0 AND total));
CREATE TABLE pedido_planejado(id INTEGER PRIMARY KEY,data TEXT NOT NULL REFERENCES demanda_diaria(data),linha TEXT NOT NULL CHECK(linha IN ('trad','fit')),principal TEXT NOT NULL REFERENCES receita(codigo),tamanho TEXT NOT NULL CHECK(tamanho IN ('P','M','G','U')),quantidade INTEGER NOT NULL CHECK(quantidade>0),variante TEXT NOT NULL);
CREATE TABLE consumo_planejado(data TEXT NOT NULL REFERENCES demanda_diaria(data),dia INTEGER NOT NULL,produto TEXT NOT NULL REFERENCES produto(codigo),quantidade_base INTEGER NOT NULL CHECK(quantidade_base>=0),PRIMARY KEY(data,produto));
CREATE TABLE recebimento_planejado(id INTEGER PRIMARY KEY,data TEXT NOT NULL REFERENCES demanda_diaria(data),dia INTEGER NOT NULL,produto TEXT NOT NULL REFERENCES produto(codigo),quantidade_base INTEGER NOT NULL CHECK(quantidade_base>0),pacotes INTEGER NOT NULL CHECK(pacotes>0),estado TEXT NOT NULL CHECK(estado IN ('INICIAL','PREVISTO')));
CREATE TABLE movimento(id INTEGER PRIMARY KEY,produto TEXT NOT NULL REFERENCES produto(codigo),tipo TEXT NOT NULL CHECK(tipo IN ('SALDO_INICIAL','ENTRADA','SAIDA')),delta INTEGER NOT NULL CHECK(typeof(delta)='integer' AND delta<>0),motivo TEXT NOT NULL CHECK(length(trim(motivo))>0),criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,CHECK((tipo IN ('SALDO_INICIAL','ENTRADA') AND delta>0) OR (tipo='SAIDA' AND delta<0)));
CREATE UNIQUE INDEX saldo_inicial_unico ON movimento(produto) WHERE tipo='SALDO_INICIAL';
CREATE TRIGGER impedir_saldo_negativo BEFORE INSERT ON movimento WHEN NEW.delta+COALESCE((SELECT SUM(delta) FROM movimento WHERE produto=NEW.produto),0)<0 BEGIN SELECT RAISE(ABORT,'Estoque insuficiente'); END;
CREATE TRIGGER impedir_inicial_tardio BEFORE INSERT ON movimento WHEN NEW.tipo='SALDO_INICIAL' AND EXISTS(SELECT 1 FROM movimento WHERE produto=NEW.produto) BEGIN SELECT RAISE(ABORT,'Saldo inicial precisa ser o primeiro movimento'); END;
CREATE TRIGGER movimento_imutavel_update BEFORE UPDATE ON movimento BEGIN SELECT RAISE(ABORT,'Historico imutavel'); END;
CREATE TRIGGER movimento_imutavel_delete BEFORE DELETE ON movimento BEGIN SELECT RAISE(ABORT,'Historico imutavel'); END;
CREATE VIEW saldo_atual AS SELECT p.codigo,p.nome,p.unidade,COALESCE(SUM(m.delta),0) AS saldo FROM produto p LEFT JOIN movimento m ON m.produto=p.codigo GROUP BY p.codigo,p.nome,p.unidade;
'''
if dbpath.exists():
    dbpath.unlink()
db=sqlite3.connect(dbpath);db.executescript(schema)
def insert(table,rows):
    for row in rows:
        keys=','.join(row); qs=','.join('?' for _ in row)
        db.execute(f'INSERT INTO {table} ({keys}) VALUES ({qs})',list(row.values()))
insert('produto',list(products.values()))
insert('receita',[{k:v for k,v in r.items() if k!='itens'} for r in recipes.values()])
insert('receita_ingrediente',[{'receita':r['codigo'],'produto':k,'quantidade_base_por_M':v} for r in recipes.values() for k,v in r['itens'].items()])
insert('demanda_diaria',daily);insert('pedido_planejado',orders);insert('consumo_planejado',consumption);insert('recebimento_planejado',receipts)
insert('movimento',[{'produto':r['produto'],'tipo':'SALDO_INICIAL','delta':r['estoque_inicial'],'motivo':'Carga fictícia de abertura - cenário acadêmico JK','criado_em':P['inicio']+' 00:00:00'} for r in stock if r['estoque_inicial']>0])
db.commit(); assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert not db.execute('PRAGMA foreign_key_check').fetchall()
(ROOT/'banco/schema_sqlite.sql').write_text(schema,encoding='utf-8')
(ROOT/'banco/base_completa_sqlite.sql').write_text('PRAGMA foreign_keys=OFF;\n'+'\n'.join(db.iterdump())+'\nPRAGMA foreign_keys=ON;\nPRAGMA foreign_key_check;\n',encoding='utf-8');db.close()
summary={'refeicoes':sum(r['total'] for r in daily),'tradicionais':sum(r['tradicional'] for r in daily),'fitness':sum(r['fitness'] for r in daily),'delivery':sum(r['delivery'] for r in daily),'produtos':len(products),'receitas':len(recipes),'grupos_pedidos':len(orders),'saldo_diario_negativo':False}
(ROOT/'dados/resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
