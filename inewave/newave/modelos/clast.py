from inewave.config import MAX_UTES

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.datetimefield import DatetimeField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from datetime import datetime
from inewave._utils.formatacao import (
    repete_vetor,
)


class BlocoUTEClasT(Section):
    """
    Bloco com informações de cargas adicionais por mês/ano
    e por subsistema.
    """

    FIM_BLOCO = " 9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campos_ute: List[Field] = [
            IntegerField(4, 1),
            LiteralField(12, 6),
            LiteralField(12, 19),
        ]
        campos_custos: List[Field] = [
            FloatField(8, 29 + 8 * i, 2) for i in range(5)
        ]
        self.__linha = Line(campos_ute + campos_custos)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoUTEClasT):
            return False
        bloco: BlocoUTEClasT = o
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
        self, file: IO, numero_anos_planejamento: int = 5, *args, **kwargs
    ):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                data={
                    "codigo_usina": repete_vetor(
                        codigo_ute, self.__numero_anos_planejamento
                    ),
                    "nome_usina": repete_vetor(
                        nome_ute, self.__numero_anos_planejamento
                    ),
                    "tipo_combustivel": repete_vetor(
                        tipo_combustivel, self.__numero_anos_planejamento
                    ),
                    "indice_ano_estudo": np.tile(
                        np.arange(1, self.__numero_anos_planejamento + 1),
                        len(codigo_ute),
                    ),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        self.__numero_anos_planejamento = numero_anos_planejamento

        # Variáveis auxiliares
        codigo_ute: List[int] = []
        nome_ute: List[str] = []
        tipo_combustivel: List[str] = []
        tabela = np.zeros((MAX_UTES, self.__numero_anos_planejamento))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                break
            if BlocoUTEClasT.FIM_BLOCO in linha:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            tabela[i, :] = dados[3:]
            codigo_ute.append(dados[0])
            nome_ute.append(dados[1])
            tipo_combustivel.append(dados[2])
            i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do clast.dat não foram lidos com sucesso")

        df = self.data.copy()
        for _, linha_usina in (
            self.data[["codigo_usina", "nome_usina", "tipo_combustivel"]]
            .drop_duplicates()
            .iterrows()
        ):
            df_ute = df.loc[
                (df["codigo_usina"] == linha_usina["codigo_usina"])
            ]
            file.write(
                self.__linha.write(
                    [
                        df_ute["codigo_usina"].iloc[0],
                        df_ute["nome_usina"].iloc[0],
                        df_ute["tipo_combustivel"].iloc[0],
                    ]
                    + df_ute.sort_values("indice_ano_estudo")["valor"].tolist()
                )
            )
        file.write(BlocoUTEClasT.FIM_BLOCO + "\n")


class BlocoModificacaoUTEClasT(Section):
    """
    Bloco de modificações das informações das
    usinas cadastradas no arquivo do NEWAVE `clast.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campos_modificacao: List[Field] = [
            IntegerField(4, 1),
            FloatField(7, 8, 2),
            DatetimeField(7, 17, format="%m %Y"),
            DatetimeField(7, 26, format="%m %Y"),
            LiteralField(12, 35),
        ]
        self.__linha = Line(campos_modificacao)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoModificacaoUTEClasT):
            return False
        bloco: BlocoModificacaoUTEClasT = o
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
            df = pd.DataFrame(
                data={
                    "codigo_usina": codigo_ute,
                    "nome_usina": nomes,
                    "data_inicio": datas_inicio,
                    "data_fim": datas_fim,
                    "custo": custo,
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Variáveis auxiliares
        codigo_ute: List[int] = []
        custo: List[float] = []
        datas_inicio: List[datetime] = []
        datas_fim: List[datetime] = []
        nomes: List[str] = []
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                if len(codigo_ute) > 0:
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            codigo_ute.append(dados[0])
            custo.append(dados[1])
            datas_inicio.append(dados[2])
            datas_fim.append(dados[3])
            nomes.append(dados[4])

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do clast.dat não foram lidos com sucesso")

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            file.write(
                self.__linha.write(
                    linha_lida[
                        [
                            "codigo_usina",
                            "custo",
                            "data_inicio",
                            "data_fim",
                            "nome_usina",
                        ]
                    ].tolist()
                )
            )
