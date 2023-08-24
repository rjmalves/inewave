from inewave.config import (
    MAX_ANOS_ESTUDO,
    MAX_PATAMARES,
    MAX_SUBMERCADOS,
    MESES_DF,
)

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from inewave._utils.formatacao import (
    prepara_vetor_anos_tabela,
    prepara_valor_ano,
    repete_vetor,
)


class BlocoNumeroPatamares(Section):
    """
    Bloco com o número de patamares de carga considerados
    no caso.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(2, 1),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumeroPatamares):
            return False
        bloco: BlocoNumeroPatamares = o
        if not all(
            [
                isinstance(self.data, int),
                isinstance(o.data, int),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO, *args, **kwargs):
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        self.data = self.__linha.read(file.readline())[0]

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, int):
            raise ValueError(
                "Dados do patamar.dat não foram lidos com sucesso"
            )
        file.write(self.__linha.write([self.data]))


class BlocoDuracaoPatamar(Section):
    """
    Bloco com a duração de cada patamar por mês
    de estudo, extraído do arquivo `patamar.dat`.
    """

    FIM_BLOCO = "SUBSISTEMA"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_ano: List[Field] = [IntegerField(4, 0)]
        campos_duracao: List[Field] = [
            FloatField(6, 6 + i * 8, 4) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_duracao)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDuracaoPatamar):
            return False
        bloco: BlocoDuracaoPatamar = o
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
                    "data": prepara_vetor_anos_tabela(anos),
                    "patamar": repete_vetor(patamares),
                    "valor": tabela.flatten(),
                }
            )
            df = df.fillna(1.0)
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        ano_atual = 0
        patamar_atual = 0
        patamares: List[int] = []
        anos: List[int] = []
        tabela = np.zeros((MAX_SUBMERCADOS * MAX_ANOS_ESTUDO, len(MESES_DF)))
        while True:
            ultima_linha = file.tell()
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoDuracaoPatamar.FIM_BLOCO in linha:
                file.seek(ultima_linha)
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                    patamar_atual = 1
                anos.append(ano_atual)
                patamares.append(patamar_atual)
                tabela[i, :] = dados[1:]
                patamar_atual += 1
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do patamar.dat não foram lidos com sucesso"
            )

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for ano in df["ano"].unique():
            for patamar in sorted(df["patamar"].unique()):
                df_ano_patamar = df.loc[
                    (df["ano"] == ano) & (df["patamar"] == patamar)
                ]
                df_ano_patamar = df_ano_patamar.sort_values(["data"])
                ano_linha = prepara_valor_ano(ano) if patamar == 1 else None
                valores = df_ano_patamar["valor"].tolist()
                file.write(self.__linha.write([ano_linha] + valores))


class BlocoCargaPatamar(Section):
    """
    Bloco com a carga de cada patamar por mês
    de estudo, extraído do arquivo `patamar.dat`.
    """

    FIM_BLOCO = "9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line([IntegerField(4, 0)])
        campo_ano: List[Field] = [IntegerField(4, 3)]
        campo_carga: List[Field] = [
            FloatField(6, 8 + i * 7, 4) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campo_carga)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCargaPatamar):
            return False
        bloco: BlocoCargaPatamar = o
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
                    "codigo_submercado": repete_vetor(submercados),
                    "data": prepara_vetor_anos_tabela(anos),
                    "patamar": repete_vetor(patamares),
                    "valor": tabela.flatten(),
                }
            )
            df = df.fillna(1.0)
            return df

        # Salta as linhas adicionais
        for _ in range(4):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        ano_atual = 0
        patamar_atual = 0
        submercados: List[int] = []
        anos: List[int] = []
        patamares: List[int] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_ANOS_ESTUDO * MAX_PATAMARES,
                len(MESES_DF),
            )
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoCargaPatamar.FIM_BLOCO in linha[:4]:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            if len(linha) < 8:
                subsis_atual = self.__linha_subsis.read(linha)[0]
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                    patamar_atual = 1
                submercados.append(subsis_atual)
                anos.append(ano_atual)
                patamares.append(patamar_atual)
                tabela[i, :] = dados[1:]
                patamar_atual += 1
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do patamar.dat não foram lidos com sucesso"
            )

        ultimo_subsistema = 0

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for _, linha_submercado in (
            df[["codigo_submercado", "ano"]].drop_duplicates().iterrows()
        ):
            for patamar in sorted(df["patamar"].unique()):
                df_merc = df.loc[
                    (
                        df["codigo_submercado"]
                        == linha_submercado["codigo_submercado"]
                    )
                    & (df["ano"] == linha_submercado["ano"])
                    & (df["patamar"] == patamar)
                ]
                df_merc = df_merc.sort_values(["data"])
                if linha_submercado["codigo_submercado"] != ultimo_subsistema:
                    ultimo_subsistema = linha_submercado["codigo_submercado"]
                    file.write(
                        self.__linha_subsis.write(
                            linha_submercado[
                                [
                                    "codigo_submercado",
                                ]
                            ].tolist()
                        )
                    )
                ano_linha = (
                    prepara_valor_ano(linha_submercado["ano"])
                    if patamar == 1
                    else None
                )
                valores = df_merc["valor"].tolist()
                file.write(self.__linha.write([ano_linha] + valores))
        file.write(BlocoCargaPatamar.FIM_BLOCO + "\n")


class BlocoIntercambioPatamarSubsistemas(Section):
    """
    Bloco com o fator de correção do intercâmbio entre subsistemas para
    cada patamar, por mês de estudo, extraído do arquivo `patamar.dat`.
    """

    FIM_BLOCO = "9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line([IntegerField(3, 1), IntegerField(3, 5)])
        campo_ano: List[Field] = [IntegerField(4, 3)]
        campos_intercambios: List[Field] = [
            FloatField(6, 8 + i * 7, 4) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_intercambios)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoIntercambioPatamarSubsistemas):
            return False
        bloco: BlocoIntercambioPatamarSubsistemas = o
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
                    "submercado_de": repete_vetor(submercados_de),
                    "submercado_para": repete_vetor(submercados_para),
                    "data": prepara_vetor_anos_tabela(anos),
                    "patamar": repete_vetor(patamares),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(5):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_de_atual = 0
        subsis_para_atual = 0
        ano_atual = 0
        patamar_atual = 0
        submercados_de: List[int] = []
        submercados_para: List[int] = []
        patamares: List[int] = []
        anos: List[int] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF),
            )
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if (
                len(linha) < 3
                or BlocoIntercambioPatamarSubsistemas.FIM_BLOCO in linha[:4]
            ):
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            if len(linha) < 12:
                dados = self.__linha_subsis.read(linha)
                subsis_de_atual = dados[0]
                subsis_para_atual = dados[1]
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                    patamar_atual = 1
                submercados_de.append(subsis_de_atual)
                submercados_para.append(subsis_para_atual)
                anos.append(ano_atual)
                patamares.append(patamar_atual)
                tabela[i, :] = dados[1:]
                patamar_atual += 1
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do patamar.dat não foram lidos com sucesso"
            )

        ultimo_subsistema_de = 0
        ultimo_subsistema_para = 0

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for _, linha_submercado in (
            df[["submercado_de", "submercado_para", "ano"]]
            .drop_duplicates()
            .iterrows()
        ):
            for patamar in sorted(df["patamar"].unique()):
                df_merc = df.loc[
                    (df["submercado_de"] == linha_submercado["submercado_de"])
                    & (
                        df["submercado_para"]
                        == linha_submercado["submercado_para"]
                    )
                    & (df["ano"] == linha_submercado["ano"])
                    & (df["patamar"] == patamar)
                ]
                df_merc = df_merc.sort_values(["data"])
                if any(
                    [
                        linha_submercado["submercado_de"]
                        != ultimo_subsistema_de,
                        linha_submercado["submercado_para"]
                        != ultimo_subsistema_para,
                    ]
                ):
                    ultimo_subsistema_de = linha_submercado["submercado_de"]
                    ultimo_subsistema_para = linha_submercado[
                        "submercado_para"
                    ]
                    file.write(
                        self.__linha_subsis.write(
                            linha_submercado[
                                [
                                    "submercado_de",
                                    "submercado_para",
                                ]
                            ].tolist()
                        )
                    )
                ano_linha = (
                    prepara_valor_ano(linha_submercado["ano"])
                    if patamar == 1
                    else None
                )
                valores = df_merc["valor"].tolist()
                file.write(self.__linha.write([ano_linha] + valores))
        file.write(BlocoIntercambioPatamarSubsistemas.FIM_BLOCO + "\n")


class BlocoUsinasNaoSimuladas(Section):
    """
    Bloco com a geração de usinas não simuladas em P.U. para
    cada patamar, por mês de estudo, extraído do arquivo `patamar.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line([IntegerField(3, 1), IntegerField(3, 5)])
        campo_ano: List[Field] = [IntegerField(4, 3)]
        campos_usinas: List[Field] = [
            FloatField(6, 8 + i * 7, 4) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_usinas)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoUsinasNaoSimuladas):
            return False
        bloco: BlocoUsinasNaoSimuladas = o
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
                    "codigo_submercado": repete_vetor(submercados),
                    "indice_bloco": repete_vetor(blocos),
                    "data": prepara_vetor_anos_tabela(anos),
                    "patamar": repete_vetor(patamares),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(4):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        patamar_atual = 0
        bloco_atual = 0
        ano_atual = 0
        submercados: List[int] = []
        blocos: List[int] = []
        patamares: List[int] = []
        anos: List[int] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF),
            )
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            if len(linha) < 12:
                dados = self.__linha_subsis.read(linha)
                subsis_atual = dados[0]
                bloco_atual = dados[1]
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                    patamar_atual = 1
                submercados.append(subsis_atual)
                patamares.append(patamar_atual)
                blocos.append(bloco_atual)
                anos.append(ano_atual)
                tabela[i, :] = dados[1:]
                patamar_atual += 1
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do patamar.dat não foram lidos com sucesso"
            )

        ultimo_subsistema = 0
        ultimo_bloco = 0

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for _, linha_submercado in (
            df[["codigo_submercado", "indice_bloco", "ano"]]
            .drop_duplicates()
            .iterrows()
        ):
            for patamar in sorted(df["patamar"].unique()):
                df_merc = df.loc[
                    (
                        df["codigo_submercado"]
                        == linha_submercado["codigo_submercado"]
                    )
                    & (df["indice_bloco"] == linha_submercado["indice_bloco"])
                    & (df["ano"] == linha_submercado["ano"])
                    & (df["patamar"] == patamar)
                ]
                df_merc = df_merc.sort_values(["data"])
                if any(
                    [
                        linha_submercado["codigo_submercado"]
                        != ultimo_subsistema,
                        linha_submercado["indice_bloco"] != ultimo_bloco,
                    ]
                ):
                    ultimo_subsistema = linha_submercado["codigo_submercado"]
                    ultimo_bloco = linha_submercado["indice_bloco"]
                    file.write(
                        self.__linha_subsis.write(
                            linha_submercado[
                                [
                                    "codigo_submercado",
                                    "indice_bloco",
                                ]
                            ].tolist()
                        )
                    )
                ano_linha = (
                    prepara_valor_ano(linha_submercado["ano"])
                    if patamar == 1
                    else None
                )
                valores = df_merc["valor"].tolist()
                file.write(self.__linha.write([ano_linha] + valores))
        file.write(BlocoIntercambioPatamarSubsistemas.FIM_BLOCO + "\n")
