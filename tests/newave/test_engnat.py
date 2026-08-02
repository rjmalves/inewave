import os
import tempfile

from inewave.newave.modelos.engnat import SecaoDadosEngnat
from inewave.newave.engnat import Engnat
from inewave.config import MAX_ANOS_HISTORICO

from tests.mocks.binarios import bytes_gz, fp_gz


ARQ_TESTE = "./tests/mocks/arquivos/engnat.dat"

NUM_CONFIGURACOES = 1
NUM_REES = 12
ANO_INICIO_HISTORICO = 1931
NUM_ENTRADAS = NUM_CONFIGURACOES * NUM_REES * 12 * MAX_ANOS_HISTORICO


def test_secao_engnat():
    r = SecaoDadosEngnat()
    r.read(
        fp_gz(ARQ_TESTE),
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_engnat():
    h = Engnat.read(
        bytes_gz(ARQ_TESTE),
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_engnat():
    h = Engnat.read(
        b"",
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_engnat():
    h1 = Engnat.read(
        bytes_gz(ARQ_TESTE),
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    h2 = Engnat.read(
        bytes_gz(ARQ_TESTE),
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    assert h1 == h2


def test_leitura_escrita_engnat():
    h1 = Engnat.read(
        bytes_gz(ARQ_TESTE),
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dat") as f:
        tmp = f.name
    try:
        h1.write(tmp)
        h2 = Engnat.read(
            tmp,
            numero_rees=NUM_REES,
            ano_inicio_historico=ANO_INICIO_HISTORICO,
            numero_configuracoes=NUM_CONFIGURACOES,
        )
        assert h1 == h2
    finally:
        os.unlink(tmp)
