from pathlib import Path
import csv,json
from collections import defaultdict
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,landscape
R=Path(__file__).resolve().parents[1]
def read(name):return list(csv.DictReader((R/'dados'/name).open(encoding='utf-8-sig'),delimiter=';'))
stocks=read('estoque_14_dias.csv');daily=read('demanda_diaria.csv');products={p['codigo']:p for p in read('produtos.csv')}
recipes=read('receitas.csv');ingredients=read('receita_ingredientes.csv');p=json.loads((R/'dados/premissas.json').read_text())
expected={'inicio':'2026-11-02','dias':14,'refeicoes_dia_util':180,'refeicoes_fim_semana':240,'fracao_fitness':.20,'fracao_delivery':.65,'margem_seguranca':.15}
if any(p.get(k)!=v for k,v in expected.items()):
    raise SystemExit('O texto deste relatório corresponde ao cenário original. Atualize a narrativa e os exemplos antes de publicar outro cenário. Os CSV e o banco usam as novas premissas.')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle('BodyJK',fontName='Helvetica',fontSize=11,leading=16,textColor=colors.HexColor('#263746'),spaceAfter=10))
styles.add(ParagraphStyle('CellJK',fontName='Helvetica',fontSize=9.4,leading=13,textColor=colors.HexColor('#263746')))
styles.add(ParagraphStyle('HeadJK',parent=styles['CellJK'],fontName='Helvetica-Bold',textColor=colors.white))
styles.add(ParagraphStyle('TitleJK',fontName='Helvetica-Bold',fontSize=25,leading=30,textColor=colors.HexColor('#17324D'),spaceAfter=16))
styles.add(ParagraphStyle('SubJK',fontName='Helvetica-Bold',fontSize=14,leading=19,textColor=colors.HexColor('#147D72'),spaceBefore=5,spaceAfter=8))
story=[]
def para(t):story.append(Paragraph(t,styles['BodyJK']))
def title(t):story.append(Paragraph(t,styles['TitleJK']))
def sub(t):story.append(Paragraph(t,styles['SubJK']))
def page(t):
    if story:story.append(PageBreak())
    title(t)
def table(headers,rows,widths):
    values=[[Paragraph(escape(str(v)),styles['HeadJK']) for v in headers]]+[[Paragraph(escape(str(v)),styles['CellJK']) for v in row] for row in rows]
    t=Table(values,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17324D')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F2F7F8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#CBD5DF'))]))
    story.append(t);story.append(Spacer(1,10))
def qty(v,u):
    n=int(v)/(1 if u=='un' else 1000)
    return (f'{n:,.0f}' if u=='un' else f'{n:,.3f}').replace(',','X').replace('.',',').replace('X','.')

page('Estoca\nEstoque fictício para 14 dias')
sub('JK Bar e Restaurante | Projeto Integrado - UNIFEOB')
para('Kauê de Oliveira Silva - RA: 26001417<br/>João Victor Rodrigues Nussa - RA: 26000516<br/>Pedro Joaquim Boletta de Piza - RA: 26001534<br/>Kauã Marques de Carvalho - RA: 26001550<br/>Ciência da Computação - 2º semestre<br/>Estoca: Seu estoque, sob controle.')
table(['Refeições previstas','Itens de estoque','Preparações','Reserva de demanda'],[['2.760','53','20','15% por bloco de compra']],[190,190,180,198])
para('<b>Objetivo:</b> criar uma base utilizável para demonstrar o gerenciamento de pequenos estoques, com ingredientes vinculados aos pratos das fotos, memória de cálculo, recebimentos programados e registro efetivo de entradas e saídas.')
para('<b>Origem:</b> cardápios enviados pelo estudante. Pratos e acompanhamentos vêm das imagens. Demanda, tamanhos de porção, receitas, mix, embalagens e calendário são fictícios. A ausência de controle de estoque foi relatada pelo estudante.')
para('<b>Período ilustrativo:</b> 02 a 15 de novembro de 2026, com funcionamento nos 14 dias. As fotos não demonstram o volume real de pedidos. Fotos repetidas foram desconsideradas como novas opções.')

