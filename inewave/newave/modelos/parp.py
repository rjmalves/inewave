# Imports do próprio módulo

from inewave.config import (
    MAX_ANOS_ESTUDO,
    MAX_ANOS_HISTORICO,
    MAX_CONFIGURACOES,
    MESES_ABREV,
    MAX_REES,
    MESES_DF,
)

# Imports de módulos externos
from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from datetime import date
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List


class BlocoSerieEnergiaREE(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de energia por REE.
    """

    BEGIN_PATTERN = "SERIE  DE ENERGIAS DO REE"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_ree = LiteralField(16, 55)
        self.__campo_cfg = IntegerField(5, 88)
        campo_ano: List[Field] = [IntegerField(4, 0)]
        campo_energia: List[Field] = [
            FloatField(10, 4 + 11 * i, 2) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campo_energia)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSerieEnergiaREE):
            return False
        bloco: BlocoSerieEnergiaREE = o
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
            df["REE"] = ree
            df["Configuração"] = cfg
            df = df[["REE", "Configuração", "Ano"] + MESES_DF]
            df = df.astype({"Ano": "int64"})
            return df

        # Identifica o REE e a configuração
        linha = file.readline()
        ree = self.__campo_ree.read(linha)
        cfg = self.__campo_cfg.read(linha)

        # Salta as linhas adicionais
        for _ in range(4):
            file.readline()

        # Variáveis auxiliares
        tabela = np.zeros((MAX_ANOS_HISTORICO, len(MESES_DF) + 1))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            tabela[i, :] = self.__linha.read(linha)
            i += 1


class BlocoCorrelEnergiasREE(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de autocorrelações
    das energias por REE.
    """

    BEGIN_PATTERN = "CORRELOGRAMO DA SERIE DE ENERGIAS"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_mes: List[Field] = [LiteralField(3, 1)]
        campo_ano: List[Field] = [LiteralField(4, 5)]
        correl: List[Field] = [
            FloatField(10, 9 + 10 * i, 5) for i in range(11)
        ]
        self.__linha = Line(campo_mes + campo_ano + correl)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelEnergiasREE):
            return False
        bloco: BlocoCorrelEnergiasREE = o
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
            cols = [f"Lag {i}" for i in range(1, 12)]
            df = pd.DataFrame(tabela, columns=cols)
            anos_conv = converte_vetor_anos(anos)
            meses_conv = converte_vetor_meses(meses)
            df["Data"] = [
                date(year=a, month=m, day=1)
                for a, m in zip(anos_conv, meses_conv)
            ]
            df = df[["Data"] + cols]
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
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados = self.__linha.read(linha)
            meses.append(dados[0])
            anos.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1


class BlocoCorrelParcialEnergiasREE(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de autocorrelações parciais
    das energias por REE.
    """

    BEGIN_PATTERN = "CORRELOGRAMO PARCIAL DA SERIE DE ENERGIAS"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_mes: List[Field] = [LiteralField(3, 1)]
        campo_ano: List[Field] = [LiteralField(4, 5)]
        correl: List[Field] = [
            FloatField(10, 9 + 10 * i, 5) for i in range(11)
        ]
        self.__linha = Line(campo_mes + campo_ano + correl)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelParcialEnergiasREE):
            return False
        bloco: BlocoCorrelParcialEnergiasREE = o
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
            cols = [f"Lag {i}" for i in range(1, 12)]
            df = pd.DataFrame(tabela, columns=cols)
            anos_conv = converte_vetor_anos(anos)
            meses_conv = converte_vetor_meses(meses)
            df["Data"] = [
                date(year=a, month=m, day=1)
                for a, m in zip(anos_conv, meses_conv)
            ]
            df = df[["Data"] + cols]
            return df

        # Salta as linhas adicionais
        for _ in range(3):
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
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados = self.__linha.read(linha)
            meses.append(dados[0])
            anos.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1


class BlocoOrdemModeloREE(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às ordens finais ajustadas do modelo e aos
    seus coeficientes por REE.
    """

    BEGIN_PATTERN = "DO MODELO AUTORREGRESSIVO PARA CADA PERIODO"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_ano: List[Field] = [LiteralField(4, 32)]
        orders: List[Field] = [
            IntegerField(5, 36 + 5 * i) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + orders)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoOrdemModeloREE):
            return False
        bloco: BlocoOrdemModeloREE = o
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
        def converte_vetor_anos(anos: List[str]) -> List[int]:
            # Descobre os anos pré e pós estudo
            numero_anos_pre = len([p for p in anos if p == "PRE"])
            numero_anos_pos = len([p for p in anos if p == "POS"])
            anos_estudo = [int(p) for p in anos if p not in ["PRE", "POS"]]
            # Descobre o primeiro ano de estudo
            primeiro_ano_estudo = sorted(anos_estudo)[0]
            # Descobre o último ano de estudo
            ultimo_ano_estudo = sorted(anos_estudo)[-1]
            indice_inicio_pos = anos.index("POS")
            # Substitui os anos pré e pós pelos valores específicos
            for a in range(numero_anos_pre):
                idx = a
                ano = primeiro_ano_estudo - (numero_anos_pre - a)
                anos[idx] = str(ano)
            for a in range(numero_anos_pos):
                idx = indice_inicio_pos + a
                ano = ultimo_ano_estudo + a + 1
                anos[idx] = str(ano)
            return [int(a) for a in anos]

        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=MESES_DF)
            df["Tipo"] = self.__tipo
            df["Ano"] = converte_vetor_anos(anos)
            df = df[["Tipo", "Ano"] + MESES_DF]
            return df

        # Salta as linhas adicionais
        linha = file.readline()
        self.__tipo = linha.split("ORDEM")[1].split("DO MODELO")[0].strip()
        for _ in range(3):
            file.readline()

        # Variáveis auxiliares
        anos: List[str] = []
        tabela = np.zeros((3 * MAX_ANOS_ESTUDO, len(MESES_DF)), dtype=np.int64)
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados = self.__linha.read(linha)
            anos.append(dados[0])
            tabela[i, :] = dados[1:]
            i += 1


