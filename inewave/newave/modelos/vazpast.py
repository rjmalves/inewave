from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from inewave._utils.formatacao import (
    repete_vetor,
)
from inewave.config import MAX_UHES, MESES_DF


class BlocoVazPast(Section):
    """
    Bloco de informações de vazões passadas
    por usina, existentes no arquivo `vazpast.dat`
    do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [IntegerField(4, 1), LiteralField(12, 6)]
            + [FloatField(10, 18 + 10 * i, 2) for i in range(len(MESES_DF))]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoVazPast):
            return False
        bloco: BlocoVazPast = o
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
            df = pd.DataFrame(
                data={
                    "codigo_usina": repete_vetor(codigos_usinas),
                    "nome_usina": repete_vetor(nomes_usinas),
                    "mes": np.tile(np.arange(1, 13), len(nomes_usinas)),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_UHES, len(MESES_DF)))
        codigos_usinas: List[int] = []
        nomes_usinas: List[str] = []
        while True:
            linha = file.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            codigos_usinas.append(dados[0])
            nomes_usinas.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do vazpast.dat não foram lidos com sucesso"
            )

        df = self.data.copy()
        usinas = self.data["codigo_usina"].unique()
        for usina in usinas:
            df_usina = df.loc[(df["codigo_usina"] == usina)]
            df_usina = df_usina.sort_values(["mes"])
            file.write(
                self.__linha.write(
                    [
                        df_usina["codigo_usina"].iloc[0],
                        df_usina["nome_usina"].iloc[0],
                    ]
                    + df_usina["valor"].tolist()
                )
            )
