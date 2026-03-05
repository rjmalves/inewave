"""
========================================
Análise do pmo.dat
========================================
"""


# %%
# Para realizar a análise do pmo.dat, será utilizado o módulo plotly
from inewave.newave import Pmo
import plotly.express as px
import plotly.io as pio

pio.templates.default = "ggplot2"


arq_pmo = Pmo.read("./newave/pmo.dat")

# %%
# Os dados associados ao processo de convergência são obtidos com:
arq_pmo.convergencia.head(10)

# %%
# O formato dos dados de custos por etapa também são acessíveis:
arq_pmo.custo_operacao_series_simuladas.head(10)

# %%
# Também é possível acessar o custo total:
arq_pmo.custo_operacao_total

# %%
# Cada arquivo pode ser visualizado de diferentes maneiras, a depender da aplicação.
# Por exemplo, é comum avaliar a convergência do modelo através da variação do Zinf.

fig = px.line(
    arq_pmo.convergencia,
    x="iteracao",
    y=["zinf", "zsup"],
)
fig

# %%
# Quando se analisam os custos de cada fonte, geralmente são feitos gráficos de barras
# empilhadas ou setores:

custos = arq_pmo.custo_operacao_series_simuladas
fig = px.pie(
    custos.loc[custos["valor_esperado"] > 0],
    values="valor_esperado",
    names="parcela",
)
fig

# %%
# Também é possível acessar diversas outras informações existentes no arquivo, como o
# relatório das produtibilidades calculadas e a tendência hidrológica vista pelo modelo.
# Mais informações estão disponíveis na página de referência.
