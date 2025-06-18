# Imports do próprio módulo

from datetime import date
from typing import IO, List

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

# Imports de módulos externos
from cfinterface.components.block import Block
from cfinterface.components.field import Field
from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField

from inewave._utils.formatacao import (
    prepara_vetor_anos_tabela,
    repete_vetor,
)
from inewave.config import (
    MAX_ANOS_HISTORICO,
    MAX_CONFIGURACOES,
    MAX_REES,
    MAX_UEES,
    MESES_ABREV,
    MESES_DF,
)


class BlocoSerieVentosUEE(Block):
    """
    Bloco de informações do arquivo `parpeol.dat`
    relativo às séries de ventos por usina.
    """

    __slots__ = [
        "__campo_uee",
        "__campo_cfg",
        "__linha",
    ]

    BEGIN_PATTERN = "SERIE  DE VENTOS   DA USINA"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_uee = LiteralField(14, 57)
        self.__campo_cfg = IntegerField(5, 88)
        campo_ano: List[Field] = [IntegerField(4, 0)]
        campo_energia: List[Field] = [
            FloatField(10, 4 + 11 * i, 2) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campo_energia)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSerieVentosUEE):
            return False
        bloco: BlocoSerieVentosUEE = o
        if not all([
            isinstance(self.data, pd.DataFrame),
            isinstance(o.data, pd.DataFrame),
        ]):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                data={
                    "data": prepara_vetor_anos_tabela(anos),
                    "valor": tabela.flatten(),
                }
            )
            df["uee"] = uee
            df["configuracao"] = cfg
            return df[["uee", "configuracao", "data", "valor"]]

        # Identifica a usina e a configuração
        linha = file.readline()
        uee = self.__campo_uee.read(linha)
        cfg = self.__campo_cfg.read(linha)

        # Salta as linhas adicionais
        for _ in range(4):
            file.readline()

        # Variáveis auxiliares
        anos: List[int] = []
        tabela = np.zeros((MAX_ANOS_HISTORICO, len(MESES_DF)))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                tabela = tabela[:i, :]  # type: ignore
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados = self.__linha.read(linha)
            anos.append(dados[0])
            tabela[i, :] = dados[1:]
            i += 1


class BlocoCorrelVentosUEE(Block):
    """
    Bloco de informações do arquivo `parpeol.dat`
    relativo às séries de autocorrelações
    dos ventos por usina.
    """

    __slots__ = [
        "__linha",
    ]

    BEGIN_PATTERN = "CORRELOGRAMO DA SERIE DE VENTOS"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_mes: List[Field] = [LiteralField(3, 1)]
        campo_ano: List[Field] = [LiteralField(4, 5)]
        correl: List[Field] = [FloatField(10, 9 + 10 * i, 5) for i in range(11)]
        self.__linha = Line(campo_mes + campo_ano + correl)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelVentosUEE):
            return False
        bloco: BlocoCorrelVentosUEE = o
        if not all([
            isinstance(self.data, pd.DataFrame),
            isinstance(o.data, pd.DataFrame),
        ]):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO, *args, **kwargs):
        def converte_vetor_anos(anos: List[str]) -> List[int]:
            # Descobre os anos pré e pós estudo
            numero_anos_pre = len([p for p in anos if p == "PRE"]) // 12
            numero_anos_pos = len([p for p in anos if p == "POS"]) // 12
            anos_estudo = [int(p) for p in anos if p not in ["PRE", "POS"]]
            # Descobre o primeiro ano de estudo
            primeiro_ano_estudo = sorted(anos_estudo)[0]
            # Descobre o último ano de estudo
            ultimo_ano_estudo = sorted(anos_estudo)[-1]
            indice_inicio_pos = anos.index("POS")
            # Substitui os anos pré e pós pelos valores específicos
            for a in range(numero_anos_pre):
                idx_i = 12 * a
                idx_f = idx_i + 12
                ano = primeiro_ano_estudo - (numero_anos_pre - a)
                anos[idx_i:idx_f] = [str(ano)] * 12
            for a in range(numero_anos_pos):
                idx_i = indice_inicio_pos + 12 * a
                idx_f = idx_i + 12
                ano = ultimo_ano_estudo + a + 1
                anos[idx_i:idx_f] = [str(ano)] * 12
            return [int(a) for a in anos]

        def converte_vetor_meses(meses: List[str]) -> List[int]:
            return [MESES_ABREV.index(m) + 1 for m in meses]

        def converte_tabela_em_df():
            anos_conv = converte_vetor_anos(anos)
            meses_conv = converte_vetor_meses(meses)
            datas = [
                date(year=a, month=m, day=1)
                for a, m in zip(anos_conv, meses_conv)
            ]
            df = pd.DataFrame(
                data={
                    "data": repete_vetor(datas, len(MESES_DF) - 1),
                    "lag": np.tile(np.arange(1, len(MESES_DF)), len(datas)),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(5):
            file.readline()

        # Variáveis auxiliares
        meses: List[str] = []
        anos: List[str] = []
        tabela = np.zeros((MAX_ANOS_HISTORICO * len(MESES_DF), 11))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                tabela = tabela[:i, :]  # type: ignore
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados = self.__linha.read(linha)
            meses.append(dados[0])
            anos.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1


class BlocoSerieRuidosUEE(Block):
    """
    Bloco de informações do arquivo `parpeol.dat`
    relativo às séries de ruídos por usina.
    """

    __slots__ = [
        "__campo_ano",
        "__linha",
    ]

    BEGIN_PATTERN = "SERIE DE RUIDOS  - ANO:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_ano = LiteralField(5, 81)
        campos: List[Field] = [
            FloatField(11, 3 + 11 * i, 3, format="E")
            for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campos)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSerieRuidosUEE):
            return False
        bloco: BlocoSerieRuidosUEE = o
        if not all([
            isinstance(self.data, pd.DataFrame),
            isinstance(o.data, pd.DataFrame),
        ]):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                data={
                    "valor": tabela.flatten(),
                }
            )
            df["ano"] = ano
            df["mes"] = np.tile(
                np.arange(1, len(MESES_DF) + 1), tabela.shape[0]
            )
            df["serie"] = repete_vetor(list(range(1, i + 1)))
            return df[["ano", "serie", "mes", "valor"]]

        # Identifica o ano em questão
        linha = file.readline()
        ano = self.__campo_ano.read(linha)

        # Salta as linhas adicionais
        for _ in range(5):
            file.readline()

        # Variáveis auxiliares
        tabela = np.zeros((MAX_ANOS_HISTORICO, len(MESES_DF)))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                tabela = tabela[:i, :]  # type: ignore
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            tabela[i, :] = self.__linha.read(linha)
            i += 1


