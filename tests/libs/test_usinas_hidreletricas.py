from inewave.libs.usinas_hidreletricas import UsinasHidreletricas
from inewave.libs.usinas_hidreletricas import (
    HidreletricaCurvaJusante,
    HidreletricaCurvaJusantePolinomioPorPartes,
    HidreletricaCurvaJusantePolinomioPorPartesSegmento,
    HidreletricaCurvaJusanteAfogamentoExplicitoUsina,
    HidreletricaCurvaJusanteAfogamentoExplicitoPadrao,
    HidreletricaProdutibilidadeEspecificaGrade,
    HidreletricaPerdaHidraulicaGrade,
    EstacaoBombeamento,
    EstacaoBombeamentoLimitesPeriodoPatamar,
    EstacaoBombeamentoSubmercado,
    VolumeReferencialTipoPadrao,
    VolumeReferencialPeriodo,
)
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch
from datetime import datetime
from tests.mocks.arquivos.usinas_hidreletricas import (
    MockHidreletricaCurvaJusante,
    MockHidreletricaCurvaJusantePolinomio,
    MockHidreletricaCurvaJusantePolinomioSegmento,
    MockHidreletricaCurvaJusanteAfogamentoExplicitoUsina,
    MockHidreletricaCurvaJusanteAfogamentoExplicitoPadrao,
    MockHidreletricaProdutibilidadeEspecificaGrade,
    MockHidreletricaPerdaHidraulicaGrade,
    MockEstacaoBombeamento,
    MockEstacaoBombeamentoLimitesPeriodoPatamar,
    MockEstacaoBombeamentoSubmercado,
    MockVolumeReferencialPadrao,
    MockVolumeReferencialPeriodo,
    MockUsinasHidreletricas,
)

ARQ_TESTE = "./tests/__init__.py"


def test_df_hidreletrica_curvajusante():
    m: MagicMock = mock_open(read_data="".join(MockHidreletricaCurvaJusante))
    with patch("builtins.open", m):
        polinjus = UsinasHidreletricas.read(ARQ_TESTE)
        df_curvajusante = polinjus.hidreletrica_curvajusante(df=True)
        assert df_curvajusante.at[0, "codigo_usina"] == 1
        assert df_curvajusante.at[0, "indice_familia"] == 1
        assert df_curvajusante.at[0, "nivel_montante_referencia"] == 885.3052


def test_registro_hidreletrica_curvajusante():
    m: MagicMock = mock_open(read_data="".join(MockHidreletricaCurvaJusante))
    r = HidreletricaCurvaJusante()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1, 885.3052]
    assert r.codigo_usina == 1
    r.codigo_usina = 0
    assert r.codigo_usina == 0
    assert r.indice_familia == 1
    r.indice_familia = 0
    assert r.indice_familia == 0
    assert r.nivel_montante_referencia == 885.3052
    r.nivel_montante_referencia = 0
    assert r.nivel_montante_referencia == 0


def test_df_hidreletrica_curvajusante_polinomio():
    m: MagicMock = mock_open(
        read_data="".join(MockHidreletricaCurvaJusantePolinomio)
    )
    with patch("builtins.open", m):
        polinjus = UsinasHidreletricas.read(ARQ_TESTE)
        df_curvajusante_polinomio = (
            polinjus.hidreletrica_curvajusante_polinomio(df=True)
        )
        assert df_curvajusante_polinomio.at[0, "codigo_usina"] == 1
        assert df_curvajusante_polinomio.at[0, "indice_familia"] == 1
        assert df_curvajusante_polinomio.at[0, "numero_polinomios"] == 2


def test_registro_hidreletrica_curvajusante_polinomio():
    m: MagicMock = mock_open(
        read_data="".join(MockHidreletricaCurvaJusantePolinomio)
    )
    r = HidreletricaCurvaJusantePolinomioPorPartes()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1, 2]
    assert r.codigo_usina == 1
    r.codigo_usina = 0
    assert r.codigo_usina == 0
    assert r.indice_familia == 1
    r.indice_familia = 0
    assert r.indice_familia == 0
    assert r.numero_polinomios == 2
    r.numero_polinomios = 0
    assert r.numero_polinomios == 0


