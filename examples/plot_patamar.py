"""
=======================================================
Análise de patamares de carga e curva de demanda
=======================================================
"""


# %%
# O arquivo patamar.dat define os patamares de carga utilizados no modelo NEWAVE
# para representar a variação horária da demanda. Este arquivo é fundamental para
# a modelagem da operação energética, pois define como a carga varia ao longo do dia
# e entre diferentes períodos do ano.

import plotly.express as px
import plotly.io as pio

from inewave.newave import Patamar

pio.templates.default = "ggplot2"

# Leitura do arquivo patamar.dat
arq_patamar = Patamar.read("./newave/patamar.dat")

# %%
# **Configuração básica dos patamares**
#
# Verificando o número de patamares definidos:

num_patamares = arq_patamar.numero_patamares

# %%
# **Análise da duração dos patamares**
#
# A duração define quantas horas por mês cada patamar representa:

duracao = arq_patamar.duracao_mensal_patamares
print(f"Total de registros de duração: {len(duracao)}")
print(f"Patamares na duração: {sorted(duracao['patamar'].unique())}")
print(f"Período: {duracao['data'].min()} a {duracao['data'].max()}")

print("\nPrimeiros registros de duração:")
print(duracao.head())

# Análise estatística das durações
print("\nEstatísticas das durações por patamar:")
duracao_stats = duracao.groupby("patamar")["valor"].agg([
    "mean",
    "std",
    "min",
    "max",
])
print(duracao_stats.round(2))

# Verificação da soma das durações (deve ser próximo a 744 horas/mês em média)
duracao_mensal_total = duracao.groupby("data")["valor"].sum()
print(
    f"\nDuração total mensal (média): {duracao_mensal_total.mean():.1f} horas"
)
print(
    f"Variação: {duracao_mensal_total.min():.1f} - {duracao_mensal_total.max():.1f} horas"
)

# Visualização da duração ao longo do tempo
if len(duracao["patamar"].unique()) > 1:
    fig = px.line(
        duracao,
        x="data",
        y="valor",
        color="patamar",
        title="Evolução da Duração dos Patamares ao Longo do Tempo",
        labels={
            "data": "Data",
            "valor": "Duração (horas)",
            "patamar": "Patamar",
        },
    )
    fig

# %%
# **Análise das cargas por patamar**
#
# As cargas em P.U. mostram como a demanda varia entre patamares:

carga = arq_patamar.carga_patamares
print(f"Total de registros de carga: {len(carga)}")
print(f"Submercados: {sorted(carga['codigo_submercado'].unique())}")
print(f"Patamares: {sorted(carga['patamar'].unique())}")

print("\nPrimeiros registros de carga:")
print(carga.head())

# Análise das cargas médias por patamar
print("\nCarga média por patamar (P.U.):")
carga_media_patamar = carga.groupby("patamar")["valor"].agg(["mean", "std"])
print(carga_media_patamar.round(4))

# Análise sazonal das cargas
if "data" in carga.columns:
    carga_copy = carga.copy()
    carga_copy["mes"] = carga_copy["data"].dt.month

    print("\nVariação sazonal das cargas por patamar:")
    carga_sazonal = (
        carga_copy.groupby(["mes", "patamar"])["valor"].mean().reset_index()
    )

    # Visualização sazonal
    if len(carga["patamar"].unique()) > 1:
        fig = px.line(
            carga_sazonal,
            x="mes",
            y="valor",
            color="patamar",
            title="Variação Sazonal das Cargas por Patamar",
            labels={
                "mes": "Mês",
                "valor": "Carga (P.U.)",
                "patamar": "Patamar",
            },
        )
        fig.update_xaxes(tickmode="linear", dtick=1)
        fig

# Análise por submercado
if len(carga["codigo_submercado"].unique()) > 1:
    print("\nCarga média por submercado e patamar:")
    carga_subm_pat = (
        carga.groupby(["codigo_submercado", "patamar"])["valor"]
        .mean()
        .reset_index()
    )
    carga_pivot = carga_subm_pat.pivot(
        index="codigo_submercado", columns="patamar", values="valor"
    )
    print(carga_pivot.round(4))

# %%
# **Análise da modulação da carga**
#
# Verificando como a carga se distribui entre os patamares:

print("Análise da modulação da carga:")

# Merge entre carga e duração para calcular energia por patamar
carga_duracao = carga.merge(
    duracao, on=["data", "patamar"], suffixes=("_carga", "_duracao")
)

# Calculando energia por patamar (carga * duração)
carga_duracao["energia_patamar"] = (
    carga_duracao["valor_carga"] * carga_duracao["valor_duracao"]
)

# Energia total por submercado e mês
energia_total = carga_duracao.groupby(["codigo_submercado", "data"])[
    "energia_patamar"
].sum()

# Participação de cada patamar na energia total
carga_duracao_energia = carga_duracao.merge(
    energia_total.reset_index().rename(
        columns={"energia_patamar": "energia_total"}
    ),
    on=["codigo_submercado", "data"],
)
carga_duracao_energia["participacao_pct"] = (
    carga_duracao_energia["energia_patamar"]
    / carga_duracao_energia["energia_total"]
    * 100
)

