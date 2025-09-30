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

# Configuração típica (ajustar conforme o caso)
tamanho_registro = 1664  # Bytes por registro de corte
indice_ultimo_corte = 5000  # Índice do último corte válido
numero_total_cortes = 10000  # Total de cortes no arquivo
codigos_rees = [1, 2, 3, 4, 11, 12]  # REEs do sistema
codigos_uhes = []  # UHEs individualizadas (se houver)
codigos_submercados = [1, 2, 3, 4]  # Submercados
ordem_maxima_parp = 12  # Ordem máxima do PAR(p)
lag_maximo_gnl = 2  # Lag máximo para GNL

print("Configuração da leitura dos cortes:")
print(f"- Tamanho do registro: {tamanho_registro} bytes")
print(f"- Último corte válido: {indice_ultimo_corte}")
print(f"- Total de cortes: {numero_total_cortes}")
print(f"- REEs: {codigos_rees}")
print(f"- Submercados: {codigos_submercados}")

# Leitura do arquivo cortes.dat
try:
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
    print("✓ Arquivo de cortes lido com sucesso")
except Exception as e:
    print(f"⚠️ Erro na leitura dos cortes: {e}")
    arq_cortes = None

# %%
# **Estrutura dos cortes de Benders**
#
# Analisando a estrutura e conteúdo dos cortes:

if arq_cortes is not None:
    cortes = arq_cortes.cortes
    if cortes is not None:
        print(f"Total de cortes válidos: {len(cortes)}")
        print(f"Colunas disponíveis: {len(cortes.columns)}")

        print("\nPrimeiros registros:")
        print(cortes.head())

        print("\nInformações básicas dos cortes:")
        print(f"- Índice mínimo: {cortes['indice_corte'].min()}")
        print(f"- Índice máximo: {cortes['indice_corte'].max()}")
        print(
            f"- Iterações de construção: {cortes['iteracao_construcao'].nunique()}"
        )
        print(f"- Forwards únicos: {cortes['indice_forward'].nunique()}")

        # Análise do RHS (termo independente)
        print("\nAnálise do RHS (valor esperado do futuro):")
        print(f"- RHS médio: {cortes['rhs'].mean():.2f}")
        print(f"- RHS mínimo: {cortes['rhs'].min():.2f}")
        print(f"- RHS máximo: {cortes['rhs'].max():.2f}")
        print(f"- Desvio padrão: {cortes['rhs'].std():.2f}")
    else:
        print("⚠️ Dados de cortes não disponíveis")
        cortes = None
else:
    cortes = None

# %%
# **Análise da construção dos cortes**
#
# Verificando como os cortes foram construídos ao longo das iterações:

if cortes is not None:
    print("Análise da construção dos cortes:")

    # Cortes por iteração de construção
    cortes_por_iteracao = (
        cortes.groupby("iteracao_construcao")
        .agg({"indice_corte": "count", "rhs": ["mean", "std"]})
        .round(2)
    )
    cortes_por_iteracao.columns = ["quantidade", "rhs_medio", "rhs_std"]

    print("Cortes construídos por iteração:")
    print(cortes_por_iteracao)

    # Visualização da construção ao longo das iterações
    fig = px.histogram(
        cortes,
        x="iteracao_construcao",
        title="Distribuição de Cortes por Iteração de Construção",
        labels={
            "iteracao_construcao": "Iteração de Construção",
            "count": "Número de Cortes",
        },
    )
    fig.show()

    # Evolução do valor médio do RHS
    if len(cortes_por_iteracao) > 1:
        fig = px.line(
            cortes_por_iteracao.reset_index(),
            x="iteracao_construcao",
            y="rhs_medio",
            title="Evolução do Valor Médio do RHS por Iteração",
            labels={
                "iteracao_construcao": "Iteração",
                "rhs_medio": "RHS Médio",
            },
        )
        fig.show()

# %%
# **Análise dos coeficientes dos cortes**
#
# Examinando os coeficientes que definem o valor da água:

if cortes is not None:
    print("Análise dos coeficientes dos cortes:")

    # Identificando colunas de coeficientes (começam com "pi_")
    colunas_pi = [col for col in cortes.columns if col.startswith("pi_")]
    print(f"Número de coeficientes por corte: {len(colunas_pi)}")

    if len(colunas_pi) > 0:
        # Estatísticas dos coeficientes
        coeficientes_stats = cortes[colunas_pi].describe()
        print("\nEstatísticas dos coeficientes:")
        print(f"- Valor médio: {coeficientes_stats.loc['mean'].mean():.6f}")
        print(
            f"- Desvio padrão médio: {coeficientes_stats.loc['std'].mean():.6f}"
        )
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
                    f"  Média: {valores.mean():.4f}, Std: {valores.std():.4f}"
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
                    f"- Lag {lag}: Média: {valores_lag.mean():.6f}, Std: {valores_lag.std():.6f}"
                )