def test_df_hidreletrica_curvajusante_polinomio_segmento():
    m: MagicMock = mock_open(
        read_data="".join(MockHidreletricaCurvaJusantePolinomioSegmento)
    )
    with patch("builtins.open", m):
        polinjus = UsinasHidreletricas.read(ARQ_TESTE)
        df_curvajusante_polinomio_segmento = (
            polinjus.hidreletrica_curvajusante_polinomio_segmento(df=True)
        )
        assert df_curvajusante_polinomio_segmento.at[0, "codigo_usina"] == 1
        assert df_curvajusante_polinomio_segmento.at[0, "indice_familia"] == 1
        assert (
            df_curvajusante_polinomio_segmento.at[0, "indice_polinomio"] == 1
        )
        assert (
            df_curvajusante_polinomio_segmento.at[
                0, "limite_inferior_vazao_jusante"
            ]
            == 0.0
        )
        assert (
            df_curvajusante_polinomio_segmento.at[
                0, "limite_superior_vazao_jusante"
            ]
            == 408.6490
        )
        assert (
            df_curvajusante_polinomio_segmento.at[0, "coeficiente_a0"]
            == 885.3052
        )
        assert (
            round(
                df_curvajusante_polinomio_segmento.at[0, "coeficiente_a1"], 4
            )
            == 0.0000
        )
        assert (
            round(
                df_curvajusante_polinomio_segmento.at[0, "coeficiente_a2"], 4
            )
            == 0.0000
        )
        assert (
            round(
                df_curvajusante_polinomio_segmento.at[0, "coeficiente_a3"], 4
            )
            == 0.0000
        )
        assert (
            round(
                df_curvajusante_polinomio_segmento.at[0, "coeficiente_a4"], 4
            )
            == 0.0000
        )


def test_registro_hidreletrica_curvajusante_polinomio_segmento():
    m: MagicMock = mock_open(
        read_data="".join(MockHidreletricaCurvaJusantePolinomioSegmento)
    )
    r = HidreletricaCurvaJusantePolinomioPorPartesSegmento()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        1,
        1,
        0,
        408.649,
        0.88530520000000e03,
        -0.31521360000000e-17,
        0.19686530000000e-04,
        -0.25518040000000e-07,
        0.00000000000000e01,
    ]
    assert r.codigo_usina == 1
    r.codigo_usina = 0
    assert r.codigo_usina == 0
    assert r.indice_familia == 1
    r.indice_familia = 0
    assert r.indice_familia == 0
    assert r.indice_polinomio == 1
    r.indice_polinomio = 0
    assert r.indice_polinomio == 0
    assert r.limite_inferior_vazao_jusante == 0
    r.limite_inferior_vazao_jusante = -1
    assert r.limite_inferior_vazao_jusante == -1
    assert r.limite_superior_vazao_jusante == 408.649
    r.limite_superior_vazao_jusante = -1
    assert r.limite_superior_vazao_jusante == -1

    assert r.coeficiente_a0 == 0.88530520000000e03
    r.coeficiente_a0 = -1
    assert r.coeficiente_a0 == -1
    assert r.coeficiente_a1 == -0.31521360000000e-17
    r.coeficiente_a1 = -1
    assert r.coeficiente_a1 == -1
    assert r.coeficiente_a2 == 0.19686530000000e-04
    r.coeficiente_a2 = -1
    assert r.coeficiente_a2 == -1
    assert r.coeficiente_a3 == -0.25518040000000e-07
    r.coeficiente_a3 = -1
    assert r.coeficiente_a3 == -1
    assert r.coeficiente_a4 == 0.00000000000000e01
    r.coeficiente_a4 = -1
    assert r.coeficiente_a4 == -1


def test_df_polinjus_hidreletrica_curvajusante_afogamentoexplicito_usina():
    m: MagicMock = mock_open(read_data="".join(MockUsinasHidreletricas))
    with patch("builtins.open", m):
        polinjus = UsinasHidreletricas.read(ARQ_TESTE)
        df_curvajusante_afogamentoexplicito_usina = (
            polinjus.hidreletrica_curvajusante_afogamentoexplicito_usina(
                df=True
            )
        )
        assert (
            df_curvajusante_afogamentoexplicito_usina.at[2, "codigo_usina"]
            == 54
        )
        assert (
            df_curvajusante_afogamentoexplicito_usina.at[
                2, "considera_afogamento"
            ]
            == "nao"
        )


