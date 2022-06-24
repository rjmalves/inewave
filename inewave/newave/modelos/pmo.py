# Imports do próprio módulo

from inewave.config import MAX_ANOS_ESTUDO, MAX_ITERS, MAX_MESES_ESTUDO
from inewave.config import MAX_REES
from inewave.config import MESES_DF

# Imports de módulos externos
from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from datetime import timedelta
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List, Optional


class BlocoEafPastTendenciaHidrolPMO(Block):
    """
    Bloco de informações de afluências passadas para
    tendência hidrológica localizado no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = "ENERGIAS AFLUENTES PASSADAS PARA A TENDENCIA HIDROLOGICA"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        ree_field: List[Field] = [LiteralField(10, 1)]
        ena_fields: List[Field] = [
            FloatField(11, 11 * (i + 1), 2) for i in range(len(MESES_DF))
        ]
        self.__line = Line(ree_field + ena_fields)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEafPastTendenciaHidrolPMO):
            return False
        bloco: BlocoEafPastTendenciaHidrolPMO = o
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
            df["REE"] = rees
            df = df[["REE"] + MESES_DF]
            return df

        # Pula as linhas iniciais
        for _ in range(4):
            file.readline()

        # Variáveis auxiliares
        rees: List[str] = []
        tabela = np.zeros((MAX_REES, len(MESES_DF)))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if "X-------" in linha:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados_linha: list = self.__line.read(linha)
            rees.append(dados_linha[0])
            tabela[i, :] = dados_linha[1:]
            i += 1


class BlocoEafPastCfugaMedioPMO(Block):
    """
    Bloco de informações de afluências passadas para
    tendência hidrológica localizado no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = (
        "ENERGIAS AFLUENTES PASSADAS EM REFERENCIA A PRIMEIRA CONFIG"
    )
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        ree_field: List[Field] = [LiteralField(10, 1)]
        ena_fields: List[Field] = [
            FloatField(11, 11 * (i + 1), 2) for i in range(len(MESES_DF))
        ]
        self.__line = Line(ree_field + ena_fields)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEafPastCfugaMedioPMO):
            return False
        bloco: BlocoEafPastCfugaMedioPMO = o
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
            df["REE"] = rees
            df = df[["REE"] + MESES_DF]
            return df

        # Pula as linhas iniciais
        for _ in range(4):
            file.readline()

        # Variáveis auxiliares
        rees: List[str] = []
        tabela = np.zeros((MAX_REES, len(MESES_DF)))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if "X-------" in linha:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados_linha: list = self.__line.read(linha)
            rees.append(dados_linha[0])
            tabela[i, :] = dados_linha[1:]
            i += 1


