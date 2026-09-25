from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.adapters.components.repository import factory
from copy import deepcopy
from datetime import datetime
from typing import Any, IO, List, Optional


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

    __slots__ = ["__identifier_field", "__previous", "__next", "__data"]

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
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

    def read(
        self, file: IO[Any], storage: str = "", *args: Any, **kwargs: Any
    ) -> bool:
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

    def write(
        self, file: IO[Any], storage: str = "", *args: Any, **kwargs: Any
    ) -> bool:
        if not self.empty:
            line = Line(
                [self.__identifier_field] + self.__class__.LINE.fields,
                delimiter=self.__class__.LINE.delimiter,
                storage=storage,
            )
            linedata = line.write([self.__class__.IDENTIFIER] + self.data)
            factory(storage).write(file, linedata)
        return True


class ModifRegisterComData(ModifRegister):
    """Base para o registro VAZMINT do modif.dat, cujo campo de ano aceita,
    além de um ano numérico, os marcadores textuais ``PRE`` (período
    pré-estudo) e ``POS`` (período pós-estudo).

    Por isso o ano é lido como texto (``LiteralField``) e ``data_inicio`` só
    devolve um ``datetime`` quando o ano é numérico; para ``PRE``/``POS``
    devolve ``None`` e o marcador fica disponível em :attr:`periodo`.

    Convenção compartilhada: ``self.data[0]`` é o mês e ``self.data[1]`` é o
    ano/marcador.
    """

    __slots__ = []

    def read(
        self, file: IO[Any], storage: str = "", *args: Any, **kwargs: Any
    ) -> bool:
        # O ano é lido como texto (LiteralField) para aceitar os marcadores
        # PRE/POS. Um ano numérico é normalizado de volta para int, preservando
        # o tipo histórico de ``data[1]`` (int) para os períodos do estudo; só
        # PRE/POS permanecem como string.
        result = super().read(file, storage, *args, **kwargs)
        ano = self.data[1]
        if ano is not None:
            ano_txt = str(ano).strip()
            if ano_txt.isdigit():
                self.data[1] = int(ano_txt)
            else:
                self.data[1] = ano_txt.upper()
        return result

    @property
    def periodo(self) -> Optional[str]:
        """O marcador de período (``"PRE"`` ou ``"POS"``), ou ``None``.

        Devolve ``None`` quando o ano é numérico (um período do estudo).

        :return: ``"PRE"``, ``"POS"`` ou ``None``
        :rtype: Optional[str]
        """
        ano = self.data[1]
        if ano is None:
            return None
        ano_txt = str(ano).strip().upper()
        return ano_txt if ano_txt in ("PRE", "POS") else None

    @property
    def mes(self) -> Optional[int]:
        """O mês da modificação (válido inclusive para ``PRE``/``POS``).

        :return: O mês, ou ``None`` se ausente
        :rtype: Optional[int]
        """
        return None if self.data[0] is None else int(self.data[0])

    @property
    def data_inicio(self) -> Optional[datetime]:
        """A data de início da modificação, quando o ano é numérico.

        Devolve ``None`` para registros de período ``PRE``/``POS`` (veja
        :attr:`periodo`) ou quando mês/ano estão ausentes.

        :return: A data de início da modificação
        :rtype: Optional[datetime]
        """
        mes = self.data[0]
        ano = self.data[1]
        if mes is None or ano is None:
            return None
        ano_txt = str(ano).strip()
        if not ano_txt.isdigit():
            return None
        return datetime(int(ano_txt), int(mes), 1)

    @data_inicio.setter
    def data_inicio(self, t: datetime) -> None:
        self.data[0] = t.month
        self.data[1] = t.year


