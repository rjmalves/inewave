from inewave.config import MAX_ANOS_ESTUDO, MAX_SUBMERCADOS, MESES_DF

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class BlocoNumeroPatamaresDeficit(Section):
    """
    Bloco com o número de patamares de déficit considerados.
    """

    def __init__(self, state=..., previous=None, next=None, data=None) -> None:
        super().__init__(state, previous, next, data)
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
    def read(self, file: IO):
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        self.data = self.__linha.read(file.readline())[0]

    # Override
    def write(self, file: IO):
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

    def __init__(self, state=..., previous=None, next=None, data=None) -> None:
        super().__init__(state, previous, next, data)
        self.__linha = Line(
            [IntegerField(3, 1)]
            + [LiteralField(13, 5)]
            + [IntegerField(1, 17)]
            + [FloatField(7, 19 + i * 8, 2) for i in range(4)]
            + [FloatField(5, 51 + i * 6, 3) for i in range(4)]
        )
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
    def read(self, file: IO):
        def converte_tabela_em_df():
            cols = [f"Custo Pat. {p}" for p in range(1, 5)] + [
                f"Corte Pat. {p}" for p in range(1, 5)
            ]
            df = pd.DataFrame(
                tabela, columns=["Num. Subsistema", "Fictício"] + cols
            )
            df["Nome"] = subsistemas
            df = df[["Num. Subsistema", "Nome", "Fictício"] + cols]
            df = df.astype({"Num. Subsistema": "int64", "Fictício": "int64"})
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsistemas: List[str] = []
        tabela = np.zeros((MAX_SUBMERCADOS, 10))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoCustosDeficit.FIM_BLOCO in linha:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                tabela[i, 0] = dados[0]
                subsistemas.append(dados[1])
                tabela[i, 1:] = dados[2:]
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )

        for _, linha in self.data.iterrows():
            file.write(self.__linha.write(linha))
        file.write(BlocoCustosDeficit.FIM_BLOCO + "\n")


class BlocoIntercambioSubsistema(Section):
    """
    Bloco com a informação de intercâmbio
    por mês/ano de estudo para cada subsistema.
    """

    FIM_BLOCO = " 999"

    def __init__(self, state=..., previous=None, next=None, data=None) -> None:
        super().__init__(state, previous, next, data)
        self.__linha_subsis = Line(
            [IntegerField(3, 1), IntegerField(3, 5), IntegerField(1, 23)]
        )
        self.__linha = Line(
            [IntegerField(4, 0)]
            + [FloatField(7, 8 + i * 8, 0) for i in range(len(MESES_DF))]
        )
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
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                tabela,
                columns=["Ano"] + MESES_DF,
            )
            df["Subsistema De"] = subsistemas_de
            df["Subsistema Para"] = subsistemas_para
            df["Sentido"] = sentidos
            df = df[
                ["Subsistema De", "Subsistema Para", "Sentido", "Ano"]
                + MESES_DF
            ]
            df = df.astype(
                {
                    "Subsistema De": "int64",
                    "Subsistema Para": "int64",
                    "Sentido": "int64",
                    "Ano": "int64",
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
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF) + 1,
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
                    sentido_atual
                    if dados[2] is None
                    else int(not sentido_atual)
                )
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                subsistemas_de.append(subsis_de_atual)
                subsistemas_para.append(subsis_para_atual)
                sentidos.append(sentido_atual)
                tabela[i, 0] = ano_atual
                tabela[i, 1:] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )

        ultimo_subsistema_de = 0
        ultimo_subsistema_para = 0
        ultimo_sentido = -1

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if any(
                [
                    linha_lida["Subsistema De"] != ultimo_subsistema_de,
                    linha_lida["Subsistema Para"] != ultimo_subsistema_para,
                    linha_lida["Sentido"] != ultimo_sentido,
                ]
            ):
                ultimo_ano = 0
                ultimo_subsistema_de = linha_lida["Subsistema De"]
                ultimo_subsistema_para = linha_lida["Subsistema Para"]
                ultimo_sentido = linha_lida["Sentido"]
                file.write(
                    self.__linha_subsis.write(
                        [
                            int(ultimo_subsistema_de),
                            int(ultimo_subsistema_para),
                            int(ultimo_sentido),
                        ]
                    )
                )
            ano_linha = (
                int(linha["Ano"]) if linha["Ano"] != ultimo_ano else None
            )
            ultimo_ano = int(linha["Ano"])
            file.write(
                self.__linha.write([ano_linha] + linha_lida[MESES_DF].tolist())
            )
        file.write(BlocoIntercambioSubsistema.FIM_BLOCO + "\n")


