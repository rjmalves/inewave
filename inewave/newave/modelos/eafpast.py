from typing import IO, List

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.section import Section

from inewave._utils.formatacao import (
    repete_vetor,
)
from inewave.config import MAX_REES, MESES_DF


class BlocoEafPast(Section):
    """
    Bloco de informações de vazões passadas
    por REE, existentes no arquivo `eafpast.dat`
    do NEWAVE.
    """

    __slots__ = ["__linha", "__cabecalhos"]

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [IntegerField(4, 0), LiteralField(10, 5)]
            + [FloatField(11, 15 + 11 * i, 2) for i in range(len(MESES_DF))]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEafPast):
            return False
        bloco: BlocoEafPast = o
        if not all([
            isinstance(self.data, pd.DataFrame),
            isinstance(o.data, pd.DataFrame),
        ]):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(
                data={
                    "codigo_ree": repete_vetor(codigos_rees),
                    "nome_ree": repete_vetor(nomes_rees),
                    "mes": np.tile(np.arange(1, 13), len(nomes_rees)),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_REES, len(MESES_DF)))
        codigos_rees: List[int] = []
        nomes_rees: List[str] = []
        while True:
            linha = file.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]  # type: ignore
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            codigos_rees.append(dados[0])
            nomes_rees.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do eafpast.dat não foram lidos com sucesso")

        df = self.data.copy()
        rees = self.data["codigo_ree"].unique()
        for ree in rees:
            df_ree = df.loc[(df["codigo_ree"] == ree)]
            df_ree = df_ree.sort_values(["mes"])
            file.write(
                self.__linha.write(
                    [df_ree["codigo_ree"].iloc[0], df_ree["nome_ree"].iloc[0]]
                    + df_ree["valor"].tolist()
                )
            )
