from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.adapters.components.repository import factory
from copy import deepcopy
from datetime import datetime
from typing import Optional, IO


class ModifRegister(Register):
    """
    Registro base para o arquivo modif.dat, que contém
    características específicas deste arquivo:

    - Possibilidade de ler uma linha assumindo que o conteúdo
        de cada campo é separado por um número variável
        de espaços.
    - Capacidade de escrever uma linha assumindo uma formatação
        constante para melhor visualização.

    OBS: Atualmente só utilizados para registros VOLMIN e VOLMAX.
    """

    def __init__(
        self,
        previous=None,
        next=None,
        data=None,
    ) -> None:
        self.__identifier_field: Field = LiteralField(
            self.__class__.IDENTIFIER_DIGITS, 0
        )
        self.__previous = previous
        self.__next = next
        if data is None:
            self.__data = [None] * len(self.__class__.LINE.fields)
        else:
            self.__data = data
        super().__init__(previous, next, data)

    def read(self, file: IO, storage: str = "", *args, **kwargs) -> bool:
        delimited_fields = [deepcopy(f) for f in self.__class__.LINE.fields]
        line = Line(
            [self.__identifier_field] + delimited_fields,
            delimiter=" ",
            storage=storage,
        )
        line_full_spaces = file.readline().strip()
        line_parts = [p for p in line_full_spaces.split(" ") if len(p) > 0]
        line_simple_spaces = " ".join(line_parts)
        self.data = line.read(line_simple_spaces)[1:]
        return True

    def write(self, file: IO, storage: str = "", *args, **kwargs) -> bool:
        if not self.empty:
            line = Line(
                [self.__identifier_field] + self.__class__.LINE.fields,
                delimiter=self.__class__.LINE.delimiter,
                storage=storage,
            )
            linedata = line.write([self.__class__.IDENTIFIER] + self.data)
            factory(storage).write(file, linedata)
        return True


