from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from inewave._utils.formatacao import (
    prepara_vetor_anos_tabela,
    repete_vetor,
)
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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(
                data={
                    "codigo_usina": repete_vetor(codigos_usinas),
                    "data": prepara_vetor_anos_tabela(anos),
                    "valor": tabela.flatten(),
                    "considera_desvio_usina_NC": repete_vetor(
                        considera_desvios
                    ),
                    "comentario": repete_vetor(comentarios),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_UHES * MAX_ANOS_ESTUDO, len(MESES_DF)))
        codigos_usinas: List[int] = []
        anos: List[str] = []
        considera_desvios: List[int] = []
        comentarios: List[str] = []
        ultimo_comentario = ""
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
            tabela[i, :] = dados[2:-2]
            anos.append(dados[0])
            codigos_usinas.append(dados[1])
            considera_desvios.append(dados[-2])
            if len(dados[-1]) > 0:
                ultimo_comentario = dados[-1]
            comentarios.append(ultimo_comentario)
            i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do confhd.dat não foram lidos com sucesso")

        # Separa os valores de cada usina
        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        ultimo_comentario = ""
        for _, linha_usina in (
            df[
                [
                    "codigo_usina",
                    "ano",
                    "considera_desvio_usina_NC",
                    "comentario",
                ]
            ]
            .drop_duplicates()
            .iterrows()
        ):
            df_usina = df.loc[
                (df["codigo_usina"] == linha_usina["codigo_usina"])
                & (df["ano"] == linha_usina["ano"])
                & (
                    df["considera_desvio_usina_NC"]
                    == linha_usina["considera_desvio_usina_NC"]
                )
                & (df["comentario"] == linha_usina["comentario"])
            ]
            num_blocos_ano = df_usina.shape[0] // len(MESES_DF)
            for i in range(num_blocos_ano):
                comentario = (
                    linha_usina["comentario"]
                    if ultimo_comentario != linha_usina["comentario"]
                    else ""
                )
                ultimo_comentario = linha_usina["comentario"]
                file.write(
                    self.__linha_uhe.write(
                        [
                            int(linha_usina["ano"]),
                            int(linha_usina["codigo_usina"]),
                        ]
                        + df_usina["valor"].tolist()[
                            len(MESES_DF) * i : len(MESES_DF) * (i + 1)
                        ]
                        + [
                            linha_usina["considera_desvio_usina_NC"],
                            comentario,
                        ]
                    )
                )

        file.write(BlocoDsvUHE.FIM_BLOCO + "\n")
