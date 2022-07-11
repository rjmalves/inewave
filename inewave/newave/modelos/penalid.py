from inewave.config import MAX_REES

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class BlocoPenalidades(Section):
    """
    Bloco com informações das penalidades por violação de restrições
    e outras ações.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(6, 1),
                FloatField(8, 14, 2),
                FloatField(8, 24, 2),
                IntegerField(3, 36),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoPenalidades):
            return False
        bloco: BlocoPenalidades = o
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
                "Penalidade 1",
                "Penalidade 2",
                "Subsistema",
            ]
            df = pd.DataFrame(tabela, columns=cols)
            df["Chave"] = chaves
            df = df[
                [
                    "Chave",
                    "Penalidade 1",
                    "Penalidade 2",
                    "Subsistema",
                ]
            ]
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        chaves: List[str] = []
        # TODO - remover o 5 mágico abaixo
        tabela = np.zeros((MAX_REES * 5, 3))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                tabela[i, :] = dados[1:]
                chaves.append(dados[0])
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do penalid.dat não foram lidos com sucesso"
            )

        for _, lin in self.data.iterrows():
            linha_escrita = lin.tolist()
            for i, v in enumerate(linha_escrita[1:], start=1):
                linha_escrita[i] = None if np.isnan(v) else v
            if linha_escrita[3] is not None:
                linha_escrita[3] = int(linha_escrita[3])
            file.write(self.__linha.write(linha_escrita))