class BlocoCoeficientesModeloREE(Block):
    """
    Lista de coeficientes dos modelos PAR ou PAR-A por REE.
    """

    BEGIN_PATTERN = " COEFICIENTES DA EQUACAO DE REGRESSAO DE UM PROCESSO"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        coefs: List[Field] = [
            FloatField(9, 11 * i, 3, format="E") for i in range(11)
        ]
        self.__linha = Line(coefs)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCoeficientesModeloREE):
            return False
        bloco: BlocoCoeficientesModeloREE = o
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
            cols = (
                [f"Psi {i}" for i in range(1, len(MESES_DF))]
                + ["Psi A"]
                + [f"Psi Norm {i}" for i in range(1, len(MESES_DF))]
                + ["Psi Norm A"]
            )
            return pd.DataFrame(tabela, columns=cols)

        linha = file.readline()

        tabela = np.zeros((1, 2 * len(MESES_DF)))
        # Processa os dados
        dados_psi = self.__linha.read(file.readline())
        dados_psi_norm = self.__linha.read(file.readline())
        linha = file.readline()
        if len(linha) < 3:
            dados_psi_a = [0.0, 0.0]
        else:
            dados_psi_a = [
                self.__linha.read(linha)[0],
                self.__linha.read(file.readline())[0],
            ]
        tabela[0, :] = (
            dados_psi + [dados_psi_a[0]] + dados_psi_norm + [dados_psi_a[1]]
        )
        self.data = converte_tabela_em_df()


class BlocoSerieRuidosREE(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de ruídos por REE.
    """

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
        if not isinstance(o, BlocoSerieRuidosREE):
            return False
        bloco: BlocoSerieRuidosREE = o
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
            df["Ano"] = ano
            df["Série"] = list(range(i))
            df = df[["Ano", "Série"] + MESES_DF]
            return df

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
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            tabela[i, :] = self.__linha.read(linha)
            i += 1


class BlocoCorrelRuidosREE(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de autocorrelações
    dos ruídos por REE.
    """

    BEGIN_PATTERN = "CORRELOGRAMO DA SERIE DE RUIDOS"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_mes: List[Field] = [LiteralField(3, 1)]
        campo_ano: List[Field] = [LiteralField(4, 5)]
        correl: List[Field] = [
            FloatField(10, 9 + 10 * i, 5) for i in range(11)
        ]
        self.__linha = Line(campo_mes + campo_ano + correl)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelRuidosREE):
            return False
        bloco: BlocoCorrelRuidosREE = o
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
            cols = [f"Lag {i}" for i in range(1, 12)]
            df = pd.DataFrame(tabela, columns=cols)
            anos_conv = converte_vetor_anos(anos)
            meses_conv = converte_vetor_meses(meses)
            df["Data"] = [
                date(year=a, month=m, day=1)
                for a, m in zip(anos_conv, meses_conv)
            ]
            df = df[["Data"] + cols]
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
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            dados = self.__linha.read(linha)
            meses.append(dados[0])
            anos.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1


