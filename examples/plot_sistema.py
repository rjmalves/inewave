"""
=====================================================
Geração de sensibilidades de mercado no sistema.dat
=====================================================
"""


# %%
# Para realizar a análise do sistema.dat, será utilizado o módulo plotly
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "ggplot2"


# %%
# O sistema.dat é o arquivo de entrada do modelo NEWAVE que contém informações
# sobre os submercados de energia. Em particular, são definidos os submercados
# e as curvas de mercado de energia esperado por estágio, para cada um.
# É uma análise comum a análise de sensibilidades em relação ao mercado de energia
# e à geração das usinas não simuladas e, por isso, será ilustrado um exemplo deste caso.
from inewave.newave import Sistema

arq_sistema = Sistema.read("./newave/sistema.dat")

# %%
# A definição dos submercados é acessível através do bloco que define os custos de déficit
arq_sistema.custo_deficit

# %%
# As informações de mercado de energia são reunidas em uma única propriedade
# e esta pode ser alterada livremente
arq_sistema.mercado_energia


# %%
# Será feito um gráfico de área empilhado. Para isso, serão geradas algumas variáveis auxiliares.
df = arq_sistema.mercado_energia
x = pd.date_range(
    df["data"].min(),
    df["data"].max(),
    freq="MS",
)

# %%
# Para a figura, são geradas as retas independentemente
fig = go.Figure()
for submercado in df["codigo_submercado"].unique():
    y = df.loc[df["codigo_submercado"] == submercado, "valor"]
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            stackgroup="one",
            name=str(submercado),
        )
    )

fig.update_xaxes(title="Data")
fig.update_yaxes(title="Mercado de Energia (MWmes)")
fig.update_layout(legend_title_text="Submercado")
fig

# %%
# É possível realizar edições livres na propriedade do arquivo, para geração de estudos
# de sensibilidades. Por exemplo, é possível aumentar a carga do submercado NORDESTE
# em 30% e conferir o efeito na operação com a execução do modelo.
arq_sistema.mercado_energia.loc[
    arq_sistema.mercado_energia["codigo_submercado"] == 3, "valor"
] *= 1.3

from io import StringIO

conteudo_sistema = StringIO()
arq_sistema.write(conteudo_sistema)
print(conteudo_sistema.getvalue())
