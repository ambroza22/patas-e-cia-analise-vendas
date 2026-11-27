# =============================================================
# Trabalho prático - Patas & Cia Pet Shop
# Análise das vendas do mês usando os arquivos:
#   - vendas.csv        (registros enviados pela equipe de vendas)
#   - configuracao.json (metas e informações enviadas pela gerência)
# =============================================================

import csv
import json


# -------------------------------------------------------------
# FUNÇÕES AUXILIARES
# -------------------------------------------------------------

# Soma todos os valores de uma lista
def calcular_total(valores):
    total = 0
    for valor in valores:
        total += valor
    return total


# Calcula a média dos valores de uma lista
def calcular_media(valores):
    if len(valores) == 0:
        return 0
    return calcular_total(valores) / len(valores)


# Formata um número no padrão de moeda brasileiro (ex.: R$ 1.234,56)
def formatar_moeda(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


# Adiciona um valor a uma chave do dicionário (cria a chave se não existir)
def acumular(dicionario, chave, valor):
    if chave in dicionario:
        dicionario[chave] += valor
    else:
        dicionario[chave] = valor


# Encontra a chave com o maior valor em um dicionário
def maior_do_dicionario(dicionario):
    chave_maior = ""
    valor_maior = 0
    for chave in dicionario:
        if dicionario[chave] > valor_maior:
            valor_maior = dicionario[chave]
            chave_maior = chave
    return chave_maior, valor_maior


# Imprime um título de seção para deixar o relatório organizado
def titulo(texto):
    print()
    print("=" * 60)
    print(texto)
    print("=" * 60)


# -------------------------------------------------------------
# 1. LEITURA DO ARQUIVO JSON (informações da gerência)
# -------------------------------------------------------------
try:
    with open("configuracao.json", "r", encoding="utf-8") as arquivo:
        config = json.load(arquivo)
except FileNotFoundError:
    print("Erro: o arquivo configuracao.json não foi encontrado.")
    exit()

titulo(f"RELATÓRIO DE VENDAS - {config['empresa'].upper()}")
print(f"Segmento: {config['segmento']}")
print(f"Cidade:   {config['cidade']}")
print(f"Período:  {config['periodo']}")


# -------------------------------------------------------------
# 2. LEITURA DO ARQUIVO CSV (vendas) E CÁLCULO DE CADA VENDA
# -------------------------------------------------------------
valores_vendas = []            # valor total de cada venda
numero_registros = 0           # contador de vendas
unidades_vendidas = 0          # acumulador de unidades
unidades_produto = {}          # unidades vendidas por produto
faturamento_produto = {}       # faturamento por produto
faturamento_categoria = {}     # faturamento por categoria
faturamento_pagamento = {}     # faturamento por forma de pagamento
faturamento_vendedor = {}     # faturamento por vendedor

titulo("VENDAS REGISTRADAS")

try:
    with open("vendas.csv", "r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")

        for linha in leitor:
            produto = linha["produto"]
            categoria = linha["categoria"]
            quantidade = int(linha["quantidade"])
            preco = float(linha["preco_unitario"])

            # valor total da venda = quantidade x preço unitário
            valor_venda = quantidade * preco
            valores_vendas.append(valor_venda)

            # contadores e acumuladores gerais
            numero_registros += 1
            unidades_vendidas += quantidade

            # agrupamentos usando dicionários
            acumular(unidades_produto, produto, quantidade)
            acumular(faturamento_produto, produto, valor_venda)
            acumular(faturamento_categoria, categoria, valor_venda)
            acumular(faturamento_pagamento, linha["forma_pagamento"], valor_venda)
            acumular(faturamento_vendedor, linha["vendedor"], valor_venda)

            print(f"{linha['data']} | {produto:<20} | {quantidade:>3} x "
                  f"{formatar_moeda(preco):>11} = {formatar_moeda(valor_venda):>12}")
except FileNotFoundError:
    print("Erro: o arquivo vendas.csv não foi encontrado.")
    exit()


# -------------------------------------------------------------
# 3. RESUMO GERAL DO PERÍODO
# -------------------------------------------------------------
faturamento_total = calcular_total(valores_vendas)
ticket_medio = calcular_media(valores_vendas)

titulo("RESUMO GERAL")
print(f"Faturamento total:      {formatar_moeda(faturamento_total)}")
print(f"Vendas registradas:     {numero_registros}")
print(f"Unidades vendidas:      {unidades_vendidas}")
print(f"Média por venda:        {formatar_moeda(ticket_medio)}")
print(f"Maior venda:            {formatar_moeda(max(valores_vendas))}")
print(f"Menor venda:            {formatar_moeda(min(valores_vendas))}")


# -------------------------------------------------------------
# 4. ANÁLISE POR PRODUTO OU SERVIÇO
# -------------------------------------------------------------
mais_vendido, maior_quantidade = maior_do_dicionario(unidades_produto)
maior_faturamento, valor_maior_faturamento = maior_do_dicionario(faturamento_produto)

titulo("ANÁLISE POR PRODUTO OU SERVIÇO")
for produto in unidades_produto:
    participacao = faturamento_produto[produto] / faturamento_total * 100
    print(f"{produto:<20} | {unidades_produto[produto]:>3} un. | "
          f"{formatar_moeda(faturamento_produto[produto]):>12} | {participacao:5.1f}% do total")

print()
print(f"Mais vendido em quantidade: {mais_vendido} ({maior_quantidade} unidades)")
print(f"Maior faturamento:          {maior_faturamento} "
      f"({formatar_moeda(valor_maior_faturamento)})")


# -------------------------------------------------------------
# 5. FATURAMENTO POR CATEGORIA x META DE CADA CATEGORIA (JSON)
# -------------------------------------------------------------
titulo("CATEGORIAS x METAS")
categorias_abaixo_meta = []

for categoria in config["categorias"]:
    valor = faturamento_categoria.get(categoria, 0)
    meta_categoria = config["meta_por_categoria"][categoria]
    percentual = valor / meta_categoria * 100

    if valor >= meta_categoria:
        situacao = "META ATINGIDA"
    else:
        situacao = f"faltaram {formatar_moeda(meta_categoria - valor)}"
        categorias_abaixo_meta.append(categoria)

    print(f"{categoria:<12} | {formatar_moeda(valor):>12} de {formatar_moeda(meta_categoria):>12} "
          f"({percentual:5.1f}%) -> {situacao}")

# comparação entre as categorias: participação no total e classificação
titulo("COMPARAÇÃO ENTRE CATEGORIAS")
categorias_restantes = dict(faturamento_categoria)   # cópia para não alterar o original
posicao = 1

while len(categorias_restantes) > 0:
    categoria, valor = maior_do_dicionario(categorias_restantes)
    participacao = valor / faturamento_total * 100
    print(f"{posicao}º lugar: {categoria:<12} | {formatar_moeda(valor):>12} | "
          f"{participacao:5.1f}% do faturamento")
    del categorias_restantes[categoria]
    posicao += 1


# -------------------------------------------------------------
# 6. FORMAS DE PAGAMENTO E DESEMPENHO DOS VENDEDORES
# -------------------------------------------------------------
titulo("FORMAS DE PAGAMENTO")
for forma in faturamento_pagamento:
    participacao = faturamento_pagamento[forma] / faturamento_total * 100
    print(f"{forma:<18} | {formatar_moeda(faturamento_pagamento[forma]):>12} | {participacao:5.1f}%")

titulo("FATURAMENTO POR VENDEDOR")
for vendedor in faturamento_vendedor:
    print(f"{vendedor:<10} | {formatar_moeda(faturamento_vendedor[vendedor]):>12}")


# -------------------------------------------------------------
# 7. COMPARAÇÃO COM A META DE FATURAMENTO (JSON)
# -------------------------------------------------------------
meta = config["meta_faturamento"]
percentual_meta = faturamento_total / meta * 100

titulo("META DE FATURAMENTO")
print(f"Meta do período:     {formatar_moeda(meta)}")
print(f"Faturamento obtido:  {formatar_moeda(faturamento_total)}")
print(f"Percentual atingido: {percentual_meta:.1f}%")

if faturamento_total >= meta:
    print(f"Meta ATINGIDA! Superou em {formatar_moeda(faturamento_total - meta)}.")
else:
    print(f"Meta NÃO atingida. Faltaram {formatar_moeda(meta - faturamento_total)}.")

# comparação do ticket médio com a meta de ticket médio
meta_ticket = config["meta_ticket_medio"]
if ticket_medio >= meta_ticket:
    print(f"Ticket médio de {formatar_moeda(ticket_medio)} acima da meta de "
          f"{formatar_moeda(meta_ticket)}.")
else:
    print(f"Ticket médio de {formatar_moeda(ticket_medio)} abaixo da meta de "
          f"{formatar_moeda(meta_ticket)}.")


# -------------------------------------------------------------
# 8. FATURAMENTO x ORÇAMENTO DE DESPESAS (JSON)
# -------------------------------------------------------------
despesas = config["orcamento_despesas"]
saldo = faturamento_total - despesas

titulo("FATURAMENTO x DESPESAS")
print(f"Orçamento de despesas: {formatar_moeda(despesas)}")

if saldo >= 0:
    print(f"O faturamento cobre as despesas. Saldo positivo de {formatar_moeda(saldo)}.")
else:
    print(f"O faturamento NÃO cobre as despesas. Faltam {formatar_moeda(-saldo)}.")


# -------------------------------------------------------------
# 9. RECOMENDAÇÕES PARA A ADMINISTRAÇÃO (PRÓXIMO MÊS)
# -------------------------------------------------------------
forma_principal, valor_forma = maior_do_dicionario(faturamento_pagamento)

titulo("RECOMENDAÇÕES PARA O PRÓXIMO MÊS")

if faturamento_total < meta:
    print(f"- Para bater a meta, é preciso vender cerca de "
          f"{formatar_moeda((meta - faturamento_total) / 4)} a mais por semana.")

for categoria in categorias_abaixo_meta:
    print(f"- Reforçar as vendas de {categoria} com promoções e exposição na loja.")

print(f"- Garantir disponibilidade de '{mais_vendido}', o item com mais unidades vendidas.")
print(f"- Priorizar '{maior_faturamento}', que gerou o maior faturamento do mês.")
print(f"- {forma_principal} foi a forma de pagamento mais usada "
      f"({valor_forma / faturamento_total * 100:.1f}% do faturamento).")

print()
print("Fim do relatório.")
