from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.datetimefield import DatetimeField
from datetime import datetime

from typing import Optional


class HidreletricaCurvaJusante(Register):
    """ """

    IDENTIFIER = "HIDRELETRICA-CURVAJUSANTE"
    IDENTIFIER_DIGITS = 26
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            FloatField(decimal_digits=4),
        ],
        delimiter=";",
    )

    @property
    def codigo_usina(self) -> Optional[int]:
        """
        O código da usina hidrelétrica relacionada ao polinômio.

        :return: O código da usina
        :rtype: int | None
        """
        return self.data[0]

    @codigo_usina.setter
    def codigo_usina(self, c: int):
        self.data[0] = c

    @property
    def indice_familia(self) -> Optional[int]:
        """
        O índice da família de polinômios.

        :return: O índice (sequencial).
        :rtype: int | None
        """
        return self.data[1]

    @indice_familia.setter
    def indice_familia(self, c: int):
        self.data[1] = c

    @property
    def nivel_montante_referencia(self) -> Optional[float]:
        """
        O nível de montante da usina de jusante
        de referência.

        :return: O nível em metros
        :rtype: float | None
        """
        return self.data[2]

    @nivel_montante_referencia.setter
    def nivel_montante_referencia(self, c: float):
        self.data[2] = c


class HidreletricaCurvaJusantePolinomioPorPartes(Register):
    """ """

    IDENTIFIER = "HIDRELETRICA-CURVAJUSANTE-POLINOMIOPORPARTES"
    IDENTIFIER_DIGITS = 45
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_usina(self) -> Optional[int]:
        """
        O código da usina hidrelétrica relacionada ao polinômio.

        :return: O código da usina
        :rtype: int | None
        """
        return self.data[0]

    @codigo_usina.setter
    def codigo_usina(self, c: int):
        self.data[0] = c

    @property
    def indice_familia(self) -> Optional[int]:
        """
        O índice da família de polinômios.

        :return: O índice (sequencial).
        :rtype: int | None
        """
        return self.data[1]

    @indice_familia.setter
    def indice_familia(self, c: int):
        self.data[1] = c

    @property
    def numero_polinomios(self) -> Optional[int]:
        """
        O número de polinômios existentes na família.

        :return: O número de polinômios
        :rtype: int | None
        """
        return self.data[2]

    @numero_polinomios.setter
    def numero_polinomios(self, c: int):
        self.data[2] = c


