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
    def read(self, file: IO):
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        self.data = self.__linha.read(file.readline())[0]

    # Override
    def write(self, file: IO):
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
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=["Ano"] + MESES_DF)
            df = df.fillna(1.0)
            df = df.astype({"Ano": "int64"})
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        ano_atual = 0
        tabela = np.zeros(
            (MAX_SUBMERCADOS * MAX_ANOS_ESTUDO, len(MESES_DF) + 1)
        )
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
                tabela[i, 0] = ano_atual
                tabela[i, 1:] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do patamar.dat não foram lidos com sucesso"
            )

        ultimo_ano = 0
        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            ano_linha = (
                int(linha_lida["Ano"])
                if linha_lida["Ano"] != ultimo_ano
                else None
            )
            ultimo_ano = int(linha_lida["Ano"])
            file.write(
                self.__linha.write([ano_linha] + linha_lida[MESES_DF].tolist())
            )


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
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=["Subsistema", "Ano"] + MESES_DF)
            df = df.fillna(1.0)
            df = df.astype({"Subsistema": "int64", "Ano": "int64"})
            return df

        # Salta as linhas adicionais
        for _ in range(4):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        ano_atual = 0
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_ANOS_ESTUDO * MAX_PATAMARES,
                len(MESES_DF) + 2,
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
                tabela[i, 0] = subsis_atual
                tabela[i, 1] = ano_atual
                tabela[i, 2:] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do patamar.dat não foram lidos com sucesso"
            )

        ultimo_subsistema = 0
        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if linha_lida["Subsistema"] != ultimo_subsistema:
                ultimo_subsistema = linha_lida["Subsistema"]
                ultimo_ano = 0
                file.write(self.__linha_subsis.write([int(ultimo_subsistema)]))
            ano_linha = (
                int(linha_lida["Ano"])
                if linha_lida["Ano"] != ultimo_ano
                else None
            )
            ultimo_ano = int(linha_lida["Ano"])
            file.write(
                self.__linha.write([ano_linha] + linha_lida[MESES_DF].tolist())
            )
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
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                tabela,
                columns=["Subsistema De", "Subsistema Para", "Ano"] + MESES_DF,
            )
            df = df.astype(
                {
                    "Subsistema De": "int64",
                    "Subsistema Para": "int64",
                    "Ano": "int64",
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
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF) + 3,
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
                tabela[i, 0] = subsis_de_atual
                tabela[i, 1] = subsis_para_atual
                tabela[i, 2] = ano_atual
                tabela[i, 3:] = dados[1:]
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "Dados do patamar.dat não foram lidos com sucesso"
            )

        ultimo_subsistema_de = 0
        ultimo_subsistema_para = 0

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if any(
                [
                    linha_lida["Subsistema De"] != ultimo_subsistema_de,
                    linha_lida["Subsistema Para"] != ultimo_subsistema_para,
                ]
            ):
                ultimo_ano = 0
                ultimo_subsistema_de = linha_lida["Subsistema De"]
                ultimo_subsistema_para = linha_lida["Subsistema Para"]
                file.write(
                    self.__linha_subsis.write(
                        [
                            int(ultimo_subsistema_de),
                            int(ultimo_subsistema_para),
                        ]
                    )
                )
            ano_linha = (
                int(linha_lida["Ano"])
                if linha_lida["Ano"] != ultimo_ano
                else None
            )
            ultimo_ano = int(linha_lida["Ano"])
            file.write(
                self.__linha.write([ano_linha] + linha_lida[MESES_DF].tolist())
            )
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
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                tabela, columns=["Subsistema", "Bloco", "Ano"] + MESES_DF
            )
            df = df.astype(
                {"Subsistema": "int64", "Bloco": "int64", "Ano": "int64"}
            )
            return df

        # Salta as linhas adicionais
        for _ in range(4):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        bloco_atual = 0
        ano_atual = 0
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
            if len(linha) < 12:
                dados = self.__linha_subsis.read(linha)
                subsis_atual = dados[0]
                bloco_atual = dados[1]
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
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
                "Dados do patamar.dat não foram lidos com sucesso"
            )

        ultimo_subsistema = 0
        ultimo_bloco = 0

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if any(
                [
                    linha_lida["Subsistema"] != ultimo_subsistema,
                    linha_lida["Bloco"] != ultimo_bloco,
                ]
            ):
                ultimo_ano = 0
                ultimo_subsistema = linha_lida["Subsistema"]
                ultimo_bloco = linha_lida["Bloco"]
                file.write(
                    self.__linha_subsis.write(
                        [
                            int(ultimo_subsistema),
                            int(ultimo_bloco),
                        ]
                    )
                )
            ano_linha = (
                int(linha_lida["Ano"])
                if linha_lida["Ano"] != ultimo_ano
                else None
            )
            ultimo_ano = int(linha_lida["Ano"])
            file.write(
                self.__linha.write([ano_linha] + linha_lida[MESES_DF].tolist())
            )
        file.write(BlocoIntercambioPatamarSubsistemas.FIM_BLOCO + "\n")