class USINA(Register):
    """
    Registro que contém a usina modificada.
    """

    __slots__: List[str] = []

    IDENTIFIER = " USINA"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(4, 9), LiteralField(20, 44)])

    def read(
        self, file: IO[Any], storage: str = "", *args: Any, **kwargs: Any
    ) -> bool:
        line_str = file.readline()
        parts = line_str.split()
        codigo = int(parts[1]) if len(parts) > 1 else None
        nome = " ".join(parts[2:]) if len(parts) > 2 else None
        self.data = [codigo, nome]
        return True

    @property
    def codigo(self) -> Optional[int]:
        """
        O principal conteúdo do registro (código da usina).

        :return: O código da usina
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo.setter
    def codigo(self, t: int) -> None:
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
    def nome(self, t: str) -> None:
        self.data[1] = t


class VOLMIN(ModifRegister):
    """
    Registro que contém uma modificação de volume mínimo
    operativo para uma usina.
    """

    __slots__ = []

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
    def volume(self, t: float) -> None:
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
    def unidade(self, t: str) -> None:
        self.data[1] = t


class VOLMAX(ModifRegister):
    """
    Registro que contém uma modificação de volume máximo
    operativo para uma usina.
    """

    __slots__ = []

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
    def volume(self, t: float) -> None:
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
    def unidade(self, t: str) -> None:
        self.data[1] = t


class NUMCNJ(ModifRegister):
    """
    Registro que contém uma modificação de número de conjunto
    de máquinas.
    """

    __slots__ = []

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
    def numero(self, t: int) -> None:
        self.data[0] = t


class NUMMAQ(ModifRegister):
    """
    Registro que contém uma modificação do número de máquinas em um
    conjunto de máquinas.
    """

    __slots__ = []

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
        return self.data[1]

    @conjunto.setter
    def conjunto(self, t: int) -> None:
        self.data[1] = t

    @property
    def numero_maquinas(self) -> Optional[int]:
        """
        O novo número de máquinas do conjunto

        :return: O número de máquinas do conjunto
        :rtype: Optional[int]
        """
        return self.data[0]

    @numero_maquinas.setter
    def numero_maquinas(self, t: int) -> None:
        self.data[0] = t


class POTEFE(ModifRegister):
    """
    Registro que contém uma modificação da potência efetiva de um
    conjunto de máquinas (MW).
    """

    __slots__ = []

    IDENTIFIER = " POTEFE"
    IDENTIFIER_DIGITS = 7
    LINE = Line([FloatField(8, 10, 2), IntegerField(3, 19)])

    @property
    def potencia(self) -> Optional[float]:
        """
        A nova potência efetiva do conjunto de máquinas

        :return: A potência efetiva em MW
        :rtype: Optional[float]
        """
        return self.data[0]

    @potencia.setter
    def potencia(self, p: float) -> None:
        self.data[0] = p

    @property
    def conjunto(self) -> Optional[int]:
        """
        O conjunto de máquinas que terá a potência alterada

        :return: O índice do conjunto de máquinas
        :rtype: Optional[int]
        """
        return self.data[1]

    @conjunto.setter
    def conjunto(self, t: int) -> None:
        self.data[1] = t


class VOLCOTA(ModifRegister):
    """
    Registro que contém uma modificação do polinômio volume-cota.
    """

    __slots__ = []

    IDENTIFIER = " VOLCOTA"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            FloatField(14, 10, 6, format="D"),
            FloatField(14, 25, 6, format="D"),
            FloatField(14, 40, 6, format="D"),
            FloatField(14, 55, 6, format="D"),
            FloatField(14, 70, 6, format="D"),
        ]
    )

    @property
    def polinomio_volume_cota(self) -> List[float]:
        """
        Os cinco coeficientes do novo polinômio volume-cota, de a0 a a4

        :return: Os coeficientes do polinômio
        :rtype: List[float]
        """
        return self.data[0:5]

    @polinomio_volume_cota.setter
    def polinomio_volume_cota(self, v: List[float]) -> None:
        self.data[0:5] = v


class COTAREA(ModifRegister):
    """
    Registro que contém uma modificação do polinômio cota-área.
    """

    __slots__ = []

    IDENTIFIER = " COTAREA"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            FloatField(14, 10, 6, format="D"),
            FloatField(14, 25, 6, format="D"),
            FloatField(14, 40, 6, format="D"),
            FloatField(14, 55, 6, format="D"),
            FloatField(14, 70, 6, format="D"),
        ]
    )

    @property
    def polinomio_cota_area(self) -> List[float]:
        """
        Os cinco coeficientes do novo polinômio cota-área, de a0 a a4

        :return: Os coeficientes do polinômio
        :rtype: List[float]
        """
        return self.data[0:5]

    @polinomio_cota_area.setter
    def polinomio_cota_area(self, v: List[float]) -> None:
        self.data[0:5] = v


class VAZMIN(ModifRegister):
    """
    Registro que contém uma modificação de vazão mínima (m3/s).
    """

    __slots__ = []

    IDENTIFIER = " VAZMIN "
    IDENTIFIER_DIGITS = 8
    LINE = Line([FloatField(8, 10, 2)])

    @property
    def vazao(self) -> Optional[float]:
        """
        O valor de vazão mínima

        :return: A nova vazão
        :rtype: Optional[float]
        """
        return self.data[0]

    @vazao.setter
    def vazao(self, t: float) -> None:
        self.data[0] = t


class CFUGA(ModifRegister):
    """
    Registro que contém uma modificação do nível do canal de fuga.
    """

    __slots__ = []

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
    def data_inicio(self, t: datetime) -> None:
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
    def nivel(self, t: float) -> None:
        self.data[2] = t


class CMONT(ModifRegister):
    """
    Registro que contém uma modificação do nível do canal de montante.
    """

    __slots__ = []

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
    def data_inicio(self, t: datetime) -> None:
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
    def nivel(self, t: float) -> None:
        self.data[2] = t


class VMAXT(ModifRegister):
    """
    Registro que contém uma modificação do volume máximo
    com data.
    """

    __slots__ = []

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
    def data_inicio(self, t: datetime) -> None:
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
    def volume(self, t: float) -> None:
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
    def unidade(self, t: str) -> None:
        self.data[3] = t


class VMINT(ModifRegister):
    """
    Registro que contém uma modificação do volume mínimo
    com data.
    """

    __slots__ = []

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
    def data_inicio(self, t: datetime) -> None:
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
    def volume(self, t: float) -> None:
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
    def unidade(self, t: str) -> None:
        self.data[3] = t


class VMINP(ModifRegister):
    """
    Registro que contém uma modificação do volume mínimo
    com data para adoção de penalidade.
    """

    __slots__ = []

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
    def data_inicio(self, t: datetime) -> None:
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
    def volume(self, t: float) -> None:
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
    def unidade(self, t: str) -> None:
        self.data[3] = t


class VAZMINT(ModifRegisterComData):
    """
    Registro que contém uma modificação da vazão mínima
    com data.

    O campo de ano aceita, além de um ano numérico, os marcadores ``PRE``
    (período pré-estudo) e ``POS`` (período pós-estudo) — o único registro do
    modif.dat em que o modelo NEWAVE admite esses marcadores.
    """

    __slots__ = []

    IDENTIFIER = " VAZMINT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            LiteralField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def vazao(self) -> Optional[float]:
        """
        A nova vazão mínima a partir da data

        :return: A nova vazão
        :rtype: Optional[float]
        """
        return self.data[2]

    @vazao.setter
    def vazao(self, t: float) -> None:
        self.data[2] = t


class VAZMAXT(ModifRegister):
    """
    Registro que contém uma modificação da vazão máxima
    com data.
    """

    __slots__ = []

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
    def data_inicio(self, t: datetime) -> None:
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
    def vazao(self, t: float) -> None:
        self.data[2] = t


class TURBMAXT(ModifRegister):
    """
    Registro que contém uma modificação da turbinamento máximo
    com data.
    """

    __slots__ = []

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
    def data_inicio(self, t: datetime) -> None:
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
    def turbinamento(self, t: float) -> None:
        self.data[2] = t


class TURBMINT(ModifRegister):
    """
    Registro que contém uma modificação da turbinamento mínimo
    com data.
    """

    __slots__ = []

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
    def data_inicio(self, t: datetime) -> None:
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
    def turbinamento(self, t: float) -> None:
        self.data[2] = t
