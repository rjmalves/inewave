# Imports de módulos externos
from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from datetime import timedelta
import pandas as pd  # type: ignore
from typing import IO, List


class BlocoTemposEtapasTim(Block):
    """
    Bloco com as informações de tempo de execução
    do NEWAVE obtidas no arquivo `newave.tim`.
    """

    __slots__ = ["__line"]

    BEGIN_PATTERN = "Leitura de Dados:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(data={"etapa": etapas, "tempo": tempos})
            return df

        # Variáveis auxiliares
        etapas: List[str] = []
        tempos: List[timedelta] = []

        # Leitura das etapas
        for _ in range(5):
            dados = self.__line.read(file.readline())
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

    def __init__(self, previous=None, next=None, data=None) -> None:
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
    def read(self, file: IO, *args, **kwargs):
        self.data = self.__linha.read(file.readline())[0]
