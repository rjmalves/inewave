"""
Testes dos arquivos de cortes/estados particionados por estágio e do layout
completo de coeficientes (incluindo PIMX_SAR), usando mocks binários gerados
que reproduzem o layout validado contra um caso real do NEWAVE.
"""

import numpy as np
import pandas as pd
import pytest

from inewave.newave.cortes import Cortes
from inewave.newave.cortese import Cortese
from tests.mocks.arquivos.cortes_particionados import (
    coeficientes_individualizado,
    coeficientes_individualizado_hibrido,
    coeficientes_ree,
    coeficientes_ree_completo,
    estado,
    gera_consolidado_cortes,
    gera_estados,
    gera_particao_cortes,
)

# --- Dimensões minúsculas (individualizado, gnl=2) ---
UHES = [1, 2, 3]
SUBMERCADOS = [1]
PARP = 2
NPAT = 1
LAG = 2
G2 = len(SUBMERCADOS) * NPAT * LAG  # 2
# n = 2 + G + U*(2+P) = 2 + 2 + 3*4 = 16
TAM_INDIV = 16 + (2 + G2 + len(UHES) * (2 + PARP)) * 8  # 144


def _registros_indiv(gnl_lag):
    """Três cortes individualizados com valores reconhecíveis."""
    g = len(SUBMERCADOS) * NPAT * gnl_lag
    registros = []
    for c in (1, 2, 3):
        gnl = [-1.0 * c - 0.1 * i for i in range(g)]
        varm = [10.0 * c + u for u in UHES]
        qafl = [
            100.0 * c + 10 * u + lag for u in UHES for lag in range(1, PARP + 1)
        ]
        sar = [0.5 * c + 0.01 * u for u in UHES]
        registros.append(
            coeficientes_individualizado(1000.0 * c, gnl, varm, qafl, sar)
        )
    return registros


def _le(content_path, **kwargs):
    return Cortes.read(
        content_path,
        tamanho_registro=kwargs.pop("tamanho_registro", TAM_INDIV),
        codigos_uhes=kwargs.pop("codigos_uhes", UHES),
        codigos_submercados=kwargs.pop("codigos_submercados", SUBMERCADOS),
        ordem_maxima_parp=kwargs.pop("ordem_maxima_parp", PARP),
        numero_patamares=kwargs.pop("numero_patamares", NPAT),
        lag_maximo_gnl=kwargs.pop("lag_maximo_gnl", LAG),
        **kwargs,
    )


def test_particao_igual_consolidado_individualizado(tmp_path):
    registros = _registros_indiv(LAG)
    consolidado = tmp_path / "cortes.dat"
    particao = tmp_path / "cortes-010.dat"
    consolidado.write_bytes(gera_consolidado_cortes(registros, TAM_INDIV))
    particao.write_bytes(gera_particao_cortes(registros, TAM_INDIV))

    dfc = _le(
        str(consolidado), indice_ultimo_corte=3, numero_total_cortes=3
    ).cortes
    dfp = _le(str(particao), por_estagio=True).cortes

    assert len(dfc) == 3 and len(dfp) == 3
    assert list(dfc.columns) == list(dfp.columns)
    # mesmos cortes (mesmo conjunto de rhs e mesmos pi)
    dfc_s = dfc.sort_values("rhs").reset_index(drop=True)
    dfp_s = dfp.sort_values("rhs").reset_index(drop=True)
    pd.testing.assert_frame_equal(dfc_s, dfp_s)


def test_valores_coeficientes_individualizado(tmp_path):
    registros = _registros_indiv(LAG)
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, TAM_INDIV))
    df = _le(str(particao), por_estagio=True).cortes

    r = df[np.isclose(df["rhs"], 2000.0)].iloc[0]  # corte c=2
    assert np.isclose(r["pi_varm_uhe1"], 21.0)
    assert np.isclose(r["pi_varm_uhe3"], 23.0)
    assert np.isclose(r["pi_qafl_uhe1_lag1"], 211.0)
    assert np.isclose(r["pi_qafl_uhe3_lag2"], 232.0)
    assert np.isclose(r["pi_gnl_sbm1_pat1_lag1"], -2.0)
    assert np.isclose(r["pi_mx_sar_uhe1"], 1.01)
    assert np.isclose(r["pi_mx_sar_uhe3"], 1.03)


