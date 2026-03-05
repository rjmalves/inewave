"""
==========================================================
Análise das séries sintéticas de vazões afluentes
==========================================================
"""


# %%
# Os arquivos vazaofXXX.dat contêm as séries sintéticas de vazões naturais
# afluentes geradas pelo modelo NEWAVE durante a simulação forward. Estes arquivos
# são essenciais para análise de cenários hidrológicos e planejamento operativo
# das usinas hidrelétricas.
# IMPORTANTE: Foi gerado um arquivo vazaof.dat reduzido utlizando o próprio módulo `inewave`
# para fins de demonstração com apenas 1 UHE. Em um caso real, utilize o arquivo gerado pelo NEWAVE.

import plotly.express as px
import plotly.io as pio

from inewave.newave import Vazaof

pio.templates.default = "ggplot2"

# Leitura do arquivo vazaof
arq_vazaof = Vazaof.read("./newave/vazaof.dat")

# %%
# **Configuração da leitura de arquivos binários**
#
# IMPORTANTE: Os arquivos vazaof são binários e requerem configuração específica
# baseada nas dimensões do estudo. Estes parâmetros devem corresponder exatamente
# ao caso de estudo:

# Exemplo de configuração típica (ajustar conforme o caso)
numero_forwards = 200  # Número de séries forward
numero_uhes = 150  # Número de UHEs
numero_estagios = 60  # Número de estágios de planejamento
numero_estagios_th = 12  # Número de estágios do horizonte térmico

print("Configuração da leitura:")
print(f"- Séries forward: {numero_forwards}")
print(f"- UHEs: {numero_uhes}")
print(f"- Estágios: {numero_estagios}")
print(f"- Estágios térmicos: {numero_estagios_th}")

# %%
# **Estrutura dos dados de vazão**
#
# As séries sintéticas são organizadas por estágio, UHE e série forward:

series = arq_vazaof.series
print(f"Total de registros de vazão: {len(series)}")
print("\nPrimeiros registros:")
print(series.head())

print("\nEstatísticas básicas:")
print(series.describe())

print(f"\nUHEs representadas: {series['uhe'].nunique()}")
print(f"Estágios: {series['estagio'].min()} a {series['estagio'].max()}")
print(f"Séries: {series['serie'].nunique()}")


# %%
# **Análise por UHE (Usina Hidrelétrica)**
#
# Análise da distribuição de vazões por usina:

print("Distribuição de vazões por UHE (primeiras 10 usinas):")
vazao_por_uhe = (
    series.groupby("uhe")
    .agg({"valor": ["count", "mean", "std", "min", "max"]})
    .round(2)
)
vazao_por_uhe.columns = ["registros", "media", "desvio", "minimo", "maximo"]
print(vazao_por_uhe.head(10))

# Identificando UHEs com maior vazão média
print("\nTop 10 UHEs com maior vazão média:")
top_uhes = vazao_por_uhe.nlargest(10, "media")
print(top_uhes[["media", "desvio"]])

# %%
# **Análise temporal das vazões**
#
# Avaliando a evolução das vazões ao longo dos estágios:

# Vazão média por estágio
vazao_por_estagio = (
    series.groupby("estagio")["valor"].agg(["mean", "std"]).reset_index()
)

print("Vazão média por estágio (primeiros 12 estágios):")
print(vazao_por_estagio.head(12))