# %%
# **Análise da qualidade dos cortes**
#
# Verificando indicadores de qualidade da política operativa:

if cortes is not None:
    print("Análise da qualidade dos cortes:")

    # 1. Verificar cortes inativos
    cortes_inativos = cortes[cortes["iteracao_inativacao"] > 0]
    taxa_inativacao = len(cortes_inativos) / len(cortes) * 100

    print(f"- Cortes inativos: {len(cortes_inativos)} ({taxa_inativacao:.1f}%)")

    if len(cortes_inativos) > 0:
        print(
            f"- Iteração média de inativação: {cortes_inativos['iteracao_inativacao'].mean():.1f}"
        )

    # 2. Distribuição dos índices forward
    forwards_unicos = cortes["indice_forward"].nunique()
    print(f"- Forwards diferentes: {forwards_unicos}")

    if forwards_unicos > 1:
        forward_dist = cortes["indice_forward"].value_counts().sort_index()
        print(
            f"- Forward mais comum: {forward_dist.idxmax()} ({forward_dist.max()} cortes)"
        )
        print(
            f"- Forward menos comum: {forward_dist.idxmin()} ({forward_dist.min()} cortes)"
        )

    # 3. Análise de convergência baseada no RHS
    if len(cortes_por_iteracao) > 1:
        rhs_primeira_iter = cortes_por_iteracao.iloc[0]["rhs_medio"]
        rhs_ultima_iter = cortes_por_iteracao.iloc[-1]["rhs_medio"]
        variacao_rhs = (
            abs(rhs_ultima_iter - rhs_primeira_iter)
            / abs(rhs_primeira_iter)
            * 100
        )

        print(f"- RHS primeira iteração: {rhs_primeira_iter:.2f}")
        print(f"- RHS última iteração: {rhs_ultima_iter:.2f}")
        print(f"- Variação do RHS: {variacao_rhs:.1f}%")

        if variacao_rhs < 5.0:
            print("  ✓ Convergência adequada (variação < 5%)")
        else:
            print("  ⚠️ Possível não convergência (variação ≥ 5%)")

# %%
# **Análise da cobertura da política**
#
# Verificando se a política cobre adequadamente o espaço de estados:

if cortes is not None and len(colunas_pi) > 0:
    print("Análise da cobertura da política:")

    # Analisando a diversidade dos coeficientes
    coef_matriz = cortes[colunas_pi].values

    # Calculando distâncias entre cortes (usando uma amostra para eficiência)
    try:
        from scipy.spatial.distance import pdist

        # Usar amostra se há muitos cortes
        amostra_size = min(1000, len(cortes))
        amostra_indices = np.random.choice(
            len(cortes), amostra_size, replace=False
        )
        coef_amostra = coef_matriz[amostra_indices]

        # Calcular distâncias
        distancias = pdist(coef_amostra)

        print(f"- Distância média entre cortes: {np.mean(distancias):.6f}")
        print(f"- Distância mínima: {np.min(distancias):.6f}")
        print(f"- Distância máxima: {np.max(distancias):.6f}")

        # Verificar cortes muito similares (possível redundância)
        cortes_similares = np.sum(distancias < np.mean(distancias) * 0.1)
        print(f"- Pares de cortes muito similares: {cortes_similares}")

        if cortes_similares > len(distancias) * 0.1:
            print("  ⚠️ Alta redundância detectada na política")
        else:
            print("  ✓ Diversidade adequada na política")

    except ImportError:
        print("  Scipy não disponível - análise de cobertura pulada")
    except Exception as e:
        print(f"  Erro na análise de cobertura: {e}")

# %%
# **Visualização da política operativa**
#
# Criando visualizações dos principais aspectos da política:

if cortes is not None and len(colunas_earm) > 0:
    print("Visualização da política operativa:")

    # Gráfico dos valores da água por REE
    fig = px.box(
        cortes,
        y=colunas_earm[:4],  # Primeiros 4 REEs
        title="Distribuição dos Valores da Água Armazenada por REE",
        labels={"variable": "REE", "value": "Coeficiente EARM"},
    )
    fig.show()

    # Relação entre RHS e coeficientes EARM
    if len(colunas_earm) > 0:
        primeiro_earm = colunas_earm[0]
        fig = px.scatter(
            cortes.sample(min(1000, len(cortes))),  # Amostra para visualização
            x=primeiro_earm,
            y="rhs",
            title=f"Relação entre {primeiro_earm} e RHS",
            labels={primeiro_earm: "Coeficiente EARM", "rhs": "RHS"},
        )
        fig.show()

