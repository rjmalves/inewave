from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore

from inewave.config import MAX_ANOS_ESTUDO, MAX_UHES, MESES_DF


class BlocoDsvUHE(Section):
    """
    Bloco de informações do desvio de água por
    usina no arquivo do NEWAVE `dsvagua.dat`.
    """

    FIM_BLOCO = "9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campos_iniciais: List[Field] = [IntegerField(4, 0), IntegerField(3, 6)]
        campos_desvios: List[Field] = [
            FloatField(6, 10 + 7 * i, 2) for i in range(len(MESES_DF))
        ]
        campos_finais: List[Field] = [
            IntegerField(4, 94),
            LiteralField(33, 103),
        ]
        self.__linha_uhe = Line(
            campos_iniciais + campos_desvios + campos_finais
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDsvUHE):
            return False
        bloco: BlocoDsvUHE = o
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
        def converte_tabela_em_df() -> pd.DataFrame:
            cols = ["Ano", "Usina"] + MESES_DF + ["Flag"]
            df = pd.DataFrame(
                tabela,
                columns=cols,
            )
            df["Comentário"] = comentarios
            df = df.astype({"Ano": "int64", "Usina": "int64", "Flag": "int64"})
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_UHES * MAX_ANOS_ESTUDO, len(MESES_DF) + 3))
        comentarios: List[str] = []
        while True:
            linha = file.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3 or BlocoDsvUHE.FIM_BLOCO in linha:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha_uhe.read(linha)
            tabela[i, :] = dados[: len(MESES_DF) + 3]
            comentarios.append(dados[-1])
            i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do confhd.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            file.write(self.__linha_uhe.write(lin.tolist()))
        file.write(BlocoDsvUHE.FIM_BLOCO + "\n")
