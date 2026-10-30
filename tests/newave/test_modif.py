# Rotinas de testes associadas ao arquivo modif.dat do NEWAVE
import io
from datetime import datetime
from typing import List, Optional, Type
from unittest.mock import MagicMock, patch

import pytest

from cfinterface.components.register import Register

from inewave.newave import Modif
from inewave.newave.modelos.modif import (
    CDESVIO,
    CFUGA,
    COEFEVAP,
    IP,
    ModifRegister,
    CMONT,
    COTAREA,
    NUMBAS,
    NUMCNJ,
    NUMMAQ,
    PERDHIDR,
    POTEFE,
    PRODESP,
    TEIF,
    TURBMAXT,
    TURBMINT,
    USINA,
    VAZMAXT,
    VAZMIN,
    VAZMINT,
    VMAXT,
    VMINP,
    VMINT,
    VOLCOTA,
    VOLMAX,
    VOLMIN,
)
from tests.mocks.arquivos.modif import (
    MockCDESVIO,
    MockCDESVIO_SEM_VAZAO,
    MockCFUGA,
    MockCOEFEVAP,
    MockIP,
    MockCMONT,
    MockCOTAREA,
    MockCOTAREA_E,
    MockModif,
    MockModif_REGISTROS_MANUAL,
    MockModif_SEM_USINA,
    MockModif_ULTIMA_USINA_FIM_ARQUIVO,
    MockModif_USINA_UNICA,
    MockModif_USINA_UNICA_SEM_REGISTROS,
    MockModif_USINA_DOIS_BLOCOS,
    MockNUMBAS,
    MockNUMCNJ,
    MockNUMMAQ,
    MockPERDHIDR,
    MockPOTEFE,
    MockPRODESP,
    MockTEIF,
    MockTURBMAXT,
    MockTURBMINT,
    MockUSINA,
    MockUSINA_PDE_3DIGIT,
    MockUSINA_PDE_MULTIWORD,
    MockVAZMAXT,
    MockVAZMIN,
    MockVAZMIN_DECIMAL,
    MockVAZMINT,
    MockVAZMINT_PDE,
    MockVAZMINT_POS,
    MockVAZMINT_PRE,
    MockVMAXT,
    MockVMAXT_PDE,
    MockVMINP,
    MockVMINT,
    MockVMINT_PDE,
    MockVOLCOTA,
    MockVOLCOTA_D,
    MockVOLMAX,
    MockVOLMIN,
)
from tests.mocks.mock_open import mock_open

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_usina_modif():
    m: MagicMock = mock_open(read_data="".join(MockUSINA))
    r = USINA()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [1, "CAMARGOS"]
    assert r.codigo == 1
    r.codigo = 2
    assert r.codigo == 2
    assert r.nome == "CAMARGOS"
    r.nome = "C1"
    assert r.nome == "C1"


def test_registro_vazmin_modif():
    m: MagicMock = mock_open(read_data="".join(MockVAZMIN))
    r = VAZMIN()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [34]
    assert r.vazao == 34
    r.vazao = 50
    assert r.vazao == 50


def test_registro_vazmin_decimal_modif():
    m: MagicMock = mock_open(read_data="".join(MockVAZMIN_DECIMAL))
    r = VAZMIN()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [34.0]
    assert r.vazao == 34.0
    r.vazao = 50.5
    assert r.vazao == 50.5


def test_registro_vmaxt_modif():
    m: MagicMock = mock_open(read_data="".join(MockVMAXT))
    r = VMAXT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [12, 2021, 61.310, "'%'"]
    assert r.data_inicio == datetime(2021, 12, 1)
    r.data_inicio = datetime(2022, 12, 1)
    assert r.data_inicio == datetime(2022, 12, 1)
    assert r.volume == 61.310
    r.volume = 50.0
    assert r.volume == 50.0
    assert r.unidade == "%"
    r.unidade = "h"
    assert r.unidade == "h"


def test_registro_vazmint_modif():
    m: MagicMock = mock_open(read_data="".join(MockVAZMINT))
    r = VAZMINT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [10, 2021, 10.00]
    assert r.data_inicio == datetime(2021, 10, 1)
    r.data_inicio = datetime(2022, 10, 1)
    assert r.data_inicio == datetime(2022, 10, 1)
    assert r.vazao == 10.00
    r.vazao = 5.0
    assert r.vazao == 5.0


