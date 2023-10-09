from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from datetime import datetime


class RegistroPEECadastro(Register):
    """
    Registro que contém um cadastro de um parque eólico equivalente.
    """

    IDENTIFIER = "PEE-CAD"
    IDENTIFIER_DIGITS = 7
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def nome_pee(self) -> Optional[str]:
        return self.data[1]

    @nome_pee.setter
    def nome_pee(self, n: str):
        self.data[1] = n


class RegistroPEEPotenciaInstaladaPeriodo(Register):
    """
    Registro que contém a informação de início e fim de
    operação para uma certa potência instalada de um parque
    eólico equivalente.
    """

    IDENTIFIER = "PEE-POT-INST-PER"
    IDENTIFIER_DIGITS = 16
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=3),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        """
        O código do PEE.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def periodo_inicial(self) -> Optional[datetime]:
        """
        A data de início para a validade da potência instalada.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[1]

    @periodo_inicial.setter
    def periodo_inicial(self, p: datetime):
        self.data[1] = p

    @property
    def periodo_final(self) -> Optional[datetime]:
        """
        A data de fim para a validade da potência instalada.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @periodo_final.setter
    def periodo_final(self, p: datetime):
        self.data[2] = p

    @property
    def potencia_instalada(self) -> Optional[float]:
        return self.data[3]

    @potencia_instalada.setter
    def potencia_instalada(self, n: float):
        self.data[3] = n


class RegistroPEEConfiguracaoPeriodo(Register):
    """
    Registro que contém um estado de operação de um PEE por
    período.
    """

    IDENTIFIER = "PEE-CONFIG-PER"
    IDENTIFIER_DIGITS = 14
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        """
        O código do PEE.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início para a validade do estado de operação.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[1]

    @data_inicio.setter
    def data_inicio(self, n: datetime):
        self.data[1] = n

    @property
    def data_fim(self) -> Optional[datetime]:
        """
        A data de fim para a validade do estado de operação.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, n: datetime):
        self.data[2] = n

    @property
    def estado_operacao(self) -> Optional[str]:
        """
        O estado de operação.

        :return: O estado
        :rtype: Optional[str]
        """
        return self.data[3]

    @estado_operacao.setter
    def estado_operacao(self, n: str):
        self.data[3] = n


class RegistroPEEFTE(Register):
    """
    Registro que contém as informações da função de produção
    linear vento-potência para um PEE.
    """

    IDENTIFIER = "PEE-FPVP-LIN-PU-PER"
    IDENTIFIER_DIGITS = 19
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(size=20, decimal_digits=17),
            FloatField(size=20, decimal_digits=17),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        """
        O código do PEE.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início para a validade da função
        de transformação eólica.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[1]

    @data_inicio.setter
    def data_inicio(self, c: datetime):
        self.data[1] = c

    @property
    def data_fim(self) -> Optional[datetime]:
        """
        A data de fim para a validade da função
        de transformação eólica.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, c: datetime):
        self.data[2] = c

    @property
    def coeficiente_linear(self) -> Optional[float]:
        """
        O coeficiente linear para a FTE

        :return: O coeficiente
        :rtype: Optional[float]
        """
        return self.data[3]

    @coeficiente_linear.setter
    def coeficiente_linear(self, c: float):
        self.data[3] = c

    @property
    def coeficiente_angular(self) -> Optional[float]:
        """
        O coeficiente angular para a FTE

        :return: O coeficiente
        :rtype: Optional[float]
        """
        return self.data[4]

    @coeficiente_angular.setter
    def coeficiente_angular(self, c: float):
        self.data[4] = c


class RegistroPEEGeracaoPatamar(Register):
    """
    Registro que contém as profundidades dos patamares de cada
    período para o histórico de geração de um PEE.
    """

    IDENTIFIER = "PEE-GER-PROF-PER-PAT"
    IDENTIFIER_DIGITS = 20
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            FloatField(decimal_digits=4),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        """
        O código do PEE.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início para a geração.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[1]

    @data_inicio.setter
    def data_inicio(self, c: datetime):
        self.data[1] = c

    @property
    def data_fim(self) -> Optional[datetime]:
        """
        A data de fim para a geração.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, c: datetime):
        self.data[2] = c

    @property
    def indice_patamar(self) -> Optional[int]:
        """
        O índice do patamar.

        :return: O patamar
        :rtype: Optional[int]
        """
        return self.data[3]

    @indice_patamar.setter
    def indice_patamar(self, c: int):
        self.data[3] = c

    @property
    def profundidade(self) -> Optional[float]:
        """
        O valor de profundidade da geração no patamar.

        :return: A profundidade do patamar
        :rtype: Optional[float]
        """
        return self.data[4]

    @profundidade.setter
    def profundidade(self, c: float):
        self.data[4] = c


class RegistroHistoricoVentoHorizonte(Register):
    """
    Registro que contém o horizonte de históricos de vento.
    """

    IDENTIFIER = "VENTO-HIST-HORIZ"
    IDENTIFIER_DIGITS = 16
    LINE = Line(
        [
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início do horizonte a ser considerado.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[0]

    @data_inicio.setter
    def data_inicio(self, c: datetime):
        self.data[0] = c

    @property
    def data_fim(self) -> Optional[datetime]:
        """
        A data de fim do horizonte a ser considerado.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[1]

    @data_fim.setter
    def data_fim(self, c: datetime):
        self.data[1] = c


