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
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=MESES_DF)
            df["Código Subsistema"] = codigo_subsis
            df["Nome Subsistema"] = nome_subsis
            df["Razão"] = razao
            df["Ano"] = anos
            df = df[
                ["Código Subsistema", "Nome Subsistema", "Razão", "Ano"]
                + MESES_DF
            ]
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
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        ultimo_codigo = 0
        ultimo_subsis = ""
        ultima_razao = ""
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do c_adic.dat não foram lidos com sucesso")

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if any(
                [
                    linha_lida["Código Subsistema"] != ultimo_codigo,
                    linha_lida["Nome Subsistema"] != ultimo_subsis,
                    linha_lida["Razão"] != ultima_razao,
                ]
            ):
                ultimo_codigo = linha_lida["Código Subsistema"]
                ultimo_subsis = linha_lida["Nome Subsistema"]
                ultima_razao = linha_lida["Razão"]
                file.write(
                    self.__linha_subsis.write(
                        linha_lida[
                            [
                                "Código Subsistema",
                                "Nome Subsistema",
                                "Razão",
                            ]
                        ].tolist()
                    )
                )
            linha_saida = linha_lida[["Ano"] + MESES_DF]
            valores_saida = []
            for valor, vazio in zip(linha_saida, linha_saida.isna()):
                valores_saida.append(None if vazio else valor)
            file.write(self.__linha_cargas.write(valores_saida))
        file.write(BlocoCargasAdicionais.FIM_BLOCO)