def test_registro_vazmint_pre_modif():
    """Registro com marcador PRE (período pré-estudo) no campo do ano:
    é lido sem erro, ``data_inicio`` é None, ``periodo`` == 'PRE', e o mês e o
    valor continuam disponíveis."""
    m: MagicMock = mock_open(read_data="".join(MockVAZMINT_PRE))
    r = VAZMINT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [1, "PRE", 330.000]
    assert r.data_inicio is None
    assert r.periodo == "PRE"
    assert r.mes == 1
    assert r.vazao == 330.000


def test_registro_vazmint_pos_modif():
    """Registro com marcador POS (período pós-estudo) no campo do ano."""
    m: MagicMock = mock_open(read_data="".join(MockVAZMINT_POS))
    r = VAZMINT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [6, "POS", 300.000]
    assert r.data_inicio is None
    assert r.periodo == "POS"
    assert r.mes == 6
    assert r.vazao == 300.000


def test_registro_vazmint_ano_numerico_periodo_none():
    """Um ano numérico normal tem ``periodo`` None e ``data_inicio`` válido."""
    m: MagicMock = mock_open(read_data="".join(MockVAZMINT))
    r = VAZMINT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.periodo is None
    assert r.data_inicio == datetime(2021, 10, 1)
    assert r.mes == 10


def test_registro_volmin_modif():
    m: MagicMock = mock_open(read_data="".join(MockVOLMIN))
    r = VOLMIN()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [15563.63, "'h'"]
    assert r.volume == 15563.63
    r.volume = 15
    assert r.volume == 15
    assert r.unidade == "h"
    r.unidade = "%"
    assert r.unidade == "%"


def test_registro_volmax_modif():
    m: MagicMock = mock_open(read_data="".join(MockVOLMAX))
    r = VOLMAX()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [55.0, "'%'"]
    assert r.volume == 55.0
    r.volume = 1000
    assert r.volume == 1000
    assert r.unidade == "%"
    r.unidade = "h"
    assert r.unidade == "h"


def test_registro_numcnj_modif():
    m: MagicMock = mock_open(read_data="".join(MockNUMCNJ))
    r = NUMCNJ()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [2]
    assert r.numero == 2
    r.numero = 1
    assert r.numero == 1


def test_registro_nummaq_modif():
    m: MagicMock = mock_open(read_data="".join(MockNUMMAQ))
    r = NUMMAQ()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [2, 5]
    assert r.numero_maquinas == 2
    r.numero_maquinas = 10
    assert r.numero_maquinas == 10
    assert r.conjunto == 5
    r.conjunto = 1
    assert r.conjunto == 1


def test_registro_potefe_modif():
    m: MagicMock = mock_open(read_data="".join(MockPOTEFE))
    r = POTEFE()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [1347.2, 2]
    assert r.potencia == 1347.2
    r.potencia = 1400.0
    assert r.potencia == 1400.0
    assert r.conjunto == 2
    r.conjunto = 1
    assert r.conjunto == 1


def test_registro_volcota_modif():
    m: MagicMock = mock_open(read_data="".join(MockVOLCOTA))
    r = VOLCOTA()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [256.72, 0.0, 0.0, 0.0, 0.0]
    assert r.polinomio_volume_cota == [256.72, 0.0, 0.0, 0.0, 0.0]
    r.polinomio_volume_cota = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert r.polinomio_volume_cota == [1.0, 2.0, 3.0, 4.0, 5.0]


def test_registro_cotarea_modif():
    m: MagicMock = mock_open(read_data="".join(MockCOTAREA))
    r = COTAREA()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    # O deck escreve o expoente em notação Fortran (D), lida como float.
    assert r.data == [-1.002796e7, 9.198078e4, -2.812294e2, 2.866181e-1, 0.0]
    assert r.polinomio_cota_area == [
        -1.002796e7,
        9.198078e4,
        -2.812294e2,
        2.866181e-1,
        0.0,
    ]
    r.polinomio_cota_area = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert r.polinomio_cota_area == [1.0, 2.0, 3.0, 4.0, 5.0]


def test_registro_volcota_notacao_exponencial_modif():
    """Os coeficientes valem o mesmo escritos em decimal ou com expoente D."""
    m: MagicMock = mock_open(read_data="".join(MockVOLCOTA_D))
    r = VOLCOTA()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.polinomio_volume_cota == [256.72, 0.0, 0.0, 0.0, 0.0]


def test_registro_cotarea_notacao_exponencial_modif():
    """Os coeficientes valem o mesmo escritos com expoente D ou E."""
    m: MagicMock = mock_open(read_data="".join(MockCOTAREA_E))
    r = COTAREA()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.polinomio_cota_area == [
        -1.002796e7,
        9.198078e4,
        -2.812294e2,
        2.866181e-1,
        0.0,
    ]


