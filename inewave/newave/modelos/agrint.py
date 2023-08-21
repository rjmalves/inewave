from inewave.config import (
    MAX_AGRUPAMENTOS_INTERCAMBIOS,
    MAX_SUBMERCADOS,
    MAX_MESES_ESTUDO,
)

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.datetimefield import DatetimeField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
from datetime import datetime
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class BlocoGruposAgrint(Section):
    """
    Bloco com informações dos intercâmbios pertencentes aos
    grupos.
    """

    FIM_BLOCO = " 999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
                IntegerField(3, 5),
                IntegerField(3, 9),
                FloatField(7, 13, 4),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoGruposAgrint):
            return False
        bloco: BlocoGruposAgrint = o
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
        def converte_tabela_em_df():
            cols = [
                "agrupamento",
                "submercado_de",
                "submercado_para",
                "coeficiente",
            ]
            df = pd.DataFrame(tabela, columns=cols)
            df = df.astype(
                {
                    "agrupamento": "int64",
                    "submercado_de": "int64",
                    "submercado_para": "int64",
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_AGRUPAMENTOS_INTERCAMBIOS * MAX_SUBMERCADOS, 4))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoGruposAgrint.FIM_BLOCO in linha[:4]:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                tabela[i, :] = dados
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do agrint.dat não foram lidos com sucesso")

        for _, linha in self.data.iterrows():
            linha_escrita = []
            for v in linha:
                linha_escrita.append(None if np.isnan(v) else int(v))
            file.write(self.__linha.write(linha_escrita))
        file.write(BlocoGruposAgrint.FIM_BLOCO + "\n")


class BlocoLimitesPorGrupoAgrint(Section):
    """
    Bloco com informações de configuração dos limites dos agrupamentos
    de intercâmbio por período de estudo.
    """

    FIM_BLOCO = " 999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
                DatetimeField(7, 6, format="%m %Y"),
                DatetimeField(7, 14, format="%m %Y"),
                FloatField(7, 22, 0),
                FloatField(7, 30, 0),
                FloatField(7, 38, 0),
                LiteralField(40, 50),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoLimitesPorGrupoAgrint):
            return False
        bloco: BlocoLimitesPorGrupoAgrint = o
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
        def converte_tabela_em_df():
            cols = [
                "agrupamento",
                "limite_p1",
                "limite_p2",
                "limite_p3",
            ]
            df = pd.DataFrame(tabela, columns=cols)
            df["comentario"] = comentarios
            df["data_inicio"] = datas_inicio
            df["data_fim"] = datas_fim
            df = df.astype(
                {
                    "agrupamento": "int64",
                }
            )
            return df[
                [
                    "agrupamento",
                    "data_inicio",
                    "data_fim",
                    "limite_p1",
                    "limite_p2",
                    "limite_p3",
                    "comentario",
                ]
            ]

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        datas_inicio: List[datetime] = []
        datas_fim: List[datetime] = []
        comentarios: List[str] = []
        tabela = np.zeros(
            (MAX_AGRUPAMENTOS_INTERCAMBIOS * MAX_MESES_ESTUDO, 4)
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoGruposAgrint.FIM_BLOCO in linha[:4]:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                tabela[i, 0] = dados[0]
                tabela[i, 1:] = dados[3:6]
                datas_inicio.append(dados[1])
                datas_fim.append(dados[2])
                comentarios.append(dados[-1])
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do agrint.dat não foram lidos com sucesso")

        for _, dados_linhas in self.data.iterrows():
            file.write(self.__linha.write(dados_linhas))
        file.write(BlocoGruposAgrint.FIM_BLOCO + "\n")
