"""
========================================================
Análise e modificação do cadastro de usinas térmicas
========================================================
"""


# %%
# O term.dat é o arquivo de entrada do modelo NEWAVE que contém as informações
# das usinas térmicas do sistema. Este arquivo define as características técnicas,
# operacionais e os limites de geração das usinas térmicas, incluindo suas
# inflexibilidades por mês.

from io import StringIO

import pandas as pd

from inewave.newave import Term

# Leitura do arquivo term.dat
arq_term = Term.read("./newave/term.dat")

# %%
# As informações das usinas térmicas são acessadas através da propriedade usinas:

usinas = arq_term.usinas
print(f"Total de registros de usinas térmicas: {len(usinas)}")
print("\nPrimeiros registros:")
print(usinas.head())

# %%
# **Análise das características técnicas das usinas**
#
# É importante compreender a capacidade instalada e os fatores de disponibilidade:

print("Estatísticas das usinas térmicas:")
stats_tecnicas = usinas[
    [
        "potencia_instalada",
        "fator_capacidade_maximo",
        "teif",
        "indisponibilidade_programada",
    ]
].describe()
print(stats_tecnicas)

# %%
# Cálculo da capacidade efetiva considerando fatores de indisponibilidade:

usinas_com_calc = usinas.copy()
usinas_com_calc["disponibilidade_total"] = (
    (100 - usinas_com_calc["teif"])
    * (100 - usinas_com_calc["indisponibilidade_programada"])
    / 10000
)
usinas_com_calc["capacidade_efetiva"] = (
    usinas_com_calc["potencia_instalada"]
    * usinas_com_calc["fator_capacidade_maximo"]
    / 100
    * usinas_com_calc["disponibilidade_total"]
)

print("Top 10 usinas térmicas por capacidade efetiva:")
top_usinas = usinas_com_calc.nlargest(10, "capacidade_efetiva")
print(top_usinas[["nome_usina", "potencia_instalada", "capacidade_efetiva"]])

# %%
# **Análise de inflexibilidades por mês**
#
# As usinas térmicas podem ter gerações mínimas obrigatórias variáveis ao longo do ano:

# Agrupando por usina para analisar perfil de inflexibilidade
print("Exemplo de análise de inflexibilidade:")
print("Usinas com geração mínima no mês 6:")
inflexibilidade_mes6 = usinas[usinas["mes"] == 6]
print(f"Quantidade de registros: {len(inflexibilidade_mes6)}")

inflexiveis = inflexibilidade_mes6[inflexibilidade_mes6["geracao_minima"] > 0]
print(f"Usinas com inflexibilidade > 0: {len(inflexiveis)}")

if len(inflexiveis) > 0:
    print("\nTop 5 usinas com maior inflexibilidade:")
    top_inflexiveis = inflexiveis.nlargest(5, "geracao_minima")
    print(top_inflexiveis[["codigo_usina", "nome_usina", "geracao_minima"]])

# %%
# **Análise temporal das inflexibilidades**
#
# Verificando como as inflexibilidades variam ao longo dos meses:


def analisar_inflexibilidade_temporal(df):
    """Analisa a variação temporal das inflexibilidades"""
    # Agrupando por mês
    inflexibilidade_mensal = (
        df.groupby("mes")
        .agg({
            "geracao_minima": ["count", "sum", "mean"],
            "codigo_usina": "nunique",
        })
        .round(2)
    )

    # Renomeando colunas para clareza
    inflexibilidade_mensal.columns = [
        "registros_total",
        "geracao_minima_total",
        "geracao_minima_media",
        "usinas_unicas",
    ]

    return inflexibilidade_mensal


print("Análise temporal das inflexibilidades:")
analise_temporal = analisar_inflexibilidade_temporal(usinas)
print(analise_temporal)

# %%
# **Identificação de usinas com perfil sazonal**
#
# Algumas usinas podem ter inflexibilidades que variam sazonalmente:


def identificar_perfil_sazonal(df):
    """Identifica usinas com variação sazonal de inflexibilidade"""
    # Pivot para ter inflexibilidade por usina e mês
    pivot_inflexibilidade = df.pivot_table(
        index="codigo_usina",
        columns="mes",
        values="geracao_minima",
        fill_value=0,
    )

    # Calculando variabilidade (desvio padrão) por usina
    pivot_inflexibilidade["variabilidade"] = pivot_inflexibilidade.std(axis=1)

    # Usinas com alta variabilidade sazonal
    alta_variabilidade = pivot_inflexibilidade[
        pivot_inflexibilidade["variabilidade"] > 0
    ].sort_values("variabilidade", ascending=False)

    return alta_variabilidade


if len(usinas[usinas["geracao_minima"] > 0]) > 0:
    print("Usinas com perfil sazonal de inflexibilidade:")
    perfil_sazonal = identificar_perfil_sazonal(usinas)
    print(f"Usinas com variação sazonal: {len(perfil_sazonal)}")
    if len(perfil_sazonal) > 0:
        print("\nTop 5 usinas com maior variação sazonal:")
        print(perfil_sazonal.head())

# %%
# **Modificação de dados térmicos**
#
# Criando cenários alternativos através de modificações programáticas:

