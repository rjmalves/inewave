# Imports de módulos externos
from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List, Optional


class BlocoVersaoModeloSimfinal(Block):
    """
    Bloco com a versão do modelo localizado no arquivo `pmo.dat`.
    """

    __slots__ = ["__line"]

    BEGIN_PATTERN = (
        " CEPEL                         MODELO ESTRATEGICO DE"
        + " GERACAO HIDROTERMICA A SUBSISTEMAS              VERSAO"
    )
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)

        self.__line = Line([LiteralField(18, 109)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoVersaoModeloSimfinal):
            return False
        bloco: BlocoVersaoModeloSimfinal = o
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

        linha = file.readline()
        dados: List[str] = self.__line.read(linha)
        self.data = dados[0].strip()


class BlocoCustoOperacaoSimfinal(Block):
    """
    Bloco de informações sobre os custos de operação categorizados
    existentes no arquivo `pmo.dat`.
    """

    __slots__ = ["__line"]

    BEGIN_PATTERN = "PARCELA           V.ESPERADO"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        self.__line = Line(
            [
                LiteralField(18, 13),
                FloatField(13, 32, 2),
                FloatField(13, 46, 2),
                FloatField(7, 60, 2),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCustoOperacaoSimfinal):
            return False
        bloco: BlocoCustoOperacaoSimfinal = o
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
            cols = ["valor_esperado", "desvio_padrao", "percentual"]
            df = pd.DataFrame(tabela, columns=cols)
            df["parcela"] = parcelas
            df = df[["parcela"] + cols]
            return df

        # Salta duas linhas
        for _ in range(2):
            file.readline()
        parcelas: List[str] = []
        tabela = np.zeros((100, 3), dtype=np.float64)
        i = 0
        while True:
            linha = file.readline()
            if "----------------" in linha:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            dados_linha = self.__line.read(linha)
            parcelas.append(dados_linha[0])
            tabela[i, :] = dados_linha[1:]
            i += 1


class BlocoCustoOperacaoTotalSimfinal(Block):
    """
    Bloco de informações sobre os custos de operação categorizados
    existentes no arquivo `pmo.dat`.
    """

    __slots__ = ["__line"]

    BEGIN_PATTERN = "           VALOR ESPERADO TOTAL:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        self.__line = Line([FloatField(24, 50, 2)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCustoOperacaoTotalSimfinal):
            return False
        bloco: BlocoCustoOperacaoTotalSimfinal = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return all([sd == d for sd, d in zip(self.data, bloco.data)])

    # Override
    def read(self, file: IO, *args, **kwargs):
        data = [0, 0]
        for i in range(2):
            data[i] = self.__line.read(file.readline())[0]
        self.data = data