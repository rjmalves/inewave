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


def _remove_aspas(valor: Optional[str]) -> Optional[str]:
    """Retira as aspas que o modif.dat usa em torno da unidade (``'%'``)."""
    if valor is None:
        return None
    return valor.strip().strip("'\"")


def _adiciona_aspas(valor: str) -> str:
    """Envolve a unidade em aspas simples, como o NEWAVE a escreve."""
    return f"'{_remove_aspas(valor)}'"


class ModifRegister(Register):
    """
    Registro base para o arquivo modif.dat, que contém
    características específicas deste arquivo:

    - Possibilidade de ler uma linha assumindo que o conteúdo
        de cada campo é separado por um número variável
        de espaços.
    - Capacidade de escrever uma linha assumindo uma formatação
        constante para melhor visualização.
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
        # Um campo opcional ausente na linha não é lido: sem zerar a cópia,
        # ele herdaria o valor que uma escrita anterior deixou no campo da
        # classe.
        for f in delimited_fields:
            f.value = None
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

        ``"h"``/``"H"`` para hm³ ou ``"%"`` para porcentagem do volume
        útil, sem as aspas com que o arquivo a escreve. A escrita
        mantém as aspas.

        :return: A unidade do volume
        :rtype: Optional[str]
        """
        return _remove_aspas(self.data[1])

    @unidade.setter
    def unidade(self, t: str) -> None:
        self.data[1] = _adiciona_aspas(t)


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

        ``"h"``/``"H"`` para hm³ ou ``"%"`` para porcentagem do volume
        útil, sem as aspas com que o arquivo a escreve. A escrita
        mantém as aspas.

        :return: A unidade do volume
        :rtype: Optional[str]
        """
        return _remove_aspas(self.data[1])

    @unidade.setter
    def unidade(self, t: str) -> None:
        self.data[1] = _adiciona_aspas(t)


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


class PRODESP(ModifRegister):
    """
    Registro que contém uma modificação da produtibilidade específica
    da usina (MW/m3/s/m).
    """

    __slots__ = []

    IDENTIFIER = " PRODESP"
    IDENTIFIER_DIGITS = 8
    LINE = Line([FloatField(10, 10, 6)])

    @property
    def produtibilidade(self) -> Optional[float]:
        """
        O novo valor da produtibilidade específica

        :return: A produtibilidade específica em MW/m3/s/m
        :rtype: Optional[float]
        """
        return self.data[0]

    @produtibilidade.setter
    def produtibilidade(self, p: float) -> None:
        self.data[0] = p


class TEIF(ModifRegister):
    """
    Registro que contém uma modificação da taxa esperada de
    indisponibilidade forçada da usina (%).
    """

    __slots__ = []

    IDENTIFIER = " TEIF "
    IDENTIFIER_DIGITS = 8
    LINE = Line([FloatField(8, 10, 3)])

    @property
    def teif(self) -> Optional[float]:
        """
        O novo valor da taxa esperada de indisponibilidade forçada

        :return: A TEIF em %
        :rtype: Optional[float]
        """
        return self.data[0]

    @teif.setter
    def teif(self, t: float) -> None:
        self.data[0] = t


class IP(ModifRegister):
    """
    Registro que contém uma modificação da indisponibilidade
    programada da usina (%).
    """

    __slots__ = []

    IDENTIFIER = " IP "
    IDENTIFIER_DIGITS = 8
    LINE = Line([FloatField(8, 10, 3)])

    @property
    def ip(self) -> Optional[float]:
        """
        O novo valor da indisponibilidade programada

        :return: A IP em %
        :rtype: Optional[float]
        """
        return self.data[0]

    @ip.setter
    def ip(self, t: float) -> None:
        self.data[0] = t


class PERDHIDR(ModifRegister):
    """
    Registro que contém uma modificação da perda hidráulica da usina,
    na mesma unidade do cadastro de usinas hidroelétricas.
    """

    __slots__ = []

    IDENTIFIER = " PERDHIDR"
    IDENTIFIER_DIGITS = 9
    LINE = Line([FloatField(8, 10, 3)])

    @property
    def perdas(self) -> Optional[float]:
        """
        O novo valor da perda hidráulica, na unidade do cadastro
        (``hidr.dat``)

        :return: A perda hidráulica
        :rtype: Optional[float]
        """
        return self.data[0]

    @perdas.setter
    def perdas(self, t: float) -> None:
        self.data[0] = t


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


class COEFEVAP(ModifRegister):
    """
    Registro que contém uma modificação do coeficiente de evaporação
    de um mês (mm/mês).
    """

    __slots__ = []

    IDENTIFIER = " COEFEVAP"
    IDENTIFIER_DIGITS = 9
    LINE = Line([IntegerField(5, 10), IntegerField(2, 16)])

    @property
    def coeficiente(self) -> Optional[int]:
        """
        O novo valor do coeficiente de evaporação

        :return: O coeficiente de evaporação em mm/mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @coeficiente.setter
    def coeficiente(self, c: int) -> None:
        self.data[0] = c

    @property
    def mes(self) -> Optional[int]:
        """
        O mês do ano (1 a 12) cujo coeficiente é alterado

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[1]

    @mes.setter
    def mes(self, m: int) -> None:
        self.data[1] = m


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

        ``"h"``/``"H"`` para hm³ ou ``"%"`` para porcentagem do volume
        útil, sem as aspas com que o arquivo a escreve. A escrita
        mantém as aspas.

        :return: A unidade
        :rtype: Optional[str]
        """
        return _remove_aspas(self.data[3])

    @unidade.setter
    def unidade(self, t: str) -> None:
        self.data[3] = _adiciona_aspas(t)


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

        ``"h"``/``"H"`` para hm³ ou ``"%"`` para porcentagem do volume
        útil, sem as aspas com que o arquivo a escreve. A escrita
        mantém as aspas.

        :return: A unidade
        :rtype: Optional[str]
        """
        return _remove_aspas(self.data[3])

    @unidade.setter
    def unidade(self, t: str) -> None:
        self.data[3] = _adiciona_aspas(t)


class NUMBAS(ModifRegister):
    """
    Registro que contém uma modificação do número de unidades de base
    da usina.
    """

    __slots__ = []

    IDENTIFIER = " NUMBAS"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(3, 10)])

    @property
    def numero(self) -> Optional[int]:
        """
        O novo valor do número de unidades de base

        :return: O número de unidades de base
        :rtype: Optional[int]
        """
        return self.data[0]

    @numero.setter
    def numero(self, n: int) -> None:
        self.data[0] = n


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

        ``"h"``/``"H"`` para hm³ ou ``"%"`` para porcentagem do volume
        útil, sem as aspas com que o arquivo a escreve. A escrita
        mantém as aspas.

        :return: A unidade
        :rtype: Optional[str]
        """
        return _remove_aspas(self.data[3])

    @unidade.setter
    def unidade(self, t: str) -> None:
        self.data[3] = _adiciona_aspas(t)


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


class CDESVIO(ModifRegister):
    """
    Registro que contém uma modificação do canal de desvio da usina:
    a usina a jusante no canal e, opcionalmente, a vazão máxima do
    canal (m3/s).
    """

    __slots__ = []

    IDENTIFIER = " CDESVIO"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(4, 10), FloatField(10, 15, 2)])

    @property
    def codigo_usina_jusante(self) -> Optional[int]:
        """
        O código da usina a jusante no canal de desvio

        :return: O código da usina
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo_usina_jusante.setter
    def codigo_usina_jusante(self, c: int) -> None:
        self.data[0] = c

    @property
    def limite_vazao(self) -> Optional[float]:
        """
        A vazão máxima do canal de desvio, de uso opcional no arquivo

        :return: A vazão máxima em m3/s, ou ``None`` se não informada
        :rtype: Optional[float]
        """
        return self.data[1]

    @limite_vazao.setter
    def limite_vazao(self, v: Optional[float]) -> None:
        self.data[1] = v