class HidreletricaCurvaJusantePolinomioPorPartesSegmento(Register):
    """ """

    IDENTIFIER = "HIDRELETRICA-CURVAJUSANTE-POLINOMIOPORPARTES-SEGMENTO"
    IDENTIFIER_DIGITS = 54
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            IntegerField(),
            FloatField(size=24, decimal_digits=3),
            FloatField(size=24, decimal_digits=3),
            FloatField(size=24, decimal_digits=14, format="E"),
            FloatField(size=24, decimal_digits=14, format="E"),
            FloatField(size=24, decimal_digits=14, format="E"),
            FloatField(size=24, decimal_digits=14, format="E"),
            FloatField(size=24, decimal_digits=14, format="E"),
        ],
        delimiter=";",
    )

    @property
    def codigo_usina(self) -> Optional[int]:
        """
        O código da usina hidrelétrica relacionada ao polinômio.

        :return: O código da usina
        :rtype: int | None
        """
        return self.data[0]

    @codigo_usina.setter
    def codigo_usina(self, c: int):
        self.data[0] = c

    @property
    def indice_familia(self) -> Optional[int]:
        """
        O índice da família de polinômios.

        :return: O índice (sequencial).
        :rtype: int | None
        """
        return self.data[1]

    @indice_familia.setter
    def indice_familia(self, c: int):
        self.data[1] = c

    @property
    def indice_polinomio(self) -> Optional[int]:
        """
        O índice do polinômio da respectiva família.

        :return: O índice do polinômio
        :rtype: int | None
        """
        return self.data[2]

    @indice_polinomio.setter
    def indice_polinomio(self, c: int):
        self.data[2] = c

    @property
    def limite_inferior_vazao_jusante(self) -> Optional[float]:
        """
        O limite inferior de vazão de jusante (defluência mais lateral)
        para janela de validade do polinômio.

        :return: O limite inferior de vazão de jusante
        :rtype: float | None
        """
        return self.data[3]

    @limite_inferior_vazao_jusante.setter
    def limite_inferior_vazao_jusante(self, c: float):
        self.data[3] = c

    @property
    def limite_superior_vazao_jusante(self) -> Optional[float]:
        """
        O limite superior de vazão de jusante (defluência mais lateral)
        para janela de validade do polinômio.

        :return: O limite superior de vazão de jusante
        :rtype: float | None
        """
        return self.data[4]

    @limite_superior_vazao_jusante.setter
    def limite_superior_vazao_jusante(self, c: float):
        self.data[4] = c

    @property
    def coeficiente_a0(self) -> Optional[float]:
        """
        O coeficiente de grau 0 do polinômio.

        :return: O coeficiente de grau 0 do polinômio
        :rtype: float | None
        """
        return self.data[5]

    @coeficiente_a0.setter
    def coeficiente_a0(self, c: float):
        self.data[5] = c

    @property
    def coeficiente_a1(self) -> Optional[float]:
        """
        O coeficiente de grau 1 do polinômio.

        :return: O coeficiente de grau 1 do polinômio
        :rtype: float | None
        """
        return self.data[6]

    @coeficiente_a1.setter
    def coeficiente_a1(self, c: float):
        self.data[6] = c

    @property
    def coeficiente_a2(self) -> Optional[float]:
        """
        O coeficiente de grau 2 do polinômio.

        :return: O coeficiente de grau 2 do polinômio
        :rtype: float | None
        """
        return self.data[7]

    @coeficiente_a2.setter
    def coeficiente_a2(self, c: float):
        self.data[7] = c

    @property
    def coeficiente_a3(self) -> Optional[float]:
        """
        O coeficiente de grau 3 do polinômio.

        :return: O coeficiente de grau 3 do polinômio
        :rtype: float | None
        """
        return self.data[8]

    @coeficiente_a3.setter
    def coeficiente_a3(self, c: float):
        self.data[8] = c

    @property
    def coeficiente_a4(self) -> Optional[float]:
        """
        O coeficiente de grau 4 do polinômio.

        :return: O coeficiente de grau 4 do polinômio
        :rtype: float | None
        """
        return self.data[9]

    @coeficiente_a4.setter
    def coeficiente_a4(self, c: float):
        self.data[9] = c


class HidreletricaCurvaJusanteAfogamentoExplicitoUsina(Register):
    """ """

    IDENTIFIER = "HIDRELETRICA-CURVAJUSANTE-AFOGAMENTO-EXPLICITO-USINA"
    IDENTIFIER_DIGITS = 53
    LINE = Line(
        [
            IntegerField(),
            LiteralField(size=3),
        ],
        delimiter=";",
    )

    @property
    def codigo_usina(self) -> Optional[int]:
        """
        O código da usina hidrelétrica relacionada ao polinômio.

        :return: O código da usina
        :rtype: int | None
        """
        return self.data[0]

    @codigo_usina.setter
    def codigo_usina(self, c: int):
        self.data[0] = c

    @property
    def considera_afogamento(self) -> Optional[str]:
        """
        Habilitação do afogamento explícito.

        :return: O flag da habilitação.
        :rtype: str | None
        """
        return self.data[1]

    @considera_afogamento.setter
    def considera_afogamento(self, c: str):
        self.data[1] = c


class HidreletricaCurvaJusanteAfogamentoExplicitoPadrao(Register):
    """ """

    IDENTIFIER = "HIDRELETRICA-CURVAJUSANTE-AFOGAMENTO-EXPLICITO-PADRAO"
    IDENTIFIER_DIGITS = 54
    LINE = Line(
        [
            LiteralField(size=3),
        ],
        delimiter=";",
    )

    @property
    def considera_afogamento(self) -> Optional[str]:
        """
        Habilitação do afogamento explícito.

        :return: O flag da habilitação.
        :rtype: str | None
        """
        return self.data[0]

    @considera_afogamento.setter
    def considera_afogamento(self, c: str):
        self.data[0] = c


