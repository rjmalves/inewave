import os
import tempfile

from inewave.newave.modelos.vazinat import SecaoDadosVazinat
from inewave.newave.vazinat import Vazinat
from inewave.config import MAX_ANOS_HISTORICO

from tests.mocks.binarios import bytes_gz, fp_gz


ARQ_TESTE = "./tests/mocks/arquivos/vazinat.dat"

NUM_CONFIGURACOES = 1
NUM_UHES = 164
ANO_INICIO_HISTORICO = 1931
NUM_ENTRADAS = NUM_CONFIGURACOES * NUM_UHES * 12 * MAX_ANOS_HISTORICO


def test_secao_vazinat():
    r = SecaoDadosVazinat()
    r.read(
        fp_gz(ARQ_TESTE),
        numero_uhes=NUM_UHES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_vazinat():
    h = Vazinat.read(
        bytes_gz(ARQ_TESTE),
        numero_uhes=NUM_UHES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_vazinat():
    h = Vazinat.read(
        b"",
        numero_uhes=NUM_UHES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_vazinat():
    h1 = Vazinat.read(
        bytes_gz(ARQ_TESTE),
        numero_uhes=NUM_UHES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    h2 = Vazinat.read(
        bytes_gz(ARQ_TESTE),
        numero_uhes=NUM_UHES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    assert h1 == h2


def test_leitura_escrita_vazinat():
    h1 = Vazinat.read(
        bytes_gz(ARQ_TESTE),
        numero_uhes=NUM_UHES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dat") as f:
        tmp = f.name
    try:
        h1.write(tmp)
        h2 = Vazinat.read(
            tmp,
            numero_uhes=NUM_UHES,
            ano_inicio_historico=ANO_INICIO_HISTORICO,
            numero_configuracoes=NUM_CONFIGURACOES,
        )
        assert h1 == h2
    finally:
        os.unlink(tmp)