def test_particao_sentinela_nao_e_lida(tmp_path):
    """O registro sentinela final (rhs=0) não deve virar corte."""
    registros = _registros_indiv(LAG)
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, TAM_INDIV))
    df = _le(str(particao), por_estagio=True).cortes
    assert len(df) == 3
    assert not np.any(np.isclose(df["rhs"], 0.0))


def test_individualizado_gnl_zero_sem_pi_gnl(tmp_path):
    registros = _registros_indiv(0)
    tam = 16 + (2 + 0 + len(UHES) * (2 + PARP)) * 8  # 128
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, tam))
    df = _le(
        str(particao), por_estagio=True, tamanho_registro=tam, lag_maximo_gnl=0
    ).cortes
    assert not any(c.startswith("pi_gnl") for c in df.columns)
    # bloco pi_varm permanece alinhado
    r = df[np.isclose(df["rhs"], 1000.0)].iloc[0]
    assert np.isclose(r["pi_varm_uhe1"], 11.0)
    assert np.isclose(r["pi_qafl_uhe3_lag2"], 132.0)


def test_individualizado_bloco_extra_hibrido_pimx_sar_ancorado(tmp_path):
    """
    Layout híbrido: há um bloco extra não-nomeado entre PIAFL e PIMX_SAR.
    PIMX_SAR deve ser lido do FIM do registro (ancorado pela cauda), sem
    desalinhar, e o bloco extra fica sem mapeamento.
    """
    n_extra = 4  # bloco extra (ex.: acoplamento por REE) de tamanho arbitrário
    # n = 2 + G + U*(2+P) + n_extra
    tam = 16 + (2 + G2 + len(UHES) * (2 + PARP) + n_extra) * 8
    registros = []
    for c in (1, 2, 3):
        gnl = [-1.0 * c - 0.1 * i for i in range(G2)]
        varm = [10.0 * c + u for u in UHES]
        qafl = [
            100.0 * c + 10 * u + lag for u in UHES for lag in range(1, PARP + 1)
        ]
        extra = [7.0 * c + 0.5 * i for i in range(n_extra)]
        sar = [0.5 * c + 0.01 * u for u in UHES]
        registros.append(
            coeficientes_individualizado_hibrido(
                1000.0 * c, gnl, varm, qafl, extra, sar
            )
        )
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, tam))
    df = _le(str(particao), por_estagio=True, tamanho_registro=tam).cortes

    r = df[np.isclose(df["rhs"], 2000.0)].iloc[0]  # corte c=2
    # pi_varm / pi_qafl permanecem corretos
    assert np.isclose(r["pi_varm_uhe1"], 21.0)
    assert np.isclose(r["pi_qafl_uhe3_lag2"], 232.0)
    # PIMX_SAR lido do fim do registro (não do bloco extra)
    assert np.isclose(r["pi_mx_sar_uhe1"], 1.01)
    assert np.isclose(r["pi_mx_sar_uhe3"], 1.03)
    # o bloco extra não vira coluna nomeada
    assert all("extra" not in c for c in df.columns)


def test_from_cortesh_exclui_uhes_ficticias(tmp_path):
    """
    `from_cortesh` deve dimensionar o registro apenas com as UHEs
    NÃO-FICTÍCIAS (``ficticia == 0``). O registro em disco carrega só essas;
    contar as fictícias levantaria ``ValueError`` de layout inconsistente.
    """

    class _CorteshStub:
        # 5 UHEs, 2 fictícias -> 3 não-fictícias (codigos 4, 20, 27),
        # em ordem de indice_usina.
        dados_uhes = pd.DataFrame(
            {
                "codigo_usina": [4, 20, 21, 27, 28],
                "indice_usina": [1, 2, 3, 4, 5],
                "ficticia": [0, 0, 1, 0, 1],
            }
        )
        numero_submercados = len(SUBMERCADOS)
        numero_patamares = NPAT
        lag_maximo_gnl = LAG
        # registro dimensionado para as 3 UHEs reais:
        # n = 2 + G + U*(2+P) = 2 + 2 + 3*4 = 16
        tamanho_registro_individualizado = 16 + (2 + G2 + 3 * (2 + PARP)) * 8

        def ordem_maxima_parp(self) -> int:
            return PARP

    codigos_reais = [4, 20, 27]
    registros = []
    for c in (1, 2):
        gnl = [-1.0 * c - 0.1 * i for i in range(G2)]
        varm = [10.0 * c + u for u in codigos_reais]
        qafl = [
            100.0 * c + u + lag
            for u in codigos_reais
            for lag in range(1, PARP + 1)
        ]
        sar = [0.0] * len(codigos_reais)
        registros.append(
            coeficientes_individualizado(1000.0 * c, gnl, varm, qafl, sar)
        )
    tam = _CorteshStub.tamanho_registro_individualizado
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, tam))

    df = Cortes.from_cortesh(
        str(particao), _CorteshStub(), por_estagio=True
    ).cortes

    # só as UHEs reais viram colunas; as fictícias (21, 28) não aparecem
    assert "pi_varm_uhe4" in df.columns
    assert "pi_varm_uhe27" in df.columns
    assert "pi_varm_uhe21" not in df.columns
    assert "pi_varm_uhe28" not in df.columns
    r = df[np.isclose(df["rhs"], 2000.0)].iloc[0]
    assert np.isclose(r["pi_varm_uhe4"], 24.0)
    assert np.isclose(r["pi_varm_uhe27"], 47.0)


