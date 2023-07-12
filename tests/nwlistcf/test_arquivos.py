from inewave.nwlistcf.modelos.arquivos import BlocoNomesArquivos
from inewave.nwlistcf import Arquivos

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.arquivos_nwlistcf import MockArquivos

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_nomes_arquivos():
    m: MagicMock = mock_open(read_data="".join(MockArquivos))
    b = BlocoNomesArquivos()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 15
    assert b.data.shape[1] == 2
    assert b.data.iloc[0, 1] == "nwlistcf.dat"
    assert b.data.iloc[-1, 1] == "vazaoxf.dat"


def test_atributos_encontrados_arquivos():
    m: MagicMock = mock_open(read_data="".join(MockArquivos))
    with patch("builtins.open", m):
        ad = Arquivos.read(ARQ_TESTE)
        assert ad.nwlistcf is not None
        assert ad.cortes is not None
        assert ad.cortesh is not None
        assert ad.newdesp is not None
        assert ad.cortese is not None
        assert ad.energiaf is not None
        assert ad.rsar is not None
        assert ad.rsarh is not None
        assert ad.rsari is not None
        assert ad.relatorio_cortes is not None
        assert ad.relatorio_estados is not None
        assert ad.relatorio_rsar is not None
        assert ad.energiaxf is not None
        assert ad.vazaof is not None
        assert ad.vazaoxf is not None


def test_atributos_nao_encontrados_arquivos():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Arquivos.read(ARQ_TESTE)
        assert ad.nwlistcf is None
        assert ad.cortes is None
        assert ad.cortesh is None
        assert ad.newdesp is None
        assert ad.cortese is None
        assert ad.energiaf is None
        assert ad.rsar is None
        assert ad.rsarh is None
        assert ad.rsari is None
        assert ad.relatorio_cortes is None
        assert ad.relatorio_estados is None
        assert ad.relatorio_rsar is None
        assert ad.energiaxf is None
        assert ad.vazaof is None
        assert ad.vazaoxf is None


def test_eq_arquivos():
    m: MagicMock = mock_open(read_data="".join(MockArquivos))
    with patch("builtins.open", m):
        ad1 = Arquivos.read(ARQ_TESTE)
        ad2 = Arquivos.read(ARQ_TESTE)
        assert ad1 == ad2


def test_neq_arquivos():
    m: MagicMock = mock_open(read_data="".join(MockArquivos))
    with patch("builtins.open", m):
        ad1 = Arquivos.read(ARQ_TESTE)
        ad2 = Arquivos.read(ARQ_TESTE)
        ad2.nwlistcf = "teste"
        assert ad1 != ad2


def test_leitura_escrita_arquivos():
    m_leitura: MagicMock = mock_open(read_data="".join(MockArquivos))
    with patch("builtins.open", m_leitura):
        ad1 = Arquivos.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ad2 = Arquivos.read(ARQ_TESTE)
        assert ad1 == ad2
