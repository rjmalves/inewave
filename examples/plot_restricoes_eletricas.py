"""
=====================================================
Processamento das restrições elétricas (CSV)
=====================================================
"""

# %%
# Para realizar o processamento do restricao-eletrica.csv, será utilizado o módulo plotly
import re

import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.templates.default = "ggplot2"


# %%
# O restricao-eletrica.csv é um arquivo de entrada das LIBS que contém as restrições
# elétricas do sistema, incluindo fórmulas, períodos de validade e limites por patamar.
# Para processar a sua informação, o usuário deve importar a classe `Restricoes`, que contém
# todos os métodos necessários
from inewave.libs import Restricoes

arq_restricoes = Restricoes.read("./libs/restricao-eletrica.csv")


# %%
# A implementação de todos os arquivos das LIBS segue o formato de arquivos por registro,
# contendo informações em linhas de comentários e com delimitador ';'. Além disso,
# a primeira coluna sempre identifica qual o registro cadastrado na linha em questão. O
# número total de colunas em cada linha é variável, de acordo com o valor da primeira coluna.

# %%
# **Análise das fórmulas de restrições elétricas (RE)**
# Estão disponíveis métodos para cada registro, com argumentos opcionais para realizar filtros
# nos objetos a serem processados
restricoes_re = arq_restricoes.re(df=True)
print(f"Total de restrições RE: {len(restricoes_re)}")
print("Colunas:", list(restricoes_re.columns))
print("\nPrimeiras restrições:")
print(restricoes_re.head())

# Análise dos componentes das fórmulas
usinas_hidr = []
intercambios = []

for formula in restricoes_re["formula"]:
    # Buscar referências a usinas hidrelétricas
    uh_matches = re.findall(r"ger_usih\((\d+)\)", formula)
    usinas_hidr.extend([int(uh) for uh in uh_matches])

    # Buscar referências a intercâmbios
    int_matches = re.findall(r"ener_interc\((\d+),(\d+)\)", formula)
    intercambios.extend([(int(orig), int(dest)) for orig, dest in int_matches])

print("\nComponentes encontrados:")
print(f"- Usinas hidrelétricas: {len(set(usinas_hidr))}")
print(f"- Intercâmbios: {len(set(intercambios))}")

# Visualização
fig = px.bar(
    x=restricoes_re["codigo_restricao"],
    y=[1] * len(restricoes_re),
    title="Códigos de Restrições Elétricas",
    labels={"x": "Código da Restrição", "y": "Contagem"},
)
fig

# %%
# **Análise dos períodos de validade (RE-HORIZ-PER)**
# É possível obter os períodos de validade das restrições
horiz_per = None
horiz_per = arq_restricoes.re_horiz_per(df=True)

print(f"\nPeríodos de validade: {len(horiz_per)}")
print("Colunas:", list(horiz_per.columns))
print("\nPrimeiros períodos:")
print(horiz_per.head())

# Análise temporal
horiz_per_copy = horiz_per.copy()
horiz_per_copy["data_inicio_dt"] = pd.to_datetime(horiz_per_copy["data_inicio"])
horiz_per_copy["data_fim_dt"] = pd.to_datetime(horiz_per_copy["data_fim"])
horiz_per_copy["duracao_dias"] = (
    horiz_per_copy["data_fim_dt"] - horiz_per_copy["data_inicio_dt"]
).dt.days + 1

print("\nAnálise temporal:")
print(f"- Duração média: {horiz_per_copy['duracao_dias'].mean():.1f} dias")
print(f"- Duração mínima: {horiz_per_copy['duracao_dias'].min()} dias")
print(f"- Duração máxima: {horiz_per_copy['duracao_dias'].max()} dias")

# Visualização temporal
fig = px.timeline(
    horiz_per_copy,
    x_start="data_inicio_dt",
    x_end="data_fim_dt",
    y="codigo_restricao",
    title="Períodos de Validade das Restrições",
    labels={"codigo_restricao": "Código da Restrição"},
)
fig


# %%
# **Edição de registros**
# É possível realizar a edição dos objetos retornados relacionados
# a cada registro. Para tal, basta atribuir valores a cada propriedade:

# Exemplo com restrição RE (se dados disponíveis)
restricoes_exemplo = arq_restricoes.re(codigo_restricao=1)
print(f"\nRestrição original: {restricoes_exemplo.formula}")
# Exemplo de modificação (comentado para não alterar dados):
# restricoes_exemplo.formula = "ger_usih(285) + ger_usih(287) + ger_usih(300)"
print("✓ Fórmula pode ser modificada via propriedade .formula")


periodo_exemplo = arq_restricoes.re_horiz_per(codigo_restricao=1)
print(
    f"Período original: {periodo_exemplo.data_inicio} a {periodo_exemplo.data_fim}"
)
# Exemplo de modificação (comentado para não alterar dados):
# from datetime import datetime
# periodo_exemplo.data_fim = datetime(2025, 8, 31)
print("✓ Período pode ser modificado via propriedades .data_inicio e .data_fim")