class HidreletricaProdutibilidadeEspecificaGrade(Register):
    """ """

    IDENTIFIER = "HIDRELETRICA-PRODUTIBILIDADE-ESPECIFICA-GRADE"
    IDENTIFIER_DIGITS = 46
    LINE = Line(
        [
            IntegerField(),
            FloatField(size=15, decimal_digits=1),
            FloatField(size=15, decimal_digits=1),
            FloatField(size=15, decimal_digits=6),
        ],
        delimiter=";",
    )

    @property
    def codigo_usina(self) -> Optional[int]:
        """
        O código da usina

        :return: O código da usina
        :rtype: int | None
        """
        return self.data[0]

    @codigo_usina.setter
    def codigo_usina(self, c: int):
        self.data[0] = c

    @property
    def altura_queda_liquida(self) -> Optional[float]:
        """
        A altura de queda líquida relativa à produbilidade.

        :return: A altura (m)
        :rtype: float | None
        """
        return self.data[1]

    @altura_queda_liquida.setter
    def altura_queda_liquida(self, c: float):
        self.data[1] = c

    @property
    def turbinamento(self) -> Optional[float]:
        """
        O turbinamento relativo à produtibilidade.

        :return: O turbinamento (m^3/s)
        :rtype: float | None
        """
        return self.data[2]

    @turbinamento.setter
    def turbinamento(self, c: float):
        self.data[2] = c

    @property
    def produtibilidade_especifica(self) -> Optional[float]:
        """
        A produtibilidade específica da usina.

        :return: A produtibilidade em MW / (m^3/s / m)
        :rtype: float | None
        """
        return self.data[3]

    @produtibilidade_especifica.setter
    def produtibilidade_especifica(self, c: float):
        self.data[3] = c


class HidreletricaPerdaHidraulicaGrade(Register):
    """ """

    IDENTIFIER = "HIDRELETRICA-PERDA-HIDRAULICA-GRADE"
    IDENTIFIER_DIGITS = 36
    LINE = Line(
        [
            IntegerField(),
            FloatField(size=15, decimal_digits=1),
            FloatField(size=15, decimal_digits=1),
        ],
        delimiter=";",
    )

    @property
    def codigo_usina(self) -> Optional[int]:
        """
        O código da usina

        :return: O código da usina
        :rtype: int | None
        """
        return self.data[0]

    @codigo_usina.setter
    def codigo_usina(self, c: int):
        self.data[0] = c

    @property
    def turbinamento(self) -> Optional[float]:
        """
        O turbinamento relativo à produtibilidade.

        :return: O turbinamento (m^3/s)
        :rtype: float | None
        """
        return self.data[1]

    @turbinamento.setter
    def turbinamento(self, c: float):
        self.data[1] = c

    @property
    def perda_hidraulica(self) -> Optional[float]:
        """
        A perda hidráulica em valores absolutos

        :return: A perda (m)
        :rtype: float | None
        """
        return self.data[2]

    @perda_hidraulica.setter
    def perda_hidraulica(self, c: float):
        self.data[2] = c