print("Exemplo de modificação: Reduzindo TEIF em 20% para todas as usinas")

# Criando uma cópia para modificação
usinas_modificadas = usinas.copy()

# Reduzindo TEIF em 20% (melhoria na manutenção)
usinas_modificadas["teif"] = usinas_modificadas["teif"] * 0.8

print("Comparação do TEIF (original vs modificado):")
comparacao_teif = pd.DataFrame({
    "original": usinas["teif"],
    "modificado": usinas_modificadas["teif"],
    "melhoria_abs": usinas["teif"] - usinas_modificadas["teif"],
})
print(comparacao_teif.describe())

# %%
# **Criação de cenários de inflexibilidade**
#
# Modificando inflexibilidades para estudos de flexibilidade do sistema:

print("Criando cenário com redução de inflexibilidades:")

# Reduzindo inflexibilidades em 30%
usinas_flex = usinas.copy()
usinas_flex["geracao_minima"] = usinas_flex["geracao_minima"] * 0.7

inflexibilidade_original = usinas["geracao_minima"].sum()
inflexibilidade_nova = usinas_flex["geracao_minima"].sum()

print(f"Inflexibilidade total original: {inflexibilidade_original:.1f} MWmed")
print(f"Inflexibilidade total nova: {inflexibilidade_nova:.1f} MWmed")
print(
    f"Redução: {inflexibilidade_original - inflexibilidade_nova:.1f} MWmed ({(1 - inflexibilidade_nova / inflexibilidade_original) * 100:.1f}%)"
)

# %%
# **Validação de dados térmicos**
#
# Implementando verificações de consistência:


def validar_dados_termicos(df):
    """Valida consistência dos dados térmicos"""
    problemas = []

    # Verificar potência instalada positiva
    pot_negativa = df[df["potencia_instalada"] <= 0]
    if len(pot_negativa) > 0:
        problemas.append(
            f"Potência instalada inválida: {len(pot_negativa)} registros"
        )

    # Verificar fator de capacidade entre 0 e 100
    fc_invalido = df[
        (df["fator_capacidade_maximo"] < 0)
        | (df["fator_capacidade_maximo"] > 100)
    ]
    if len(fc_invalido) > 0:
        problemas.append(
            f"Fator de capacidade inválido: {len(fc_invalido)} registros"
        )

    # Verificar TEIF entre 0 e 100
    teif_invalido = df[(df["teif"] < 0) | (df["teif"] > 100)]
    if len(teif_invalido) > 0:
        problemas.append(f"TEIF inválido: {len(teif_invalido)} registros")

    # Verificar se geração mínima não excede capacidade
    geracao_excessiva = df[df["geracao_minima"] > df["potencia_instalada"]]
    if len(geracao_excessiva) > 0:
        problemas.append(
            f"Geração mínima > Potência instalada: {len(geracao_excessiva)} registros"
        )

    # Verificar mês válido (1-13)
    mes_invalido = df[(df["mes"] < 1) | (df["mes"] > 13)]
    if len(mes_invalido) > 0:
        problemas.append(f"Mês inválido: {len(mes_invalido)} registros")

    return problemas


print("Validação dos dados térmicos:")
problemas = validar_dados_termicos(usinas)
if problemas:
    for problema in problemas:
        print(f"- {problema}")
else:
    print("✓ Dados térmicos validados com sucesso!")


# %%
# **Aplicando modificações ao arquivo**
#
# Para salvar as modificações realizadas:

# Aplicando as modificações de TEIF reduzido
arq_term.usinas = usinas_modificadas

# %%
# **Exportação do arquivo modificado**

# Exportação para buffer em memória
buffer = StringIO()
arq_term.write(buffer)
print(f"Arquivo térmico modificado gerado: {len(buffer.getvalue())} caracteres")

# Para salvar em disco:
# arq_term.write("./term_modificado.dat")

# %%
# **Análise de capacidade firme**
#
# Calculando a capacidade firme das térmicas considerando todos os fatores:


def calcular_capacidade_firme(df):
    """Calcula capacidade firme das usinas térmicas"""
    resultado = df.groupby("codigo_usina").first()  # Uma linha por usina

    # Capacidade firme = Pot_instalada * FC_max * (1-TEIF/100) * (1-IP/100)
    resultado["capacidade_firme"] = (
        resultado["potencia_instalada"]
        * resultado["fator_capacidade_maximo"]
        / 100
        * (1 - resultado["teif"] / 100)
        * (1 - resultado["indisponibilidade_programada"] / 100)
    )

    return resultado[["nome_usina", "potencia_instalada", "capacidade_firme"]]


print("Capacidade firme das usinas térmicas:")
capacidade_firme = calcular_capacidade_firme(usinas)
print(
    f"Capacidade instalada total: {capacidade_firme['potencia_instalada'].sum():.1f} MW"
)
print(
    f"Capacidade firme total: {capacidade_firme['capacidade_firme'].sum():.1f} MW"
)
print(
    f"Fator de capacidade firme médio: {capacidade_firme['capacidade_firme'].sum() / capacidade_firme['potencia_instalada'].sum() * 100:.1f}%"
)

print("\nTop 10 usinas por capacidade firme:")
print(capacidade_firme.nlargest(10, "capacidade_firme"))