def test_registro_vmint_modif():
    m: MagicMock = mock_open(read_data="".join(MockVMINT))
    r = VMINT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [10, 2021, 20.0, "'%'"]
    assert r.data_inicio == datetime(2021, 10, 1)
    r.data_inicio = datetime(2022, 10, 1)
    assert r.data_inicio == datetime(2022, 10, 1)
    assert r.volume == 20.0
    r.volume = 10.0
    assert r.volume == 10.0
    assert r.unidade == "%"
    r.unidade = "h"
    assert r.unidade == "h"


def test_registro_vminp_modif():
    m: MagicMock = mock_open(read_data="".join(MockVMINP))
    r = VMINP()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [10, 2021, 20.0, "'%'"]
    assert r.data_inicio == datetime(2021, 10, 1)
    r.data_inicio = datetime(2022, 10, 1)
    assert r.data_inicio == datetime(2022, 10, 1)
    assert r.volume == 20.0
    r.volume = 10.0
    assert r.volume == 10.0
    assert r.unidade == "%"
    r.unidade = "h"
    assert r.unidade == "h"


def test_registro_cfuga_modif():
    m: MagicMock = mock_open(read_data="".join(MockCFUGA))
    r = CFUGA()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [10, 2021, 5.60]
    assert r.data_inicio == datetime(2021, 10, 1)
    r.data_inicio = datetime(2022, 10, 1)
    assert r.data_inicio == datetime(2022, 10, 1)
    assert r.nivel == 5.60
    r.nivel = 10.0
    assert r.nivel == 10.0


def test_registro_cmont_modif():
    m: MagicMock = mock_open(read_data="".join(MockCMONT))
    r = CMONT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [10, 2021, 71.30]
    assert r.data_inicio == datetime(2021, 10, 1)
    r.data_inicio = datetime(2022, 10, 1)
    assert r.data_inicio == datetime(2022, 10, 1)
    assert r.nivel == 71.30
    r.nivel = 10.0
    assert r.nivel == 10.0


def test_registro_vazmaxt_modif():
    m: MagicMock = mock_open(read_data="".join(MockVAZMAXT))
    r = VAZMAXT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [1, 2020, 0.00]
    assert r.data_inicio == datetime(2020, 1, 1)
    r.data_inicio = datetime(2022, 10, 1)
    assert r.data_inicio == datetime(2022, 10, 1)
    assert r.vazao == 0.0
    r.vazao = 5.0
    assert r.vazao == 5.0


def test_registro_turbmaxt_modif():
    m: MagicMock = mock_open(read_data="".join(MockTURBMAXT))
    r = TURBMAXT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [1, 2020, 0.00]
    assert r.data_inicio == datetime(2020, 1, 1)
    r.data_inicio = datetime(2022, 10, 1)
    assert r.data_inicio == datetime(2022, 10, 1)
    assert r.turbinamento == 0.0
    r.turbinamento = 5.0
    assert r.turbinamento == 5.0


def test_registro_turbmint_modif():
    m: MagicMock = mock_open(read_data="".join(MockTURBMINT))
    r = TURBMINT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data == [1, 2020, 0.00]
    assert r.data_inicio == datetime(2020, 1, 1)
    r.data_inicio = datetime(2022, 10, 1)
    assert r.data_inicio == datetime(2022, 10, 1)
    assert r.turbinamento == 0.0
    r.turbinamento = 5.0
    assert r.turbinamento == 5.0


def _le_registro(registro: Type[ModifRegister], conteudo: str) -> ModifRegister:
    r = registro()
    r.read(io.StringIO(conteudo))
    return r


def test_registro_prodesp_modif():
    r = _le_registro(PRODESP, MockPRODESP)
    assert isinstance(r, PRODESP)
    assert r.data == [0.008829]
    assert r.produtibilidade == 0.008829
    r.produtibilidade = 0.0091
    assert r.produtibilidade == 0.0091


def test_registro_teif_modif():
    r = _le_registro(TEIF, MockTEIF)
    assert isinstance(r, TEIF)
    assert r.data == [2.851]
    assert r.teif == 2.851
    r.teif = 3.0
    assert r.teif == 3.0


def test_registro_ip_modif():
    r = _le_registro(IP, MockIP)
    assert isinstance(r, IP)
    assert r.data == [5.3]
    assert r.ip == 5.3
    r.ip = 4.0
    assert r.ip == 4.0


