"""
==========================================================
Análise das séries sintéticas de energia afluente
==========================================================
"""


# %%
# Os arquivos energiafXXX.dat contêm as séries sintéticas de energia natural
# afluente geradas pelo modelo NEWAVE durante a simulação forward. Estes arquivos
# são fundamentais para análise de cenários hidrológicos e avaliação da
# variabilidade energética do sistema.
# IMPORTANTE: Foi gerado um arquivo energiaf.dat reduzido utlizando o próprio módulo `inewave`
# para fins de demonstração com apenas 1 REE. Em um caso real, utilize o arquivo gerado pelo NEWAVE.

import plotly.express as px
import plotly.io as pio

from inewave.newave import Energiaf

pio.templates.default = "ggplot2"

# Leitura do arquivo energiaf
arq_energiaf = Energiaf.read("./newave/energiaf.dat")

# %%
# **Configuração da leitura de arquivos binários**
#
# IMPORTANTE: Os arquivos energiaf são binários e requerem configuração específica
# baseada nas dimensões do estudo. Estes parâmetros normalmente vêm do arquivo
# forwarh.dat ou são conhecidos do caso de estudo:

# Exemplo de configuração típica (ajustar conforme o caso)
numero_forwards = 200  # Número de séries forward
numero_rees = 12  # Número de REEs
numero_estagios = 60  # Número de estágios de planejamento
numero_estagios_th = 12  # Número de estágios considerados para tendência hidrológica (6 ou 12 geralmente)

print("Configuração da leitura:")
print(f"- Séries forward: {numero_forwards}")
print(f"- REEs: {numero_rees}")
print(f"- Estágios: {numero_estagios}")
print(f"- Estágios térmicos: {numero_estagios_th}")

# %%
# **Estrutura dos dados de energia**
#
# As séries sintéticas são organizadas por estágio, REE e série forward:

series = arq_energiaf.series
print(f"Total de registros de energia: {len(series)}")
print("\nPrimeiros registros:")
print(series.head())

print("\nEstatísticas básicas:")
print(series.describe())

# %%
# **Análise por REE (Reservatório Equivalente de Energia)**
#
# Análise da distribuição de energia por REE:

print("Distribuição de energia por REE:")
energia_por_ree = (
    series.groupby("ree")
    .agg({"valor": ["count", "mean", "std", "min", "max"]})
    .round(2)
)
energia_por_ree.columns = [
    "registros",
    "media",
    "desvio",
    "minimo",
    "maximo",
]
print(energia_por_ree)

# %%
# **Análise temporal das séries**
#
# Avaliando a evolução da energia ao longo dos estágios:


# Energia média por estágio
energia_por_estagio = (
    series.groupby("estagio")["valor"].agg(["mean", "std"]).reset_index()
)

print("Energia média por estágio (primeiros 10 estágios):")
print(energia_por_estagio.head(10))

# Gráfico da evolução temporal
fig = px.line(
    energia_por_estagio,
    x="estagio",
    y="mean",
    title="Evolução da Energia Afluente Média por Estágio",
    labels={"mean": "Energia Média (MWmes)", "estagio": "Estágio"},
)
fig.add_scatter(
    x=energia_por_estagio["estagio"],
    y=energia_por_estagio["mean"] + energia_por_estagio["std"],
    mode="lines",
    line=dict(width=0),
    showlegend=False,
    hovertemplate=None,
    hoverinfo="skip",
)
fig.add_scatter(
    x=energia_por_estagio["estagio"],
    y=energia_por_estagio["mean"] - energia_por_estagio["std"],
    mode="lines",
    line=dict(width=0),
    fill="tonexty",
    fillcolor="rgba(0,100,80,0.2)",
    name="±1 Desvio Padrão",
    hovertemplate=None,
    hoverinfo="skip",
)
fig

# %%
# **Análise de variabilidade entre séries**
#
# Comparando diferentes séries forward para avaliar a incerteza hidrológica:

# Selecionando um REE específico para análise detalhada
ree_analise = 1
series_ree = series[series["ree"] == ree_analise]

if len(series_ree) > 0:
    print(f"Análise de variabilidade - REE {ree_analise}:")

    # Estatísticas por série
    stats_por_serie = (
        series_ree.groupby("serie")["valor"].agg(["mean", "std"]).reset_index()
    )

    print("Estatísticas das séries forward:")
    print(
        f"- Energia média entre séries: {stats_por_serie['mean'].mean():.1f} MWmes"
    )
    print(
        f"- Desvio padrão entre médias: {stats_por_serie['mean'].std():.1f} MWmes"
    )
    print(
        f"- Coeficiente de variação: {stats_por_serie['mean'].std() / stats_por_serie['mean'].mean() * 100:.1f}%"
    )

