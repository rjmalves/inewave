# Imports do próprio módulo

from inewave.config import (
    MAX_ANOS_ESTUDO,
    MAX_ANOS_HISTORICO,
    MAX_UHES,
    MESES_ABREV,
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


class BlocoSerieVazoesUHE(Block):
    """
    Bloco de informações do arquivo `parpvaz.dat`
    relativo às séries de vazões por usina.
    """

    BEGIN_PATTERN = "SERIE  DE VAZOES   DA USINA"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__campo_uhe = LiteralField(14, 57)
        self.__campo_cfg = IntegerField(5, 88)
        campo_ano: List[Field] = [IntegerField(4, 0)]
        campo_vazao: List[Field] = [
            FloatField(10, 4 + 11 * i, 2) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campo_vazao)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSerieVazoesUHE):
            return False
        bloco: BlocoSerieVazoesUHE = o
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
            df["UHE"] = uhe
            df["Configuração"] = cfg
            df = df[["UHE", "Configuração", "Ano"] + MESES_DF]
            df = df.astype({"Ano": "int64"})
            return df

        # Identifica a usina e a configuração
        linha = file.readline()
        uhe = self.__campo_uhe.read(linha)
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


class BlocoCorrelVazoesUHE(Block):
    """
    Bloco de informações do arquivo `parpvaz.dat`
    relativo às séries de autocorrelações
    das vazões por usina.
    """

    BEGIN_PATTERN = "CORRELOGRAMO DA SERIE DE VAZOES"
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
        if not isinstance(o, BlocoCorrelVazoesUHE):
            return False
        bloco: BlocoCorrelVazoesUHE = o
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
            # TODO - remover fallback de 1970 quando estiver o ano correto.
            primeiro_ano_estudo = (
                sorted(anos_estudo)[0] if len(anos_estudo) > 0 else 1970
            )
            # Descobre o último ano de estudo
            ultimo_ano_estudo = (
                sorted(anos_estudo)[-1] if len(anos_estudo) > 0 else 1970
            )
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


class BlocoCorrelParcialVazoesUHE(Block):
    """
    Bloco de informações do arquivo `parpvaz.dat`
    relativo às séries de autocorrelações parciais
    das vazões por UHE.
    """

    BEGIN_PATTERN = "CORRELOGRAMO PARCIAL DA SERIE DE VAZOES"
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
        if not isinstance(o, BlocoCorrelParcialVazoesUHE):
            return False
        bloco: BlocoCorrelParcialVazoesUHE = o
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
            # TODO - remover fallback de 1970 quando estiver o ano correto.
            # Descobre o primeiro ano de estudo
            primeiro_ano_estudo = (
                sorted(anos_estudo)[0] if len(anos_estudo) > 0 else 1970
            )
            # Descobre o último ano de estudo
            ultimo_ano_estudo = (
                sorted(anos_estudo)[-1] if len(anos_estudo) > 0 else 1970
            )
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


class BlocoOrdemModeloUHE(Block):
    """
    Bloco de informações do arquivo `parpvaz.dat`
    relativo às ordens finais ajustadas do modelo e aos
    seus coeficientes por UHE.
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
        if not isinstance(o, BlocoOrdemModeloUHE):
            return False
        bloco: BlocoOrdemModeloUHE = o
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
            # TODO - remover fallback de 1970 quando estiver o ano correto.
            # Descobre o primeiro ano de estudo
            primeiro_ano_estudo = (
                sorted(anos_estudo)[0] if len(anos_estudo) > 0 else 1970
            )
            # Descobre o último ano de estudo
            ultimo_ano_estudo = (
                sorted(anos_estudo)[-1] if len(anos_estudo) > 0 else 1970
            )
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


class BlocoCoeficientesModeloUHE(Block):
    """
    Lista de coeficientes dos modelos PAR ou PAR-A por UHE.
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
        if not isinstance(o, BlocoCoeficientesModeloUHE):
            return False
        bloco: BlocoCoeficientesModeloUHE = o
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


class BlocoSerieRuidosUHE(Block):
    """
    Bloco de informações do arquivo `parpvaz.dat`
    relativo às séries de ruídos por usina.
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
        if not isinstance(o, BlocoSerieRuidosUHE):
            return False
        bloco: BlocoSerieRuidosUHE = o
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


class BlocoCorrelRuidosUHE(Block):
    """
    Bloco de informações do arquivo `parpvaz.dat`
    relativo às séries de autocorrelações
    dos ruídos por usina.
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
        if not isinstance(o, BlocoCorrelRuidosUHE):
            return False
        bloco: BlocoCorrelRuidosUHE = o
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
            # TODO - remover fallback de 1970 quando estiver o ano correto.
            # Descobre o primeiro ano de estudo
            primeiro_ano_estudo = (
                sorted(anos_estudo)[0] if len(anos_estudo) > 0 else 1970
            )
            # Descobre o último ano de estudo
            ultimo_ano_estudo = (
                sorted(anos_estudo)[-1] if len(anos_estudo) > 0 else 1970
            )
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


class BlocoCorrelEspacialAnualMensalUHE(Block):
    """
    Bloco de informações do arquivo `parpvaz.dat`
    relativo à correlação espacial histórica anual e
    mensal para as UHEs.
    """

    BEGIN_PATTERN = "CORRELACAO ESPACIAL HISTORICA MENSAL/ANUAL ENTRE AS UHEs"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_uhe_1: List[Field] = [LiteralField(12, 1)]
        campo_uhe_2: List[Field] = [LiteralField(12, 15)]
        correl: List[Field] = [FloatField(6, 28 + 7 * i, 2) for i in range(13)]
        self.__linha = Line(campo_uhe_1 + campo_uhe_2 + correl)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrelEspacialAnualMensalUHE):
            return False
        bloco: BlocoCorrelEspacialAnualMensalUHE = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(bloco.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=MESES_DF + ["Anual"])
            df["UHE 1"] = uhes1
            df["UHE 2"] = uhes2
            return df[["UHE 1", "UHE 2"] + MESES_DF + ["Anual"]]

        for _ in range(4):
            file.readline()

        # Variáveis auxiliares
        uhes1: List[str] = []
        uhes2: List[str] = []
        tabela = np.zeros((int(MAX_UHES * (MAX_UHES - 1) / 2), 13))
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
            uhes1.append(dados[0])
            uhes2.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1
