"""
=====================================================
Processamento dos dados do polinjus.csv
=====================================================
"""

# %%
# Para realizar o processamento do polinjus.csv, será utilizado o módulo plotly
import plotly.graph_objects as go
import plotly.io as pio
from numpy.polynomial import Polynomial

pio.templates.default = "ggplot2"


# %%
# O polinjus.csv é um arquivo de entrada das LIBS, utilizado pelo modelo NEWAVE particularmente
# em casos com estágios individualizados, ou para execução da simulação final individualizada.
# Para processar a sua informação, o usuário deve importar a class `UsinasHidreletricas`, que contém
# todos os métodos necessários
from inewave.libs import UsinasHidreletricas

arq_polinjus = UsinasHidreletricas.read("./libs/polinjus.csv")

# %%
# A implementação de todos os arquivos das LIBS segue o formato de arquivos por registro,
# contendo informações em linhas de comentários e com delimitador ';'. Além disso,
# a primeira coluna sempre identifica qual o registro cadastrado na linha em questão. O
# número total de colunas em cada linha é variável, de acordo com o valor da primeira coluna.

# %%
# Estão disponíveis métodos para cada registro, com argumentos opcionais para realizar filtros
# nos objetos a serem processados
registros = arq_polinjus.hidreletrica_curvajusante(codigo_usina=1)
registros


# %%
# É possível realizar a edição dos objetos retornados relacionados
# a cada registro. Para tal, basta atribuir valores a cada propriedade:
registros[0].indice_familia = 5


# %%
# Outra possibilidade é gerar uma visualização dos conteúdos do arquivo
# no formato de DataFrame. Neste caso, a informação é somente leitura
df = arq_polinjus.hidreletrica_curvajusante(df=True)
df.head()

# %%
# Com as informações do polinjus.csv é possível gerar uma visualização para os polinômios
# de jusante. Em particular, o registro HIDRELETRICA-CURVAJUSANTE-POLINOMIOPORPARTES-SEGMENTO
# contém as informações desejadas. No caso, por exemplo, para a usina de código 7
df = arq_polinjus.hidreletrica_curvajusante_polinomio_segmento(df=True)
df = df.loc[df["codigo_usina"] == 7]
df.head()

# %%
# Para a visualização, vamos gerar 100 amostras para cada segmento, que é aproximado
# por um polinômio.
num_pontos = 100
ordem_polinomios = 4
cols_coeficientes = [f"coeficiente_a{i}" for i in range(ordem_polinomios + 1)]

num_curvas = len(df["indice_familia"].unique())
vazoes_limites = []
pontos_familias = {}
for indice_familia in range(num_curvas):
    df_familia = df.loc[df["indice_familia"] == indice_familia]
    pontos_familias[indice_familia] = {"x": [], "y": []}
    indices_polinomios = df_familia["indice_polinomio"].unique().tolist()
    for indice_polinomio in indices_polinomios:
        df_polinomio = df_familia.loc[
            df_familia["indice_polinomio"] == indice_polinomio
        ]
        lim_inf = df_polinomio["limite_inferior_vazao_jusante"].iloc[0]
        lim_sup = df_polinomio["limite_superior_vazao_jusante"].iloc[0]
        vazoes_limites += [lim_inf, lim_sup]
        coeficientes = df_polinomio[cols_coeficientes].to_numpy().flatten()
        polinomio = Polynomial(coeficientes, domain=[lim_inf, lim_sup])
        x, y = polinomio.linspace(n=num_pontos)
        pontos_familias[indice_familia]["x"] += list(x)
        pontos_familias[indice_familia]["y"] += list(y)


# %%
# Para visualizar:

fig = go.Figure()
for familia, pontos in pontos_familias.items():
    fig.add_trace(
        go.Scatter(
            x=pontos["x"],
            y=pontos["y"],
            mode="lines",
            name=str(familia),
        )
    )

fig.update_xaxes(title="Vazão Defluente (m3/s)")
fig.update_yaxes(title="Nível de Jusante (m)")
fig.update_layout(legend_title_text="Família")
fig
