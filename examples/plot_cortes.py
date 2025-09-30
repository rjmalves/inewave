"""
=======================================================
Análise dos cortes de Benders e política operativa
=======================================================
"""


# %%
# O arquivo cortes.dat (binário) contém os cortes de Benders gerados durante
# o processo de otimização do NEWAVE. Estes cortes definem a política operativa
# do sistema hidrotérmico, representando o valor futuro da água em função
# do estado do sistema.

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

from inewave.newave import Cortes

pio.templates.default = "ggplot2"

# %%
# **Leitura dos cortes de Benders**
#
# IMPORTANTE: A leitura dos cortes requer configuração específica baseada nas
# dimensões do caso de estudo. Estes parâmetros devem corresponder exatamente
# às configurações utilizadas na execução do NEWAVE:
# IMPORTANTE: Foi gerado um arquivo cortes.dat reduzido utlizando o próprio módulo `inewave`
# para fins de demonstração com apenas 1 corte. Em um caso real, utilize o arquivo gerado pelo NEWAVE.

tamanho_registro = 17568
indice_ultimo_corte = 1
numero_total_cortes = 1
codigos_rees = [1, 6, 7, 5, 10, 12, 2, 11, 3, 4, 8, 9]
codigos_uhes = list(range(154))
codigos_submercados = [1, 2, 3, 4] 
ordem_maxima_parp = 12 
lag_maximo_gnl = 2 

print("Configuração da leitura dos cortes:")
print(f"- Tamanho do registro: {tamanho_registro} bytes")
print(f"- Último corte válido: {indice_ultimo_corte}")
print(f"- Total de cortes: {numero_total_cortes}")
print(f"- REEs: {codigos_rees}")
print(f"- Submercados: {codigos_submercados}")

# Leitura do arquivo cortes.dat
arq_cortes = Cortes.read(
    "./newave/cortes.dat",
    tamanho_registro=tamanho_registro,
    indice_ultimo_corte=indice_ultimo_corte,
    numero_total_cortes=numero_total_cortes,
    codigos_rees=codigos_rees,
    codigos_uhes=codigos_uhes,
    codigos_submercados=codigos_submercados,
    ordem_maxima_parp=ordem_maxima_parp,
    lag_maximo_gnl=lag_maximo_gnl,
)


# %%
# **Estrutura dos cortes de Benders**
#
# Analisando a estrutura e conteúdo dos cortes:

cortes = arq_cortes.cortes
print(f"Total de cortes válidos: {len(cortes)}")
print(f"Colunas disponíveis: {len(cortes.columns)}")

print("\nPrimeiros registros:")
print(cortes.head())


# %%
# **Análise dos coeficientes dos cortes**
#
# Examinando os coeficientes que definem o valor da água:

print("Análise dos coeficientes dos cortes:")

# Identificando colunas de coeficientes (começam com "pi_")
colunas_pi = [col for col in cortes.columns if col.startswith("pi_")]
print(f"Número de coeficientes por corte: {len(colunas_pi)}")

if len(colunas_pi) > 0:
    # Estatísticas dos coeficientes
    coeficientes_stats = cortes[colunas_pi].describe()
    print("\nEstatísticas dos coeficientes:")
    print(f"- Valor médio: {coeficientes_stats.loc['mean'].mean():.6f}")
    print(f"- Mínimo global: {coeficientes_stats.loc['min'].min():.6f}")
    print(f"- Máximo global: {coeficientes_stats.loc['max'].max():.6f}")

    # Analisando coeficientes de EARM (valor da água armazenada)
    colunas_earm = [col for col in colunas_pi if "earm" in col.lower()]
    if len(colunas_earm) > 0:
        print(
            f"\nAnálise dos coeficientes de EARM ({len(colunas_earm)} REEs):"
        )

        for col in colunas_earm[:5]:  # Primeiros 5 para não sobrecarregar
            ree_num = col.split("_")[-1] if "_" in col else "N/A"
            valores = cortes[col]
            print(f"- {col} (REE {ree_num}):")
            print(
                f"  Média: {valores.mean():.4f}"
            )
            print(f"  Min: {valores.min():.4f}, Max: {valores.max():.4f}")

    # Analisando coeficientes de ENA (valor da energia afluente)
    colunas_ena = [col for col in colunas_pi if "ena" in col.lower()]
    if len(colunas_ena) > 0:
        print(
            f"\nAnálise dos coeficientes de ENA ({len(colunas_ena)} termos):"
        )

        # Agrupando por lag
        ena_por_lag = {}
        for col in colunas_ena:
            if "lag" in col:
                lag = col.split("lag")[-1]
                if lag not in ena_por_lag:
                    ena_por_lag[lag] = []
                ena_por_lag[lag].append(col)

        for lag, cols in list(ena_por_lag.items())[:3]:  # Primeiros 3 lags
            valores_lag = cortes[cols].mean(
                axis=1
            )  # Média entre REEs para cada corte
            print(
                f"- Lag {lag}: Média: {valores_lag.mean():.6f}"
            )
