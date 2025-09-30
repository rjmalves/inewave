"""
=======================================================
Análise da programação de manutenção das térmicas
=======================================================
"""


# %%
# O arquivo manutt.dat contém a programação de manutenção das usinas
# termelétricas, especificando períodos de indisponibilidade para
# manutenção preventiva ou revisões programadas.

import pandas as pd
import plotly.express as px
import plotly.io as pio

from inewave.newave import Manutt

pio.templates.default = "ggplot2"

# %%
# **Leitura da programação de manutenção**
#
# O arquivo manutt.dat é crucial para o planejamento operativo,
# pois define quando as usinas térmicas estarão indisponíveis:

arq_manutt = Manutt.read("./newave/manutt.dat")
print("Arquivo manutt.dat lido com sucesso")

# %%
# **Análise geral das manutenções**
#
# Examinando o escopo e características das manutenções programadas:

manutencoes = arq_manutt.manutencoes
print(f"Total de manutenções programadas: {len(manutencoes)}")
print(f"Colunas disponíveis: {list(manutencoes.columns)}")

print("\nPrimeiras manutenções:")
print(manutencoes.head())

# Análise por empresa
manut_por_empresa = (
    manutencoes.groupby("nome_empresa")
    .agg({
        "codigo_usina": "nunique",
        "duracao": ["sum", "mean"],
        "potencia": "sum",
    })
    .round(2)
)
manut_por_empresa.columns = [
    "usinas",
    "duracao_total",
    "duracao_media",
    "potencia_total",
]

print("\nManutenções por empresa:")
print(manut_por_empresa)

# Análise por usina
manut_por_usina = (
    manutencoes.groupby("nome_usina")
    .agg({"duracao": ["sum", "count"], "potencia": "mean"})
    .round(2)
)
manut_por_usina.columns = [
    "duracao_total",
    "num_manutencoes",
    "potencia_media",
]

print(f"\nUsinas com manutenção: {len(manut_por_usina)}")
print("Usinas com mais manutenções:")
print(manut_por_usina.sort_values("num_manutencoes", ascending=False).head())


# %%
# **Análise temporal das manutenções**
#
# Verificando a distribuição das manutenções ao longo do tempo:

print("Análise temporal das manutenções:")

# Convertendo datas se necessário
if not pd.api.types.is_datetime64_any_dtype(manutencoes["data_inicio"]):
    manutencoes["data_inicio"] = pd.to_datetime(manutencoes["data_inicio"])

# Criando cópias com informações temporais
manut_temporal = manutencoes.copy()
manut_temporal["ano"] = manut_temporal["data_inicio"].dt.year
manut_temporal["mes"] = manut_temporal["data_inicio"].dt.month
manut_temporal["trimestre"] = manut_temporal["data_inicio"].dt.quarter
manut_temporal["data_fim"] = manut_temporal["data_inicio"] + pd.to_timedelta(
    manut_temporal["duracao"], unit="D"
)

# Análise por ano
manut_por_ano = (
    manut_temporal.groupby("ano")
    .agg({"codigo_usina": "count", "duracao": "sum", "potencia": "sum"})
    .round(2)
)
manut_por_ano.columns = [
    "num_manutencoes",
    "duracao_total",
    "potencia_total",
]

print("Manutenções por ano:")
print(manut_por_ano)

# Visualização temporal
fig = px.bar(
    manut_por_ano.reset_index(),
    x="ano",
    y="num_manutencoes",
    title="Distribuição de Manutenções por Ano",
    labels={"ano": "Ano", "num_manutencoes": "Número de Manutenções"},
)
fig

# Análise por mês (sazonalidade)
manut_por_mes = (
    manut_temporal.groupby("mes")
    .agg({"codigo_usina": "count", "duracao": "mean", "potencia": "sum"})
    .round(2)
)
manut_por_mes.columns = [
    "num_manutencoes",
    "duracao_media",
    "potencia_total",
]

print("\nSazonalidade das manutenções:")
meses_nomes = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]
manut_por_mes.index = [meses_nomes[i - 1] for i in manut_por_mes.index]
print(manut_por_mes)

# Visualização da sazonalidade
fig = px.bar(
    manut_por_mes.reset_index(),
    x="mes",
    y="num_manutencoes",
    title="Sazonalidade das Manutenções por Mês",
    labels={"mes": "Mês", "num_manutencoes": "Número de Manutenções"},
)
fig.show()

# Identificando períodos de maior concentração
mes_pico = manut_por_mes["num_manutencoes"].idxmax()
mes_baixo = manut_por_mes["num_manutencoes"].idxmin()

print("\nSazonalidade identificada:")
print(
    f"- Mês de pico: {mes_pico} ({manut_por_mes.loc[mes_pico, 'num_manutencoes']} manutenções)"
)
print(
    f"- Mês de menor atividade: {mes_baixo} ({manut_por_mes.loc[mes_baixo, 'num_manutencoes']} manutenções)"
)

# %%
# **Análise da duração das manutenções**
#
# Verificando padrões na duração e intensidade das manutenções:

print("Análise da duração das manutenções:")

duracao_stats = manutencoes["duracao"].describe()
print(f"- Duração média: {duracao_stats['mean']:.1f} dias")
print(f"- Duração mediana: {duracao_stats['50%']:.1f} dias")
print(f"- Duração mínima: {int(duracao_stats['min'])} dias")
print(f"- Duração máxima: {int(duracao_stats['max'])} dias")
print(f"- Desvio padrão: {duracao_stats['std']:.1f} dias")

# Distribuição das durações
fig = px.histogram(
    manutencoes,
    x="duracao",
    nbins=20,
    title="Distribuição da Duração das Manutenções",
    labels={"duracao": "Duração (dias)", "count": "Número de Manutenções"},
)
fig.show()