# %%
# **Análise sazonal**
#
# Identificando padrões sazonais nas séries sintéticas:

# Assumindo que os estágios representam meses (ajustar conforme necessário)
series_com_mes = series.copy()
series_com_mes["mes"] = ((series_com_mes["estagio"] - 1) % 12) + 1

# Energia média por mês
energia_mensal = (
    series_com_mes.groupby("mes")["valor"].agg(["mean", "std"]).reset_index()
)

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
energia_mensal["mes_nome"] = energia_mensal["mes"].map(
    lambda x: meses_nomes[x - 1]
)

print("Padrão sazonal da energia afluente:")
print(energia_mensal[["mes_nome", "mean", "std"]].round(1))

# Gráfico sazonal
fig = px.bar(
    energia_mensal,
    x="mes_nome",
    y="mean",
    error_y="std",
    title="Padrão Sazonal da Energia Afluente",
    labels={"mean": "Energia Média (MWmes)", "mes_nome": "Mês"},
)
fig

# %%
# **Análise de cenários extremos**
#
# Identificando cenários de energia alta e baixa:

# Energia total por série (somando todos os REEs e estágios)
energia_total_serie = series.groupby("serie")["valor"].sum().reset_index()
energia_total_serie = energia_total_serie.sort_values("valor")

# Identificando cenários extremos
p10 = energia_total_serie["valor"].quantile(0.10)
p90 = energia_total_serie["valor"].quantile(0.90)

cenarios_secos = energia_total_serie[energia_total_serie["valor"] <= p10]
cenarios_umidos = energia_total_serie[energia_total_serie["valor"] >= p90]

print("Análise de cenários extremos:")
print(f"Cenários secos (≤P10): {len(cenarios_secos)} séries")
print(f"Cenários úmidos (≥P90): {len(cenarios_umidos)} séries")
print(f"Energia P10: {p10:.0f} MWmes")
print(f"Energia P90: {p90:.0f} MWmes")
print(f"Relação P90/P10: {p90 / p10:.2f}")

# %%
# **Comparação entre REEs**
#
# Analisando correlações e diferenças entre REEs:

# Criando matriz REE x série para análise de correlação
pivot_energia = series.pivot_table(
    index=["serie", "estagio"], columns="ree", values="valor"
)

if len(pivot_energia.columns) > 1:
    # Matriz de correlação entre REEs
    correlacao_rees = pivot_energia.corr()

    print("Correlação entre REEs (primeiros 5x5):")
    print(correlacao_rees.iloc[:5, :5].round(3))

    # Contribuição de cada REE para o total
    contrib_ree = series.groupby("ree")["valor"].sum()
    contrib_ree_pct = (contrib_ree / contrib_ree.sum() * 100).round(1)

    print("\nContribuição percentual por REE:")
    for ree, pct in contrib_ree_pct.items():
        print(f"REE {ree}: {pct}%")


# %%
# **Processamento de dados para análises externas**
#
# Preparando dados para exportação ou análises complementares:

# Convertendo para formato pivot para análise em planilha
energia_pivot = series.pivot_table(
    index=["estagio"], columns=["ree", "serie"], values="valor"
)

print("Formato pivot para exportação:")
print(f"Dimensões: {energia_pivot.shape}")
print("Colunas (REE, Série):", energia_pivot.columns[:5].tolist())

# Resumo estatístico por REE
resumo_ree = (
    series.groupby("ree")["valor"]
    .agg([
        "count",
        "mean",
        "std",
        "min",
        "max",
        lambda x: x.quantile(0.1),  # P10
        lambda x: x.quantile(0.5),  # P50
        lambda x: x.quantile(0.9),  # P90
    ])
    .round(2)
)
resumo_ree.columns = [
    "registros",
    "media",
    "desvio",
    "minimo",
    "maximo",
    "P10",
    "P50",
    "P90",
]

print("\nResumo estatístico por REE:")
print(resumo_ree)

# %%
# **Exportação de resultados processados**

# Exemplo de como exportar dados processados
print("\nOpções de exportação:")
print("1. Séries originais: arq_energiaf.series")
print("2. Formato pivot: energia_pivot")
print("3. Resumo por REE: resumo_ree")
print("4. Energia por estágio: energia_por_estagio")

# Para salver em CSV (exemplo):
# energia_por_estagio.to_csv('energia_por_estagio.csv', index=False)
# resumo_ree.to_csv('resumo_energia_ree.csv')