def test_registro_perdhidr_modif():
    r = _le_registro(PERDHIDR, MockPERDHIDR)
    assert isinstance(r, PERDHIDR)
    assert r.data == [0.65]
    assert r.perdas == 0.65
    r.perdas = 1.2
    assert r.perdas == 1.2


def test_registro_coefevap_modif():
    r = _le_registro(COEFEVAP, MockCOEFEVAP)
    assert isinstance(r, COEFEVAP)
    assert r.data == [-12, 7]
    assert r.coeficiente == -12
    assert r.mes == 7
    r.coeficiente = 5
    r.mes = 12
    assert r.coeficiente == 5
    assert r.mes == 12


def test_registro_numbas_modif():
    r = _le_registro(NUMBAS, MockNUMBAS)
    assert isinstance(r, NUMBAS)
    assert r.data == [2]
    assert r.numero == 2
    r.numero = 3
    assert r.numero == 3


def test_registro_cdesvio_modif():
    r = _le_registro(CDESVIO, MockCDESVIO)
    assert isinstance(r, CDESVIO)
    assert r.data == [66, 1500.5]
    assert r.codigo_usina_jusante == 66
    assert r.limite_vazao == 1500.5
    r.codigo_usina_jusante = 67
    r.limite_vazao = None
    assert r.codigo_usina_jusante == 67
    assert r.limite_vazao is None


def test_registro_cdesvio_sem_vazao_modif():
    r = _le_registro(CDESVIO, MockCDESVIO_SEM_VAZAO)
    assert isinstance(r, CDESVIO)
    assert r.codigo_usina_jusante == 66
    assert r.limite_vazao is None


def test_registro_cdesvio_vazao_ilegivel_modif():
    r = _le_registro(CDESVIO, " CDESVIO   66   abc\n")
    assert r.codigo_usina_jusante == 66
    assert r.limite_vazao is None


@pytest.mark.parametrize(
    "registro, conteudo",
    [
        (PRODESP, MockPRODESP),
        (TEIF, MockTEIF),
        (IP, MockIP),
        (PERDHIDR, MockPERDHIDR),
        (COEFEVAP, MockCOEFEVAP),
        (NUMBAS, MockNUMBAS),
        (CDESVIO, MockCDESVIO),
        (CDESVIO, MockCDESVIO_SEM_VAZAO),
    ],
)
def test_registros_do_manual_escrita_e_releitura(
    registro: Type[ModifRegister], conteudo: str
):
    r = _le_registro(registro, conteudo)
    saida = io.StringIO()
    r.write(saida)
    escrito = saida.getvalue()
    assert registro.matches(escrito)
    assert _le_registro(registro, escrito).data == r.data


@pytest.mark.parametrize(
    "registro, completo, sem_opcional",
    [
        (CDESVIO, MockCDESVIO, MockCDESVIO_SEM_VAZAO),
        (VOLMIN, MockVOLMIN, " VOLMIN   10.0\n"),
    ],
)
def test_campo_opcional_ausente_nao_herda_valor_de_escrita_anterior(
    registro: Type[ModifRegister], completo: str, sem_opcional: str
):
    _le_registro(registro, completo).write(io.StringIO())
    assert _le_registro(registro, sem_opcional).data[-1] is None


def test_identificadores_curtos_nao_casam_com_prefixos():
    assert not IP.matches(" IPXXX    5.3\n")
    assert not TEIF.matches(" TEIFX    2.0\n")


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
        assert isinstance(ad.potefe(), POTEFE)
        assert isinstance(ad.volcota(), VOLCOTA)
        assert isinstance(ad.cotarea(), COTAREA)
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


def test_registro_usina_pde_3digit():
    m: MagicMock = mock_open(read_data="".join(MockUSINA_PDE_3DIGIT))
    r = USINA()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.codigo == 228
    assert r.nome == "COLIDER"


def test_registro_usina_pde_multiword_name():
    m: MagicMock = mock_open(read_data="".join(MockUSINA_PDE_MULTIWORD))
    r = USINA()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.codigo == 4
    assert r.nome == "FUNIL GRANDE"


def test_registro_vmaxt_pde_spacing():
    m: MagicMock = mock_open(read_data="".join(MockVMAXT_PDE))
    r = VMAXT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data_inicio == datetime(2024, 1, 1)
    assert r.volume == 80.7
    assert r.unidade == "%"


