"""
==============================================================
Análise de configuração dos REEs (Reservatórios Equivalentes)
==============================================================
"""


# %%
# O arquivo ree.dat contém as configurações dos REEs (Reservatórios Equivalentes
# de Energia) do sistema NEWAVE. Os REEs são agregações de usinas hidrelétricas
# que permitem uma representação simplificada do sistema hidroelétrico para
# fins de otimização.

import plotly.express as px
import plotly.io as pio

from inewave.newave import Ree

pio.templates.default = "ggplot2"

# Leitura do arquivo ree.dat
arq_ree = Ree.read("./newave/ree.dat")

# %%
# **Estrutura dos REEs**
#
# Cada REE agrupa usinas hidrelétricas de uma região e está associado a um submercado:

rees = arq_ree.rees
print(f"Total de REEs configurados: {len(rees)}")
print("\nREEs do sistema:")
print(rees)

print(f"\nSubmercados representados: {sorted(rees['submercado'].unique())}")
print(f"Códigos de REE: {sorted(rees['codigo'].unique())}")

# %%
# **Análise da distribuição por submercado**
#
# Verificando como os REEs estão distribuídos entre os submercados:

print("Distribuição de REEs por submercado:")

# Contagem de REEs por submercado
rees_por_submercado = (
    rees.groupby("submercado")
    .agg({"codigo": "count", "nome": lambda x: ", ".join(x)})
    .rename(columns={"codigo": "quantidade_rees", "nome": "nomes_rees"})
)

print(rees_por_submercado)

# Visualização da distribuição
fig = px.bar(
    rees_por_submercado.reset_index(),
    x="submercado",
    y="quantidade_rees",
    title="Distribuição de REEs por Submercado",
    labels={
        "submercado": "Submercado",
        "quantidade_rees": "Quantidade de REEs",
    },
)
fig

# %%
# **Análise de períodos individualizados**
#
# Verificando configurações de individualização de usinas:

print("Análise de períodos individualizados:")

# Verificar REEs com período de individualização definido
rees_individualizados = rees[
    (rees["mes_fim_individualizado"].notna())
    & (rees["ano_fim_individualizado"].notna())
    & (rees["mes_fim_individualizado"] > 0)
    & (rees["ano_fim_individualizado"] > 0)
]

if len(rees_individualizados) > 0:
    print(f"REEs com individualização: {len(rees_individualizados)}")
    print("\nREEs individualizados:")
    print(
        rees_individualizados[
            [
                "codigo",
                "nome",
                "mes_fim_individualizado",
                "ano_fim_individualizado",
            ]
        ]
    )

    # Criando data de fim da individualização
    rees_individualizados_copy = rees_individualizados.copy()
    rees_individualizados_copy["data_fim"] = (
        rees_individualizados_copy["ano_fim_individualizado"].astype(str)
        + "-"
        + rees_individualizados_copy["mes_fim_individualizado"]
        .astype(str)
        .str.zfill(2)
    )

    print("\nDatas de fim da individualização:")
    datas_fim = rees_individualizados_copy.groupby("data_fim")["codigo"].count()
    print(datas_fim)

    # Verificar configuração de remoção de fictícias
    remocao_ficticias = arq_ree.remocao_ficticias
    if remocao_ficticias is not None:
        print(f"\nRemoção de usinas fictícias: {remocao_ficticias}")
        opcoes_remocao = {
            0: "Não remove fictícias",
            1: "Remove fictícias no período individualizado",
        }
        descricao = opcoes_remocao.get(remocao_ficticias, "Opção desconhecida")
        print(f"Significado: {descricao}")


# %%
# **Modificação da configuração dos REEs**
#
# Exemplo de como modificar configurações para estudos específicos:

print("Exemplo de modificação de configuração:")

# Cenário: Alterando período de individualização de um REE específico
rees_modificado = rees.copy()

# Exemplo: Extendendo individualização do primeiro REE até dezembro de 2025
if len(rees_modificado) > 0:
    primeiro_ree = rees_modificado.iloc[0]["codigo"]

    print(f"Modificando individualização do REE {primeiro_ree}:")
    print(
        f"Antes: {rees_modificado.iloc[0]['mes_fim_individualizado']}/{rees_modificado.iloc[0]['ano_fim_individualizado']}"
    )

    # Aplicando modificação
    rees_modificado.iloc[
        0, rees_modificado.columns.get_loc("mes_fim_individualizado")
    ] = 12
    rees_modificado.iloc[
        0, rees_modificado.columns.get_loc("ano_fim_individualizado")
    ] = 2025

    print(
        f"Depois: {rees_modificado.iloc[0]['mes_fim_individualizado']}/{rees_modificado.iloc[0]['ano_fim_individualizado']}"
    )

    # Aplicando modificação ao arquivo
    arq_ree.rees = rees_modificado
    print("✓ Modificação aplicada ao arquivo")
