"""
========================================
Análise de modificações do modif.dat
========================================
"""


# %%
# Para realizar a análise do modif.dat será utilizado o módulo plotly
import plotly.express as px
import plotly.io as pio
import pandas as pd
from datetime import datetime

pio.templates.default = "ggplot2"

# %%
# O modif.dat é principal arquivo de entrada do NEWAVE para alterações cadastrais
# relacioanadas a usinas hidrelétricas. Também nele são encontradas algumas restrições
# físicas e operativas das usinas, que frequentemente precisam ser alteradas.
# Assim, este exemplo contém uma análise e edição nas restrições operativas
# de uma UHE. O modif.dat é o único arquivo modelado com a abordagem de registros
# que é exclusivo do modelo NEWAVE e, por isso, sua lógica é diferente dos demais.
from inewave.newave import Modif

arq_modif = Modif.read("./newave/modif.dat")


# %%
# É possível visualizar todos os registros de um mesmo tipo existentes no arquivo
# no formato de DataFrame, porém este formato é apenas para visualização.
arq_modif.usina(df=True)

# %%
# O outro formato para visualização dos registros é a extração dos objetos em si,
# que é a maneira de se realizar também a edição de seus conteúdos. Desta forma, também
# é possível aplicar filtros no registro desejado.
arq_modif.vazmint(data_inicio=datetime(2021, 2, 1))

# %%
# Para editar o arquivo modif, necessitamos frequentemente de deletar registros existentes
# e de criar novos registros. Para isto, instanciamos os modelos dos registros existentes
# no módulo *inewave* e adicionamos ao objeto do arquivo através dos métodos da classe.
from inewave.newave.modif import TURBMAXT

codigo_usina_modificada = 7

novo_registro = TURBMAXT()
novo_registro.data_inicio = datetime(2021, 2, 1)
novo_registro.turbinamento = 1000.0
arq_modif.data.add_after(
    arq_modif.usina(codigo=codigo_usina_modificada),
    novo_registro,
)

# %%
# Podemos conferir se a inserção foi feita com sucesso ao listar os registros da usina
# em questão:
registros_usinas = arq_modif.modificacoes_usina(codigo_usina_modificada)
print([r for r in registros_usinas if isinstance(r, TURBMAXT)])


# %%
# Além de edições, podemos visualizar informações contidas no modif. Por exemplo, a variação
# da cota de montante de JIRAU ao longo do tempo:
from inewave.newave.modif import CMONT

registros_cmont = [
    r for r in arq_modif.modificacoes_usina(codigo=285) if isinstance(r, CMONT)
]
datas = [r.data_inicio for r in registros_cmont]
cotas = [r.nivel for r in registros_cmont]
df_cmont = pd.DataFrame(data={"data": datas, "cota": cotas})
fig = px.line(df_cmont, x="data", y="cota")
fig
