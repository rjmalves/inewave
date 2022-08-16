from inewave.newave.modelos.arquivos import BlocoNomesArquivos
from inewave.newave import Arquivos

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.arquivos import MockArquivos


def test_bloco_nomes_arquivos():

    m: MagicMock = mock_open(read_data="".join(MockArquivos))
    b = BlocoNomesArquivos()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 41
    assert b.data.shape[1] == 2
    assert b.data.iloc[0, 1] == "dger.dat"
    assert b.data.iloc[-1, 1] == "clasgas.dat"


def test_atributos_encontrados_arquivos():
    m: MagicMock = mock_open(read_data="".join(MockArquivos))
    with patch("builtins.open", m):
        ad = Arquivos.le_arquivo("")
        assert ad.dger is not None
        assert ad.sistema is not None
        assert ad.confhd is not None
        assert ad.modif is not None
        assert ad.conft is not None
        assert ad.term is not None
        assert ad.clast is not None
        assert ad.exph is not None
        assert ad.expt is not None
        assert ad.patamar is not None
        assert ad.cortes is not None
        assert ad.cortesh is not None
        assert ad.pmo is not None
        assert ad.parp is not None
        assert ad.forward is not None
        assert ad.forwardh is not None
        assert ad.shist is not None
        assert ad.manutt is not None
        assert ad.newdesp is not None
        assert ad.vazpast is not None
        assert ad.itaipu is not None
        assert ad.bid is not None
        assert ad.c_adic is not None
        assert ad.perda is not None
        assert ad.gtminpat is not None
        assert ad.elnino is not None
        assert ad.ensoaux is not None
        assert ad.dsvagua is not None
        assert ad.penalid is not None
        assert ad.curva is not None
        assert ad.agrint is not None
        assert ad.adterm is not None
        assert ad.ghmin is not None
        assert ad.sar is not None
        assert ad.cvar is not None
        assert ad.ree is not None
        assert ad.re is not None
        assert ad.tecno is not None
        assert ad.abertura is not None
        assert ad.gee is not None
        assert ad.clasgas is not None


def test_atributos_nao_encontrados_arquivos():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Arquivos.le_arquivo("")
        assert ad.dger is None
        assert ad.sistema is None
        assert ad.confhd is None
        assert ad.modif is None
        assert ad.conft is None
        assert ad.term is None
        assert ad.clast is None
        assert ad.exph is None
        assert ad.expt is None
        assert ad.patamar is None
        assert ad.cortes is None
        assert ad.cortesh is None
        assert ad.pmo is None
        assert ad.parp is None
        assert ad.forward is None
        assert ad.forwardh is None
        assert ad.shist is None
        assert ad.manutt is None
        assert ad.newdesp is None
        assert ad.vazpast is None
        assert ad.itaipu is None
        assert ad.bid is None
        assert ad.c_adic is None
        assert ad.perda is None
        assert ad.gtminpat is None
        assert ad.elnino is None
        assert ad.ensoaux is None
        assert ad.dsvagua is None
        assert ad.penalid is None
        assert ad.curva is None
        assert ad.agrint is None
        assert ad.adterm is None
        assert ad.ghmin is None
        assert ad.sar is None
        assert ad.cvar is None
        assert ad.ree is None
        assert ad.re is None
        assert ad.tecno is None
        assert ad.abertura is None
        assert ad.gee is None
        assert ad.clasgas is None


def test_eq_arquivos():
    m: MagicMock = mock_open(read_data="".join(MockArquivos))
    with patch("builtins.open", m):
        ad1 = Arquivos.le_arquivo("")
        ad2 = Arquivos.le_arquivo("")
        assert ad1 == ad2


def test_neq_arquivos():
    m: MagicMock = mock_open(read_data="".join(MockArquivos))
    with patch("builtins.open", m):
        ad1 = Arquivos.le_arquivo("")
        ad2 = Arquivos.le_arquivo("")
        ad2.dger = "teste"
        assert ad1 != ad2


def test_leitura_escrita_arquivos():
    m_leitura: MagicMock = mock_open(read_data="".join(MockArquivos))
    with patch("builtins.open", m_leitura):
        ad1 = Arquivos.le_arquivo("")
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(2, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ad2 = Arquivos.le_arquivo("")
        assert ad1 == ad2
