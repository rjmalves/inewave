# Imports de módulos externos
from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from datetime import datetime, timedelta
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from typing import Any, IO, List, Optional, Tuple
import re


class BlocoTemposEtapasTim(Block):
    """
    Bloco com as informações de tempo de execução
    do NEWAVE obtidas no arquivo `newave.tim`.
    """

    __slots__ = ["__line"]

    BEGIN_PATTERN = "Leitura de Dados:"
    END_PATTERN = ""

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        etapa_field: List[Field] = [LiteralField(25, 0)]
        tempo_field: List[Field] = [LiteralField(14, 25)]
        self.__line = Line(etapa_field + tempo_field)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTemposEtapasTim):
            return False
        bloco: BlocoTemposEtapasTim = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(data={"etapa": etapas, "tempo": tempos})
            return df

        # Variáveis auxiliares
        etapas: List[str] = []
        tempos: List[timedelta] = []

        # Leitura das etapas
        while True:
            dados = self.__line.read(file.readline())
            if not dados or not dados[0].strip("- \t\n"):
                break
            etapas.append(dados[0].split(":")[0])
            h = int(dados[1].split("h")[0])
            min = int(dados[1].split("h")[1].split("min")[0])
            s = float(dados[1].split("min")[1].split("s")[0])
            ts = timedelta(hours=h, minutes=min, seconds=s)
            tempos.append(ts)

        self.data = converte_tabela_em_df()


class BlocoVersaoModeloTim(Block):
    """
    Bloco com a versão do NEWAVE obtida no
    arquivo `newave.tim`.
    """

    __slots__ = ["__linha", "__biblioteca_pl"]

    BEGIN_PATTERN = r"            Versao "
    END_PATTERN = ""

    __BIBLIOTECA = re.compile(r"Biblioteca Solucao PLs:?\s*(.*?)\s*$")

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(16, 78)])
        self.__biblioteca_pl: Optional[str] = None

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoVersaoModeloTim):
            return False
        bloco: BlocoVersaoModeloTim = o
        if not all(
            [
                isinstance(self.data, str),
                isinstance(o.data, str),
            ]
        ):
            return False
        else:
            return (
                self.data == bloco.data
                and self.biblioteca_pl == bloco.biblioteca_pl
            )

    @property
    def biblioteca_pl(self) -> Optional[str]:
        """
        O texto da biblioteca de PLs escrito na linha da versão, nas
        versões do NEWAVE que a escrevem nessa linha, ou `None`.
        """
        return self.__biblioteca_pl

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        linha = file.readline()
        self.data = self.__linha.read(linha)[0]
        m = self.__BIBLIOTECA.search(linha)
        self.__biblioteca_pl = m.group(1) if m is not None else None


class BlocoTemposIteracoesTim(Block):
    """
    Bloco com os tempos de cada iteração do cálculo da política, obtidos
    no arquivo `newave.tim`, onde cada iteração ocupa três linhas::

        Iteracao   2 - Backward: 000h 00min 01s
                       Forward:  000h 00min 03s
                       Total:    000h 00min 04s
    """

    __slots__: List[str] = []

    BEGIN_PATTERN = r"^Iteracao\s+\d+\s+-\s+Backward:"
    END_PATTERN = ""

    __TEMPO = r"(\d+)h\s*(\d+)min\s*([\d.]+)s"
    __ITERACAO = re.compile(r"^Iteracao\s+(\d+)\s+-\s+Backward:\s*" + __TEMPO)
    __FORWARD = re.compile(r"^\s*Forward:\s*" + __TEMPO)
    __TOTAL = re.compile(r"^\s*Total:\s*" + __TEMPO)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTemposIteracoesTim):
            return False
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        return bool(self.data.equals(o.data))

    @staticmethod
    def __tempo(m: "re.Match[str]", inicio: int) -> timedelta:
        return timedelta(
            hours=int(m.group(inicio)),
            minutes=int(m.group(inicio + 1)),
            seconds=float(m.group(inicio + 2)),
        )

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        iteracoes: List[int] = []
        backward: List[timedelta] = []
        forward: List[timedelta] = []
        total: List[timedelta] = []
        # Lê iterações enquanto as três linhas seguem o formato; a primeira
        # linha fora dele encerra o bloco.
        while True:
            m_iteracao = self.__ITERACAO.match(file.readline())
            if m_iteracao is None:
                break
            m_forward = self.__FORWARD.match(file.readline())
            if m_forward is None:
                break
            m_total = self.__TOTAL.match(file.readline())
            if m_total is None:
                break
            iteracoes.append(int(m_iteracao.group(1)))
            backward.append(self.__tempo(m_iteracao, 2))
            forward.append(self.__tempo(m_forward, 1))
            total.append(self.__tempo(m_total, 1))
        self.data = pd.DataFrame(
            data={
                "iteracao": iteracoes,
                "backward": backward,
                "forward": forward,
                "total": total,
            }
        )


