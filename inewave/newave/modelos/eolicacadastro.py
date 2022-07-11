from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from datetime import datetime


class RegistroEolicaCadastro(Register):
    """
    Registro que contém um cadastro de usina eólica.
    """

    IDENTIFIER = "EOLICA-CADASTRO"
    IDENTIFIER_DIGITS = 15
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
            LiteralField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def nome_eolica(self) -> Optional[str]:
        return self.data[1]

    @nome_eolica.setter
    def nome_eolica(self, n: str):
        self.data[1] = n

    @property
    def identificador_eolica(self) -> Optional[str]:
        return self.data[2]

    @identificador_eolica.setter
    def identificador_eolica(self, n: str):
        self.data[2] = n

    @property
    def quantidade_conjuntos(self) -> Optional[int]:
        return self.data[3]

    @quantidade_conjuntos.setter
    def quantidade_conjuntos(self, q: int):
        self.data[3] = q


class RegistroEolicaCadastroConjuntoAerogeradores(Register):
    """
    Registro que contém o cadastro de um conjunto de
    aerogeradores em uma usina eólica.
    """

    IDENTIFIER = "EOLICA-CADASTRO-CONJUNTO-AEROGERADORES"
    IDENTIFIER_DIGITS = 38
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            LiteralField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def indice_conjunto(self) -> Optional[int]:
        return self.data[1]

    @indice_conjunto.setter
    def indice_conjunto(self, c: int):
        self.data[1] = c

    @property
    def nome_conjunto(self) -> Optional[str]:
        return self.data[2]

    @nome_conjunto.setter
    def nome_conjunto(self, n: str):
        self.data[2] = n

    @property
    def quantidade_aerogeradores(self) -> Optional[int]:
        return self.data[3]

    @quantidade_aerogeradores.setter
    def quantidade_aerogeradores(self, c: int):
        self.data[3] = c


class RegistroEolicaCadastroAerogerador(Register):
    """
    Registro que contém o cadastro de um aerogerador
    pertencente a um conjunto de aerogeradores em uma
    usina eólica.
    """

    IDENTIFIER = "EOLICA-CADASTRO-AEROGERADOR"
    IDENTIFIER_DIGITS = 27
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def indice_conjunto(self) -> Optional[int]:
        return self.data[1]

    @indice_conjunto.setter
    def indice_conjunto(self, c: int):
        self.data[1] = c

    @property
    def velocidade_cutin(self) -> Optional[float]:
        return self.data[2]

    @velocidade_cutin.setter
    def velocidade_cutin(self, v: float):
        self.data[2] = v

    @property
    def velocidade_nominal(self) -> Optional[float]:
        return self.data[3]

    @velocidade_nominal.setter
    def velocidade_nominal(self, v: float):
        self.data[3] = v

    @property
    def velocidade_cutout(self) -> Optional[float]:
        return self.data[4]

    @velocidade_cutout.setter
    def velocidade_cutout(self, v: float):
        self.data[4] = v

    @property
    def potencia_velocidade_cutin(self) -> Optional[float]:
        return self.data[5]

    @potencia_velocidade_cutin.setter
    def potencia_velocidade_cutin(self, p: float):
        self.data[5] = p

    @property
    def potencia_velocidade_nominal(self) -> Optional[float]:
        return self.data[6]

    @potencia_velocidade_nominal.setter
    def potencia_velocidade_nominal(self, p: float):
        self.data[6] = p

    @property
    def potencia_velocidade_cutout(self) -> Optional[float]:
        return self.data[7]

    @potencia_velocidade_cutout.setter
    def potencia_velocidade_cutout(self, p: float):
        self.data[7] = p

    @property
    def altura_torre(self) -> Optional[float]:
        return self.data[8]

    @altura_torre.setter
    def altura_torre(self, h: float):
        self.data[8] = h


class RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo(Register):
    """
    Registro que contém a informação de início e fim de
    operação de um conjunto de aerogeradores.
    """

    IDENTIFIER = "EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO"
    IDENTIFIER_DIGITS = 57
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def indice_conjunto(self) -> Optional[int]:
        return self.data[1]

    @indice_conjunto.setter
    def indice_conjunto(self, c: int):
        self.data[1] = c

    @property
    def periodo_inicial(self) -> Optional[datetime]:
        return self.data[2]

    @periodo_inicial.setter
    def periodo_inicial(self, p: datetime):
        self.data[2] = p

    @property
    def periodo_final(self) -> Optional[datetime]:
        return self.data[3]

    @periodo_final.setter
    def periodo_final(self, p: datetime):
        self.data[3] = p

    @property
    def numero_aerogeradores(self) -> Optional[int]:
        return self.data[4]

    @numero_aerogeradores.setter
    def numero_aerogeradores(self, n: int):
        self.data[4] = n


class RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva(Register):
    """
    Registro que contém a informação de início e fim de
    operação para uma certa potência efetiva de um conjunto
    de aerogeradores.
    """

    IDENTIFIER = "EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO"
    IDENTIFIER_DIGITS = 53
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=3),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def indice_conjunto(self) -> Optional[int]:
        return self.data[1]

    @indice_conjunto.setter
    def indice_conjunto(self, c: int):
        self.data[1] = c

    @property
    def periodo_inicial(self) -> Optional[datetime]:
        return self.data[2]

    @periodo_inicial.setter
    def periodo_inicial(self, p: datetime):
        self.data[2] = p

    @property
    def periodo_final(self) -> Optional[datetime]:
        return self.data[3]

    @periodo_final.setter
    def periodo_final(self, p: datetime):
        self.data[3] = p

    @property
    def potencia_efetiva(self) -> Optional[float]:
        return self.data[4]

    @potencia_efetiva.setter
    def potencia_efetiva(self, n: float):
        self.data[4] = n
