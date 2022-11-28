from inewave.config import MAX_CORTES, MAX_UHES

from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class EstadosPeriodoNwlistcf(Block):
    """
    Bloco do arquivo estados.rel que armazena os estados visitados
    por período na construção dos cortes da FCF.
    """

    BEGIN_PATTERN = "PERIODO: "
    END_PATTERN = "PERIODO: "

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_periodo = Line([IntegerField(4, 19)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, EstadosPeriodoNwlistcf):
            return False
        bloco: EstadosPeriodoNwlistcf = o
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
            df = pd.DataFrame(tabela, columns=campos_cabecalho)
            df = df.astype(
                {
                    "IREG": "int64",
                    "ITEc": "int64",
                    "SIMc": "int64",
                    "ITEf": "int64",
                    "REE": "int64",
                }
            )
            df["PERIODO"] = self.__periodo
            df = df[["PERIODO"] + campos_cabecalho]
            df = df.fillna(0.0)
            return df

        # Lê o período e as linhas de cabeçalho
        self.__periodo = self.__linha_periodo.read(file.readline())[0]
        file.readline()
        cabecalho = file.readline()
        campos_cabecalho = [c for c in cabecalho.split("  ")]
        campos_cabecalho = [c.strip() for c in campos_cabecalho]
        campos_cabecalho = [c for c in campos_cabecalho if len(c) > 1]
        campos_cabecalho = [c.replace(" ", "") for c in campos_cabecalho]
        campos_cabecalho = (
            [campos_cabecalho[0]]
            + [
                campos_cabecalho[1][:4],
                campos_cabecalho[1][4:8],
                campos_cabecalho[1][8:],
            ]
            + campos_cabecalho[2:]
        )
        campos_iniciais: List[Field] = [
            IntegerField(8, 2),
            IntegerField(4, 11),
            IntegerField(4, 16),
            IntegerField(4, 21),
            IntegerField(4, 26),
            FloatField(17, 31, 4),
        ]
        campos_pis: List[Field] = [
            FloatField(17, 49 + 18 * i, 9)
            for i in range(len(campos_cabecalho) - len(campos_iniciais))
        ]
        self.__linha = Line(campos_iniciais + campos_pis)

        # Lê as linhas de cortes
        self.__ireg_atual = 0
        self.__itec_atual = 0
        self.__simc_atual = 0
        self.__itef_atual = 0
        tabela = np.zeros((MAX_CORTES * MAX_UHES, len(campos_cabecalho)))
        i = 0
        while True:
            ultima_posicao = file.tell()
            linha = file.readline()
            if self.ends(linha) or len(linha) < 3:
                file.seek(ultima_posicao)
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            if dados[0] is not None:
                self.__ireg_atual = dados[0]
            if dados[1] is not None:
                self.__itec_atual = dados[1]
            if dados[2] is not None:
                self.__simc_atual = dados[2]
            if dados[3] is not None:
                self.__itef_atual = dados[3]
            tabela[i, 0] = self.__ireg_atual
            tabela[i, 1] = self.__itec_atual
            tabela[i, 2] = self.__simc_atual
            tabela[i, 3] = self.__itef_atual
            tabela[i, 4:] = dados[4:]
            i += 1