def test_registro_polinjus_hidreletrica_curvajusante_afogamentoexplicito_usina():
    m: MagicMock = mock_open(
        read_data="".join(MockHidreletricaCurvaJusanteAfogamentoExplicitoUsina)
    )
    r = HidreletricaCurvaJusanteAfogamentoExplicitoUsina()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [22, "sim"]
    assert r.codigo_usina == 22
    r.codigo_usina = 0
    assert r.codigo_usina == 0
    assert r.considera_afogamento == "sim"
    r.considera_afogamento = "nao"
    assert r.considera_afogamento == "nao"


def test_registro_polinjus_hidreletrica_curvajusante_afogamentoexplicito_padrao():
    m: MagicMock = mock_open(
        read_data="".join(
            MockHidreletricaCurvaJusanteAfogamentoExplicitoPadrao
        )
    )
    r = HidreletricaCurvaJusanteAfogamentoExplicitoPadrao()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == ["nao"]
    assert r.considera_afogamento == "nao"
    r.considera_afogamento = "sim"
    assert r.considera_afogamento == "sim"


def test_registro_hidreletrica_produtibilidade_especifica_grade():
    m: MagicMock = mock_open(
        read_data="".join(MockHidreletricaProdutibilidadeEspecificaGrade)
    )
    r = HidreletricaProdutibilidadeEspecificaGrade()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [7, 0, 10, 0.012345]
    assert r.codigo_usina == 7
    r.codigo_usina = 2
    assert r.codigo_usina == 2
    assert r.altura_queda_liquida == 0.0
    r.altura_queda_liquida = 1.0
    assert r.altura_queda_liquida == 1.0
    assert r.turbinamento == 10.0
    r.turbinamento = 1.0
    assert r.turbinamento == 1.0
    assert r.produtibilidade_especifica == 0.012345
    r.produtibilidade_especifica = 1.5
    assert r.produtibilidade_especifica == 1.5


def test_registro_hidreletrica_perda_hidraulica_grade():
    m: MagicMock = mock_open(
        read_data="".join(MockHidreletricaPerdaHidraulicaGrade)
    )
    r = HidreletricaPerdaHidraulicaGrade()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 10.0, 1.0]
    assert r.codigo_usina == 1
    r.codigo_usina = 2
    assert r.codigo_usina == 2
    assert r.turbinamento == 10.0
    r.turbinamento = 1.0
    assert r.turbinamento == 1.0
    assert r.perda_hidraulica == 1.0
    r.perda_hidraulica = 1.5
    assert r.perda_hidraulica == 1.5


def test_registro_estacao_bombeamento():
    m: MagicMock = mock_open(read_data="".join(MockEstacaoBombeamento))
    r = EstacaoBombeamento()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "Sta Cecilia", 125, 181, 0.20, 181]
    assert r.codigo_estacao == 1
    r.codigo_estacao = 2
    assert r.codigo_estacao == 2
    assert r.nome_estacao == "Sta Cecilia"
    r.nome_estacao = "Sto Cecilia"
    assert r.nome_estacao == "Sto Cecilia"
    assert r.codigo_usina_origem == 125
    r.codigo_usina_origem = 124
    assert r.codigo_usina_origem == 124
    assert r.codigo_usina_destino == 181
    r.codigo_usina_destino = 180
    assert r.codigo_usina_destino == 180
    assert r.consumo_estacao == 0.2
    r.consumo_estacao = 0.5
    assert r.consumo_estacao == 0.5
    assert r.bombeamento_maximo == 181
    r.bombeamento_maximo = 180
    assert r.bombeamento_maximo == 180


def test_registro_estacao_bombeamento_limites_periodo_patamar():
    m: MagicMock = mock_open(
        read_data="".join(MockEstacaoBombeamentoLimitesPeriodoPatamar)
    )
    r = EstacaoBombeamentoLimitesPeriodoPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(2023, 3, 1), None, 1, 0, 181]
    assert r.codigo_estacao == 1
    r.codigo_estacao = 2
    assert r.codigo_estacao == 2
    assert r.data_inicio == datetime(2023, 3, 1)
    r.data_inicio = datetime(2023, 2, 1)
    assert r.data_inicio == datetime(2023, 2, 1)
    assert r.data_fim is None
    r.data_fim = datetime(2023, 3, 2)
    assert r.data_fim == datetime(2023, 3, 2)
    assert r.patamar == 1
    r.patamar = 3
    assert r.patamar == 3
    assert r.limite_inferior == 0
    r.limite_inferior = 3
    assert r.limite_inferior == 3
    assert r.limite_superior == 181
    r.limite_superior = 151
    assert r.limite_superior == 151