class BlocoCorrelRuidosUEE(Block):
    """
    Bloco de informações do arquivo `parpeol.dat`
    relativo às séries de autocorrelações
    dos ruídos por usina.
    """

    __slots__ = [
        "__linha",
    ]

    BEGIN_PATTERN = "CORRELOGRAMO DA SERIE DE RUIDOS"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_mes: List[Field] = [LiteralField(3, 1)]
        campo_ano: List[Field] = [LiteralField(4, 5)]
        correl: List[Field] = [FloatField(10, 9 + 10 * i, 5) for i in range(11)]
        self.__linha = Line(campo_mes + campo_ano + correl)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelRuidosUEE):
            return False
        bloco: BlocoCorrelRuidosUEE = o
        if not all([
            isinstance(self.data, pd.DataFrame),
            isinstance(o.data, pd.DataFrame),
        ]):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO, *args, **kwargs):
        def converte_vetor_anos(anos: List[str]) -> List[int]:
            # Descobre os anos pré e pós estudo
            numero_anos_pre = len([p for p in anos if p == "PRE"]) // 12
            numero_anos_pos = len([p for p in anos if p == "POS"]) // 12
            anos_estudo = [int(p) for p in anos if p not in ["PRE", "POS"]]
            # Descobre o primeiro ano de estudo
            primeiro_ano_estudo = sorted(anos_estudo)[0]
            # Descobre o último ano de estudo
            ultimo_ano_estudo = sorted(anos_estudo)[-1]
            indice_inicio_pos = anos.index("POS")
            # Substitui os anos pré e pós pelos valores específicos
            for a in range(numero_anos_pre):
                idx_i = 12 * a
                idx_f = idx_i + 12
                ano = primeiro_ano_estudo - (numero_anos_pre - a)
                anos[idx_i:idx_f] = [str(ano)] * 12
            for a in range(numero_anos_pos):
                idx_i = indice_inicio_pos + 12 * a
                idx_f = idx_i + 12
                ano = ultimo_ano_estudo + a + 1
                anos[idx_i:idx_f] = [str(ano)] * 12
            return [int(a) for a in anos]

        def converte_vetor_meses(meses: List[str]) -> List[int]:
            return [MESES_ABREV.index(m) + 1 for m in meses]

        def converte_tabela_em_df():
            anos_conv = converte_vetor_anos(anos)
            meses_conv = converte_vetor_meses(meses)
            datas = [
                date(year=a, month=m, day=1)
                for a, m in zip(anos_conv, meses_conv)
            ]
            df = pd.DataFrame(
                data={
                    "data": repete_vetor(datas, len(MESES_DF) - 1),
                    "lag": np.tile(np.arange(1, len(MESES_DF)), len(datas)),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(4):
            file.readline()

        # Variáveis auxiliares
        meses: List[str] = []
        anos: List[str] = []
        tabela = np.zeros((MAX_ANOS_HISTORICO * len(MESES_DF), 11))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                tabela = tabela[:i, :]  # type: ignore
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados = self.__linha.read(linha)
            meses.append(dados[0])
            anos.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1


class BlocoCorrelEspacialAnualConfig(Block):
    """
    Bloco de informações do arquivo `parpeol.dat`
    relativo à correlação espacial histórica espacial
    anual por configuração.
    """

    __slots__ = ["__campo_cfg", "__linha"]

    BEGIN_PATTERN = "CORRELACAO ESPACIAL HISTORICA ANUAL"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_cfg = IntegerField(4, 68)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelEspacialAnualConfig):
            return False
        bloco: BlocoCorrelEspacialAnualConfig = o
        if not all([
            isinstance(self.data, pd.DataFrame),
            isinstance(o.data, pd.DataFrame),
        ]):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=rees_uees)
            df["uee"] = uees
            df["configuracao"] = cfg
            df = df[["configuracao", "uee"] + rees_uees]
            return df

        # Identifica a configuração
        linha = file.readline()
        cfg = self.__campo_cfg.read(linha)

        file.readline()
        linha = file.readline()
        rees_uees = [r.strip() for r in linha.split(" ") if len(r) > 2]
        campo_uee: List[Field] = [LiteralField(12, 0)]
        campo_correl: List[Field] = [
            FloatField(13, 12 + 13 * i, 4) for i in range(len(rees_uees))
        ]
        self.__linha = Line(campo_uee + campo_correl)

        # Variáveis auxiliares
        uees: List[str] = []
        tabela = np.zeros((MAX_UEES, len(rees_uees)))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                tabela = tabela[:i, :]  # type: ignore
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados = self.__linha.read(linha)
            tabela[i, :] = dados[1:]
            uees.append(dados[0])
            i += 1


