from inewave.config import MAX_LAG_ADTERM, MAX_UTES

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


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
    def read(self, file: IO):
        def converte_tabela_em_df():
            cols = [f"Patamar {i}" for i in range(1, n_pat + 1)]
            df = pd.DataFrame(tabela, columns=cols)
            df["Código UTE"] = codigo_utes
            df["Nome UTE"] = nome_utes
            df["Lag"] = lag_utes
            df = df[["Código UTE", "Nome UTE", "Lag"] + cols]
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Obtem o número de patamares e constroi a linha de despachos
        n_pat = len(
            [
                s.strip()
                for s in self.__cabecalhos[1].split(" ")
                if "XXXXXXX.XX" in s
            ]
        )
        self.__linha_despachos = Line(
            [FloatField(12, 22 + 12 * i, 2) for i in range(n_pat)]
        )

        # Variáveis auxiliares
        codigo_utes: List[int] = []
        nome_utes: List[str] = []
        lag_utes: List[int] = []
        codigo_atual = 0
        nome_atual = ""
        lag_atual = 0
        tabela = np.zeros((MAX_UTES * MAX_LAG_ADTERM, n_pat))
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
            else:
                tabela[i, :] = self.__linha_despachos.read(linha)
                codigo_utes.append(codigo_atual)
                nome_utes.append(nome_atual)
                lag_utes.append(lag_atual)
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do adterm.dat não foram lidos com sucesso")

        ultima_ute = 0
        cols_despachos = [c for c in list(self.data.columns) if "Patamar" in c]
        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if linha_lida["Código UTE"] != ultima_ute:
                ultima_ute = linha_lida["Código UTE"]
                file.write(
                    self.__linha_ute.write(
                        linha_lida[["Código UTE", "Nome UTE", "Lag"]].tolist()
                    )
                )
            file.write(
                self.__linha_despachos.write(
                    linha_lida[cols_despachos].tolist()
                )
            )
        file.write(BlocoUTEAdTerm.FIM_BLOCO + "\n")