page('Premissas e memória de cálculo')
table(['Decisão','Hipótese aplicada'],[
['Demanda média-alta','180 refeições por dia útil e 240 por dia de fim de semana: 10 × 180 + 4 × 240 = 2.760.'],
['Linhas de produto','80% tradicional (2.208) e 20% fitness (552). Cada refeição recebe um principal e os acompanhamentos da variante do dia.'],
['Mix tradicional','35% frango grelhado, 25% frango empanado, 10% omelete e 30% especiais do dia. Havendo dois especiais, divide-se a parcela igualmente.'],
['Mix fitness','50% frango grelhado, 30% tilápia grelhada e 20% omelete. Contagens inteiras por distribuição dos maiores restos.'],
['Tamanhos','Tradicional: aproximadamente 25% P, 50% M e 25% G. P = 0,85 × M; G = 1,15 × M. Fitness tem porção única equivalente a M.'],
['Ovos','Omelete usa 2 ovos no P, 3 no M/fitness e 4 no G. Frações dos empanados são agregadas antes do arredondamento diário.'],
['Delivery','65% das refeições: 1.794 conjuntos de marmita com tampa, sacolas e kits de talheres antes da reserva. Um conjunto por refeição.']],[152,606])
para('Os tamanhos P e G usam a parte inteira de 25% de cada grupo; M recebe o restante. Isso evita frações de pedido e mantém a simetria das porções. Quantidades das fichas representam insumos brutos de compra, não peso final cozido.')

page('Do pedido à compra')
sub('Cálculo auditável')
para('1. Distribuir a demanda diária entre linhas, pratos e tamanhos.<br/>2. Somar principal + base + acompanhamentos da variante.<br/>3. Multiplicar insumo por porção, fator de tamanho e número de pedidos.<br/>4. Agregar por produto/dia e arredondar para cima em g, ml ou un.<br/>5. Para cada bloco de abastecimento: compra = teto(consumo do bloco × 1,15 ÷ embalagem) × embalagem.')
para('<b>Exemplo de frango:</b> consumo de 351,120 kg no período. Compra programada: 404 kg, divididos em 202 kg na abertura e 202 kg no dia 8. O saldo-base projetado ao fim é 52,880 kg. A reserva pode ser consumida caso a demanda supere a previsão.')
table(['Grupo','Recebimentos previstos','Interpretação'],[
['Hortifruti','Dias 1, 3, 5, 7, 9, 11 e 13','Cada lote de compra cobre seu bloco de 2 dias mais reserva.'],
['Proteínas, ovos e laticínios','Dias 1 e 8','Cada lote de compra cobre 7 dias mais reserva.'],
['Secos, conservas e embalagens','Dia 1','Compra do período com reserva e arredondamento de pacote.']],[210,205,343])
para('O excedente de cada bloco permanece no saldo simulado; a compra seguinte não o desconta. Por isso, a reserva total pode superar 15%, especialmente em itens de baixo consumo ou embalagens grandes. Na operação, as compras devem ser revistas conforme saldo utilizável e validade.')
para('<b>Limite:</b> os ciclos são premissas logísticas, não prazos de conservação. A cobertura matemática depende de recebimento antes do consumo do dia e não comprova capacidade física, validade ou cadeia de conservação.')

for start in range(0,len(stocks),14):
    page(f'Estoque por produto - parte {start//14+1}')
    para('Abertura = primeiro recebimento. Reposição = compras futuras. Compra total = abertura + reposição. Valores em kg, L ou unidades, conforme a coluna.')
    rows=[]
    for r in stocks[start:start+14]:
        u=r['unidade'];unit={'g':'kg','ml':'L','un':'un'}[u]
        rows.append([r['nome'],unit]+[qty(r[k],u) for k in ['consumo_14d','estoque_inicial','reposicao_14d','total_compras','saldo_final']])
    table(['Produto','Un.','Consumo 14d','Abertura','Reposição','Compra total','Sobra-base'],rows,[238,35,97,97,97,97,97])

page('Calendário de refeições e cardápios')
table(['Dia','Data','Total','Tradicional','Fitness','Delivery','Variante'],[[r['dia'],r['data'],r['total'],r['tradicional'],r['fitness'],r['delivery'],r['variante']] for r in daily],[40,115,70,105,90,90,248])
para('A: ponta de peito; batata-doce e legumes. B: lasanha/sobrecoxa; batata canoa e creme de milho. C: carne assada/tilápia empanada; brócolis com bacon e macarronese. D: carne de panela; abobrinha empanada e repolho com bacon. As opções fixas de frango e omelete permanecem disponíveis.')

groups=defaultdict(list)
for r in ingredients:
    v=float(r['quantidade_base_por_M']);q=str(int(v)) if v.is_integer() else str(v).replace('.',',')
    groups[r['receita']].append(f"{products[r['produto']]['nome']}: {q} {products[r['produto']]['unidade']}")