# Gráfico da evolução temporal
fig = px.line(
    vazao_por_estagio,
    x="estagio",
    y="mean",
    title="Evolução da Vazão Afluente Média por Estágio",
    labels={"mean": "Vazão Média (hm³)", "estagio": "Estágio"},
)
fig.add_scatter(
    x=vazao_por_estagio["estagio"],
    y=vazao_por_estagio["mean"] + vazao_por_estagio["std"],
    mode="lines",
    line=dict(width=0),
    showlegend=False,
    hovertemplate=None,
    hoverinfo="skip",
)
fig.add_scatter(
    x=vazao_por_estagio["estagio"],
    y=vazao_por_estagio["mean"] - vazao_por_estagio["std"],
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
# **Análise sazonal das vazões**
#
# Identificando padrões sazonais nas vazões afluentes:

# Assumindo que os primeiros 12 estágios representam meses
series_sazonais = series[series["estagio"] <= 12].copy()

if len(series_sazonais) > 0:
    # Vazão média por mês
    vazao_mensal = (
        series_sazonais.groupby("estagio")["valor"]
        .agg(["mean", "std"])
        .reset_index()
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
    vazao_mensal["mes_nome"] = vazao_mensal["estagio"].map(
        lambda x: meses_nomes[x - 1] if x <= 12 else f"Est{x}"
    )

    print("Padrão sazonal das vazões afluentes:")
    print(vazao_mensal[["mes_nome", "mean", "std"]].round(1))

    # Gráfico sazonal
    fig = px.bar(
        vazao_mensal,
        x="mes_nome",
        y="mean",
        error_y="std",
        title="Padrão Sazonal das Vazões Afluentes",
        labels={"mean": "Vazão Média (hm³)", "mes_nome": "Mês"},
    )
    fig

# %%
# **Análise de variabilidade hidrológica**
#
# Comparando diferentes séries para avaliar a incerteza hidrológica:

# Selecionando uma UHE específica para análise detalhada
uhe_analise = series["uhe"].iloc[0]  # Primeira UHE disponível
series_uhe = series[series["uhe"] == uhe_analise]

if len(series_uhe) > 0:
    print(f"Análise de variabilidade - UHE {uhe_analise}:")

    # Estatísticas por série
    stats_por_serie = (
        series_uhe.groupby("serie")["valor"].agg(["mean", "std"]).reset_index()
    )

    print("Estatísticas das séries forward:")
    print(
        f"- Vazão média entre séries: {stats_por_serie['mean'].mean():.1f} hm³"
    )
    print(
        f"- Desvio padrão entre médias: {stats_por_serie['mean'].std():.1f} hm³"
    )
    print(
        f"- Coeficiente de variação: {stats_por_serie['mean'].std() / stats_por_serie['mean'].mean() * 100:.1f}%"
    )

    # Distribuição das médias por série
    fig = px.histogram(
        stats_por_serie,
        x="mean",
        title=f"Distribuição da Vazão Média por Série - UHE {uhe_analise}",
        labels={"mean": "Vazão Média (hm³)", "count": "Frequência"},
    )
    fig

# %%
# **Análise de cenários extremos**
#
# Identificando cenários de vazão alta e baixa:

# Vazão total por série (somando todas as UHEs e estágios)
vazao_total_serie = series.groupby("serie")["valor"].sum().reset_index()
vazao_total_serie = vazao_total_serie.sort_values("valor")

# Identificando cenários extremos
p10 = vazao_total_serie["valor"].quantile(0.10)
p90 = vazao_total_serie["valor"].quantile(0.90)

cenarios_secos = vazao_total_serie[vazao_total_serie["valor"] <= p10]
cenarios_umidos = vazao_total_serie[vazao_total_serie["valor"] >= p90]

print("Análise de cenários hidrológicos extremos:")
print(f"Cenários secos (≤P10): {len(cenarios_secos)} séries")
print(f"Cenários úmidos (≥P90): {len(cenarios_umidos)} séries")
print(f"Vazão P10: {p10:.0f} hm³")
print(f"Vazão P90: {p90:.0f} hm³")
print(f"Relação P90/P10: {p90 / p10:.2f}")

print("\nSéries dos cenários mais secos:")
print(cenarios_secos["serie"].tolist()[:10])  # Primeiras 10

print("\nSéries dos cenários mais úmidos:")
print(cenarios_umidos["serie"].tolist()[:10])  # Primeiras 10

# %%
# **Comparação entre usinas hidrelétricas**
#
# Analisando correlações e diferenças entre UHEs:

# Selecionando algumas UHEs para análise de correlação
uhes_principais = series["uhe"].value_counts().head(10).index.tolist()

if len(uhes_principais) > 1:
    # Criando matriz UHE x série para análise de correlação
    series_subset = series[series["uhe"].isin(uhes_principais)]

    # Calculando vazão média por UHE e série
    vazao_media_uhe_serie = (
        series_subset.groupby(["uhe", "serie"])["valor"].mean().reset_index()
    )

    pivot_vazao = vazao_media_uhe_serie.pivot_table(
        index="serie", columns="uhe", values="valor"
    )

    # Matriz de correlação entre UHEs
    correlacao_uhes = pivot_vazao.corr()

    print("Correlação entre UHEs principais (5x5):")
    print(correlacao_uhes.iloc[:5, :5].round(3))

    # Contribuição de cada UHE para o total
    contrib_uhe = (
        series.groupby("uhe")["valor"].sum().sort_values(ascending=False)
    )
    contrib_uhe_pct = (contrib_uhe / contrib_uhe.sum() * 100).round(1)

    print("\nTop 10 UHEs por contribuição total:")
    for uhe, pct in contrib_uhe_pct.head(10).items():
        print(f"UHE {uhe}: {pct}%")

# %%
# **Análise de consistência hidrológica**
#
# Verificando propriedades hidrológicas das séries:


def analisar_consistencia_hidrologica(df):
    """Análise de consistência das séries de vazão"""
    resultados = {}

    # 1. Verificar vazões negativas
    vazoes_negativas = df[df["valor"] < 0]
    resultados["vazoes_negativas"] = len(vazoes_negativas)

    # 2. Verificar vazões extremamente altas (outliers)
    q99 = df["valor"].quantile(0.99)
    q01 = df["valor"].quantile(0.01)
    outliers_altos = df[df["valor"] > q99 * 3]  # 3x o P99
    outliers_baixos = df[df["valor"] < q01 * 0.1]  # <10% do P01

    resultados["outliers_altos"] = len(outliers_altos)
    resultados["outliers_baixos"] = len(outliers_baixos)

    # 3. Verificar completude dos dados
    total_esperado = (
        df["serie"].nunique() * df["uhe"].nunique() * df["estagio"].nunique()
    )
    resultados["completude_pct"] = len(df) / total_esperado * 100

    # 4. Estatísticas básicas
    resultados["vazao_media_global"] = df["valor"].mean()
    resultados["vazao_std_global"] = df["valor"].std()
    resultados["cv_global"] = df["valor"].std() / df["valor"].mean()

    return resultados


print("Análise de consistência hidrológica:")
consistencia = analisar_consistencia_hidrologica(series)

print(f"- Vazões negativas: {consistencia['vazoes_negativas']} registros")
print(f"- Outliers altos: {consistencia['outliers_altos']} registros")
print(f"- Outliers baixos: {consistencia['outliers_baixos']} registros")
print(f"- Completude dos dados: {consistencia['completude_pct']:.1f}%")
print(f"- Vazão média global: {consistencia['vazao_media_global']:.1f} hm³")
print(f"- Coef. variação global: {consistencia['cv_global']:.3f}")

if consistencia["vazoes_negativas"] > 0:
    print("⚠️ Atenção: Vazões negativas detectadas")
if consistencia["completude_pct"] < 95:
    print("⚠️ Atenção: Dados incompletos detectados")


# %%
# **Processamento para análises externas**
#
# Preparando dados para exportação:

# Resumo estatístico por UHE
resumo_uhe = (
    series.groupby("uhe")["valor"]
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
resumo_uhe.columns = [
    "registros",
    "media",
    "desvio",
    "minimo",
    "maximo",
    "P10",
    "P50",
    "P90",
]

print("Resumo estatístico por UHE (primeiras 10):")
print(resumo_uhe.head(10))

# Vazões agregadas por estágio
vazoes_agregadas = (
    series.groupby("estagio")
    .agg({"valor": ["sum", "mean", "std", "count"]})
    .round(2)
)
vazoes_agregadas.columns = ["total", "media", "desvio", "registros"]

print("\nVazões agregadas por estágio (primeiros 12):")
print(vazoes_agregadas.head(12))

# %%
# **Exportação de resultados processados**

print("\nOpções de exportação disponíveis:")
print("1. Séries originais: arq_vazaof.series")
print("2. Resumo por UHE: resumo_uhe")
print("3. Vazões por estágio: vazao_por_estagio")
print("4. Vazões agregadas: vazoes_agregadas")
print("5. Cenários extremos: cenarios_secos, cenarios_umidos")

# Exemplos de exportação:
# resumo_uhe.to_csv('resumo_vazoes_uhe.csv')
# vazao_por_estagio.to_csv('vazoes_por_estagio.csv', index=False)