class BlocoSerieMediasREE(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de médias de 12 meses por REE.
    """

    BEGIN_PATTERN = "SERIE MEDIA 12 MESES - ANO:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_ano = LiteralField(5, 77)
        campos: List[Field] = [
            FloatField(11, 3 + 11 * i, 2, format="F")
            for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campos)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSerieMediasREE):
            return False
        bloco: BlocoSerieMediasREE = o
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
            df["Ano"] = ano
            df["Série"] = list(range(i))
            df = df[["Ano", "Série"] + MESES_DF]
            return df

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
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            tabela[i, :] = self.__linha.read(linha)
            i += 1


class BlocoCorrelCruzadaMediaREE(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de correlação cruzada da variável
    anual com as energias por REE.
    """

    BEGIN_PATTERN = "CORRELACAO CRUZADA VARIAVEL ANUAL  ENERGIAS"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_mes: List[Field] = [LiteralField(3, 1)]
        campo_ano: List[Field] = [LiteralField(4, 5)]
        correl: List[Field] = [
            FloatField(10, 9 + 10 * i, 5) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_mes + campo_ano + correl)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelCruzadaMediaREE):
            return False
        bloco: BlocoCorrelCruzadaMediaREE = o
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
            df = pd.DataFrame(tabela, columns=MESES_DF)
            anos_conv = converte_vetor_anos(anos)
            meses_conv = converte_vetor_meses(meses)
            df["Data"] = [
                date(year=a, month=m, day=1)
                for a, m in zip(anos_conv, meses_conv)
            ]
            df = df[["Data"] + MESES_DF]
            return df

        # Salta as linhas adicionais
        for _ in range(5):
            file.readline()

        # Variáveis auxiliares
        meses: List[str] = []
        anos: List[str] = []
        tabela = np.zeros((MAX_ANOS_HISTORICO * len(MESES_DF), len(MESES_DF)))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                tabela = tabela[:i, :]
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
    Bloco de informações do arquivo `parp.dat`
    relativo à correlação espacial histórica espacial
    anual por configuração.
    """

    BEGIN_PATTERN = "CORRELACAO ESPACIAL HISTORICA ANUAL"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_cfg = IntegerField(4, 68)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelEspacialAnualConfig):
            return False
        bloco: BlocoCorrelEspacialAnualConfig = o
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
            df = pd.DataFrame(tabela, columns=rees)
            df["REE"] = rees
            df["Configuração"] = cfg
            df = df[["Configuração", "REE"] + rees]
            return df

        # Identifica a configuração
        linha = file.readline()
        cfg = self.__campo_cfg.read(linha)

        file.readline()
        linha = file.readline()
        rees = [r.strip() for r in linha.split(" ") if len(r) > 2]
        campo_ree: List[Field] = [LiteralField(12, 0)]
        campo_correl: List[Field] = [
            FloatField(13, 12 + 13 * i, 4) for i in range(len(rees))
        ]
        self.__linha = Line(campo_ree + campo_correl)

        # Variáveis auxiliares
        tabela = np.zeros((len(rees), len(rees)))
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                self.data = converte_tabela_em_df()
                break
            # Senão, processa os dados
            tabela[i, :] = self.__linha.read(linha)[1:]
            i += 1


class BlocoCorrelEspacialMensalConfig(Block):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo à correlação espacial histórica espacial
    mensal por configuração.
    """

    BEGIN_PATTERN = "CORRELACAO ESPACIAL HISTORICA MENSAL"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_cfg = IntegerField(4, 69)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelEspacialMensalConfig):
            return False
        bloco: BlocoCorrelEspacialMensalConfig = o
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
            df = pd.DataFrame(tabela, columns=rees)
            df["REE"] = valores_rees
            df["Configuração"] = cfg
            df = df[["Configuração", "REE"] + rees]
            df = df.astype({"MES": "int64"})
            return df

        # Identifica a configuração
        linha = file.readline()
        cfg = self.__campo_cfg.read(linha)

        file.readline()
        linha = file.readline()
        rees = [r.strip() for r in linha.split(" ") if len(r) > 2]
        campo_ree: List[Field] = [LiteralField(12, 0)]
        campo_mes: List[Field] = [IntegerField(2, 15)]
        campo_correl: List[Field] = [
            FloatField(8, 17 + 13 * i, 4) for i in range(len(rees) - 1)
        ]
        self.__linha = Line(campo_ree + campo_mes + campo_correl)

        # Variáveis auxiliares
        tabela = np.zeros(
            (MAX_CONFIGURACOES * MAX_REES * len(MESES_DF), len(rees))
        )
        valores_rees: List[str] = []
        i = 0
        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 4:
                linha = file.readline()
                if len(linha) < 4:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                    break
                else:
                    continue
            # Senão, processa os dados
            dados_linha = self.__linha.read(linha)
            valores_rees.append(dados_linha[0])
            tabela[i, :] = dados_linha[1:]
            i += 1
