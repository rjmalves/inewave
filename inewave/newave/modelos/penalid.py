from inewave.config import MAX_REES, MAX_VARIAVEIS_FOLGA_PENALIDADE

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
                IntegerField(2, 42),
                FloatField(8, 46, 2),
                FloatField(8, 56, 2),
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
    def read(
        self, file: IO, numero_patamares_penalidade: int = 2, *args, **kwargs
    ):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                data={
                    "variavel": repete_vetor(
                        chaves, self.__numero_patamares_penalidade
                    ),
                    "codigo_ree_submercado": repete_vetor(
                        codigos_ree_submercado,
                        self.__numero_patamares_penalidade,
                    ),
                    "patamar_penalidade": np.tile(
                        np.arange(1, self.__numero_patamares_penalidade + 1),
                        len(chaves),
                    ),
                    "patamar_carga": repete_vetor(
                        patamares_carga, self.__numero_patamares_penalidade
                    ),
                    "valor_R$_MWh": tabela_MWh.flatten(),
                    "valor_R$_hm3": tabela_hm3.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        self.__numero_patamares_penalidade = numero_patamares_penalidade

        i = 0
        chaves: List[str] = []
        codigos_ree_submercado: List[int] = []
        patamares_carga: List[int] = []
        tabela_MWh = np.zeros((MAX_REES * MAX_VARIAVEIS_FOLGA_PENALIDADE, 2))
        tabela_hm3 = np.zeros((MAX_REES * MAX_VARIAVEIS_FOLGA_PENALIDADE, 2))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3:
                # Converte para df e salva na variável
                if i > 0:
                    tabela_MWh = tabela_MWh[:i, :]
                    tabela_hm3 = tabela_hm3[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                chaves.append(dados[0])
                codigos_ree_submercado.append(dados[3])
                patamares_carga.append(dados[4])
                tabela_MWh[i, :] = dados[1:3]
                tabela_hm3[i, :] = dados[5:7]
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do penalid.dat não foram lidos com sucesso"
            )

        df = self.data.copy()
        for _, linha_penalidade in (
            self.data[
                [
                    "variavel",
                    "codigo_ree_submercado",
                    "patamar_carga",
                ]
            ]
            .drop_duplicates()
            .iterrows()
        ):
            df_penalid = df.loc[df["variavel"] == linha_penalidade["variavel"]]
            if linha_penalidade["codigo_ree_submercado"] is not None:
                df_penalid = df_penalid.loc[
                    df_penalid["codigo_ree_submercado"]
                    == linha_penalidade["codigo_ree_submercado"]
                ]
            if linha_penalidade["patamar_carga"] is not None:
                df_penalid = df_penalid.loc[
                    df_penalid["patamar_carga"]
                    == linha_penalidade["patamar_carga"]
                ]
            file.write(
                self.__linha.write(
                    [
                        df_penalid["variavel"].iloc[0],
                    ]
                    + df_penalid.sort_values("patamar_penalidade")[
                        "valor_R$_MWh"
                    ].tolist()
                    + [
                        df_penalid["codigo_ree_submercado"].iloc[0],
                        df_penalid["patamar_carga"].iloc[0],
                    ]
                    + df_penalid.sort_values("patamar_penalidade")[
                        "valor_R$_hm3"
                    ].tolist()
                )
            )