class BlocoConvergenciaPMO(Block):
    """
    Bloco com as informações de convergência do NEWAVE obtidas
    no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = "    ITER               LIM.INF.        "
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        iter_field: List[Field] = [IntegerField(4, 4)]
        conv_fields: List[Field] = [
            FloatField(23, 9 + 23 * i, 2) for i in range(6)
        ]
        self.__line = Line(iter_field + conv_fields)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConvergenciaPMO):
            return False
        bloco: BlocoConvergenciaPMO = o
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
            df = pd.DataFrame(tabela)
            df.columns = [
                "Iteração",
                "Lim. Inf. ZINF",
                "ZINF",
                "Lim. Sup. ZINF",
                "ZSUP",
                "Delta ZINF",
                "ZSUP Iteração",
            ]
            df = df.astype({"Iteração": "int64"})
            df["Tempo"] = tempos
            return df

        # Salta as duas linhas iniciais
        for _ in range(3):
            file.readline()
        # Variáveis auxiliares
        tabela = np.zeros((3 * MAX_ITERS, 7), dtype=np.float64)
        tempos: List[Optional[timedelta]] = []
        i = 0
        while True:
            linha: str = file.readline()
            # Confere se já acabou
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Se não tem nada na coluna de iteração, ignora a linha
            if linha[4:9] == "     ":
                continue
            # Senão, lê a linha
            tabela[i, :] = self.__line.read(linha)
            # Lê o tempo, que tem formato personalizado
            if "min" in linha[153:168]:
                tempo = linha[153:168]
                h = int(tempo.split("h")[0])
                min = int(tempo.split("h")[1].split("min")[0])
                s = float(tempo.split("min")[1].split("s")[0])
                ts = timedelta(hours=h, minutes=min, seconds=s)
                tempos.append(ts)
            else:
                tempos.append(None)
            i += 1


class BlocoConfiguracoesExpansaoPMO(Block):
    """
    Bloco de informações sobre as configurações de expansão
    do sistema existentes no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = "CONFIGURACOES POR"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        self.__line = Line([IntegerField(6, 6 * (i + 1)) for i in range(13)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConfiguracoesExpansaoPMO):
            return False
        bloco: BlocoConfiguracoesExpansaoPMO = o
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
            return df

        # Pula as linhas iniciais
        for _ in range(6):
            file.readline()
        # Variáveis auxiliares
        tabela = np.zeros((MAX_ANOS_ESTUDO, len(MESES_DF) + 1), dtype=np.int64)
        i = 0
        while True:
            linha: str = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Lê mais uma linha
            tabela[i, :] = self.__line.read(linha)
            i += 1


class BlocoMARSPMO(Block):
    """
    Bloco de informações sobre o modelo MARS ajustado
    para as retas de perdas por engolimento máximo
    existentes no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = "PARAMETROS DAS RETAS DE PERDAS POR ENGOLIMENTO MAXIMO"
    END_PATTERN = 'ENERGIA FIO D"AGUA LIQUIDA|CEPEL'

    MAX_RETAS_MARS = 3

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        self.__line = Line(
            [
                IntegerField(12, 1),
                FloatField(12, 14, 5, format="E"),
                FloatField(12, 27, 5, format="E"),
            ]
        )
        self.__ree_field = LiteralField(10, 6)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMARSPMO):
            return False
        bloco: BlocoMARSPMO = o
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
            colunas = ["Reta", "Coeficiente Angular", "Constante"]
            df = pd.DataFrame(tabela, columns=colunas)
            df["REE"] = rees
            df = df[["REE"] + colunas]
            df = df.astype({"Reta": "int64"})
            return df

        # Variáveis auxiliares
        ree_atual = ""
        rees: List[str] = []
        tabela = np.zeros(
            (BlocoMARSPMO.MAX_RETAS_MARS * MAX_REES * MAX_MESES_ESTUDO, 3),
            dtype=np.float64,
        )
        i = 0
        while True:
            linha: str = file.readline()
            if self.ends(linha):
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            elif "REE:" in linha:
                ree_atual = self.__ree_field.read(linha)
            else:
                dados_linha = self.__line.read(linha)
                if dados_linha[0] is not None:
                    rees.append(ree_atual)
                    tabela[i, :] = dados_linha
                    i += 1


class BlocoRiscoDeficitENSPMO(Block):
    """
    Bloco de informações sobre os riscos de déficit e
    ENS (energia não suprida) existentes no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = "RISCO ANUAL DE DEFICIT E E\(ENS\) \(%\)"  # noqa
    END_PATTERN = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRiscoDeficitENSPMO):
            return False
        bloco: BlocoRiscoDeficitENSPMO = o
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
            df = pd.DataFrame(tabela)
            cols = ["Ano"]
            for sub in subsistemas:
                cols += [f"Risco - {sub}", f"EENS - {sub}"]
            df.columns = cols
            df = df.astype({"Ano": "int64"})
            return df

        # Pula as três linhas iniciais
        for _ in range(3):
            file.readline()
        # Identifica os subsistemas em questão e constroi
        # a estrutura da linha da tabela a ser lida
        subsistemas = [
            s.strip() for s in file.readline().split(" ") if len(s) > 1
        ]
        # Pula três linhas adicionais
        for _ in range(3):
            file.readline()
        campos: List[Field] = [IntegerField(4, 1)]
        ultima_coluna = 6
        for _ in subsistemas:
            campos.append(FloatField(6, ultima_coluna, 2))
            ultima_coluna += 6
            campos.append(FloatField(8, ultima_coluna, 2))
            ultima_coluna += 8
        self.__line = Line(campos)
        # Variáveis auxiliares
        tabela = np.zeros((MAX_ANOS_ESTUDO, 2 * len(subsistemas) + 1))
        i = 0
        while True:
            linha: str = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            tabela[i, :] = self.__line.read(linha)
            i += 1


class BlocoCustoOperacaoPMO(Block):
    """
    Bloco de informações sobre os custos de operação categorizados
    existentes no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = "PARCELA           V.ESPERADO"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        self.__line = Line(
            [
                LiteralField(18, 13),
                FloatField(13, 32, 2),
                FloatField(13, 46, 2),
                FloatField(7, 60, 2),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCustoOperacaoPMO):
            return False
        bloco: BlocoCustoOperacaoPMO = o
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
            cols = ["Valor Esperado", "Desvio Padrão do VE", "(%)"]
            df = pd.DataFrame(tabela, columns=cols)
            df["Parcela"] = parcelas
            df = df[["Parcela"] + cols]
            return df

        # Salta duas linhas
        for _ in range(2):
            file.readline()
        parcelas: List[str] = []
        tabela = np.zeros((30, 3), dtype=np.float64)
        i = 0
        while True:
            linha = file.readline()
            if "----------------" in linha:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            dados_linha = self.__line.read(linha)
            parcelas.append(dados_linha[0])
            tabela[i, :] = dados_linha[1:]
            i += 1


class BlocoCustoOperacaoTotalPMO(Block):
    """
    Bloco de informações sobre os custos de operação categorizados
    existentes no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = "           VALOR ESPERADO TOTAL:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        self.__line = Line([FloatField(24, 50, 2)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCustoOperacaoTotalPMO):
            return False
        bloco: BlocoCustoOperacaoTotalPMO = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return all([sd == d for sd, d in zip(self.data, bloco.data)])

    # Override
    def read(self, file: IO):
        data = [0, 0]
        for i in range(2):
            data[i] = self.__line.read(file.readline())[0]
        self.data = data
