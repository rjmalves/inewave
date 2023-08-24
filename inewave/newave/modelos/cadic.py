from inewave.config import (
    MAX_ANOS_ESTUDO,
    MAX_SUBMERCADOS,
    MESES_DF,
)

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from inewave._utils.formatacao import (
    prepara_vetor_anos_tabela,
    prepara_valor_ano,
    repete_vetor,
)


class BlocoCargasAdicionais(Section):
    """
    Bloco com informações de cargas adicionais por mês/ano
    e por subsistema.
    """

    FIM_BLOCO = " 999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line(
            [IntegerField(3, 1), LiteralField(10, 6), LiteralField(12, 21)]
        )
        campo_ano: List[Field] = [LiteralField(4, 0)]
        campos_cargas: List[Field] = [
            FloatField(8, 6 + 8 * i, 0) for i in range(len(MESES_DF))
        ]
        self.__linha_cargas = Line(campo_ano + campos_cargas)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCargasAdicionais):
            return False
        bloco: BlocoCargasAdicionais = o
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
                    "codigo_submercado": repete_vetor(codigo_subsis),
                    "nome_submercado": repete_vetor(nome_subsis),
                    "razao": repete_vetor(razao),
                    "data": prepara_vetor_anos_tabela(anos),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Variáveis auxiliares
        codigo_subsis: List[int] = []
        nome_subsis: List[str] = []
        razao: List[str] = []
        anos: List[str] = []
        codigo_atual = 0
        nome_atual = ""
        razao_atual = ""
        tabela = np.zeros((MAX_ANOS_ESTUDO * MAX_SUBMERCADOS, len(MESES_DF)))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                break
            if BlocoCargasAdicionais.FIM_BLOCO in linha:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            if len(linha.strip()) < 80:
                (
                    codigo_atual,
                    nome_atual,
                    razao_atual,
                ) = self.__linha_subsis.read(linha)
            else:
                dados = self.__linha_cargas.read(linha)
                tabela[i, :] = dados[1:]
                codigo_subsis.append(codigo_atual)
                nome_subsis.append(nome_atual)
                razao.append(razao_atual)
                anos.append(dados[0])
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        ultimo_codigo = 0
        ultimo_subsis = ""
        ultima_razao = ""
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do c_adic.dat não foram lidos com sucesso")

        # Separa os valores de cada submercado, razao, ano
        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for _, linha_razao in (
            df[["codigo_submercado", "nome_submercado", "razao", "ano"]]
            .drop_duplicates()
            .iterrows()
        ):
            df_razao = df.loc[
                (df["codigo_submercado"] == linha_razao["codigo_submercado"])
                & (df["razao"] == linha_razao["razao"])
                & (df["ano"] == linha_razao["ano"])
            ]
            df_razao = df_razao.sort_values(["data"])
            if any(
                [
                    linha_razao["codigo_submercado"] != ultimo_codigo,
                    linha_razao["nome_submercado"] != ultimo_subsis,
                    linha_razao["razao"] != ultima_razao,
                ]
            ):
                ultimo_codigo = linha_razao["codigo_submercado"]
                ultimo_subsis = linha_razao["nome_submercado"]
                ultima_razao = linha_razao["razao"]
                file.write(
                    self.__linha_subsis.write(
                        linha_razao[
                            [
                                "codigo_submercado",
                                "nome_submercado",
                                "razao",
                            ]
                        ].tolist()
                    )
                )
            ano = prepara_valor_ano(linha_razao["ano"])
            valores = df_razao["valor"].tolist()
            file.write(self.__linha_cargas.write([ano] + valores))

        file.write(BlocoCargasAdicionais.FIM_BLOCO)
