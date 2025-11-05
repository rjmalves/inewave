"""
===========================================================
Análise e modificação do cadastro de usinas hidrelétricas
===========================================================
"""


# %%
# O hidr.dat é o arquivo binário de entrada do modelo NEWAVE que contém o cadastro
# completo das usinas hidrelétricas do sistema. Este arquivo é fundamental para a
# modelagem do sistema hidrotérmico, pois define as características técnicas e
# operacionais de cada usina hidroelétrica.

import pandas as pd

from inewave.newave import Hidr

# Leitura do arquivo hidr.dat
arq_hidr = Hidr.read("./newave/hidr.dat")

# %%
# O cadastro completo das usinas pode ser acessado através da propriedade cadastro,
# que retorna um DataFrame pandas com todas as informações das usinas:

cadastro = arq_hidr.cadastro
print(f"Total de usinas hidrelétricas: {len(cadastro)}")
print("\nPrimeiras 5 usinas:")
print(cadastro.head())

# %%
# É possível analisar informações específicas das usinas. Por exemplo,
# verificar as características dos reservatórios:

print("Estatísticas dos volumes dos reservatórios (hm³):")
print(
    cadastro[["volume_minimo", "volume_maximo", "volume_vertedouro"]].describe()
)

# %%
# Para análises operacionais, é comum examinar as capacidades instaladas
# e características das máquinas:

# Calculando a potência total instalada por usina
potencia_cols = [f"potencia_nominal_conjunto_{i}" for i in range(1, 6)]
maquinas_cols = [f"maquinas_conjunto_{i}" for i in range(1, 6)]

cadastro_com_potencia = cadastro.copy()
cadastro_com_potencia["potencia_total"] = 0

for i in range(1, 6):
    pot_col = f"potencia_nominal_conjunto_{i}"
    maq_col = f"maquinas_conjunto_{i}"
    cadastro_com_potencia["potencia_total"] += (
        cadastro_com_potencia[pot_col] * cadastro_com_potencia[maq_col]
    )

print("Usinas com maior capacidade instalada:")
cadastro_com_potencia.nlargest(10, "potencia_total")[
    ["nome_usina", "potencia_total"]
]

# %%
# Análise por submercado é uma prática comum no planejamento energético:

print("Distribuição de usinas por submercado:")
distribuicao_submercado = (
    cadastro.groupby("submercado")
    .agg({"nome_usina": "count", "volume_maximo": "sum"})
    .rename(
        columns={
            "nome_usina": "quantidade_usinas",
            "volume_maximo": "volume_total",
        }
    )
)
print(distribuicao_submercado)

# %%
# Uma análise importante é verificar as usinas em cascata através dos
# códigos de jusante:

print("Exemplo de usinas com jusante definido:")
usinas_com_jusante = cadastro[cadastro["codigo_usina_jusante"] > 0]
print(f"Usinas em cascata: {len(usinas_com_jusante)} de {len(cadastro)} total")
usinas_com_jusante[["nome_usina", "codigo_usina_jusante"]].head(10)

# %%
# **Modificação de dados cadastrais**
#
# Uma das principais vantagens do inewave é permitir modificações programáticas
# dos arquivos de entrada. Por exemplo, pode-se alterar volumes mínimos para
# estudos de sensibilidade:

# Criando uma cópia para modificação
cadastro_modificado = cadastro.copy()

# Aumentando em 10% o volume mínimo de todas as usinas
cadastro_modificado["volume_minimo"] = (
    cadastro_modificado["volume_minimo"] * 1.1
)

print("Comparação dos volumes mínimos (original vs modificado):")
comparacao = pd.DataFrame({
    "original": cadastro["volume_minimo"],
    "modificado": cadastro_modificado["volume_minimo"],
    "diferenca_pct": (
        (cadastro_modificado["volume_minimo"] - cadastro["volume_minimo"])
        / cadastro["volume_minimo"]
        * 100
    ),
})
print(comparacao.head())

# %%
# Para aplicar as modificações ao arquivo, atualiza-se o cadastro:
arq_hidr.cadastro = cadastro_modificado

# %%
# **Criação de novos casos de estudo**
#
# É possível filtrar usinas para criar casos específicos. Por exemplo,
# analisando apenas usinas de um determinado submercado:

submercado_interesse = 1
usinas_submercado = cadastro[cadastro["submercado"] == submercado_interesse]

print(f"Usinas do submercado {submercado_interesse}:")
print(f"Quantidade: {len(usinas_submercado)}")
print(f"Volume total: {usinas_submercado['volume_maximo'].sum():.0f} hm³")

# %%
# **Validação de dados**
#
# O inewave permite implementar verificações de consistência dos dados:


def validar_cadastro(df):
    """Função para validar consistência do cadastro hidrelétrico"""
    problemas = []

    # Verificar se volume mínimo é menor que máximo
    vol_inconsistente = df[df["volume_minimo"] >= df["volume_maximo"]]
    if len(vol_inconsistente) > 0:
        problemas.append(
            f"Volumes inconsistentes: {len(vol_inconsistente)} usinas"
        )

    # Verificar se cota mínima é menor que máxima
    cota_inconsistente = df[df["cota_minima"] >= df["cota_maxima"]]
    if len(cota_inconsistente) > 0:
        problemas.append(
            f"Cotas inconsistentes: {len(cota_inconsistente)} usinas"
        )

    # Verificar usinas sem nome
    sem_nome = df[df["nome_usina"].isna() | (df["nome_usina"] == "")]
    if len(sem_nome) > 0:
        problemas.append(f"Usinas sem nome: {len(sem_nome)} usinas")

    return problemas


print("Validação do cadastro:")
problemas = validar_cadastro(cadastro)
if problemas:
    for problema in problemas:
        print(f"- {problema}")
else:
    print("✓ Cadastro validado com sucesso!")

# %%
# **Exportação do arquivo modificado**
#
# Após as modificações, o arquivo pode ser exportado para uso no NEWAVE:

from io import BytesIO

# Exportação para buffer em memória (útil para APIs web ou bancos de dados)
buffer = BytesIO()
arq_hidr.write(buffer)
print(f"Arquivo modificado gerado em memória: {len(buffer.getvalue())} bytes")

# Para salvar em disco, use:
# arq_hidr.write("./hidr_modificado.dat")

# %%
# **Análise de evaporação**
#
# Os coeficientes de evaporação são importantes para modelagem de reservatórios:

meses = [
    "jan",
    "fev",
    "mar",
    "abr",
    "mai",
    "jun",
    "jul",
    "ago",
    "set",
    "out",
    "nov",
    "dez",
]
colunas_evap = [f"evaporacao_{mes.upper()}" for mes in meses]

print("Estatísticas de evaporação por mês (mm):")
evaporacao_stats = cadastro[colunas_evap].describe()
print(evaporacao_stats.loc[["mean", "std", "min", "max"]])

# %%
# **Análise de produtibilidade**
#
# A produtibilidade específica é um parâmetro crucial para o desempenho das usinas:

print("Distribuição de produtibilidade específica:")
prod_stats = cadastro["produtibilidade_especifica"].describe()
print(prod_stats)

print("\nUsinas com maior produtibilidade específica:")
high_prod = cadastro.nlargest(5, "produtibilidade_especifica")
print(high_prod[["nome_usina", "produtibilidade_especifica", "submercado"]])
