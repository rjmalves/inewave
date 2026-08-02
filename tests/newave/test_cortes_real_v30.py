"""
Testes de regressão contra uma amostra REAL de um caso NEWAVE v30.0.04 com GNL
(estágio individualizado). Os valores esperados foram extraídos e conferidos
contra a saída do NWLISTCF do próprio caso (`nwlistcf.rel` / `estados.rel`),
garantindo que a leitura binária reproduz a saída oficial do modelo.

As fixtures em ``tests/mocks/arquivos/cortes_v30_gnl/`` são versionadas
comprimidas (`.gz`) — o `cortesh.dat` é ~99,8% zeros e o conjunto ocupa ~60 KB
em vez de ~8 MB. Como os leitores aceitam `bytes`, os testes descomprimem em
memória.
"""

import gzip

import numpy as np

from inewave.newave import Cortes, Cortese, Cortesh

DIR = "./tests/mocks/arquivos/cortes_v30_gnl"


def _bytes(nome: str) -> bytes:
    with gzip.open(f"{DIR}/{nome}.gz", "rb") as fp:
        return fp.read()


def _cortesh() -> Cortesh:
    return Cortesh.read(_bytes("cortesh.dat"))


def test_cortesh_real_dimensoes():
    h = _cortesh()
    assert h.versao_newave == 300004
    assert h.tamanho_corte == 17584
    assert h.lag_maximo_gnl == 2
    assert len(h.dados_uhes) == 155
    assert h.ordem_maxima_parp() == 12


def test_particao_cortes_real_valores_nwlistcf():
    """PIVARM/PIAFL/PIGTAD/PIMX_SAR do corte batem com o nwlistcf.rel."""
    h = _cortesh()
    df = Cortes.from_cortesh(
        _bytes("cortes-009.dat"), h, por_estagio=True
    ).cortes
    # 12 cortes reais (registro sentinela final descartado)
    assert len(df) == 12
    assert not np.any(np.isclose(df["rhs"], 0.0))

    # corte IREG 756 do nwlistcf (PERIODO 9)
    r = df[np.isclose(df["rhs"], 60135476.9239, atol=1e-2)].iloc[0]
    assert np.isclose(r["pi_varm_uhe4"], 0.00093)
    assert np.isclose(r["pi_varm_uhe20"], 0.00063)
    assert np.isclose(r["pi_qafl_uhe4_lag1"], 0.00457)
    assert np.isclose(r["pi_qafl_uhe4_lag12"], 0.00011)
    assert np.isclose(r["pi_gnl_sbm1_pat1_lag1"], -0.00014)
    assert np.isclose(r["pi_gnl_sbm1_pat3_lag2"], -0.00009)
    # bloco PIMX_SAR presente (nulo neste caso, SAR inativo)
    assert "pi_mx_sar_uhe4" in df.columns
    assert np.isclose(r["pi_mx_sar_uhe4"], 0.0)


def test_particao_estados_real_valores_estados_rel():
    """VARM/EARM/SGT do estado batem com o estados.rel."""
    h = _cortesh()
    df = Cortese.from_cortesh(_bytes("cortese-009.dat"), h).estados
    # 12 estados reais (estados NÃO possuem registro sentinela)
    assert len(df) == 12
    assert sum(c.startswith("varm_uhe") for c in df.columns) == 155
    assert sum(c.startswith("sgt_") for c in df.columns) == 45  # 5*3*3

    r0 = df.iloc[0]  # estados.rel IREG 249
    assert np.isclose(r0["funcao_objetivo"], 48041840.06, atol=1e-1)
    assert np.isclose(r0["varm_uhe4"], 0.0)
    assert np.isclose(r0["varm_uhe20"], 337.89, atol=1e-2)
    assert np.isclose(r0["earm_ree1"], 20253.73, atol=1e-2)
    assert np.isclose(r0["sgt_sbm1_pat1_est1"], 0.0)
    assert r0["iteracao_construcao"] == 1
    assert r0["indice_forward"] == 1