def test_registro_estacao_bombeamento_submercado():
    m: MagicMock = mock_open(
        read_data="".join(MockEstacaoBombeamentoSubmercado)
    )
    r = EstacaoBombeamentoSubmercado()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1]
    assert r.codigo_estacao == 1
    r.codigo_estacao = 2
    assert r.codigo_estacao == 2
    assert r.codigo_submercado == 1
    r.codigo_submercado = 2
    assert r.codigo_submercado == 2


def test_registro_volume_referencial_tipo_padrao():
    m: MagicMock = mock_open(read_data="".join(MockVolumeReferencialPadrao))
    r = VolumeReferencialTipoPadrao()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1]
    assert r.tipo_referencia == 1
    r.tipo_referencia = 2
    assert r.tipo_referencia == 2


def test_registro_volume_referencial_periodo():
    m: MagicMock = mock_open(read_data="".join(MockVolumeReferencialPeriodo))
    r = VolumeReferencialPeriodo()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [4, datetime(2023, 4, 1), None, 266.0]
    assert r.codigo_usina == 4
    r.codigo_usina = 5
    assert r.codigo_usina == 5
    assert r.data_inicio == datetime(2023, 4, 1)
    r.data_inicio = datetime(2023, 5, 1)
    assert r.data_inicio == datetime(2023, 5, 1)
    assert r.data_fim is None
    r.data_fim = datetime(2023, 6, 1)
    assert r.data_fim == datetime(2023, 6, 1)
    assert r.volume_referencia == 266.0
    r.volume_referencia = 0.0
    assert r.volume_referencia == 0.0


def test_atributos_encontrados():
    m: MagicMock = mock_open(read_data="".join(MockUsinasHidreletricas))
    with patch("builtins.open", m):
        uhes = UsinasHidreletricas.read(ARQ_TESTE)
        assert uhes.hidreletrica_curvajusante() is not None
        assert uhes.hidreletrica_curvajusante_polinomio() is not None
        assert uhes.hidreletrica_curvajusante_polinomio_segmento() is not None
        assert (
            uhes.hidreletrica_curvajusante_afogamentoexplicito_usina()
            is not None
        )
        assert (
            uhes.hidreletrica_curvajusante_afogamentoexplicito_padrao()
            is not None
        )
        assert uhes.hidreletrica_produtibilidade_especifica_grade() is not None
        assert uhes.hidreletrica_perda_hidraulica_grade() is not None
        assert uhes.estacao_bombeamento() is not None
        assert uhes.estacao_bombeamento_limites_periodo_patamar() is not None
        assert uhes.estacao_bombeamento_submercado() is not None
        assert uhes.volume_referencial_tipo_padrao() is not None
        assert uhes.volume_referencial_periodo() is not None


def test_eq():
    m: MagicMock = mock_open(read_data="".join(MockUsinasHidreletricas))
    with patch("builtins.open", m):
        log1 = UsinasHidreletricas.read(ARQ_TESTE)
        log2 = UsinasHidreletricas.read(ARQ_TESTE)
        assert log1 == log2


def test_neq():
    m: MagicMock = mock_open(read_data="".join(MockUsinasHidreletricas))
    with patch("builtins.open", m):
        log1 = UsinasHidreletricas.read(ARQ_TESTE)
        log2 = UsinasHidreletricas.read(ARQ_TESTE)
        log1.hidreletrica_curvajusante_polinomio_segmento()[
            0
        ].codigo_usina = -1
        assert log1 != log2


def test_leitura_escrita_usinas_hidreletricas():
    m_leitura: MagicMock = mock_open(
        read_data="".join(MockUsinasHidreletricas)
    )
    with patch("builtins.open", m_leitura):
        cf1 = UsinasHidreletricas.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
        for li in linhas_escritas:
            print(li)
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = UsinasHidreletricas.read(ARQ_TESTE)
        assert cf1 == cf2
