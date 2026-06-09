from io import BytesIO
from unittest.mock import MagicMock, patch

import pandas as pd  # type: ignore[import-untyped]
import pytest

from inewave.newave.hidr import Hidr
from inewave.newave.modelos.hidr import RegistroUHEHidr, RegistroUHEHidrF64
from tests.mocks.mock_open import mock_open

ARQ_TESTE = "./tests/mocks/arquivos/hidr.dat"
ARQ_TESTE_F64 = "./tests/mocks/arquivos/hidr_f64.dat"

NUM_REGISTROS = 320


def converte_arq_teste_para_f64() -> bytes:
    h = Hidr.read(ARQ_TESTE)
    h.converte_tamanho_registro("f64")
    buffer = BytesIO()
    h.write(buffer)
    return buffer.getvalue()


def test_registro_uhe_hidr():
    r = RegistroUHEHidr()
    with open(ARQ_TESTE, "rb") as fp:
        r.read(fp, storage="BINARY")

    assert len(r.data) == 111
    assert r.nome == "CAMARGOS"


def test_registro_uhe_hidr_f64():
    r = RegistroUHEHidrF64()
    with open(ARQ_TESTE_F64, "rb") as fp:
        r.read(fp, storage="BINARY")

    assert len(r.data) == 111
    assert r.nome == "CAMARGOS"
    assert r.posto == 1
    assert r.volume_minimo == pytest.approx(107.6, rel=1e-6)
    assert r.polinomio_volume_cota == pytest.approx(
        [893.0279, 0.06682515, -0.0001183834, 1.282643e-07, -5.560146e-11],
        rel=1e-12,
    )
    assert r.polinomio_cota_area == pytest.approx(
        [3211416.0, -10547.2, 11.54139, -0.004207735, 0.0],
        rel=1e-12,
        abs=1e-15,
    )
    assert r.canal_fuga_medio == pytest.approx(885.72906, rel=1e-6)
    assert r.data_referencia == "13-05-26"
    assert r.tipo_regulacao == "M"


def test_atributos_encontrados_hidr():
    h = Hidr.read(ARQ_TESTE)
    assert h.cadastro is not None


def test_atributos_encontrados_hidr_f64():
    h = Hidr.read(ARQ_TESTE_F64)
    assert h.cadastro is not None


def test_atributos_nao_encontrados_hidr():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Hidr.read(ARQ_TESTE)
        assert ad.cadastro is None


def test_atributos_nao_encontrados_hidr_f64():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Hidr.read(ARQ_TESTE_F64)
        assert ad.cadastro is None


def test_eq_hidr():
    h1 = Hidr.read(ARQ_TESTE)
    h2 = Hidr.read(ARQ_TESTE)
    assert h1 == h2


def test_eq_hidr_f64():
    h1 = Hidr.read(ARQ_TESTE_F64)
    h2 = Hidr.read(ARQ_TESTE_F64)
    assert h1 == h2


def test_neq_hidr():
    h1 = Hidr.read(ARQ_TESTE)
    h2 = Hidr.read(ARQ_TESTE)
    h2.cadastro.iloc[0, 0] = "TESTE"
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h2.write(ARQ_TESTE)
        assert h1 != h2


def test_neq_hidr_f64():
    h1 = Hidr.read(ARQ_TESTE_F64)
    h2 = Hidr.read(ARQ_TESTE_F64)
    h2.cadastro.iloc[0, 0] = "TESTE"
    h2.write(BytesIO())
    assert h1 != h2


def test_deteccao_formato_792():
    h = Hidr.read(ARQ_TESTE)
    assert h.tamanho_registro == RegistroUHEHidr.TAMANHO_REGISTRO


def test_deteccao_formato_832():
    h = Hidr.read(ARQ_TESTE_F64)
    assert h.tamanho_registro == RegistroUHEHidrF64.TAMANHO_REGISTRO
    assert len(h.cadastro) == NUM_REGISTROS


def test_leitura_com_versao_explicita():
    h32 = Hidr.read(ARQ_TESTE, version="f32")
    assert h32.tamanho_registro == RegistroUHEHidr.TAMANHO_REGISTRO
    h64 = Hidr.read(ARQ_TESTE_F64, version="f64")
    assert h64.tamanho_registro == RegistroUHEHidrF64.TAMANHO_REGISTRO


def test_escrita_mantem_formato_f64():
    h64 = Hidr.read(ARQ_TESTE_F64)
    buffer = BytesIO()
    h64.write(buffer)
    assert (
        len(buffer.getvalue())
        == NUM_REGISTROS * RegistroUHEHidrF64.TAMANHO_REGISTRO
    )


def test_conversao_para_f64():
    conteudo = converte_arq_teste_para_f64()
    assert len(conteudo) == NUM_REGISTROS * RegistroUHEHidrF64.TAMANHO_REGISTRO
    h32 = Hidr.read(ARQ_TESTE)
    h64 = Hidr.read(conteudo)
    assert h64.tamanho_registro == RegistroUHEHidrF64.TAMANHO_REGISTRO
    pd.testing.assert_frame_equal(h32.cadastro, h64.cadastro)


def test_conversao_para_f32():
    h64 = Hidr.read(ARQ_TESTE_F64)
    h32 = Hidr.read(ARQ_TESTE_F64)
    h32.converte_tamanho_registro("f32")
    buffer = BytesIO()
    h32.write(buffer)
    assert (
        len(buffer.getvalue())
        == NUM_REGISTROS * RegistroUHEHidr.TAMANHO_REGISTRO
    )
    relido = Hidr.read(buffer.getvalue())
    assert relido.tamanho_registro == RegistroUHEHidr.TAMANHO_REGISTRO
    # A conversão para f32 perde precisão nos coeficientes dos
    # polinômios, então a comparação é aproximada
    pd.testing.assert_frame_equal(
        h64.cadastro, relido.cadastro, check_exact=False, rtol=1e-6
    )


def test_conversao_ida_e_volta_preserva_valores():
    h1 = Hidr.read(ARQ_TESTE)
    h2 = Hidr.read(ARQ_TESTE)
    h2.converte_tamanho_registro("f64")
    h2.converte_tamanho_registro("f32")
    assert h2.tamanho_registro == RegistroUHEHidr.TAMANHO_REGISTRO
    assert h1 == h2


def test_conversao_precisao_invalida():
    h = Hidr.read(ARQ_TESTE)
    with pytest.raises(ValueError, match="Precisão inválida: 'f16'"):
        h.converte_tamanho_registro("f16")


def test_deteccao_formato_ambiguo():
    # 82368 bytes = 104 registros de 792 bytes = 99 registros de 832
    # bytes (mínimo múltiplo comum dos dois tamanhos)
    with open(ARQ_TESTE, "rb") as fp:
        conteudo = fp.read(82368)
    with pytest.warns(UserWarning, match="Não foi possível distinguir"):
        h = Hidr.read(conteudo)
    assert h.tamanho_registro == RegistroUHEHidr.TAMANHO_REGISTRO
    assert len(h.cadastro) == 104


def test_leitura_escrita_hidr():
    h1 = Hidr.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        h1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data=b"".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        h2 = Hidr.read(ARQ_TESTE)
        assert h1 == h2


def test_leitura_escrita_hidr_f64():
    h1 = Hidr.read(ARQ_TESTE_F64)
    buffer = BytesIO()
    h1.write(buffer)
    h2 = Hidr.read(buffer.getvalue())
    assert h2.tamanho_registro == RegistroUHEHidrF64.TAMANHO_REGISTRO
    assert h1 == h2