class BlocoMercadoEnergiaSistema(Section):
    """
    Bloco com a informação de mercado de energia
    por mês/ano de estudo para cada subsistema.
    """

    FIM_BLOCO = " 999"

    def __init__(self, state=..., previous=None, next=None, data=None) -> None:
        super().__init__(state, previous, next, data)
        self.__linha_subsis = Line([IntegerField(3, 1)])
        self.__linha = Line(
            [LiteralField(4, 0)]
            + [FloatField(7, 7 + i * 8, 0) for i in range(len(MESES_DF))]
        )
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
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                tabela,
                columns=["Subsistema"] + MESES_DF,
            )
            df = df.astype(
                {
                    "Subsistema": "int64",
                }
            )
            df["Ano"] = anos
            df = df[["Subsistema", "Ano"] + MESES_DF]
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        ano_atual = ""
        anos: List[str] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF) + 1,
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
                tabela[i, 0] = subsis_atual
                tabela[i, 1:] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )

        ultimo_subsistema = 0

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if any(
                [
                    linha_lida["Subsistema"] != ultimo_subsistema,
                ]
            ):
                ultimo_ano = ""
                ultimo_subsistema = linha_lida["Subsistema"]
                file.write(
                    self.__linha_subsis.write(
                        [
                            int(ultimo_subsistema),
                        ]
                    )
                )
            ano_linha = linha["Ano"] if linha["Ano"] != ultimo_ano else None
            ultimo_ano = linha["Ano"]
            file.write(
                self.__linha.write([ano_linha] + linha_lida[MESES_DF].tolist())
            )
        file.write(BlocoMercadoEnergiaSistema.FIM_BLOCO + "\n")


class BlocoGeracaoUsinasNaoSimuladas(Section):
    """
    Bloco com a geração de usinas não simuladas em P.U. para
    cada patamar, por mês de estudo, extraído do arquivo `sistema.dat`.
    """

    FIM_BLOCO = " 999"

    def __init__(self, state=..., previous=None, next=None, data=None) -> None:
        super().__init__(state, previous, next, data)
        self.__linha_subsis = Line(
            [IntegerField(3, 1), IntegerField(3, 6), LiteralField(3, 11)]
        )
        self.__linha = Line(
            [IntegerField(4, 0)]
            + [FloatField(7, 7 + i * 8, 0) for i in range(len(MESES_DF))]
        )
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
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                tabela, columns=["Subsistema", "Bloco", "Ano"] + MESES_DF
            )
            df["Razão"] = razoes
            df = df.astype(
                {"Subsistema": "int64", "Bloco": "int64", "Ano": "int64"}
            )
            df = df[["Subsistema", "Bloco", "Razão", "Ano"] + MESES_DF]
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        bloco_atual = 0
        razao_atual = ""
        ano_atual = 0
        razoes: List[str] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF) + 3,
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
                tabela[i, 0] = subsis_atual
                tabela[i, 1] = bloco_atual
                tabela[i, 2] = ano_atual
                tabela[i, 3:] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do sistema.dat não foram lidos com sucesso"
            )

        ultimo_subsistema = 0
        ultimo_bloco = 0
        ultima_razao = ""

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if any(
                [
                    linha_lida["Subsistema"] != ultimo_subsistema,
                    linha_lida["Bloco"] != ultimo_bloco,
                    linha_lida["Razão"] != ultima_razao,
                ]
            ):
                ultimo_ano = 0
                ultimo_subsistema = linha_lida["Subsistema"]
                ultimo_bloco = linha_lida["Bloco"]
                ultima_razao = linha_lida["Razão"]
                file.write(
                    self.__linha_subsis.write(
                        [
                            int(ultimo_subsistema),
                            int(ultimo_bloco),
                            str(ultima_razao),
                        ]
                    )
                )
            ano_linha = (
                int(linha["Ano"]) if linha["Ano"] != ultimo_ano else None
            )
            ultimo_ano = int(linha["Ano"])
            file.write(
                self.__linha.write([ano_linha] + linha_lida[MESES_DF].tolist())
            )
        file.write(BlocoGeracaoUsinasNaoSimuladas.FIM_BLOCO + "\n")
