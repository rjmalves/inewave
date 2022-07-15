from inewave.config import MAX_REES

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class BlocoReesSubmercados(Section):
    """
    Bloco com informações dos REEs e suas relações com os
    submercados.
    """

    FIM_BLOCO = "999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
                LiteralField(10, 5),
                IntegerField(3, 18),
                IntegerField(2, 23),
                IntegerField(4, 26),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoReesSubmercados):
            return False
        bloco: BlocoReesSubmercados = o
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
    def read(self, file: IO):
        def converte_tabela_em_df():
            cols = [
                "Número",
                "Submercado",
                "Mês Fim Individualizado",
                "Ano Fim Individualizado",
            ]
            df = pd.DataFrame(tabela, columns=cols)
            df["Nome"] = nomes
            df = df.astype({"Submercado": np.int64, "Número": np.int64})
            df = df[
                [
                    "Número",
                    "Nome",
                    "Submercado",
                    "Mês Fim Individualizado",
                    "Ano Fim Individualizado",
                ]
            ]
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        nomes: List[str] = []
        tabela = np.zeros((MAX_REES, 4))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoReesSubmercados.FIM_BLOCO in linha:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                tabela[i, :] = [dados[0]] + dados[2:]
                nomes.append(dados[1])
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do ree.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            linha_escrita = lin.tolist()
            for i, v in enumerate(linha_escrita[2:], start=2):
                linha_escrita[i] = None if np.isnan(v) else int(v)
            file.write(self.__linha.write(linha_escrita))
        file.write(BlocoReesSubmercados.FIM_BLOCO + "\n")


class BlocoFicticiasIndividualizado(Section):
    """
    Bloco com a opção de remover usinas fictícias nos
    períodos individualizados.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(20, 0), IntegerField(4, 21)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoFicticiasIndividualizado):
            return False
        bloco: BlocoFicticiasIndividualizado = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))