# Classificação por duração
manutencoes_copy = manutencoes.copy()
manutencoes_copy["tipo_manutencao"] = pd.cut(
    manutencoes_copy["duracao"],
    bins=[0, 7, 30, 90, float("inf")],
    labels=[
        "Curta (≤7d)",
        "Média (8-30d)",
        "Longa (31-90d)",
        "Extensa (>90d)",
    ],
)

tipo_distribuicao = manutencoes_copy["tipo_manutencao"].value_counts()
print("\nClassificação por duração:")
for tipo, count in tipo_distribuicao.items():
    percentual = count / len(manutencoes_copy) * 100
    print(f"- {tipo}: {count} manutenções ({percentual:.1f}%)")

# Visualização da classificação
fig = px.pie(
    values=tipo_distribuicao.values,
    names=tipo_distribuicao.index,
    title="Distribuição dos Tipos de Manutenção por Duração",
)
fig

# %%
# **Análise da potência afetada**
#
# Verificando o impacto das manutenções na capacidade instalada:

print("Análise da potência afetada pelas manutenções:")

potencia_stats = manutencoes["potencia"].describe()
print(f"- Potência média por manutenção: {potencia_stats['mean']:.1f} MW")
print(f"- Potência total afetada: {manutencoes['potencia'].sum():.1f} MW")
print(f"- Maior potência individual: {potencia_stats['max']:.1f} MW")
print(f"- Menor potência individual: {potencia_stats['min']:.1f} MW")

# Impacto total por período
if "data_inicio" in manutencoes.columns:
    impacto_mensal = (
        manut_temporal.groupby(["ano", "mes"])
        .agg({"potencia": "sum", "duracao": "sum"})
        .round(1)
    )
    impacto_mensal["impacto_mwh"] = (
        impacto_mensal["potencia"] * impacto_mensal["duracao"] * 24
    )

    print("\nImpacto energético das manutenções (MWh indisponíveis):")
    print(f"- Total anual: {impacto_mensal['impacto_mwh'].sum():,.0f} MWh")
    print(f"- Média mensal: {impacto_mensal['impacto_mwh'].mean():,.0f} MWh")

    # Top 5 meses com maior impacto
    top_impacto = impacto_mensal.nlargest(5, "impacto_mwh")
    print("\nTop 5 períodos com maior impacto:")
    for (ano, mes), row in top_impacto.iterrows():
        mes_nome = meses_nomes[mes - 1] if "meses_nomes" in locals() else mes
        print(
            f"- {mes_nome}/{ano}: {row['impacto_mwh']:,.0f} MWh ({row['potencia']:.0f} MW, {row['duracao']:.0f} dias)"
        )

# Análise por faixa de potência
manutencoes_copy["faixa_potencia"] = pd.cut(
    manutencoes_copy["potencia"],
    bins=[0, 50, 200, 500, float("inf")],
    labels=[
        "Pequena (<50MW)",
        "Média (50-200MW)",
        "Grande (200-500MW)",
        "Muito Grande (>500MW)",
    ],
)

faixa_distribuicao = manutencoes_copy["faixa_potencia"].value_counts()
print("\nDistribuição por faixa de potência:")
for faixa, count in faixa_distribuicao.items():
    percentual = count / len(manutencoes_copy) * 100
    potencia_media = manutencoes_copy[
        manutencoes_copy["faixa_potencia"] == faixa
    ]["potencia"].mean()
    print(
        f"- {faixa}: {count} manutenções ({percentual:.1f}%, média: {potencia_media:.1f} MW)"
    )

# %%
# **Análise de sobreposições e conflitos**
#
# Identificando períodos de alta concentração de manutenções:

print("Análise de sobreposições e conflitos:")

# Criando timeline de manutenções
timeline_data = []
for _, manut in manut_temporal.iterrows():
    for dia in pd.date_range(manut["data_inicio"], manut["data_fim"]):
        timeline_data.append({
            "data": dia,
            "usina": manut["nome_usina"],
            "potencia": manut["potencia"],
            "empresa": manut["nome_empresa"],
        })

if timeline_data:
    timeline_df = pd.DataFrame(timeline_data)

    # Potência total indisponível por dia
    potencia_diaria = timeline_df.groupby("data")["potencia"].sum()

    print(
        f"- Período analisado: {potencia_diaria.index.min().date()} a {potencia_diaria.index.max().date()}"
    )
    print(f"- Potência média indisponível: {potencia_diaria.mean():.1f} MW/dia")
    print(f"- Pico de indisponibilidade: {potencia_diaria.max():.1f} MW")
    print(f"- Data do pico: {potencia_diaria.idxmax().date()}")

    # Identificando dias críticos (alto nível de manutenção)
    limite_critico = potencia_diaria.quantile(0.95)  # Top 5% dos dias
    dias_criticos = potencia_diaria[potencia_diaria >= limite_critico]

    print(
        f"\nDias críticos (≥{limite_critico:.1f} MW indisponível): {len(dias_criticos)}"
    )

    if len(dias_criticos) > 0:
        print("Principais dias críticos:")
        for data, potencia in dias_criticos.nlargest(5).items():
            usinas_dia = timeline_df[timeline_df["data"] == data][
                "usina"
            ].nunique()
            print(f"- {data.date()}: {potencia:.1f} MW ({usinas_dia} usinas)")

    # Visualização da evolução temporal
    if len(potencia_diaria) > 1:
        fig = px.line(
            x=potencia_diaria.index,
            y=potencia_diaria.values,
            title="Evolução da Potência Indisponível por Manutenção",
            labels={"x": "Data", "y": "Potência Indisponível (MW)"},
        )
        fig
