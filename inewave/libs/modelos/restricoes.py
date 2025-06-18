from datetime import datetime
from typing import Optional

from cfinterface.components.datetimefield import DatetimeField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.register import Register


class RegistroRE(Register):
    """
    Registro que contém um cadastro de restrição elétrica (RE).
    """

    IDENTIFIER = "RE"
    IDENTIFIER_DIGITS = 2
    LINE = Line(
        [
            IntegerField(),
            LiteralField(size=200),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def formula(self) -> Optional[str]:
        """
        A fórmula da restrição.

        :return: A fórmula
        :rtype: Optional[str]
        """
        return self.data[1]

    @formula.setter
    def formula(self, n: str):
        self.data[1] = n


class RegistroREHorizPer(Register):
    """
    Registro que contém o cadastro do horizonte de validade
    da restrição RE.
    """

    IDENTIFIER = "RE-HORIZ-PER"
    IDENTIFIER_DIGITS = 12
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade da restrição.

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
        A data de fim da validade da restrição.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, n: datetime):
        self.data[2] = n


class RegistroRELimFormPer(Register):
    """
    Registro que contém os limites de cada restrição
    RE por patamar.
    """

    IDENTIFIER = "RE-LIM-FORM-PER-PAT"
    IDENTIFIER_DIGITS = 19
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            LiteralField(size=200),
            LiteralField(size=200),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade dos limites da restrição.

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
        A data de fim da validade dos limites da restrição.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, v: datetime):
        self.data[2] = v

    @property
    def patamar(self) -> Optional[int]:
        """
        O índice do patamar para os limites.

        :return: O patamar
        :rtype: Optional[int]
        """
        return self.data[3]

    @patamar.setter
    def patamar(self, v: int):
        self.data[3] = v

    @property
    def limite_inferior(self) -> Optional[str]:
        """
        A equação que da o limite inferior da restrição.

        :return: A equação
        :rtype: Optional[str]
        """
        return self.data[4]

    @limite_inferior.setter
    def limite_inferior(self, v: str):
        self.data[4] = v

    @property
    def limite_superior(self) -> Optional[str]:
        """
        A equação que da o limite superior da restrição.

        :return: A equação
        :rtype: Optional[str]
        """
        return self.data[5]

    @limite_superior.setter
    def limite_superior(self, v: str):
        self.data[5] = v


class RegistroRHE(Register):
    """
    Registro que contém um cadastro de restrição de
    energia (RHE).
    """

    IDENTIFIER = "RHE"
    IDENTIFIER_DIGITS = 3
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def formula(self) -> Optional[str]:
        """
        A fórmula da restrição.

        :return: A fórmula
        :rtype: Optional[str]
        """
        return self.data[1]

    @formula.setter
    def formula(self, n: str):
        self.data[1] = n


class RegistroRHEHorizPer(Register):
    """
    Registro que contém o cadastro do horizonte de validade
    da restrição RHE.
    """

    IDENTIFIER = "RHE-HORIZ-PER"
    IDENTIFIER_DIGITS = 13
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade da restrição.

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
        A data de fim da validade da restrição.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, n: datetime):
        self.data[2] = n


class RegistroRHELsLPPEarmi(Register):
    """
    Registro que contém as retas de cada restrição
    RHE modelada como restrição linear por partes.
    """

    IDENTIFIER = "RHE-LS-LPP-EARMI"
    IDENTIFIER_DIGITS = 16
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            FloatField(size=16, decimal_digits=4),
            FloatField(size=16, decimal_digits=4),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def indice_reta(self) -> Optional[int]:
        """
        O índice da reta que compõe a restrição.

        :return: O índice da reta
        :rtype: Optional[int]
        """
        return self.data[1]

    @indice_reta.setter
    def indice_reta(self, c: int):
        self.data[1] = c

    @property
    def coeficiente_angular(self) -> Optional[float]:
        """
        O coeficiente angular da reta.

        :return: O coeficiente
        :rtype: Optional[float]
        """
        return self.data[2]

    @coeficiente_angular.setter
    def coeficiente_angular(self, v: float):
        self.data[2] = v

    @property
    def coeficiente_linear(self) -> Optional[float]:
        """
        O coeficiente linear da reta.

        :return: O coeficiente
        :rtype: Optional[float]
        """
        return self.data[3]

    @coeficiente_linear.setter
    def coeficiente_linear(self, v: float):
        self.data[3] = v


class RegistroRHQ(Register):
    """
    Registro que contém um cadastro de restrição de
    vazão (RHQ).
    """

    IDENTIFIER = "RHQ"
    IDENTIFIER_DIGITS = 3
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def formula(self) -> Optional[str]:
        """
        A fórmula da restrição.

        :return: A fórmula
        :rtype: Optional[str]
        """
        return self.data[1]

    @formula.setter
    def formula(self, n: str):
        self.data[1] = n


