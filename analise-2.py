# Trabalho prático - Patas & Cia Pet Shop
# Análise das vendas de novembro usando os arquivos vendas.csv e configuracao.json

import csv
import json


# função que soma os valores de uma lista
def calcular_total(valores):
    total = 0
    for valor in valores:
        total += valor
    return total


# função que calcula a média dos valores de uma lista
def calcular_media(valores):
    total = calcular_total(valores)
    media = total / len(valores)
    return media


# função que soma um valor dentro de um dicionário
# se a chave ainda não existe, ela é criada
def somar_no_dicionario(dicionario, chave, valor):
    if chave in dicionario:
        dicionario[chave] += valor
    else:
        dicionario[chave] = valor


# leitura do arquivo JSON com as informações da gerência
with open("configuracao.json", "r", encoding="utf-8") as arquivo:
    empresa = json.load(arquivo)

print("===== RELATÓRIO DE VENDAS =====")
print(f"Empresa: {empresa['empresa']}")
print(f"Cidade: {empresa['cidade']}")
print(f"Período: {empresa['periodo']}")
print()

# variáveis que vão guardar os resultados
valores_vendas = []
quantidade_registros = 0
unidades_vendidas = 0
unidades_produto = {}
faturamento_produto = {}
faturamento_categoria = {}
faturamento_pagamento = {}
faturamento_vendedor = {}

# leitura do arquivo CSV com as vendas
print("Vendas do mês:")

with open("vendas.csv", "r", encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=";")

    for linha in leitor:
        produto = linha["produto"]
        categoria = linha["categoria"]
        quantidade = int(linha["quantidade"])
        preco = float(linha["preco_unitario"])

        # valor total da venda
        valor_venda = quantidade * preco
        valores_vendas.append(valor_venda)

        # contador de registros e acumulador de unidades
        quantidade_registros += 1
        unidades_vendidas += quantidade

        # separando as informações por produto, categoria, pagamento e vendedor
        somar_no_dicionario(unidades_produto, produto, quantidade)
        somar_no_dicionario(faturamento_produto, produto, valor_venda)
        somar_no_dicionario(faturamento_categoria, categoria, valor_venda)
        somar_no_dicionario(faturamento_pagamento, linha["forma_pagamento"], valor_venda)
        somar_no_dicionario(faturamento_vendedor, linha["vendedor"], valor_venda)

        print(f"{linha['data']} - {produto}: {quantidade} x R$ {preco:.2f} = R$ {valor_venda:.2f}")

# resumo geral do mês
faturamento_total = calcular_total(valores_vendas)
media_venda = calcular_media(valores_vendas)

print()
print("===== RESUMO DO MÊS =====")
print(f"Faturamento total: R$ {faturamento_total:.2f}")
print(f"Vendas registradas: {quantidade_registros}")
print(f"Unidades vendidas: {unidades_vendidas}")
print(f"Média por venda: R$ {media_venda:.2f}")
print(f"Maior venda: R$ {max(valores_vendas):.2f}")
print(f"Menor venda: R$ {min(valores_vendas):.2f}")

# faturamento de cada produto e produto mais vendido
mais_vendido = ""
maior_quantidade = 0
produto_maior_faturamento = ""
maior_faturamento = 0

print()
print("===== PRODUTOS E SERVIÇOS =====")
for produto in unidades_produto:
    print(f"{produto}: {unidades_produto[produto]} unidades - R$ {faturamento_produto[produto]:.2f}")

    if unidades_produto[produto] > maior_quantidade:
        maior_quantidade = unidades_produto[produto]
        mais_vendido = produto

    if faturamento_produto[produto] > maior_faturamento:
        maior_faturamento = faturamento_produto[produto]
        produto_maior_faturamento = produto

print()
print(f"Mais vendido: {mais_vendido} ({maior_quantidade} unidades)")
print(f"Maior faturamento: {produto_maior_faturamento} (R$ {maior_faturamento:.2f})")

# faturamento de cada categoria comparado com a meta da categoria
categorias_abaixo_meta = []
melhor_categoria = ""
maior_valor_categoria = 0

print()
print("===== CATEGORIAS =====")
for categoria in empresa["categorias"]:
    valor = faturamento_categoria[categoria]
    meta_categoria = empresa["meta_por_categoria"][categoria]
    participacao = valor / faturamento_total * 100

    if valor >= meta_categoria:
        print(f"{categoria}: R$ {valor:.2f} ({participacao:.1f}% do total) - meta de R$ {meta_categoria:.2f} atingida")
    else:
        print(f"{categoria}: R$ {valor:.2f} ({participacao:.1f}% do total) - meta de R$ {meta_categoria:.2f} não atingida")
        categorias_abaixo_meta.append(categoria)

    # comparação entre as categorias para achar a que mais faturou
    if valor > maior_valor_categoria:
        maior_valor_categoria = valor
        melhor_categoria = categoria

print(f"Categoria com maior faturamento: {melhor_categoria}")

# formas de pagamento e vendedores
print()
print("===== FORMAS DE PAGAMENTO =====")
for forma in faturamento_pagamento:
    print(f"{forma}: R$ {faturamento_pagamento[forma]:.2f}")

print()
print("===== VENDEDORES =====")
for vendedor in faturamento_vendedor:
    print(f"{vendedor}: R$ {faturamento_vendedor[vendedor]:.2f}")

# comparação com a meta de faturamento do mês
meta = empresa["meta_faturamento"]
porcentagem_meta = faturamento_total / meta * 100

print()
print("===== META DO MÊS =====")
print(f"Meta de faturamento: R$ {meta:.2f}")
print(f"Porcentagem atingida: {porcentagem_meta:.1f}%")

if faturamento_total >= meta:
    print("Parabéns! A meta do mês foi atingida.")
else:
    falta = meta - faturamento_total
    print(f"A meta não foi atingida. Faltaram R$ {falta:.2f}.")

# comparação da média por venda com a meta de ticket médio
meta_ticket = empresa["meta_ticket_medio"]
if media_venda >= meta_ticket:
    print(f"A média por venda ficou acima da meta de R$ {meta_ticket:.2f}.")
else:
    print(f"A média por venda ficou abaixo da meta de R$ {meta_ticket:.2f}.")

# comparação com o orçamento de despesas
despesas = empresa["orcamento_despesas"]
saldo = faturamento_total - despesas

print()
print("===== DESPESAS =====")
print(f"Orçamento de despesas: R$ {despesas:.2f}")

if saldo >= 0:
    print(f"O faturamento cobre as despesas. Sobram R$ {saldo:.2f}.")
else:
    print(f"O faturamento não cobre as despesas. Faltam R$ {-saldo:.2f}.")

# sugestões para a administração no próximo mês
print()
print("===== SUGESTÕES PARA O PRÓXIMO MÊS =====")
for categoria in categorias_abaixo_meta:
    print(f"- Fazer promoções para aumentar as vendas de {categoria}.")

print(f"- Continuar investindo em {mais_vendido}, que foi o mais vendido.")
print(f"- Dar destaque para {produto_maior_faturamento}, que trouxe o maior faturamento.")
