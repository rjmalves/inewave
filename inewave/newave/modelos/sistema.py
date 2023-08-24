from inewave.config import (
    MAX_ANOS_ESTUDO,
    MAX_SUBMERCADOS,
    MESES_DF,
    MAX_PATAMARES_DEFICIT,
)

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO, Optional
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from inewave._utils.formatacao import (
    prepara_vetor_anos_tabela,
    prepara_valor_ano,
    repete_vetor,
)


class BlocoNumeroPatamaresDeficit(Section):
    """
    Bloco com o número de patamares de déficit considerados.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumeroPatamaresDeficit):
            return False
        bloco: BlocoNumeroPatamaresDeficit = o
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
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        self.data = self.__linha.read(file.readline())[0]

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, int):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )
        file.write(self.__linha.write([self.data]))


class BlocoCustosDeficit(Section):
    """
    Bloco com informações sobre o custo de déficit por
    patamar de déficit e o número de patamares de déficit.
    """

    FIM_BLOCO = " 999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campos_iniciais: List[Field] = [
            IntegerField(3, 1),
            LiteralField(12, 5),
            IntegerField(1, 17),
        ]
        campos_custos: List[Field] = [
            FloatField(7, 19 + i * 8, 2) for i in range(4)
        ]
        campos_cortes: List[Field] = [
            FloatField(5, 51 + i * 6, 3) for i in range(4)
        ]
        self.__linha = Line(campos_iniciais + campos_custos + campos_cortes)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCustosDeficit):
            return False
        bloco: BlocoCustosDeficit = o
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
                    "codigo_submercado": repete_vetor(
                        codigos_submercados, MAX_PATAMARES_DEFICIT
                    ),
                    "nome_submercado": repete_vetor(
                        nomes_submercados,
                        MAX_PATAMARES_DEFICIT,
                    ),
                    "ficticio": repete_vetor(
                        ficticios,
                        MAX_PATAMARES_DEFICIT,
                    ),
                    "patamar_deficit": np.tile(
                        np.arange(1, MAX_PATAMARES_DEFICIT + 1),
                        len(codigos_submercados),
                    ),
                    "custo": tabela_custo.flatten(),
                    "corte": tabela_corte.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        codigos_submercados: List[int] = []
        nomes_submercados: List[str] = []
        ficticios: List[int] = []
        tabela_custo = np.zeros((MAX_SUBMERCADOS, MAX_PATAMARES_DEFICIT))
        tabela_corte = np.zeros((MAX_SUBMERCADOS, MAX_PATAMARES_DEFICIT))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoCustosDeficit.FIM_BLOCO in linha[:4]:
                # Converte para df e salva na variável
                if i > 0:
                    tabela_custo = tabela_custo[:i, :]
                    tabela_corte = tabela_corte[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                codigos_submercados.append(dados[0])
                nomes_submercados.append(dados[1])
                ficticios.append(dados[2])
                tabela_custo[i, :] = dados[3 : 3 + MAX_PATAMARES_DEFICIT]
                tabela_corte[i, :] = dados[
                    3 + MAX_PATAMARES_DEFICIT : 3 + 2 * MAX_PATAMARES_DEFICIT
                ]
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )
        df = self.data.copy()
        for _, linha_submercado in (
            self.data[
                [
                    "codigo_submercado",
                    "nome_submercado",
                    "ficticio",
                ]
            ]
            .drop_duplicates()
            .iterrows()
        ):
            df_penalid = df.loc[
                (
                    df["codigo_submercado"]
                    == linha_submercado["codigo_submercado"]
                )
                & (
                    df["nome_submercado"]
                    == linha_submercado["nome_submercado"]
                )
                & (df["ficticio"] == linha_submercado["ficticio"])
            ]

            file.write(
                self.__linha.write(
                    [
                        linha_submercado["codigo_submercado"],
                        linha_submercado["nome_submercado"],
                        linha_submercado["ficticio"],
                    ]
                    + df_penalid.sort_values("patamar_deficit")[
                        "custo"
                    ].tolist()
                    + df_penalid.sort_values("patamar_deficit")[
                        "corte"
                    ].tolist()
                )
            )

        file.write(BlocoCustosDeficit.FIM_BLOCO + "\n")


class BlocoIntercambioSubsistema(Section):
    """
    Bloco com a informação de intercâmbio
    por mês/ano de estudo para cada subsistema.
    """

    FIM_BLOCO = " 999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line(
            [IntegerField(3, 1), IntegerField(3, 5), IntegerField(1, 23)]
        )
        campo_ano: List[Field] = [IntegerField(4, 0)]
        campos_interc: List[Field] = [
            FloatField(6, 8 + i * 8, 0) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_interc)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoIntercambioSubsistema):
            return False
        bloco: BlocoIntercambioSubsistema = o
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
                    "submercado_de": repete_vetor(subsistemas_de),
                    "submercado_para": repete_vetor(subsistemas_para),
                    "sentido": repete_vetor(sentidos),
                    "data": prepara_vetor_anos_tabela(anos),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_de_atual = 0
        subsis_para_atual = 0
        sentido_atual = -1
        ano_atual = 0
        subsistemas_de: List[int] = []
        subsistemas_para: List[int] = []
        sentidos: List[int] = []
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
            if BlocoIntercambioSubsistema.FIM_BLOCO in linha[:4] or (
                len(linha) < 3 and i == 0
            ):
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            if len(linha) < 30:
                dados = self.__linha_subsis.read(linha)
                subsis_de_atual = (
                    subsis_de_atual if dados[0] is None else dados[0]
                )
                subsis_para_atual = (
                    subsis_para_atual if dados[1] is None else dados[1]
                )
                sentido_atual = (
                    dados[2]
                    if dados[2] is not None
                    else int(not sentido_atual)
                )
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                anos.append(ano_atual)
                subsistemas_de.append(subsis_de_atual)
                subsistemas_para.append(subsis_para_atual)
                sentidos.append(sentido_atual)
                tabela[i, :] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )

        ultimo_subsistema_de = 0
        ultimo_subsistema_para = 0
        ultimo_sentido = -1

        # Separa os valores de cada submercado, razao, ano
        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for _, linha_submercados_sentido in (
            df[["submercado_de", "submercado_para", "sentido", "ano"]]
            .drop_duplicates()
            .iterrows()
        ):
            df_interc = df.loc[
                (
                    df["submercado_de"]
                    == linha_submercados_sentido["submercado_de"]
                )
                & (
                    df["submercado_para"]
                    == linha_submercados_sentido["submercado_para"]
                )
                & (df["sentido"] == linha_submercados_sentido["sentido"])
                & (df["ano"] == linha_submercados_sentido["ano"])
            ]
            df_interc = df_interc.sort_values(["data"])
            if any(
                [
                    linha_submercados_sentido["submercado_de"]
                    != ultimo_subsistema_de,
                    linha_submercados_sentido["submercado_para"]
                    != ultimo_subsistema_para,
                    linha_submercados_sentido["sentido"] != ultimo_sentido,
                ]
            ):
                ultimo_subsistema_de = linha_submercados_sentido[
                    "submercado_de"
                ]
                ultimo_subsistema_para = linha_submercados_sentido[
                    "submercado_para"
                ]
                ultimo_sentido = linha_submercados_sentido["sentido"]
                file.write(
                    self.__linha_subsis.write(
                        linha_submercados_sentido[
                            [
                                "submercado_de",
                                "submercado_para",
                                "sentido",
                            ]
                        ].tolist()
                    )
                )
            ano = prepara_valor_ano(linha_submercados_sentido["ano"])
            valores = df_interc["valor"].tolist()
            file.write(self.__linha.write([ano] + valores))

        file.write(BlocoIntercambioSubsistema.FIM_BLOCO + "\n")


class BlocoMercadoEnergiaSistema(Section):
    """
    Bloco com a informação de mercado de energia
    por mês/ano de estudo para cada subsistema.
    """

    FIM_BLOCO = " 999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line([IntegerField(3, 1)])
        campo_ano: List[Field] = [LiteralField(4, 0)]
        campos_mercado: List[Field] = [
            FloatField(7, 7 + i * 8, 0) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_mercado)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMercadoEnergiaSistema):
            return False
        bloco: BlocoMercadoEnergiaSistema = o
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
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        ano_atual = ""
        submercados: List[int] = []
        anos: List[str] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF),
            )
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if (
                len(linha) < 3
                or BlocoMercadoEnergiaSistema.FIM_BLOCO in linha[:4]
            ):
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            if len(linha) < 12:
                dados = self.__linha_subsis.read(linha)
                subsis_atual = dados[0]
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], str) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                anos.append(ano_atual)
                submercados.append(subsis_atual)
                tabela[i, :] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )

        ultimo_subsistema = 0

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for _, linha_submercado in (
            df[["codigo_submercado", "ano"]].drop_duplicates().iterrows()
        ):
            df_merc = df.loc[
                (
                    df["codigo_submercado"]
                    == linha_submercado["codigo_submercado"]
                )
                & (df["ano"] == linha_submercado["ano"])
            ]
            df_merc = df_merc.sort_values(["data"])
            if any(
                [
                    linha_submercado["codigo_submercado"] != ultimo_subsistema,
                ]
            ):
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
            ano = prepara_valor_ano(linha_submercado["ano"])
            valores = df_merc["valor"].tolist()
            file.write(self.__linha.write([ano] + valores))
        file.write(BlocoMercadoEnergiaSistema.FIM_BLOCO + "\n")


class BlocoGeracaoUsinasNaoSimuladas(Section):
    """
    Bloco com a geração de usinas não simuladas em P.U. para
    cada patamar, por mês de estudo, extraído do arquivo `sistema.dat`.
    """

    FIM_BLOCO = " 999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line(
            [IntegerField(3, 1), IntegerField(3, 6), LiteralField(3, 11)]
        )

        campo_ano: List[Field] = [IntegerField(4, 0)]
        campos_geradores: List[Field] = [
            FloatField(7, 7 + i * 8, 0) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_geradores)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoGeracaoUsinasNaoSimuladas):
            return False
        bloco: BlocoGeracaoUsinasNaoSimuladas = o
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
                    "fonte": repete_vetor(razoes),
                    "data": prepara_vetor_anos_tabela(anos),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        bloco_atual = 0
        razao_atual = ""
        ano_atual = 0
        submercados: List[int] = []
        blocos: List[int] = []
        razoes: List[str] = []
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
                BlocoGeracaoUsinasNaoSimuladas.FIM_BLOCO in linha[:4]
                or len(linha) < 3
            ):
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            if len(linha) < 30:
                dados = self.__linha_subsis.read(linha)
                subsis_atual = dados[0]
                bloco_atual = dados[1]
                razao_atual = dados[2]
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                razoes.append(razao_atual)
                submercados.append(subsis_atual)
                blocos.append(bloco_atual)
                anos.append(ano_atual)
                tabela[i, :] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )

        ultimo_subsistema: Optional[int] = 0
        ultimo_bloco: Optional[int] = 0
        ultima_razao: Optional[str] = ""

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for _, linha_submercado_fonte in (
            df[["codigo_submercado", "indice_bloco", "fonte", "ano"]]
            .drop_duplicates()
            .iterrows()
        ):
            df_ger = df.loc[
                (
                    df["codigo_submercado"]
                    == linha_submercado_fonte["codigo_submercado"]
                )
                & (
                    df["indice_bloco"]
                    == linha_submercado_fonte["indice_bloco"]
                )
                & (df["fonte"] == linha_submercado_fonte["fonte"])
                & (df["ano"] == linha_submercado_fonte["ano"])
            ]
            df_ger = df_ger.sort_values(["data"])
            if any(
                [
                    linha_submercado_fonte["codigo_submercado"]
                    != ultimo_subsistema,
                    linha_submercado_fonte["indice_bloco"] != ultimo_bloco,
                    linha_submercado_fonte["fonte"] != ultima_razao,
                ]
            ):
                ultimo_subsistema = linha_submercado_fonte["codigo_submercado"]
                ultimo_bloco = linha_submercado_fonte["indice_bloco"]
                ultima_razao = linha_submercado_fonte["fonte"]
                file.write(
                    self.__linha_subsis.write(
                        linha_submercado_fonte[
                            [
                                "codigo_submercado",
                                "indice_bloco",
                                "fonte",
                            ]
                        ].tolist()
                    )
                )
            ano = prepara_valor_ano(linha_submercado_fonte["ano"])
            valores = df_ger["valor"].tolist()
            file.write(self.__linha.write([ano] + valores))
        file.write(BlocoGeracaoUsinasNaoSimuladas.FIM_BLOCO + "\n")