def test_agregado_ree(tmp_path):
    rees = [1, 2]
    parp = 2
    g = len(SUBMERCADOS) * NPAT * LAG
    # n = 1 + R*(1+P) + G = 1 + 2*3 + 2 = 9
    tam = 16 + (1 + len(rees) * (1 + parp) + g) * 8
    registros = []
    for c in (1, 2):
        earm = [-0.1 * c - r for r in rees]
        ena = [
            0.01 * c + r + 0.1 * lag for r in rees for lag in range(1, parp + 1)
        ]
        gnl = [-1.0 * c - 0.1 * i for i in range(g)]
        registros.append(coeficientes_ree(500.0 * c, earm, ena, gnl))
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, tam))
    df = Cortes.read(
        str(particao),
        tamanho_registro=tam,
        codigos_rees=rees,
        codigos_submercados=SUBMERCADOS,
        ordem_maxima_parp=parp,
        numero_patamares=NPAT,
        lag_maximo_gnl=LAG,
        por_estagio=True,
    ).cortes
    assert len(df) == 2
    r = df[np.isclose(df["rhs"], 500.0)].iloc[0]
    assert np.isclose(r["pi_earm_ree1"], -1.1)
    assert np.isclose(r["pi_ena_ree1_lag1"], 1.11)
    assert np.isclose(r["pi_gnl_sbm1_pat1_lag1"], -1.0)


def test_agregado_ree_completo_com_pimx_sar(tmp_path):
    """
    Layout REE COMPLETO: rhs · PIEARM · PIH · PIGTAD · reservado · PIMX_SAR(R).
    O leitor deve mapear o bloco PIMX_SAR(R) ancorado pela cauda.
    """
    rees = [1, 2]
    parp = 2
    g = len(SUBMERCADOS) * NPAT * LAG
    # n = 1 + R*(1+P) + G + reservado(1) + R = 1 + 6 + 2 + 1 + 2 = 12
    tam = 16 + (1 + len(rees) * (1 + parp) + g + 1 + len(rees)) * 8
    registros = []
    for c in (1, 2):
        earm = [-0.1 * c - r for r in rees]
        ena = [
            0.01 * c + r + 0.1 * lag for r in rees for lag in range(1, parp + 1)
        ]
        gnl = [-1.0 * c - 0.1 * i for i in range(g)]
        mx_sar = [0.7 * c + r for r in rees]
        registros.append(
            coeficientes_ree_completo(500.0 * c, earm, ena, gnl, mx_sar)
        )
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, tam))
    df = Cortes.read(
        str(particao),
        tamanho_registro=tam,
        codigos_rees=rees,
        codigos_submercados=SUBMERCADOS,
        ordem_maxima_parp=parp,
        numero_patamares=NPAT,
        lag_maximo_gnl=LAG,
        por_estagio=True,
    ).cortes
    r = df[np.isclose(df["rhs"], 1000.0)].iloc[0]  # corte c=2
    assert np.isclose(r["pi_earm_ree1"], -1.2)
    assert np.isclose(r["pi_ena_ree2_lag2"], 2.22)
    assert np.isclose(r["pi_gnl_sbm1_pat1_lag1"], -2.0)
    # bloco PIMX_SAR(R) lido corretamente da cauda
    assert np.isclose(r["pi_mx_sar_ree1"], 2.4)
    assert np.isclose(r["pi_mx_sar_ree2"], 3.4)
    # todos os coeficientes nomeados presentes (só o reservado fica de fora)
    assert {"pi_mx_sar_ree1", "pi_mx_sar_ree2"} <= set(df.columns)