class RegistroRHQHorizPer(Register):
    """
    Registro que contém o cadastro do horizonte de validade
    da restrição RHQ.
    """

    IDENTIFIER = "RHQ-HORIZ-PER"
    IDENTIFIER_DIGITS = 13
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade da restrição.

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
        A data de fim da validade da restrição.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, n: datetime):
        self.data[2] = n


class RegistroRHQLsLPPVoli(Register):
    """
    Registro que contém as retas de cada restrição
    RHQ modelada como restrição linear por partes.
    """

    IDENTIFIER = "RHQ-LS-LPP-VOLI"
    IDENTIFIER_DIGITS = 15
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            FloatField(size=16, decimal_digits=4),
            FloatField(size=16, decimal_digits=4),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def indice_reta(self) -> Optional[int]:
        """
        O índice da reta que compõe a restrição.

        :return: O índice da reta
        :rtype: Optional[int]
        """
        return self.data[1]

    @indice_reta.setter
    def indice_reta(self, c: int):
        self.data[1] = c

    @property
    def coeficiente_angular(self) -> Optional[float]:
        """
        O coeficiente angular da reta.

        :return: O coeficiente
        :rtype: Optional[float]
        """
        return self.data[2]

    @coeficiente_angular.setter
    def coeficiente_angular(self, v: float):
        self.data[2] = v

    @property
    def coeficiente_linear(self) -> Optional[float]:
        """
        O coeficiente linear da reta.

        :return: O coeficiente
        :rtype: Optional[float]
        """
        return self.data[3]

    @coeficiente_linear.setter
    def coeficiente_linear(self, v: float):
        self.data[3] = v


class RegistroRHQLimFormPerPat(Register):
    """
    Registro que contém os limites inferiores e superiores
    para restrições RHQ.
    """

    IDENTIFIER = "RHQ-LIM-FORM-PER-PAT"
    IDENTIFIER_DIGITS = 20
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            FloatField(size=16, decimal_digits=2),
            FloatField(size=16, decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade dos limites da restrição.

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
        A data de fim da validade dos limites da restrição.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, n: datetime):
        self.data[2] = n

    @property
    def patamar(self) -> Optional[int]:
        """
        O índice do patamar para os limites.

        :return: O patamar.
        :rtype: Optional[int]
        """
        return self.data[3]

    @patamar.setter
    def patamar(self, c: int):
        self.data[3] = c

    @property
    def limite_inferior(self) -> Optional[float]:
        """
        O limite inferior para a restrição.

        :return: O limite inferior
        :rtype: Optional[float]
        """
        return self.data[4]

    @limite_inferior.setter
    def limite_inferior(self, v: float):
        self.data[4] = v

    @property
    def limite_superior(self) -> Optional[float]:
        """
        O limite superior para a restrição.

        :return: O limite superior
        :rtype: Optional[float]
        """
        return self.data[5]

    @limite_superior.setter
    def limite_superior(self, v: float):
        self.data[5] = v


class RegistroRHV(Register):
    """
    Registro que contém um cadastro de restrição de
    volume (RHV).
    """

    IDENTIFIER = "RHV"
    IDENTIFIER_DIGITS = 3
    LINE = Line(
        [
            IntegerField(size=8),
            LiteralField(size=200),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def formula(self) -> Optional[str]:
        """
        A fórmula da restrição.

        :return: A fórmula
        :rtype: Optional[str]
        """
        return self.data[1]

    @formula.setter
    def formula(self, n: str):
        self.data[1] = n


class RegistroRHVHorizPer(Register):
    """
    Registro que contém o cadastro do horizonte de validade
    da restrição RHV.
    """

    IDENTIFIER = "RHV-HORIZ-PER"
    IDENTIFIER_DIGITS = 13
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade da restrição.

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
        A data de fim da validade da restrição.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, n: datetime):
        self.data[2] = n


class RegistroRHVLimFormPer(Register):
    """
    Registro que contém os limites inferiores e superiores
    para restrições RHV.
    """

    IDENTIFIER = "RHV-LIM-FORM-PER"
    IDENTIFIER_DIGITS = 16
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(size=16, decimal_digits=2),
            FloatField(size=16, decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        """
        O código da restrição.

        :return: O código
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def data_inicio(self) -> Optional[datetime]:
        """
        A data de início da validade dos limites da restrição.

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
        A data de fim da validade dos limites da restrição.

        :return: A data
        :rtype: Optional[datetime]
        """
        return self.data[2]

    @data_fim.setter
    def data_fim(self, n: datetime):
        self.data[2] = n

    @property
    def limite_inferior(self) -> Optional[float]:
        """
        O limite inferior para a restrição.

        :return: O limite inferior
        :rtype: Optional[float]
        """
        return self.data[3]

    @limite_inferior.setter
    def limite_inferior(self, v: float):
        self.data[3] = v

    @property
    def limite_superior(self) -> Optional[float]:
        """
        O limite superior para a restrição.

        :return: O limite superior
        :rtype: Optional[float]
        """
        return self.data[4]

    @limite_superior.setter
    def limite_superior(self, v: float):
        self.data[4] = v
