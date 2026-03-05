"""
=====================================================
Leitura dos binários forwarh.dat e forward.dat
=====================================================
"""


# %%
# .. warning::
#
#     Estes arquivos podem mudar de formato com frequência mediante o versionamento
#     do modelo. Recomenda-se atenção com o uso da propriedade `set_version` para a
#     versão correta e, caso esta não seja suportada, a abertura de uma `issue <https://github.com/rjmalves/inewave/issues>`_.
#

# %%
# Para ilustrar o processamento destes arquivos, serão usados módulos de visualização
# como o plotly
import plotly.io as pio

pio.templates.default = "ggplot2"


# %%
# O forward.dat é o arquivo binário de saída do modelo NEWAVE que contém as informações
# sobre a simulação final. Para casos oficiais, seu tamanho pode chegar a vários GB.
# A leitura deste arquivo só é possível ao processar anteriormente o arquivo forwarh.dat,
# que contém informações necessárias para configurar a leitura do forward.dat.

from inewave.newave.forwarh import Forwarh

arq_cabecalho = Forwarh.read("./newave/forwarh.dat")

tamanho_registro = arq_cabecalho.tamanho_registro_arquivo_forward

numero_estagios = 1  # arq_cabecalho.numero_estagios_estudo
numero_forwards = 2  # arq_cabecalho.numero_series_gravadas

numero_forwards = arq_cabecalho.numero_registros_arquivo_forward
numero_rees = arq_cabecalho.numero_rees
numero_submercados = arq_cabecalho.numero_submercados
numero_total_submercados = arq_cabecalho.numero_total_submercados
numero_patamares_carga = arq_cabecalho.numero_patamares_carga
numero_patamares_deficit = arq_cabecalho.numero_patamares_deficit
numero_classes_termicas_submercados = (
    arq_cabecalho.numero_classes_termicas_submercados
)

# %%
# Além do arquivo forwarh.dat, é necessário obter informações de alguns outros
# arquivos de entrada, que serão utilizadas para a montagem dos `DataFrame` retornados
# pelas propriedades da classe `Forward` de maneira coerente

from inewave.newave import Adterm, Agrint, Confhd, Conft

arq_adterm = Adterm.read("./newave/adterm.dat")
arq_agrint = Agrint.read("./newave/agrint.dat")
arq_confhd = Confhd.read("./newave/confhd.dat")
arq_conft = Conft.read("./newave/conft.dat")

numero_agrupamentos_intercambio = len(
    arq_agrint.agrupamentos["agrupamento"].unique()
)

uhes = arq_confhd.usinas
nomes_usinas_hidreletricas = uhes["nome_usina"].to_list()
numero_usinas_hidreletricas = len(nomes_usinas_hidreletricas)

utes = arq_conft.usinas
utes = utes.sort_values("submercado")
nomes_classes_termicas = utes["nome_usina"].unique()

lag_maximo_usinas_gnl = arq_adterm.despachos["lag"].max()


# %%
# .. warning::
#
#     Caso a leitura esteja sendo feita nos arquivos provenientes de uma execução
#     oficial do modelo, recomenda-se que seja em um ambiente com quantidade suficiente
#     de memória RAM. A implementação atual realiza a conversão de todos os dados lidos
#     para formato de DataFrames, resultando em um grande consumo de memória. Os arquivos
#     tratados neste exemplo são de uma execução reduzida específica para os testes.
#


# %%
# A leitura do arquivo binário com os dados é feita utilizando as informações
# adquiridas anteriormente. O número de estágios e simulações forward,
# que deveriam ser obtidos do arquivo cabeçalho, são atribuídos manualmente como constantes,
# pois o arquivo de dados foi editado manualmente para economia de espaço no repositório.
# Da mesma forma, as variáveis de número de parques eólicos equivalentes e estações
# de bombeamento também foram atribuídos manualmente, pois deveriam ser lidos dos
# arquivos em formato LIBS, que não existiam para o caso de teste.

from inewave.newave.forward import Forward

arq_binario = Forward.read(
    "./newave/forward.dat",
    tamanho_registro=tamanho_registro,
    numero_estagios=1,
    numero_forwards=2,
    numero_rees=numero_rees,
    numero_submercados=numero_submercados,
    numero_total_submercados=numero_total_submercados,
    numero_patamares_carga=numero_patamares_carga,
    numero_patamares_deficit=numero_patamares_deficit,
    numero_agrupamentos_intercambio=numero_agrupamentos_intercambio,
    numero_classes_termicas_submercados=numero_classes_termicas_submercados,
    numero_usinas_hidreletricas=numero_usinas_hidreletricas,
    lag_maximo_usinas_gnl=lag_maximo_usinas_gnl,
    numero_parques_eolicos_equivalentes=0,
    numero_estacoes_bombeamento=0,
    nomes_classes_termicas=nomes_classes_termicas,
    nomes_usinas_hidreletricas=nomes_usinas_hidreletricas,
)

# %%
# O arquivo binário possui um grande número de propriedades, que podem
# ser consultadas diretamente na documentação do :ref:`Forward <forward>`. Um exemplo é
# o custo marginal da operação em R$/MWh

cmo = arq_binario.custo_marginal_operacao
cmo
