from inewave.config import MAX_LAG_ADTERM, MAX_UTES

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from inewave._utils.formatacao import (
    repete_vetor,
)


class BlocoUTEAdTerm(Section):
    """
    Bloco com os despachos antecipados das UTEs por patamar.
    """

    FIM_BLOCO = " 9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_ute = Line(
            [IntegerField(4, 1), LiteralField(12, 7), IntegerField(1, 21)]
        )
        self.__linha_despachos = Line([])
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoUTEAdTerm):
            return False
        bloco: BlocoUTEAdTerm = o
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
    def read(self, file: IO, numero_patamares: int = 3, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                data={
                    "codigo_usina": repete_vetor(
                        codigo_utes, self.__numero_patamares
                    ),
                    "nome_usina": repete_vetor(
                        nome_utes, self.__numero_patamares
                    ),
                    "lag": repete_vetor(lag_utes, self.__numero_patamares),
                    "patamar": np.tile(
                        np.arange(1, self.__numero_patamares + 1),
                        len(codigo_utes),
                    ),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        self.__numero_patamares = numero_patamares
        self.__linha_despachos = Line(
            [
                FloatField(12, 22 + 12 * i, 2)
                for i in range(self.__numero_patamares)
            ]
        )

        # Variáveis auxiliares
        codigo_utes: List[int] = []
        nome_utes: List[str] = []
        lag_utes: List[int] = []
        codigo_atual = 0
        nome_atual = ""
        lag_atual = 0
        tabela = np.zeros((MAX_UTES * MAX_LAG_ADTERM, self.__numero_patamares))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                break
            if BlocoUTEAdTerm.FIM_BLOCO in linha:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, confere se é uma linha de UTE ou despacho
            if len(linha[:5].strip()) > 0:
                codigo_atual, nome_atual, lag_atual = self.__linha_ute.read(
                    linha
                )
                lag_atual = 0
            else:
                lag_atual += 1
                tabela[i, :] = self.__linha_despachos.read(linha)
                codigo_utes.append(codigo_atual)
                nome_utes.append(nome_atual)
                lag_utes.append(lag_atual)
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do adterm.dat não foram lidos com sucesso")
        df = self.data.copy()
        ultima_ute = 0
        for _, linha_usina in (
            self.data[["codigo_usina", "lag"]].drop_duplicates().iterrows()
        ):
            df_lag = df.loc[
                (df["codigo_usina"] == linha_usina["codigo_usina"])
                & (df["lag"] == linha_usina["lag"])
            ]
            if df_lag["codigo_usina"].iloc[0] != ultima_ute:
                ultima_ute = df_lag["codigo_usina"].iloc[0]
                max_lag_usina = df.loc[
                    df["codigo_usina"] == ultima_ute, "lag"
                ].max()
                file.write(
                    self.__linha_ute.write(
                        df_lag[["codigo_usina", "nome_usina"]]
                        .iloc[0, :]
                        .tolist()
                        + [max_lag_usina]
                    )
                )
            file.write(
                self.__linha_despachos.write(
                    df_lag.sort_values("patamar")["valor"].tolist()
                )
            )
        file.write(BlocoUTEAdTerm.FIM_BLOCO + "\n")