def test_registro_vmint_pde_spacing():
    m: MagicMock = mock_open(read_data="".join(MockVMINT_PDE))
    r = VMINT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data_inicio == datetime(2024, 1, 1)
    assert r.volume == 13.23
    assert r.unidade == "%"


def test_registro_vazmint_pde_spacing():
    m: MagicMock = mock_open(read_data="".join(MockVAZMINT_PDE))
    r = VAZMINT()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)

    assert r.data_inicio == datetime(2024, 1, 1)
    assert r.vazao == 79.0


def _modificacoes_usina(
    conteudo: List[str], codigo: int
) -> Optional[List[Register]]:
    m: MagicMock = mock_open(read_data="".join(conteudo))
    with patch("builtins.open", m):
        modif = Modif.read(ARQ_TESTE)
    return modif.modificacoes_usina(codigo)


def test_modificacoes_usina_ultima_usina_fim_arquivo_inclui_ultimo_registro():
    regs = _modificacoes_usina(MockModif_ULTIMA_USINA_FIM_ARQUIVO, 2)
    assert regs is not None
    assert [type(r) for r in regs] == [CMONT, CMONT]
    assert [r.nivel for r in regs] == [96.01, 96.78]
    assert regs[-1].data_inicio == datetime(2026, 12, 1)


def test_modificacoes_usina_intermediaria_para_na_proxima_usina():
    regs = _modificacoes_usina(MockModif_ULTIMA_USINA_FIM_ARQUIVO, 1)
    assert regs is not None
    assert [type(r) for r in regs] == [VOLMIN]
    assert regs[0].volume == 10.0


def test_modificacoes_usina_unica_retorna_registros():
    regs = _modificacoes_usina(MockModif_USINA_UNICA, 1)
    assert regs is not None
    assert [type(r) for r in regs] == [VOLMIN, CFUGA]
    assert regs[1].nivel == 900.0


def test_modificacoes_usina_unica_sem_registros_retorna_lista_vazia():
    assert _modificacoes_usina(MockModif_USINA_UNICA_SEM_REGISTROS, 1) == []


def test_modificacoes_usina_codigo_inexistente_retorna_lista_vazia():
    assert _modificacoes_usina(MockModif_ULTIMA_USINA_FIM_ARQUIVO, 99) == []


def test_modificacoes_usina_dois_blocos_considera_apenas_o_primeiro():
    regs = _modificacoes_usina(MockModif_USINA_DOIS_BLOCOS, 1)
    assert regs is not None
    assert [type(r) for r in regs] == [VOLMIN]
    assert regs[0].volume == 10.0


def test_modificacoes_usina_arquivo_sem_usina_retorna_none():
    assert _modificacoes_usina(MockModif_SEM_USINA, 1) is None


def test_modificacoes_usina_mock_completo_ultima_usina():
    regs = _modificacoes_usina(MockModif, 190)
    assert regs is not None
    assert len(regs) == 23
    assert all(isinstance(r, VMAXT) for r in regs[-2:])
    assert regs[-1].data_inicio == datetime(2025, 12, 1)
    assert regs[-1].volume == 69.14


def test_atributos_df_modif():
    m: MagicMock = mock_open(read_data="".join(MockModif))
    with patch("builtins.open", m):
        ad = Modif.read(ARQ_TESTE)
    acessores = {
        ad.usina: USINA,
        ad.volmin: VOLMIN,
        ad.volmax: VOLMAX,
        ad.numcnj: NUMCNJ,
        ad.nummaq: NUMMAQ,
        ad.potefe: POTEFE,
        ad.volcota: VOLCOTA,
        ad.cotarea: COTAREA,
        ad.vazmin: VAZMIN,
        ad.cfuga: CFUGA,
        ad.cmont: CMONT,
        ad.vmaxt: VMAXT,
        ad.vmint: VMINT,
        ad.vminp: VMINP,
        ad.vazmint: VAZMINT,
        ad.vazmaxt: VAZMAXT,
        ad.turbmaxt: TURBMAXT,
        ad.turbmint: TURBMINT,
    }
    for acessor, tipo in acessores.items():
        registros = list(ad.data.of_type(tipo))
        df = acessor(df=True)
        assert list(df.columns) == registros[0].custom_properties, tipo
        assert len(df) == len(registros), tipo