print("Participação média de cada patamar na energia total:")
participacao_media = carga_duracao_energia.groupby("patamar")[
    "participacao_pct"
].mean()
for patamar, part in participacao_media.items():
    print(f"Patamar {patamar}: {part:.1f}%")

# Visualização da modulação
if len(carga_duracao_energia["patamar"].unique()) > 1:
    fig = px.box(
        carga_duracao_energia,
        x="patamar",
        y="participacao_pct",
        title="Distribuição da Participação dos Patamares na Energia Total",
        labels={
            "patamar": "Patamar",
            "participacao_pct": "Participação (%)",
        },
    )
    fig

# %%
# **Análise do intercâmbio por patamares**
#
# Fatores de correção do intercâmbio entre submercados:

intercambio = arq_patamar.intercambio_patamares
print(f"Registros de intercâmbio por patamares: {len(intercambio)}")
print("Pares de submercados com intercâmbio:")
pares_intercambio = intercambio.groupby([
    "submercado_de",
    "submercado_para",
]).size()
print(pares_intercambio)

# Análise dos fatores de intercâmbio
print("\nEstatísticas dos fatores de intercâmbio:")
intercambio_stats = intercambio.groupby("patamar")["valor"].agg([
    "mean",
    "std",
    "min",
    "max",
])
print(intercambio_stats.round(4))

# Verificando se há assimetrias significativas
if len(intercambio) > 0:
    fatores_extremos = intercambio[
        (intercambio["valor"] < 0.8) | (intercambio["valor"] > 1.2)
    ]

    if len(fatores_extremos) > 0:
        print(
            f"\nFatores de intercâmbio extremos (fora da faixa 0.8-1.2): {len(fatores_extremos)}"
        )
        print("Casos extremos:")
        print(
            fatores_extremos[
                ["submercado_de", "submercado_para", "patamar", "valor"]
            ].head()
        )
    else:
        print(
            "\n✓ Todos os fatores de intercâmbio estão na faixa razoável (0.8-1.2)"
        )

# %%
# **Análise das usinas não simuladas**
#
# Fatores para representar geração não simulada individualmente:

usinas_nao_sim = arq_patamar.usinas_nao_simuladas
print(f"Registros de usinas não simuladas: {len(usinas_nao_sim)}")
print(f"Submercados: {sorted(usinas_nao_sim['codigo_submercado'].unique())}")
print(f"Blocos de usinas: {sorted(usinas_nao_sim['indice_bloco'].unique())}")

# Análise dos fatores por patamar
print("\nFatores médios das usinas não simuladas por patamar:")
uns_por_patamar = usinas_nao_sim.groupby("patamar")["valor"].agg([
    "mean",
    "std",
    "count",
])
print(uns_por_patamar.round(4))

# Análise por submercado
print("\nFatores médios por submercado:")
uns_por_subm = usinas_nao_sim.groupby("codigo_submercado")["valor"].agg([
    "mean",
    "std",
])
print(uns_por_subm.round(4))

# Variabilidade temporal
if "data" in usinas_nao_sim.columns:
    uns_temporal = usinas_nao_sim.groupby("data")["valor"].mean()
    print("\nVariabilidade temporal:")
    print(f"Fator médio mínimo: {uns_temporal.min():.4f}")
    print(f"Fator médio máximo: {uns_temporal.max():.4f}")
    print(
        f"Coeficiente de variação: {uns_temporal.std() / uns_temporal.mean():.4f}"
    )

# %%
# **Criação de cenários alternativos**
#
# Modificando patamares para estudos específicos:

print("Exemplo de modificação de patamares:")

# Cenário: Aumentando a modulação da carga (diferença entre ponta e fora ponta)
carga_modificada = carga.copy()

if len(carga["patamar"].unique()) >= 2:
    # Identificando patamar de ponta (maior carga média) e fora ponta (menor carga média)
    carga_media = carga.groupby("patamar")["valor"].mean()
    patamar_ponta = carga_media.idxmax()
    patamar_leve = carga_media.idxmin()

    print(
        f"Patamar de ponta identificado: {patamar_ponta} (carga média: {carga_media[patamar_ponta]:.3f})"
    )
    print(
        f"Patamar leve identificado: {patamar_leve} (carga média: {carga_media[patamar_leve]:.3f})"
    )

    # Aplicando modificação: +10% na ponta, -5% no leve
    mask_ponta = carga_modificada["patamar"] == patamar_ponta
    mask_leve = carga_modificada["patamar"] == patamar_leve

    carga_modificada.loc[mask_ponta, "valor"] *= 1.10
    carga_modificada.loc[mask_leve, "valor"] *= 0.95

    # Comparação
    nova_media_ponta = carga_modificada[mask_ponta]["valor"].mean()
    nova_media_leve = carga_modificada[mask_leve]["valor"].mean()

    print(
        f"Nova carga ponta: {nova_media_ponta:.3f} (+{(nova_media_ponta / carga_media[patamar_ponta] - 1) * 100:.1f}%)"
    )
    print(
        f"Nova carga leve: {nova_media_leve:.3f} ({(nova_media_leve / carga_media[patamar_leve] - 1) * 100:.1f}%)"
    )

    # Aplicando modificação ao arquivo
    arq_patamar.carga_patamares = carga_modificada
    print("✓ Modificação aplicada ao arquivo")
