# Patas & Cia Pet Shop — Análise de vendas com Python

Trabalho prático de análise de dados de uma empresa usando **Python**, **CSV** e **JSON**.

## Contexto da empresa

A **Patas & Cia Pet Shop** é um pet shop localizado em **Valinhos - SP** que atende cães e gatos. A empresa trabalha com três categorias:

| Categoria | Exemplos |
|---|---|
| **Serviços** | Banho, banho e tosa |
| **Alimentação** | Ração premium 15 kg, petisco natural, areia higiênica |
| **Acessórios** | Coleira ajustável, brinquedo mordedor, cama para pets |

A administração precisa tomar decisões para o próximo mês, mas as informações estão em arquivos diferentes: a equipe de vendas enviou os registros de **novembro de 2026** e a gerência enviou as metas da empresa. O programa reúne esses dados e gera um relatório para apoiar as decisões.

## Arquivos do projeto

| Arquivo | Descrição |
|---|---|
| `vendas.csv` | 15 registros de vendas enviados pela equipe de vendas. Colunas: `data`, `produto`, `categoria`, `quantidade`, `preco_unitario`, `forma_pagamento` e `vendedor`. Separador: ponto e vírgula (`;`). |
| `configuracao.json` | Informações da gerência: nome da empresa, segmento, cidade, período, meta de faturamento, orçamento de despesas, meta de ticket médio, categorias e meta de cada categoria. |
| `analise.py` | Programa em Python que lê os dois arquivos, faz os cálculos e mostra o relatório. |
| `README.md` | Este arquivo, com a explicação do projeto. |

## Funcionamento do programa

O `analise.py` usa os módulos `csv` e `json` do Python e executa as seguintes etapas:

1. **Lê o `configuracao.json`** com `json.load()` e mostra os dados da empresa.
2. **Lê o `vendas.csv`** com `csv.DictReader()`, linha por linha.
3. **Calcula o valor de cada venda** (quantidade × preço unitário).
4. **Calcula o faturamento total** do período.
5. **Mostra o número de registros, as unidades vendidas**, o ticket médio e a maior e a menor venda.
6. **Identifica o produto ou serviço mais vendido** em quantidade e o de maior faturamento.
7. **Compara o faturamento com a meta** do JSON e mostra o percentual atingido e quanto faltou ou sobrou.
8. **Apresenta mensagens claras para a administração**, organizadas em seções.

**Análises extras:**
- Faturamento e participação (%) de cada produto.
- Média por venda (ticket médio), maior venda e menor venda.
- Faturamento de cada categoria comparado com a meta da categoria.
- Comparação entre categorias, com a participação (%) de cada uma e a classificação da que mais faturou para a que menos faturou.
- Faturamento por forma de pagamento e por vendedor.
- Média por venda comparada com a meta de ticket médio do JSON.
- Faturamento comparado com o orçamento de despesas.
- Recomendações automáticas para o próximo mês.

**Conceitos de Python utilizados:** funções, listas, dicionários, estruturas de repetição (`for` e `while`), estruturas condicionais (`if`/`else`), contadores e acumuladores, f-strings e tratamento de erro com `try`/`except` para o caso de algum arquivo não ser encontrado.

## Como executar

1. Tenha o **Python 3** instalado. O programa não precisa de nenhuma biblioteca externa.
2. Baixe ou clone este repositório:
   ```bash
   git clone https://github.com/ambroza22/patas-e-cia-analise-vendas.git
   ```
3. Entre na pasta do projeto:
   ```bash
   cd patas-e-cia-analise-vendas
   ```
4. Execute o programa:
   ```bash
   python analise.py
   ```
   No Mac ou Linux, pode ser necessário usar `python3 analise.py`.

Os três arquivos (`vendas.csv`, `configuracao.json` e `analise.py`) precisam estar na **mesma pasta**.

## Principais resultados de novembro de 2026

| Indicador | Resultado |
|---|---|
| Faturamento total | R$ 7.167,80 |
| Meta de faturamento | R$ 7.500,00 (95,6% atingido) |
| Vendas registradas | 15 |
| Unidades vendidas | 125 |
| Ticket médio | R$ 477,85 (meta de R$ 450,00 atingida) |
| Mais vendido em quantidade | Banho (32 unidades) |
| Maior faturamento | Banho e tosa (R$ 1.785,00) |
| Saldo após despesas | R$ 1.967,80 |

**Conclusão:** a categoria **Serviços** superou a meta (107,4%), mas **Alimentação** (92,8%) e **Acessórios** (69,8%) ficaram abaixo, o que impediu o pet shop de atingir a meta geral por R$ 332,20. Para o próximo mês, a recomendação é reforçar a venda de acessórios e rações, aproveitando o fluxo de clientes que já vão à loja para os serviços de banho e tosa.

## Autor

Joao Ambrozini