class RegistroHistoricoVento(Register):
    """
    Registro que contém os históricos de vento para o horizonte
    considerado em um PEE.
    """

    IDENTIFIER = "VENTO-HIST"
    IDENTIFIER_DIGITS = 10
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=2),
            FloatField(decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_posto(self) -> Optional[int]:
        """
        O código do posto.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início do valor histórico.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[1]

    @data_inicio.setter
    def data_inicio(self, c: datetime):
        self.data[1] = c

    @property
    def data_fim(self) -> Optional[datetime]:
        """
        A data de fim do valor histórico.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, c: datetime):
        self.data[2] = c

    @property
    def velocidade(self) -> Optional[float]:
        """
        A velocidade média do vento no período.

        :return: A velocidade
        :rtype: Optional[float]
        """
        return self.data[3]

    @velocidade.setter
    def velocidade(self, c: float):
        self.data[3] = c

    @property
    def direcao(self) -> Optional[float]:
        """
        A direção média do vento no período.

        :return: A direção
        :rtype: Optional[float]
        """
        return self.data[4]

    @direcao.setter
    def direcao(self, c: float):
        self.data[4] = c


class RegistroPostoVentoCadastro(Register):
    """
    Registro que contém um cadastro de um posto de vento.
    """

    IDENTIFIER = "POSTO-VENTO-CAD"
    IDENTIFIER_DIGITS = 15
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_posto(self) -> Optional[int]:
        """
        O código do posto.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[0] = c

    @property
    def nome_posto(self) -> Optional[str]:
        """
        O nome do posto.

        :return: O nome
        :rtype: Optional[str]
        """
        return self.data[1]

    @nome_posto.setter
    def nome_posto(self, n: str):
        self.data[1] = n


class RegistroPEEPostoVento(Register):
    """
    Registro que contém um mapeamento de PEE para posto de vento
    """

    IDENTIFIER = "PEE-POSTO"
    IDENTIFIER_DIGITS = 9
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        """
        O código do PEE.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def codigo_posto(self) -> Optional[int]:
        """
        O código do posto.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[1]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[1] = c


class RegistroPEESubmercado(Register):
    """
    Registro que contém uma relação entre PEE e submercado.
    """

    IDENTIFIER = "PEE-SUBM"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        """
        O código do PEE.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def codigo_submercado(self) -> Optional[int]:
        """
        O código do submercado.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[1]

    @codigo_submercado.setter
    def codigo_submercado(self, c: int):
        self.data[1] = c
