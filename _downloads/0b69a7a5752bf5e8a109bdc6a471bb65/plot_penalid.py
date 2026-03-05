"""
=========================================================
Análise e configuração de penalidades por déficit
=========================================================
"""


# %%
# O arquivo penalid.dat contém as penalidades aplicadas por desvios no modelo
# NEWAVE. Estas penalidades são fundamentais para a operação do sistema, pois
# definem os custos associados ao não atendimento da demanda e outros desvios
# operacionais.

import plotly.express as px
import plotly.io as pio

from inewave.newave import Penalid

pio.templates.default = "ggplot2"

# Leitura do arquivo penalid.dat
arq_penalid = Penalid.read("./newave/penalid.dat")

# %%
# **Estrutura das penalidades**
#
# As penalidades são organizadas por variável, submercado/REE e patamar:

penalidades = arq_penalid.penalidades
print(f"Total de registros de penalidades: {len(penalidades)}")
print("\nPrimeiros registros:")
print(penalidades.head())

print(f"\nVariáveis penalizadas: {sorted(penalidades['variavel'].unique())}")
print(
    f"Submercados/REEs: {sorted(penalidades['codigo_ree_submercado'].unique())}"
)
print(f"Patamares: {sorted(penalidades['patamar_penalidade'].unique())}")

# %%
# **Análise das penalidades por déficit**
#
# As penalidades de déficit são as mais críticas para o planejamento:

# Filtrando penalidades de déficit
deficit_pen = penalidades[
    penalidades["variavel"].str.contains("DEFIC", na=False)
]

if len(deficit_pen) > 0:
    print("Análise das penalidades por déficit:")
    print(f"Registros de déficit: {len(deficit_pen)}")

    # Estatísticas das penalidades de déficit
    print("\nEstatísticas das penalidades de déficit (R$/MWh):")
    deficit_stats = deficit_pen["valor_R$_MWh"].describe()
    print(deficit_stats)

    # Distribuição por patamar
    print("\nPenalidades médias por patamar de carga:")
    deficit_por_patamar = deficit_pen.groupby("patamar_carga")[
        "valor_R$_MWh"
    ].agg(["mean", "min", "max", "count"])
    print(deficit_por_patamar.round(2))

    # Visualização das penalidades por patamar
    if len(deficit_pen["patamar_carga"].unique()) > 1:
        fig = px.box(
            deficit_pen,
            x="patamar_carga",
            y="valor_R$_MWh",
            title="Distribuição das Penalidades de Déficit por Patamar",
            labels={
                "patamar_carga": "Patamar de Carga",
                "valor_R$_MWh": "Penalidade (R$/MWh)",
            },
        )
        fig

# %%
# **Análise por submercado/REE**
#
# Comparando penalidades entre diferentes regiões:

print("Análise por submercado/REE:")

# Penalidades médias por submercado
pen_por_submercado = (
    penalidades.groupby("codigo_ree_submercado")
    .agg({
        "valor_R$_MWh": ["mean", "std", "min", "max"],
        "valor_R$_hm3": ["mean", "std", "min", "max"],
        "variavel": "count",
    })
    .round(2)
)
pen_por_submercado.columns = [
    "MWh_media",
    "MWh_std",
    "MWh_min",
    "MWh_max",
    "hm3_media",
    "hm3_std",
    "hm3_min",
    "hm3_max",
    "qtd_penalidades",
]

print("Penalidades por submercado/REE:")
print(pen_por_submercado)

# Visualização das penalidades por submercado
if len(penalidades["codigo_ree_submercado"].unique()) > 1:
    fig = px.bar(
        pen_por_submercado.reset_index(),
        x="codigo_ree_submercado",
        y="MWh_media",
        title="Penalidade Média por Submercado/REE",
        labels={
            "codigo_ree_submercado": "Código Submercado/REE",
            "MWh_media": "Penalidade Média (R$/MWh)",
        },
    )
    fig

# %%
# **Análise das diferentes variáveis penalizadas**
#
# Identificando todas as variáveis que possuem penalidades:

print("Análise das variáveis penalizadas:")

# Agrupando por variável
pen_por_variavel = (
    penalidades.groupby("variavel")
    .agg({
        "valor_R$_MWh": ["mean", "std", "count"],
        "valor_R$_hm3": ["mean", "std"],
        "codigo_ree_submercado": "nunique",
    })
    .round(2)
)
pen_por_variavel.columns = [
    "MWh_media",
    "MWh_std",
    "registros",
    "hm3_media",
    "hm3_std",
    "regioes",
]

print("Penalidades por tipo de variável:")
print(pen_por_variavel)

# Identificando variáveis com maiores penalidades
print("\nTop 5 variáveis com maiores penalidades (R$/MWh):")
top_variaveis = pen_por_variavel.nlargest(5, "MWh_media")
print(top_variaveis[["MWh_media", "registros", "regioes"]])

# %%
# **Análise da estrutura de patamares**
#
# Compreendendo a relação entre patamares de penalidade e carga:

print("Análise da estrutura de patamares:")

# Relação entre patamar de penalidade e patamar de carga
patamar_crosstab = (
    penalidades.groupby(["patamar_penalidade", "patamar_carga"])
    .size()
    .reset_index(name="count")
)

if len(patamar_crosstab) > 0:
    print("Distribuição patamar penalidade vs patamar carga:")
    patamar_pivot = patamar_crosstab.pivot(
        index="patamar_penalidade", columns="patamar_carga", values="count"
    ).fillna(0)
    print(patamar_pivot.astype(int))

    # Penalidades médias por patamar de penalidade
    pen_por_pat_pen = penalidades.groupby("patamar_penalidade")[
        "valor_R$_MWh"
    ].agg(["mean", "std", "count"])
    print("\nPenalidades por patamar de penalidade:")
    print(pen_por_pat_pen.round(2))


# %%
# **Criação de cenários alternativos**
#
# Modificando penalidades para estudos de sensibilidade:
print("Exemplo de modificação de penalidades:")

# Criando cenário com aumento de 20% nas penalidades de déficit
penalidades_mod = penalidades.copy()

# Identificando registros de déficit
mask_deficit = penalidades_mod["variavel"].str.contains("DEFIC", na=False)

# Aplicando aumento de 20%
penalidades_mod.loc[mask_deficit, "valor_R$_MWh"] *= 1.2

# Comparação
if mask_deficit.any():
    original_media = penalidades[mask_deficit]["valor_R$_MWh"].mean()
    nova_media = penalidades_mod[mask_deficit]["valor_R$_MWh"].mean()

    print(f"Penalidade média original (déficit): {original_media:.2f} R$/MWh")
    print(f"Penalidade média nova (déficit): {nova_media:.2f} R$/MWh")
    print(f"Aumento: {(nova_media / original_media - 1) * 100:.1f}%")

    # Aplicando modificação ao arquivo
    arq_penalid.penalidades = penalidades_mod
    print("✓ Modificação aplicada ao arquivo")
