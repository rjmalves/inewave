"""
=======================================================
Análise das configurações das usinas hidrelétricas
=======================================================
"""


# %%
# O arquivo confhd.dat contém as configurações das usinas hidrelétricas
# do sistema brasileiro, incluindo características físicas, períodos
# históricos e modificações específicas do estudo.

import plotly.express as px
import plotly.io as pio

from inewave.newave import Confhd

pio.templates.default = "ggplot2"

# %%
# **Leitura das configurações hidrelétricas**
#
# O arquivo confhd.dat é essencial para definir o sistema hidrelétrico
# que será simulado pelo NEWAVE:

arq_confhd = Confhd.read("./newave/confhd.dat")
print("Arquivo confhd.dat lido com sucesso")

# %%
# **Análise geral das usinas**
#
# Examinando as características básicas do sistema hidrelétrico:

usinas = arq_confhd.usinas
print(f"Total de usinas hidrelétricas: {len(usinas)}")
print(f"Colunas disponíveis: {list(usinas.columns)}")

print("\nPrimeiras usinas:")
print(usinas.head())

# Análise por REE
usinas_por_ree = (
    usinas.groupby("ree")
    .agg({"codigo_usina": "count", "volume_inicial_percentual": "mean"})
    .round(2)
)
usinas_por_ree.columns = ["quantidade", "volume_inicial_medio"]

print("\nDistribuição de usinas por REE:")
print(usinas_por_ree)

# Visualização da distribuição por REE
fig = px.bar(
    usinas_por_ree.reset_index(),
    x="ree",
    y="quantidade",
    title="Distribuição de Usinas Hidrelétricas por REE",
    labels={"ree": "REE", "quantidade": "Número de Usinas"},
)
fig

# %%
# **Análise das usinas existentes vs. futuras**
#
# Classificando usinas por status de existência:

# Distribuição por status de existência
status_dist = usinas["usina_existente"].value_counts()
print("Distribuição por status:")
for status, count in status_dist.items():
    percentual = count / len(usinas) * 100
    print(f"- {status}: {count} usinas ({percentual:.1f}%)")

# Visualização do status
fig = px.pie(
    values=status_dist.values,
    names=status_dist.index,
    title="Distribuição de Usinas por Status de Existência",
)
fig

# %%
# **Análise dos volumes iniciais**
#
# Verificando as condições iniciais dos reservatórios:


print("Análise dos volumes iniciais:")

vol_inicial = usinas["volume_inicial_percentual"]
print(f"- Volume inicial médio: {vol_inicial.mean():.1f}%")
print(f"- Volume inicial mediano: {vol_inicial.median():.1f}%")
print(f"- Desvio padrão: {vol_inicial.std():.1f}%")
print(f"- Mínimo: {vol_inicial.min():.1f}%")
print(f"- Máximo: {vol_inicial.max():.1f}%")

# Distribuição dos volumes iniciais
fig = px.histogram(
    usinas,
    x="volume_inicial_percentual",
    nbins=20,
    title="Distribuição dos Volumes Iniciais dos Reservatórios",
    labels={
        "volume_inicial_percentual": "Volume Inicial (%)",
        "count": "Número de Usinas",
    },
)
fig

# %%
# **Análise da topologia do sistema**
#
# Examinando as conexões entre usinas (cascata):


print("Análise da topologia do sistema:")

# Identificando usinas de cabeceira (sem montante)
usinas_cabeceira = usinas[
    ~usinas["codigo_usina"].isin(usinas["codigo_usina_jusante"])
]
print(f"- Usinas de cabeceira: {len(usinas_cabeceira)}")

# Identificando usinas finais (sem jusante ou jusante = 0)
usinas_finais = usinas[
    (usinas["codigo_usina_jusante"] == 0)
    | (usinas["codigo_usina_jusante"].isna())
]
print(f"- Usinas finais: {len(usinas_finais)}")

# Analisando as conexões válidas
conexoes_validas = usinas[usinas["codigo_usina_jusante"] > 0]
print(f"- Conexões de cascata: {len(conexoes_validas)}")

# Distribuição das conexões por REE
if len(conexoes_validas) > 0:
    conexoes_por_ree = conexoes_validas.groupby("ree").size()
    print("\nConexões de cascata por REE:")
    for ree, count in conexoes_por_ree.items():
        print(f"- REE {ree}: {count} conexões")

# Verificando consistência da topologia
codigos_existentes = set(usinas["codigo_usina"])
jusantes_referenciados = set(
    usinas[usinas["codigo_usina_jusante"] > 0]["codigo_usina_jusante"]
)

jusantes_invalidos = jusantes_referenciados - codigos_existentes
if jusantes_invalidos:
    print(
        f"⚠️ Códigos de jusante inválidos encontrados: {len(jusantes_invalidos)}"
    )