def test_parp_incorreto_levanta(tmp_path):
    registros = _registros_indiv(LAG)
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, TAM_INDIV))
    with pytest.raises(ValueError, match="Layout de coeficientes"):
        _le(str(particao), por_estagio=True, ordem_maxima_parp=99)


def test_tamanho_registro_nao_multiplo_levanta(tmp_path):
    registros = _registros_indiv(LAG)
    particao = tmp_path / "cortes-010.dat"
    conteudo = gera_particao_cortes(registros, TAM_INDIV)
    particao.write_bytes(conteudo + b"\x00\x00\x00")  # cauda espúria
    with pytest.raises(ValueError, match="não é múltiplo"):
        _le(str(particao), por_estagio=True)


def test_indice_global_em_particao_levanta(tmp_path):
    registros = _registros_indiv(LAG)
    particao = tmp_path / "cortes-010.dat"
    particao.write_bytes(gera_particao_cortes(registros, TAM_INDIV))
    with pytest.raises(ValueError, match="fora do arquivo"):
        _le(str(particao), indice_ultimo_corte=630000, numero_total_cortes=3)


def test_indice_nao_positivo_levanta(tmp_path):
    registros = _registros_indiv(LAG)
    consolidado = tmp_path / "cortes.dat"
    consolidado.write_bytes(gera_consolidado_cortes(registros, TAM_INDIV))
    with pytest.raises(ValueError, match="deve ser positivo"):
        _le(str(consolidado), indice_ultimo_corte=0, numero_total_cortes=3)


# --- Estados (cortese) ---
NREE = 2
NTOT_SUB = 1
E = LAG + 1  # 3
SGT = NTOT_SUB * NPAT * E  # 3
RESERVADO = 2
# m = 1 + R + U + SGT + reservado = 1 + 2 + 3 + 3 + 2 = 11
TAM_ESTADO = 12 + (1 + NREE + len(UHES) + SGT + RESERVADO) * 8


def _registros_estado():
    estados = []
    iteracoes = []
    for c in (1, 2, 3):
        earm = [1000.0 * c + r for r in range(1, NREE + 1)]
        varm = [10.0 * c + u for u in UHES]
        sgt = [-1.0 * c - 0.1 * i for i in range(SGT)]
        estados.append(estado(9000.0 * c, earm, varm, sgt, [0.0] * RESERVADO))
        iteracoes.append((c, c, 0))
    return estados, iteracoes


def test_estados_consolidado_e_particao(tmp_path):
    estados, iteracoes = _registros_estado()
    cons = tmp_path / "cortese.dat"
    part = tmp_path / "cortese-010.dat"
    cons.write_bytes(gera_estados(estados, iteracoes, TAM_ESTADO))
    part.write_bytes(gera_estados(estados, iteracoes, TAM_ESTADO))

    def ler(p):
        return Cortese.read(
            str(p),
            tamanho_estado=TAM_ESTADO,
            numero_rees=NREE,
            codigos_uhes=UHES,
            numero_total_submercados=NTOT_SUB,
            numero_patamares=NPAT,
            lag_maximo_gnl=LAG,
        ).estados

    dfc = ler(cons)
    dfp = ler(part)
    assert len(dfc) == 3 and len(dfp) == 3  # estados NÃO têm sentinela
    assert sum(c.startswith("earm") for c in dfc.columns) == NREE
    assert sum(c.startswith("varm") for c in dfc.columns) == len(UHES)
    assert sum(c.startswith("sgt") for c in dfc.columns) == SGT
    r = dfc.iloc[1]  # c=2
    assert np.isclose(r["funcao_objetivo"], 18000.0)
    assert np.isclose(r["earm_ree1"], 2001.0)
    assert np.isclose(r["varm_uhe1"], 21.0)
    assert np.isclose(r["sgt_sbm1_pat1_est1"], -2.0)
    assert r["iteracao_construcao"] == 2 and r["indice_forward"] == 2
