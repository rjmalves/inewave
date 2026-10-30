# Imports de módulos externos
from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from datetime import timedelta
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from typing import Any, IO, List, Optional
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

    __slots__ = ["__linha"]

    BEGIN_PATTERN = r"            Versao "
    END_PATTERN = ""

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(16, 78)])

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
            return self.data == bloco.data

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        self.data = self.__linha.read(file.readline())[0]


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