class EstacaoBombeamento(Register):
    """ """

    IDENTIFIER = "ESTACAO-BOMBEAMENTO"
    IDENTIFIER_DIGITS = 20
    LINE = Line(
        [
            IntegerField(),
            LiteralField(size=30),
            IntegerField(),
            IntegerField(),
            FloatField(size=15, decimal_digits=2),
            FloatField(size=8, decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_estacao(self) -> Optional[int]:
        """
        O código da estação

        :return: O código da estação
        :rtype: int | None
        """
        return self.data[0]

    @codigo_estacao.setter
    def codigo_estacao(self, c: int):
        self.data[0] = c

    @property
    def nome_estacao(self) -> Optional[str]:
        """
        O nome da estação de bomeamento

        :return: O nome como string.
        :rtype: str | None
        """
        return self.data[1]

    @nome_estacao.setter
    def nome_estacao(self, c: str):
        self.data[1] = c

    @property
    def codigo_usina_origem(self) -> Optional[int]:
        """
        O código da usina de origem da estação.

        :return: O código da usina
        :rtype: int | None
        """
        return self.data[2]

    @codigo_usina_origem.setter
    def codigo_usina_origem(self, c: int):
        self.data[2] = c

    @property
    def codigo_usina_destino(self) -> Optional[int]:
        """
        O código da usina de destino da estação.

        :return: O código da usina
        :rtype: int | None
        """
        return self.data[3]

    @codigo_usina_destino.setter
    def codigo_usina_destino(self, c: int):
        self.data[3] = c

    @property
    def consumo_estacao(self) -> Optional[float]:
        """
        O consumo da estação de bomeamento

        :return: O consumo
        :rtype: float | None
        """
        return self.data[4]

    @consumo_estacao.setter
    def consumo_estacao(self, c: float):
        self.data[4] = c

    @property
    def bombeamento_maximo(self) -> Optional[float]:
        """
        O limite de capacidade de bombeamento da estação

        :return: O limite máximo
        :rtype: float | None
        """
        return self.data[5]

    @bombeamento_maximo.setter
    def bombeamento_maximo(self, c: float):
        self.data[5] = c


class EstacaoBombeamentoLimitesPeriodoPatamar(Register):
    """
    Registro que contém os limites de bombeamento de cada
    estação por período e patamar.
    """

    IDENTIFIER = "ESTACAO-BOMBEAMENTO-LIMITES-PERIODO-PATAMAR"
    IDENTIFIER_DIGITS = 44
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            FloatField(size=16, decimal_digits=4, format="e"),
            FloatField(size=16, decimal_digits=4, format="e"),
        ],
        delimiter=";",
    )

    @property
    def codigo_estacao(self) -> Optional[int]:
        """
        O código da estação.

        :return: O código
        :rtype:  int | None
        """
        return self.data[0]

    @codigo_estacao.setter
    def codigo_estacao(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade dos limites da estação.

        :return: A data
        :rtype: datetime | None
        """
        return self.data[1]

    @data_inicio.setter
    def data_inicio(self, c: datetime):
        self.data[1] = c

    @property
    def data_fim(self) -> Optional[datetime]:
        """
        A data de fim da validade dos limites da estação.

        :return: A data
        :rtype: datetime | None
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, v: datetime):
        self.data[2] = v

    @property
    def patamar(self) -> Optional[int]:
        """
        O índice do patamar de validade dos limites.

        :return: O patamar
        :rtype: int | None
        """
        return self.data[3]

    @patamar.setter
    def patamar(self, v: int):
        self.data[3] = v

    @property
    def limite_inferior(self) -> Optional[float]:
        """
        O limite inferior para a estação.

        :return: O limite inferior
        :rtype: float | None
        """
        return self.data[4]

    @limite_inferior.setter
    def limite_inferior(self, v: float):
        self.data[4] = v

    @property
    def limite_superior(self) -> Optional[float]:
        """
        O limite superior para a estação.

        :return: O limite superior
        :rtype: float | None
        """
        return self.data[5]

    @limite_superior.setter
    def limite_superior(self, v: float):
        self.data[5] = v


class EstacaoBombeamentoSubmercado(Register):
    """ """

    IDENTIFIER = "ESTACAO-BOMBEAMENTO-SUBMERCADO"
    IDENTIFIER_DIGITS = 31
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_estacao(self) -> Optional[int]:
        """
        O código da estação

        :return: O código da estação
        :rtype: int | None
        """
        return self.data[0]

    @codigo_estacao.setter
    def codigo_estacao(self, c: int):
        self.data[0] = c

    @property
    def codigo_submercado(self) -> Optional[int]:
        """
        O código do submercado da estação

        :return: O código do submercado
        :rtype: int | None
        """
        return self.data[1]

    @codigo_submercado.setter
    def codigo_submercado(self, c: int):
        self.data[1] = c


class VolumeReferencialTipoPadrao(Register):
    """ """

    IDENTIFIER = "VOLUME-REFERENCIAL-TIPO-PADRAO"
    IDENTIFIER_DIGITS = 30
    LINE = Line(
        [
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def tipo_referencia(self) -> Optional[int]:
        """
        O tipo de volume de referência adotado.

        :return: O tipo de volume
        :rtype: int | None
        """
        return self.data[0]

    @tipo_referencia.setter
    def tipo_referencia(self, c: int):
        self.data[0] = c


class VolumeReferencialPeriodo(Register):
    """ """

    IDENTIFIER = "CADH-VOL-REF-PER"
    IDENTIFIER_DIGITS = 16
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(size=15, decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_usina(self) -> Optional[int]:
        """
        O código da usina

        :return: O código
        :rtype: int | None
        """
        return self.data[0]

    @codigo_usina.setter
    def codigo_usina(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade do volume de referência.

        :return: A data
        :rtype: datetime | None
        """
        return self.data[1]

    @data_inicio.setter
    def data_inicio(self, c: datetime):
        self.data[1] = c

    @property
    def data_fim(self) -> Optional[datetime]:
        """
        A data de fim da validade do volume de referência.

        :return: A data
        :rtype: datetime | None
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, v: datetime):
        self.data[2] = v

    @property
    def volume_referencia(self) -> Optional[float]:
        """
        O volume de referência da usina.

        :return: O volume
        :rtype: float | None
        """
        return self.data[3]

    @volume_referencia.setter
    def volume_referencia(self, c: float):
        self.data[3] = c