else:
    print("✓ Topologia consistente - todos os códigos de jusante são válidos")


# %%
# **Análise por posto fluviométrico**
#
# Verificando a associação com postos de medição:

# Estatísticas dos postos
postos_stats = usinas["posto"].describe()
print(f"- Número de postos únicos: {usinas['posto'].nunique()}")
print(f"- Posto mínimo: {int(postos_stats['min'])}")
print(f"- Posto máximo: {int(postos_stats['max'])}")

# Verificando usinas por posto
usinas_por_posto = usinas["posto"].value_counts()
print(f"- Postos com mais usinas: {usinas_por_posto.head().to_dict()}")

# Postos com múltiplas usinas (possível cascata)
postos_multiplos = usinas_por_posto[usinas_por_posto > 1]
print(f"- Postos com múltiplas usinas: {len(postos_multiplos)}")

if len(postos_multiplos) > 0:
    print(f"- Total de usinas em postos múltiplos: {postos_multiplos.sum()}")

    # Visualização da distribuição
    fig = px.histogram(
        x=usinas_por_posto.values,
        title="Distribuição de Usinas por Posto",
        labels={"x": "Número de Usinas por Posto", "y": "Número de Postos"},
    )
    fig

# %%
# **Identificação de padrões regionais**
#
# Analisando características por região (REE):

# Análise detalhada por REE
analise_ree = (
    usinas.groupby("ree")
    .agg({
        "codigo_usina": "count",
        "volume_inicial_percentual": ["mean", "std", "min", "max"],
        "usina_modificada": "sum",
    })
    .round(2)
)

# Simplificando nomes das colunas
analise_ree.columns = [
    "total_usinas",
    "vol_medio",
    "vol_std",
    "vol_min",
    "vol_max",
    "modificadas",
]

print("Características por REE:")
print(analise_ree)

# Criando análise de correlação entre REEs
if len(analise_ree) > 1:
    # Volume inicial médio vs número de usinas modificadas
    fig = px.scatter(
        analise_ree.reset_index(),
        x="vol_medio",
        y="modificadas",
        size="total_usinas",
        hover_data=["ree"],
        title="Relação: Volume Inicial Médio vs Usinas Modificadas por REE",
        labels={
            "vol_medio": "Volume Inicial Médio (%)",
            "modificadas": "Número de Usinas Modificadas",
            "total_usinas": "Total de Usinas",
        },
    )
    fig

# %%
# **Criação de cenários alternativos**
#
# Demonstrando como modificar as configurações:

# Cenário 1: Aumentar volumes iniciais em REEs específicos
usinas_modificadas = usinas.copy()

# Aumentar volume inicial em 10% para REE 1 (limitado a 100%)
mask_ree1 = usinas_modificadas["ree"] == 1
if mask_ree1.any():
    volumes_novos = (
        usinas_modificadas.loc[mask_ree1, "volume_inicial_percentual"] * 1.1
    )
    volumes_novos = volumes_novos.clip(upper=100)  # Limitar a 100%
    usinas_modificadas.loc[mask_ree1, "volume_inicial_percentual"] = (
        volumes_novos
    )

    volume_original = usinas[mask_ree1]["volume_inicial_percentual"].mean()
    volume_novo = usinas_modificadas[mask_ree1][
        "volume_inicial_percentual"
    ].mean()

    print("Cenário - Volume inicial REE 1:")
    print(f"- Original: {volume_original:.1f}%")
    print(f"- Modificado: {volume_novo:.1f}%")
    print(f"- Incremento: {volume_novo - volume_original:.1f}%")

# Cenário 2: Marcar usinas específicas como modificadas
# Exemplo: marcar usinas com volume inicial baixo
mask_volume_baixo = usinas_modificadas["volume_inicial_percentual"] < 40
usinas_modificadas.loc[mask_volume_baixo, "usina_modificada"] = 1

modificadas_originais = usinas["usina_modificada"].sum()
modificadas_novas = usinas_modificadas["usina_modificada"].sum()

print("\nCenário - Usinas modificadas:")
print(f"- Original: {modificadas_originais}")
print(f"- Novo: {modificadas_novas}")
print(f"- Adicionadas: {modificadas_novas - modificadas_originais}")

# Salvando configuração modificada
arq_confhd.usinas = usinas_modificadas
# arq_confhd.write("./saida/confhd_modificado.dat")
print("\n✓ Configurações modificadas disponíveis para escrita")

print("\nDados processados disponíveis:")
print("1. usinas - DataFrame original")
print("2. usinas_modificadas - DataFrame com modificações")
print("3. analise_ree - Análise por REE")
print("4. arq_confhd - Objeto modificado para escrita")