class _BlocoLinhaTim(Block):
    """
    Bloco de uma única linha do cabeçalho do arquivo `newave.tim`.
    As subclasses definem `BEGIN_PATTERN` e `_converte`.
    """

    __slots__: List[str] = []

    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, _BlocoLinhaTim)
            and type(o) is type(self)
            and bool(self.data == o.data)
        )

    def _converte(self, linha: str) -> Any:
        raise NotImplementedError

    @staticmethod
    def _casa(
        padrao: "re.Pattern[str]", linha: str, propriedade: str
    ) -> "re.Match[str]":
        m = padrao.match(linha)
        if m is None:
            raise ValueError(
                f"{propriedade}: linha ilegível: {linha.strip()!r}"
            )
        return m

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        self.data = self._converte(file.readline())


class BlocoBibliotecaPLTim(_BlocoLinhaTim):
    """
    Bloco com a biblioteca de PLs do NEWAVE, escrita em uma linha
    própria no cabeçalho do arquivo `newave.tim`.
    """

    __slots__: List[str] = []

    BEGIN_PATTERN = r"^Biblioteca Solucao PLs:"

    def _converte(self, linha: str) -> str:
        return linha.split(":", 1)[1].strip()


class BlocoCasoTim(_BlocoLinhaTim):
    """
    Bloco com o nome do caso obtido no arquivo `newave.tim`.
    """

    __slots__: List[str] = []

    BEGIN_PATTERN = r"^Caso:"

    def _converte(self, linha: str) -> str:
        return linha.split(":", 1)[1].strip()


class BlocoDataHoraTim(_BlocoLinhaTim):
    """
    Bloco com uma data e hora do arquivo `newave.tim`, como
    `Data: 03-11-2026    Hora: 01h 15min 40.046sec`.
    """

    __slots__: List[str] = []

    BEGIN_PATTERN = r"^Data:"

    __PROPRIEDADES = "data_hora_inicio ou data_hora_inicio_politica"
    __DATA_HORA = re.compile(
        r"Data:\s*(\d{2})-(\d{2})-(\d{4})"
        r"\s+Hora:\s*(\d+)h\s*(\d+)min\s*(\d+)\.(\d+)sec"
    )

    def _converte(self, linha: str) -> datetime:
        dia, mes, ano, hora, minuto, segundo, fracao = self._casa(
            self.__DATA_HORA, linha, self.__PROPRIEDADES
        ).groups()
        try:
            return datetime(
                int(ano),
                int(mes),
                int(dia),
                int(hora),
                int(minuto),
                int(segundo),
                int(fracao.ljust(6, "0")),
            )
        except ValueError as e:
            raise ValueError(
                f"{self.__PROPRIEDADES}: data ilegível: {linha.strip()!r}"
            ) from e


class BlocoInicioPoliticaTim(_BlocoLinhaTim):
    """
    Bloco com a linha que antecede a data e hora do início do
    processo iterativo do cálculo da política, escrita por
    algumas versões do NEWAVE no arquivo `newave.tim`.
    """

    __slots__: List[str] = []

    BEGIN_PATTERN = r"^Inicio do processo iterativo"

    def _converte(self, linha: str) -> str:
        return linha.strip()


class BlocoNumeroProcessosTim(_BlocoLinhaTim):
    """
    Bloco com o número de processos e de nós do NEWAVE, como
    `Numero de Processos:  200 (    3 no(s) )`, obtidos no
    arquivo `newave.tim`. O dado é a tupla (processos, nós).
    """

    __slots__: List[str] = []

    BEGIN_PATTERN = r"^Numero de Processos:"

    __PROPRIEDADES = "numero_processos e numero_nos"
    __PROCESSOS = re.compile(
        r"^Numero de Processos:\s*(\d+)\s*\(\s*(\d+)\s*no\(s\)\s*\)"
    )

    def _converte(self, linha: str) -> Tuple[int, int]:
        m = self._casa(self.__PROCESSOS, linha, self.__PROPRIEDADES)
        return int(m.group(1)), int(m.group(2))


class BlocoTipoExecucaoTim(_BlocoLinhaTim):
    """
    Bloco com o tipo de execução do NEWAVE obtido no
    arquivo `newave.tim`.
    """

    __slots__: List[str] = []

    BEGIN_PATTERN = r"^Tipo de Execucao:"

    def _converte(self, linha: str) -> str:
        return linha.split(":", 1)[1].strip()


class BlocoIteracoesMinMaxTim(_BlocoLinhaTim):
    """
    Bloco com os números mínimo e máximo de iterações da política,
    como `Iteracoes:   50  50     ( Min/Max )`, obtidos no
    arquivo `newave.tim`. O dado é a tupla (mínimo, máximo).
    """

    __slots__: List[str] = []

    BEGIN_PATTERN = r"^\s+Iteracoes:\s+\d+\s+\d+\s+\(\s*Min/Max"

    __PROPRIEDADES = "iteracoes_minimo e iteracoes_maximo"
    __ITERACOES = re.compile(r"^\s+Iteracoes:\s+(\d+)\s+(\d+)\s+\(\s*Min/Max")

    def _converte(self, linha: str) -> Tuple[int, int]:
        m = self._casa(self.__ITERACOES, linha, self.__PROPRIEDADES)
        return int(m.group(1)), int(m.group(2))
