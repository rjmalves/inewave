from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore

from inewave.config import MESES_DF, MAX_UTES
from inewave._utils.formatacao import (
    repete_vetor,
)


class BlocoTermUTE(Section):
    """
    Bloco de informações das classes de usinas térmicas
    existentes no arquivo do NEWAVE `term.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
                LiteralField(12, 5),
                FloatField(5, 19, 0),
                FloatField(4, 25, 0),
                FloatField(6, 31, 2),
                FloatField(6, 38, 2),
            ]
            + [FloatField(6, 45 + 7 * i, 2) for i in range(len(MESES_DF) + 1)]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTermUTE):
            return False
        bloco: BlocoTermUTE = o
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
                    "codigo_usina": repete_vetor(numeros, len(MESES_DF) + 1),
                    "nome_usina": repete_vetor(nomes, len(MESES_DF) + 1),
                    "potencia_instalada": repete_vetor(
                        potencias, len(MESES_DF) + 1
                    ),
                    "fator_capacidade_maximo": repete_vetor(
                        fatores_capacidade, len(MESES_DF) + 1
                    ),
                    "teif": repete_vetor(teifs, len(MESES_DF) + 1),
                    "indisponibilidade_programada": repete_vetor(
                        indisponibilidades_programadas, len(MESES_DF) + 1
                    ),
                    "mes": np.tile(
                        np.arange(1, len(MESES_DF) + 2), len(numeros)
                    ),
                    "geracao_minima": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_UTES, len(MESES_DF) + 1))
        numeros: List[int] = []
        nomes: List[str] = []
        potencias: List[float] = []
        fatores_capacidade: List[float] = []
        teifs: List[float] = []
        indisponibilidades_programadas: List[float] = []
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
            tabela[i, :] = dados[6:]
            numeros.append(dados[0])
            nomes.append(dados[1])
            potencias.append(dados[2])
            fatores_capacidade.append(dados[3])
            teifs.append(dados[4])
            indisponibilidades_programadas.append(dados[5])
            i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do term.dat não foram lidos com sucesso")

        df = self.data.copy()
        for _, linha_usina in (
            df[
                [
                    "codigo_usina",
                    "nome_usina",
                    "potencia_instalada",
                    "fator_capacidade_maximo",
                    "teif",
                    "indisponibilidade_programada",
                ]
            ]
            .drop_duplicates()
            .iterrows()
        ):
            df_usina = df.loc[
                df["codigo_usina"] == linha_usina["codigo_usina"]
            ]

            file.write(
                self.__linha.write(
                    linha_usina.tolist()
                    + df_usina.sort_values("mes")["geracao_minima"].tolist()
                )
            )