for start in range(0,len(recipes),5):
    page(f'Fichas fictícias de preparo - parte {start//5+1}')
    para('Quantidades por porção M ou fitness, em equivalente bruto de compra. São estimativas acadêmicas, incluindo rendimento e aparas presumidos, sem fator adicional de perda. Não foram medidas na cozinha do restaurante.')
    table(['Preparação','Insumos por porção'],[[r['nome'],'; '.join(groups[r['codigo']])] for r in recipes[start:start+5]],[200,558])
    para('Cada refeição tradicional combina um principal + arroz/feijão + variante tradicional. Cada fitness combina um principal + arroz integral/folhas/tomate + variante fitness. Os ingredientes compartilhados são somados por produto; as variantes não são servidas todas no mesmo prato.')

page('Banco preenchido e regras de funcionamento')
table(['Tabela ou visão','Conteúdo e relacionamento'],[
['produto','53 produtos com código, categoria, unidade-base, tamanho da embalagem, ciclo e origem.'],
['receita / receita_ingrediente','20 preparações. Relação muitos-para-muitos com produto, armazenando a quantidade por porção.'],
['demanda_diaria / pedido_planejado','14 dias e 231 grupos de pedidos; são previsões, não vendas efetivadas.'],
['consumo_planejado','742 combinações produto/dia, incluindo consumo zero para rastreabilidade.'],
['recebimento_planejado','Agenda de abastecimento. INICIAL identifica o primeiro recebimento; PREVISTO não aumenta o saldo atual.'],
['movimento / saldo_atual','Movimentos efetivos de abertura, entrada e saída. A visão calcula a soma dos deltas por produto.']],[210,548])
para('<b>Regras implementadas:</b> chaves primárias/estrangeiras, unidade controlada, quantidade-base inteira, saldo não negativo, abertura única e inicial, motivo obrigatório e histórico imutável. Operações locais com Python usam transação. Cada conexão deve habilitar PRAGMA foreign_keys=ON, como fazem os scripts entregues.')
para('<b>Verificação:</b> 19 testes locais aprovados, incluindo restauração do SQL em banco vazio, reconciliação dos saldos e cobertura diária com consumo 15% maior. Os testes operacionais usam uma cópia em memória, preservando o banco entregue.')

page('Decisões, limites e continuidade')
sub('O que muda no projeto')
para('O Estoca passa a demonstrar estoque gastronômico, com unidades de massa/volume, fichas técnicas e previsão de abastecimento. A identidade do sistema permanece separada da identidade do restaurante. O arquivo decisoes_e_alteracoes.md registra a justificativa das mudanças e a continuidade do projeto.')
sub('O que a base entrega agora')
para('Banco SQLite preenchido, SQL para recriação, CSV para integração, Excel com consolidação por fórmulas, relatório e comandos locais para consultar saldo, registrar entrada e registrar saída. Custos não foram estimados. Não há bebidas no cenário, porque seus produtos e vendas não aparecem nos cardápios enviados.')
sub('O que ainda será validado ou desenvolvido')
para('Aplicação final, login e permissões, lotes/validade, baixa automática por receita, confirmação de recebimento sem duplicidade e integração ao banco definitivo. GitHub depende dos acessos que serão disponibilizados. O arquivo Power BI nativo e os demais trabalhos acadêmicos não são declarados concluídos por esta entrega de dados.')
sub('Caminho de expansão')
para('Priorizar lotes, perdas, rastreabilidade e alertas. Depois, integrar compras e pedidos, medir rendimento das receitas e automatizar baixas. Com investimento, expandir para múltiplos depósitos, código de barras, aplicativo móvel e múltiplos estabelecimentos com isolamento dos dados.')
para('Antes de uso operacional, validar porções, demanda, capacidade de produção/armazenamento, entrega de fornecedores e conservação. O teste de cobertura não garante disponibilidade sob atrasos, perdas extras ou alteração do mix de pratos.')

def footer(c,doc):
    w,h=landscape(A4);c.saveState();c.setFillColor(colors.HexColor('#147D72'));c.rect(0,h-10,w,10,fill=1,stroke=0)
    c.setFillColor(colors.HexColor('#17324D'));c.setFont('Helvetica-Bold',9);c.drawString(42,h-30,'ESTOCA  /  JK BAR E RESTAURANTE')
    c.setFont('Helvetica',8);c.drawString(42,24,'UNIFEOB - Base acadêmica fictícia - versão 1.0');c.drawRightString(w-42,24,str(doc.page));c.restoreState()
out=R/'documentacao/Estoque_JK_14_dias.pdf'
SimpleDocTemplate(str(out),pagesize=landscape(A4),leftMargin=42,rightMargin=42,topMargin=50,bottomMargin=45,title='Estoca - Estoque fictício JK para 14 dias',author='Kauê de Oliveira Silva - RA: 26001417; João Victor Rodrigues Nussa - RA: 26000516; Pedro Joaquim Boletta de Piza - RA: 26001534; Kauã Marques de Carvalho - RA: 26001550').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