class BlocoCorrelEspacialMensalConfig(Block):
    """
    Bloco de informações do arquivo `parpeol.dat`
    relativo à correlação espacial histórica espacial
    mensal por configuração.
    """

    __slots__ = ["__campo_cfg", "__linha"]

    BEGIN_PATTERN = "CORRELACAO ESPACIAL HISTORICA MENSAL"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_cfg = IntegerField(4, 69)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelEspacialMensalConfig):
            return False
        bloco: BlocoCorrelEspacialMensalConfig = o
        if not all([
            isinstance(self.data, pd.DataFrame),
            isinstance(o.data, pd.DataFrame),
        ]):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=uees_rees)
            df["uee"] = uees
            df["configuracao"] = cfg
            df = df[["configuracao", "uee"] + uees_rees]
            df = df.rename(columns={"MES": "mes"})
            df = df.astype({"mes": "int64"})
            return df

        # Identifica a configuração
        linha = file.readline()
        cfg = self.__campo_cfg.read(linha)

        file.readline()
        linha = file.readline()
        uees_rees = [r.strip() for r in linha.split(" ") if len(r) > 2]
        campo_uee: List[Field] = [LiteralField(12, 0)]
        campo_mes: List[Field] = [IntegerField(2, 15)]
        campo_correl: List[Field] = [
            FloatField(8, 17 + 13 * i, 4) for i in range(len(uees_rees) - 1)
        ]
        self.__linha = Line(campo_uee + campo_mes + campo_correl)

        # Variáveis auxiliares
        tabela = np.zeros((
            MAX_CONFIGURACOES * (MAX_UEES + MAX_REES) * len(MESES_DF),
            len(uees_rees),
        ))
        uees: List[str] = []
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                linha = file.readline()
                if len(linha) < 4:
                    tabela = tabela[:i, :]  # type: ignore
                    self.data = converte_tabela_em_df()
                    break
                else:
                    continue
            # Senão, processa os dados
            dados_linha = self.__linha.read(linha)
            uees.append(dados_linha[0])
            tabela[i, :] = dados_linha[1:]
            i += 1
