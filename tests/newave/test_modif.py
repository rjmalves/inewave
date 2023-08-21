# Rotinas de testes associadas ao arquivo modif.dat do NEWAVE
from inewave.newave.modelos.modif import (
    USINA,
    VOLMIN,
    VOLMAX,
    NUMCNJ,
    NUMMAQ,
    VAZMIN,
    CFUGA,
    CMONT,
    VMAXT,
    VMINT,
    VMINP,
    VAZMINT,
    VAZMAXT,
    TURBMAXT,
    TURBMINT,
)

from inewave.newave import Modif

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.modif import (
    MockModif,
    MockUSINA,
    MockVOLMIN,
    MockVOLMAX,
    MockNUMCNJ,
    MockNUMMAQ,
    MockVAZMIN,
    MockCFUGA,
    MockCMONT,
    MockVMAXT,
    MockVMINT,
    MockVMINP,
    MockVAZMINT,
    MockVAZMAXT,
    MockTURBMAXT,
    MockTURBMINT,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_usina_modif():
    m: MagicMock = mock_open(read_data="".join(MockUSINA))
    r = USINA()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "CAMARGOS"]
    assert r.codigo == 1
    assert r.nome == "CAMARGOS"


def test_registro_vazmin_modif():
    m: MagicMock = mock_open(read_data="".join(MockVAZMIN))
    r = VAZMIN()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [34]
    assert r.vazao == 34


def test_registro_vmaxt_modif():
    m: MagicMock = mock_open(read_data="".join(MockVMAXT))
    r = VMAXT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2021, 12, 1), 61.310, "'%'"]
    assert r.data_inicio == datetime(2021, 12, 1)
    assert r.volume == 61.310
    assert r.unidade == "'%'"


def test_registro_vazmint_modif():
    m: MagicMock = mock_open(read_data="".join(MockVAZMINT))
    r = VAZMINT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2021, 10, 1), 10.00]
    assert r.data_inicio == datetime(2021, 10, 1)
    assert r.vazao == 10.00


def test_registro_volmin_modif():
    m: MagicMock = mock_open(read_data="".join(MockVOLMIN))
    r = VOLMIN()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [15563.63, "'h'"]
    assert r.volume == 15563.63


def test_registro_volmax_modif():
    m: MagicMock = mock_open(read_data="".join(MockVOLMAX))
    r = VOLMAX()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [55.0, "'%'"]
    assert r.volume == 55.0
    assert r.unidade == "'%'"


def test_registro_numcnj_modif():
    m: MagicMock = mock_open(read_data="".join(MockNUMCNJ))
    r = NUMCNJ()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [2]
    assert r.numero == 2


def test_registro_nummaq_modif():
    m: MagicMock = mock_open(read_data="".join(MockNUMMAQ))
    r = NUMMAQ()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [2, 5]
    assert r.conjunto == 2
    assert r.numero_maquinas == 5


def test_registro_vmint_modif():
    m: MagicMock = mock_open(read_data="".join(MockVMINT))
    r = VMINT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2021, 10, 1), 20.0, "'%'"]
    assert r.data_inicio == datetime(2021, 10, 1)
    assert r.volume == 20.0
    assert r.unidade == "'%'"


def test_registro_vminp_modif():
    m: MagicMock = mock_open(read_data="".join(MockVMINP))
    r = VMINP()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2021, 10, 1), 20.0, "'%'"]
    assert r.data_inicio == datetime(2021, 10, 1)
    assert r.volume == 20.0
    assert r.unidade == "'%'"


def test_registro_cfuga_modif():
    m: MagicMock = mock_open(read_data="".join(MockCFUGA))
    r = CFUGA()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2021, 10, 1), 5.60]
    assert r.data_inicio == datetime(2021, 10, 1)
    assert r.nivel == 5.60


def test_registro_cmont_modif():
    m: MagicMock = mock_open(read_data="".join(MockCMONT))
    r = CMONT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2021, 10, 1), 71.30]
    assert r.data_inicio == datetime(2021, 10, 1)
    assert r.nivel == 71.30


def test_registro_vazmaxt_modif():
    m: MagicMock = mock_open(read_data="".join(MockVAZMAXT))
    r = VAZMAXT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2020, 1, 1), 0.00]
    assert r.data_inicio == datetime(2020, 1, 1)
    assert r.vazao == 0.0


def test_registro_turbmaxt_modif():
    m: MagicMock = mock_open(read_data="".join(MockTURBMAXT))
    r = TURBMAXT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2020, 1, 1), 0.00]
    assert r.data_inicio == datetime(2020, 1, 1)
    assert r.turbinamento == 0.0


def test_registro_turbmint_modif():
    m: MagicMock = mock_open(read_data="".join(MockTURBMINT))
    r = TURBMINT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(2020, 1, 1), 0.00]
    assert r.data_inicio == datetime(2020, 1, 1)
    assert r.turbinamento == 0.0


def test_atributos_encontrados_modif():
    m: MagicMock = mock_open(read_data="".join(MockModif))
    with patch("builtins.open", m):
        ad = Modif.read(ARQ_TESTE)
        assert len(ad.usina()) > 0
        assert len(ad.vazmin()) > 0
        assert len(ad.vmaxt()) > 0
        assert len(ad.vazmint()) > 0
        assert isinstance(ad.volmin(), VOLMIN)
        assert isinstance(ad.volmax(), VOLMAX)
        assert len(ad.numcnj()) > 0
        assert len(ad.nummaq()) > 0
        assert len(ad.vmint()) > 0
        assert len(ad.vminp()) > 0
        assert len(ad.cfuga()) > 0
        assert len(ad.cmont()) > 0
        assert len(ad.vazmaxt()) > 0
        assert len(ad.turbmaxt()) > 0
        assert len(ad.turbmint()) > 0


def test_leitura_escrita_modif():
    m_leitura: MagicMock = mock_open(read_data="".join(MockModif))
    with patch("builtins.open", m_leitura):
        cf1 = Modif.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Modif.read(ARQ_TESTE)
        assert cf1 == cf2