# %%
# **Análise de sensibilidade da política**
#
# Verificando como a política responde a diferentes condições:

if cortes is not None:
    print("Análise de sensibilidade da política:")

    # Dividindo cortes em quartis de RHS
    cortes_copy = cortes.copy()
    cortes_copy["quartil_rhs"] = pd.qcut(
        cortes_copy["rhs"], 4, labels=["Q1", "Q2", "Q3", "Q4"]
    )

    # Comparando coeficientes médios por quartil
    if len(colunas_earm) > 0:
        sensibilidade_earm = cortes_copy.groupby("quartil_rhs")[
            colunas_earm[:3]
        ].mean()

        print("Coeficientes EARM médios por quartil de RHS:")
        print(sensibilidade_earm.round(4))

        # Verificando monotonia (valores devem aumentar com RHS maior)
        for col in colunas_earm[:3]:
            valores_quartis = sensibilidade_earm[col].values
            monotona = all(
                valores_quartis[i] <= valores_quartis[i + 1]
                for i in range(len(valores_quartis) - 1)
            )

            status = "✓" if monotona else "⚠️"
            print(
                f"{status} {col}: {'Monótona crescente' if monotona else 'Não monótona'}"
            )

# %%
# **Validação dos cortes**
#
# Verificando consistência dos dados de cortes:

if cortes is not None:

    def validar_cortes(df):
        """Valida a consistência dos cortes de Benders"""
        problemas = []

        # Verificar índices únicos
        if df["indice_corte"].duplicated().any():
            problemas.append("Índices de corte duplicados")

        # Verificar RHS válidos
        rhs_invalidos = df[(df["rhs"].isna()) | (df["rhs"] == 0)]
        if len(rhs_invalidos) > 0:
            problemas.append(f"RHS inválidos: {len(rhs_invalidos)} cortes")

        # Verificar coeficientes válidos
        if len(colunas_pi) > 0:
            coef_invalidos = df[colunas_pi].isna().sum().sum()
            if coef_invalidos > 0:
                problemas.append(
                    f"Coeficientes inválidos: {coef_invalidos} valores"
                )

        # Verificar iterações
        iter_invalidas = df[df["iteracao_construcao"] <= 0]
        if len(iter_invalidas) > 0:
            problemas.append(
                f"Iterações inválidas: {len(iter_invalidas)} cortes"
            )

        return problemas

    print("Validação dos cortes:")
    problemas = validar_cortes(cortes)

    if problemas:
        for problema in problemas:
            print(f"⚠️ {problema}")
    else:
        print("✓ Cortes validados com sucesso!")

# %%
# **Exportação de dados processados**
#
# Preparando dados dos cortes para análises externas:

if cortes is not None:
    print("Dados processados disponíveis para exportação:")

    # Resumo dos cortes
    resumo_cortes = {
        "total_cortes": len(cortes),
        "cortes_ativos": len(cortes[cortes["iteracao_inativacao"] == 0]),
        "iteracoes_construcao": cortes["iteracao_construcao"].nunique(),
        "rhs_medio": cortes["rhs"].mean(),
        "rhs_std": cortes["rhs"].std(),
        "numero_coeficientes": len(colunas_pi),
    }

    print("1. Resumo geral:")
    for chave, valor in resumo_cortes.items():
        if isinstance(valor, float):
            print(f"   {chave}: {valor:.4f}")
        else:
            print(f"   {chave}: {valor}")

    print(
        f"2. Cortes completos: {len(cortes)} registros x {len(cortes.columns)} colunas"
    )
    print("3. Análises por iteração: cortes_por_iteracao")

    if len(colunas_earm) > 0:
        print("4. Coeficientes EARM: colunas_earm")

    if "sensibilidade_earm" in locals():
        print("5. Análise de sensibilidade: sensibilidade_earm")

    # Exemplo de exportação:
    # cortes[['indice_corte', 'rhs'] + colunas_earm[:5]].to_csv('cortes_resumo.csv', index=False)
    # with open('resumo_politica.json', 'w') as f:
    #     import json
    #     json.dump(resumo_cortes, f, indent=2)

else:
    print("⚠️ Dados não disponíveis - verifique:")
    print("1. Arquivo cortes.dat existe e é acessível")
    print("2. Parâmetros de leitura estão corretos")
    print("3. Configuração corresponde ao caso de estudo")