@pytest.mark.parametrize(
    "registro, conteudo, unidade_lida",
    [
        (VOLMIN, MockVOLMIN, "h"),
        (VOLMAX, MockVOLMAX, "%"),
        (VMAXT, MockVMAXT, "%"),
        (VMINT, MockVMINT, "%"),
        (VMINP, MockVMINP, "%"),
    ],
)
def test_unidade_sem_aspas_e_escrita_com_aspas(
    registro: Type[ModifRegister], conteudo: str, unidade_lida: str
) -> None:
    m: MagicMock = mock_open(read_data=conteudo)
    r = registro()
    with patch("builtins.open", m), open("", "") as fp:
        r.read(fp)
    assert r.unidade == unidade_lida

    # A escrita preserva as aspas lidas do arquivo.
    escrita = io.StringIO()
    r.write(escrita)
    assert f"'{unidade_lida}'" in escrita.getvalue()

    # Uma unidade atribuída sem aspas é escrita entre aspas.
    r.unidade = "H"
    assert r.unidade == "H"
    escrita = io.StringIO()
    r.write(escrita)
    assert "'H'" in escrita.getvalue()


def test_unidade_sem_aspas_no_dataframe_e_no_filtro():
    m: MagicMock = mock_open(read_data="".join(MockModif))
    with patch("builtins.open", m):
        modif = Modif.read(ARQ_TESTE)
    assert set(modif.vmaxt(df=True)["unidade"]) == {"%"}
    filtrados = modif.vmaxt(unidade="%")
    assert isinstance(filtrados, list) and len(filtrados) > 0


def test_registros_do_manual_no_arquivo():
    m: MagicMock = mock_open(read_data="".join(MockModif_REGISTROS_MANUAL))
    with patch("builtins.open", m):
        ad = Modif.read(ARQ_TESTE)
    assert isinstance(ad.prodesp(), PRODESP)
    assert isinstance(ad.teif(), TEIF)
    assert isinstance(ad.ip(), IP)
    assert isinstance(ad.perdhidr(), PERDHIDR)
    assert isinstance(ad.numbas(), NUMBAS)
    assert len(ad.coefevap()) == 2
    assert ad.coefevap(mes=8).coeficiente == -10
    desvios = ad.cdesvio()
    assert [d.codigo_usina_jusante for d in desvios] == [66, 1]
    assert [d.limite_vazao for d in desvios] == [1500.5, None]
    assert ad.cdesvio(codigo_usina_jusante=1).limite_vazao is None

    bloco = ad.modificacoes_usina(1)
    assert [type(r) for r in bloco] == [
        PRODESP,
        TEIF,
        IP,
        PERDHIDR,
        COEFEVAP,
        COEFEVAP,
        NUMBAS,
        CDESVIO,
    ]
    assert [type(r) for r in ad.modificacoes_usina(2)] == [CDESVIO]


def test_registros_do_manual_dataframe():
    m: MagicMock = mock_open(read_data="".join(MockModif_REGISTROS_MANUAL))
    with patch("builtins.open", m):
        ad = Modif.read(ARQ_TESTE)
    acessores = {
        ad.prodesp: PRODESP,
        ad.teif: TEIF,
        ad.ip: IP,
        ad.perdhidr: PERDHIDR,
        ad.coefevap: COEFEVAP,
        ad.numbas: NUMBAS,
        ad.cdesvio: CDESVIO,
    }
    for acessor, tipo in acessores.items():
        registros = list(ad.data.of_type(tipo))
        df = acessor(df=True)
        assert list(df.columns) == registros[0].custom_properties, tipo
        assert len(df) == len(registros), tipo
    df = ad.cdesvio(df=True)
    assert df["codigo_usina_jusante"].tolist() == [66, 1]


def test_registros_do_manual_leitura_escrita():
    m_leitura: MagicMock = mock_open(
        read_data="".join(MockModif_REGISTROS_MANUAL)
    )
    with patch("builtins.open", m_leitura):
        cf1 = Modif.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.write(ARQ_TESTE)
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Modif.read(ARQ_TESTE)
    assert cf1 == cf2
    assert len(cf2.cdesvio()) == 2


def test_palavra_chave_minuscula_modif():
    linha_minuscula = MockCDESVIO.lower()
    m: MagicMock = mock_open(
        read_data="".join(MockModif_REGISTROS_MANUAL) + linha_minuscula
    )
    with patch("builtins.open", m):
        ad = Modif.read(ARQ_TESTE)
    assert len(ad.cdesvio()) == 2
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad.write(ARQ_TESTE)
    chamadas = m_escrita.mock_calls
    escritas = [chamadas[i].args[0] for i in range(1, len(chamadas) - 1)]
    assert linha_minuscula in escritas