class USINA(Register):
    """
    Registro que contém a usina modificada.
    """

    IDENTIFIER = " USINA"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(4, 9), LiteralField(20, 44)])

    @property
    def codigo(self) -> Optional[int]:
        """
        O principal conteúdo do registro (código da usina).

        :return: O código da usina
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo.setter
    def codigo(self, t: int):
        self.data[0] = t

    @property
    def nome(self) -> Optional[str]:
        """
        O nome da usina (opcional).

        :return: O nome da usina
        :rtype: Optional[str]
        """
        return self.data[1]

    @nome.setter
    def nome(self, t: str):
        self.data[1] = t


class VOLMIN(ModifRegister):
    """
    Registro que contém uma modificação de volume mínimo
    operativo para uma usina.
    """

    IDENTIFIER = " VOLMIN"
    IDENTIFIER_DIGITS = 8
    LINE = Line([FloatField(8, 10, 2), LiteralField(3, 19)])

    @property
    def volume(self) -> Optional[float]:
        """
        O novo valor de volume

        :return: O novo valor de volume
        :rtype: Optional[float]
        """
        return self.data[0]

    @volume.setter
    def volume(self, t: float):
        self.data[0] = t

    @property
    def unidade(self) -> Optional[str]:
        """
        A unidade do volume informado

        :return: A unidade do volume
        :rtype: Optional[str]
        """
        return self.data[1]

    @unidade.setter
    def unidade(self, t: str):
        self.data[1] = t


class VOLMAX(ModifRegister):
    """
    Registro que contém uma modificação de volume máximo
    operativo para uma usina.
    """

    IDENTIFIER = " VOLMAX"
    IDENTIFIER_DIGITS = 8
    LINE = Line([FloatField(6, 10, 3), LiteralField(3, 17)])

    @property
    def volume(self) -> Optional[float]:
        """
        O novo valor de volume

        :return: O novo valor de volume
        :rtype: Optional[float]
        """
        return self.data[0]

    @volume.setter
    def volume(self, t: float):
        self.data[0] = t

    @property
    def unidade(self) -> Optional[str]:
        """
        A unidade do volume informado

        :return: A unidade do volume
        :rtype: Optional[str]
        """
        return self.data[1]

    @unidade.setter
    def unidade(self, t: str):
        self.data[1] = t


class NUMCNJ(ModifRegister):
    """
    Registro que contém uma modificação de número de conjunto
    de máquinas.
    """

    IDENTIFIER = " NUMCNJ"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(2, 11)])

    @property
    def numero(self) -> int:
        """
        O novo valor do número de conjuntos

        :return: O novo número de conjuntos
        :rtype: Optional[int]
        """
        return self.data[0]

    @numero.setter
    def numero(self, t: int):
        self.data[0] = t


class NUMMAQ(ModifRegister):
    """
    Registro que contém uma modificação do número de máquinas em um
    conjunto de máquinas.
    """

    IDENTIFIER = " NUMMAQ"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(3, 11), IntegerField(3, 14)])

    @property
    def conjunto(self) -> Optional[int]:
        """
        O conjunto de máquinas que terá o número alterado

        :return: O índice do conjunto de máquinas
        :rtype: Optional[int]
        """
        return self.data[0]

    @conjunto.setter
    def conjunto(self, t: int):
        self.data[0] = t

    @property
    def numero_maquinas(self) -> Optional[int]:
        """
        O novo número de máquinas do conjunto

        :return: O número de máquinas do conjunto
        :rtype: Optional[int]
        """
        return self.data[1]

    @numero_maquinas.setter
    def numero_maquinas(self, t: int):
        self.data[1] = t


class VAZMIN(ModifRegister):
    """
    Registro que contém uma modificação de vazão mínima (m3/s).
    """

    IDENTIFIER = " VAZMIN "
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(8, 10)])

    @property
    def vazao(self) -> Optional[int]:
        """
        O valor de vazão mínima

        :return: A nova vazão
        :rtype: Optional[int]
        """
        return self.data[0]

    @vazao.setter
    def vazao(self, t: int):
        self.data[0] = t


class CFUGA(ModifRegister):
    """
    Registro que contém uma modificação do nível do canal de fuga.
    """

    IDENTIFIER = " CFUGA"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [IntegerField(2, 10), IntegerField(4, 13), FloatField(7, 18, 3)]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def nivel(self) -> float:
        """
        O novo nivel do canal de fuga

        :return: O novo nível
        :rtype: Optional[int]
        """
        return self.data[2]

    @nivel.setter
    def nivel(self, t: float):
        self.data[2] = t


class CMONT(ModifRegister):
    """
    Registro que contém uma modificação do nível do canal de montante.
    """

    IDENTIFIER = " CMONT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [IntegerField(2, 10), IntegerField(4, 13), FloatField(7, 18, 3)]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def nivel(self) -> Optional[float]:
        """
        O novo nivel do canal de montante

        :return: O novo nível
        :rtype: Optional[float]
        """
        return self.data[2]

    @nivel.setter
    def nivel(self, t: float):
        self.data[2] = t


class VMAXT(Register):
    """
    Registro que contém uma modificação do volume máximo
    com data.
    """

    IDENTIFIER = " VMAXT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 3),
            LiteralField(3, 26),
        ]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def volume(self) -> Optional[float]:
        """
        O novo volume máximo

        :return: O novo volume
        :rtype: Optional[float]
        """
        return self.data[2]

    @volume.setter
    def volume(self, t: float):
        self.data[2] = t

    @property
    def unidade(self) -> Optional[str]:
        """
        A unidade de fornecimento do volume

        :return: A unidade
        :rtype: Optional[str]
        """
        return self.data[3]

    @unidade.setter
    def unidade(self, t: str):
        self.data[3] = t


class VMINT(Register):
    """
    Registro que contém uma modificação do volume mínimo
    com data.
    """

    IDENTIFIER = " VMINT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 3),
            LiteralField(3, 26),
        ]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def volume(self) -> Optional[float]:
        """
        O novo volume mínimo

        :return: O novo volume
        :rtype: Optional[float]
        """
        return self.data[2]

    @volume.setter
    def volume(self, t: float):
        self.data[2] = t

    @property
    def unidade(self) -> Optional[str]:
        """
        A unidade de fornecimento do volume

        :return: A unidade
        :rtype: Optional[str]
        """
        return self.data[3]

    @unidade.setter
    def unidade(self, t: str):
        self.data[3] = t


class VMINP(Register):
    """
    Registro que contém uma modificação do volume mínimo
    com data para adoção de penalidade.
    """

    IDENTIFIER = " VMINP"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 3),
            LiteralField(3, 26),
        ]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def volume(self) -> Optional[float]:
        """
        O novo volume mínimo a partir da data

        :return: O novo volume
        :rtype: Optional[float]
        """
        return self.data[2]

    @volume.setter
    def volume(self, t: float):
        self.data[2] = t

    @property
    def unidade(self) -> Optional[str]:
        """
        A unidade do volume fornecido

        :return: A unidade
        :rtype: Optional[str]
        """
        return self.data[3]

    @unidade.setter
    def unidade(self, t: str):
        self.data[3] = t


class VAZMINT(Register):
    """
    Registro que contém uma modificação da vazão mínima
    com data.
    """

    IDENTIFIER = " VAZMINT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def vazao(self) -> Optional[float]:
        """
        A nova vazão mínima a partir da data

        :return: A nova vazão
        :rtype: Optional[float]
        """
        return self.data[2]

    @vazao.setter
    def vazao(self, t: float):
        self.data[2] = t


class VAZMAXT(Register):
    """
    Registro que contém uma modificação da vazão máxima
    com data.
    """

    IDENTIFIER = " VAZMAXT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def vazao(self) -> Optional[float]:
        """
        A nova vazão máxima a partir da data

        :return: A nova vazão
        :rtype: Optional[float]
        """
        return self.data[2]

    @vazao.setter
    def vazao(self, t: float):
        self.data[2] = t


class TURBMAXT(Register):
    """
    Registro que contém uma modificação da turbinamento máximo
    com data.
    """

    IDENTIFIER = " TURBMAXT"
    IDENTIFIER_DIGITS = 9
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def turbinamento(self) -> Optional[float]:
        """
        O novo turbinamento máximo a partir da data

        :return: O novo turbinamento
        :rtype: Optional[float]
        """
        return self.data[2]

    @turbinamento.setter
    def turbinamento(self, t: float):
        self.data[2] = t


class TURBMINT(Register):
    """
    Registro que contém uma modificação da turbinamento mínimo
    com data.
    """

    IDENTIFIER = " TURBMINT"
    IDENTIFIER_DIGITS = 9
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def data_inicio(self) -> datetime:
        """
        A data de início da modificação

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        return datetime(self.data[1], self.data[0], 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime):
        self.data[0] = t.month
        self.data[1] = t.year

    @property
    def turbinamento(self) -> Optional[float]:
        """
        O novo turbinamento mínimo a partir da data

        :return: O novo turbinamento
        :rtype: Optional[float]
        """
        return self.data[2]

    @turbinamento.setter
    def turbinamento(self, t: float):
        self.data[2] = t
