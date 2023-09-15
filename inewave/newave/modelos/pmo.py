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
from inewave._utils.formatacao import (
    prepara_vetor_anos_tabela,
    repete_vetor,
)


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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                data={
                    "nome_ree": repete_vetor(rees),
                    "mes": np.tile(np.arange(1, len(MESES_DF) + 1), len(rees)),
                    "valor": tabela.flatten(),
                }
            )
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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                data={
                    "nome_ree": repete_vetor(rees),
                    "mes": np.tile(np.arange(1, len(MESES_DF) + 1), len(rees)),
                    "valor": tabela.flatten(),
                }
            )
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


class BlocoEnergiaArmazenadaInicialPMO(Block):
    """
    Bloco de informações da energia armazenada inicial dos REE
    localizado no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = r"ENERGIA ARMAZENADA INICIAL \(MWmes"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEnergiaArmazenadaInicialPMO):
            return False
        bloco: BlocoEnergiaArmazenadaInicialPMO = o
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
                    "nome_ree": nomes,
                    "valor_MWmes": valores_MWmes,
                    "valor_percentual": valores_percentual,
                }
            )
            return df

        # Pula as linhas iniciais
        for _ in range(2):
            file.readline()

        linha_nomes = file.readline()
        nomes = [n.strip() for n in linha_nomes.split(" ") if len(n) > 2]
        num_rees = len(nomes)
        linha_valores = Line(
            [FloatField(11, 13 * i, 1) for i in range(num_rees)]
        )
        valores_MWmes: List[float] = linha_valores.read(file.readline())
        valores_percentual: List[float] = linha_valores.read(file.readline())
        self.data = converte_tabela_em_df()


class BlocoVolumeArmazenadoInicialPMO(Block):
    """
    Bloco de informações do volume armazenado inicial das UHE
    localizado no arquivo `pmo.dat`.
    """

    BEGIN_PATTERN = r" VOLUME ARMAZENADO INICIAL"
    END_PATTERN = "X-----X------------X"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(5, 2),
                LiteralField(12, 8),
                FloatField(14, 21, 1),
                FloatField(12, 36, 1),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoVolumeArmazenadoInicialPMO):
            return False
        bloco: BlocoVolumeArmazenadoInicialPMO = o
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
                    "codigo_usina": codigos_uhes,
                    "nome_usina": nomes_uhes,
                    "valor_hm3": volume_hm3,
                    "valor_percentual": volume_percentual,
                }
            )
            return df

        # Pula as linhas iniciais
        for _ in range(5):
            file.readline()

        # Variáveis auxiliares
        codigos_uhes: List[int] = []
        nomes_uhes: List[str] = []
        volume_hm3: List[float] = []
        volume_percentual: List[float] = []

        while True:
            linha = file.readline()
            if self.ends(linha):
                self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            codigos_uhes.append(dados[0])
            nomes_uhes.append(dados[1])
            volume_hm3.append(dados[2])
            volume_percentual.append(dados[3])

        self.data = converte_tabela_em_df()


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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = [
                "iteracao",
                "limite_inferior_zinf",
                "zinf",
                "limite_superior_zinf",
                "zsup",
                "delta_zinf",
                "zsup_iteracao",
            ]
            df = df.astype({"iteracao": "int64"})
            df["tempo"] = tempos
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
        self.__line = Line([IntegerField(6, 5 + 6 * i) for i in range(13)])

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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame(
                data={
                    "data": prepara_vetor_anos_tabela(anos),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Pula as linhas iniciais
        for _ in range(6):
            file.readline()
        # Variáveis auxiliares
        anos: List[int] = []
        tabela = np.zeros((MAX_ANOS_ESTUDO, len(MESES_DF)), dtype=np.int64)
        i = 0
        while True:
            linha: str = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            # Lê mais uma linha
            dados = self.__line.read(linha)
            anos.append(dados[0])
            tabela[i, :] = dados[1:]
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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            colunas = ["reta", "coeficiente_angular", "coeficiente_linear"]
            df = pd.DataFrame(tabela, columns=colunas)
            df["nome_ree"] = rees
            df = df[["nome_ree"] + colunas]
            df = df.astype({"reta": "int64"})
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

    BEGIN_PATTERN = r"RISCO ANUAL DE DEFICIT E E\(ENS\) \(%\)"  # noqa
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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(
                data={
                    "ano": repete_vetor(list(tabela[:, 0]), len(subsistemas)),
                    "nome_submercado": np.tile(subsistemas, tabela.shape[0]),
                    "risco": tabela[:, 1::2].flatten(),
                    "eens": tabela[:, 2::2].flatten(),
                }
            )
            return df.astype({"ano": int})

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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df() -> pd.DataFrame:
            cols = ["valor_esperado", "desvio_padrao", "percentual"]
            df = pd.DataFrame(tabela, columns=cols)
            df["parcela"] = parcelas
            df = df[["parcela"] + cols]
            return df

        # Salta duas linhas
        for _ in range(2):
            file.readline()
        parcelas: List[str] = []
        tabela = np.zeros((100, 3), dtype=np.float64)
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
    def read(self, file: IO, *args, **kwargs):
        data = [0, 0]
        for i in range(2):
            data[i] = self.__line.read(file.readline())[0]
        self.data = data


class BlocoProdutibilidadesConfiguracaoPMO(Block):
    """
    Bloco de informações sobre as produtibilidades das UHEs por
    configuração.
    """

    BEGIN_PATTERN = r"PRODUTIBILIDADES \(MW/m3/s\)"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        # Cria a estrutura de uma linha da tabela
        self.__cfg_line = Line([IntegerField(4, 16)])
        self.__prodt_line = Line([LiteralField(14, 2), FloatField(9, 17, 4)])
        self.__prodt_reserv_line = Line(
            [LiteralField(12, 2)]
            + [FloatField(8, 15 + 9 * i, 4) for i in range(4)]
        )
        self.__prod_acum_line = Line(
            [LiteralField(12, 2)]
            + [FloatField(8, 15 + 9 * i, 4) for i in range(9)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoProdutibilidadesConfiguracaoPMO):
            return False
        bloco: BlocoProdutibilidadesConfiguracaoPMO = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(bloco.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    def __le_produtibilidade_usinas(self, file: IO) -> pd.DataFrame:
        # Salta 3 linhas
        for _ in range(3):
            file.readline()
        nomes: List[str] = []
        prodts: List[float] = []
        while True:
            linha = file.readline()
            # Confere se acabou
            if "X------------X" in linha:
                return pd.DataFrame(
                    data={
                        "nome_usina": nomes,
                        "produtibilidade_equivalente_volmin_volmax": prodts,
                    }
                )
            dados = self.__prodt_line.read(linha)
            nomes.append(dados[0])
            prodts.append(dados[1])

    def __le_produtibilidade_reservatorios(self, file: IO) -> pd.DataFrame:
        # Salta 1 linha
        file.readline()
        cols = self.__colunas_produtibilidades_reservatorios()
        nomes: List[str] = []
        prodts: List[List[float]] = [[] for _ in range(len(cols))]
        while True:
            linha = file.readline()
            # Confere se acabou
            if "X--------------" in linha:
                dados_df = {c: p for c, p in zip(cols, prodts)}
                df = pd.DataFrame(data=dados_df)
                df["nome_usina"] = nomes
                return df
            dados = self.__prodt_reserv_line.read(linha)
            nomes.append(dados[0])
            for i in range(len(cols)):
                prodts[i].append(dados[i + 1])

    def __le_produtibilidade_acumulada(self, file: IO) -> pd.DataFrame:
        # Salta 3 linhas
        for _ in range(3):
            file.readline()
        cols = self.__colunas_produtibilidades_acumuladas()
        nomes: List[str] = []
        prodts: List[List[float]] = [[] for _ in range(len(cols))]
        while True:
            linha = file.readline()
            # Confere se acabou
            if "X--------------" in linha or len(linha.strip()) < 3:
                dados_df = {c: p for c, p in zip(cols, prodts)}
                df = pd.DataFrame(data=dados_df)
                df["nome_usina"] = nomes
                return df
            dados = self.__prod_acum_line.read(linha)
            nomes.append(dados[0])
            for i in range(len(cols)):
                prodts[i].append(dados[i + 1])

    def __colunas_produtibilidades_reservatorios(self) -> List[str]:
        return [
            "produtibilidade_equivalente_volmin_vol65",
            "produtibilidade_altura_minima",
            "produtibilidade_altura_65",
            "produtibilidade_altura_maxima",
        ]

    def __colunas_produtibilidades_acumuladas(self) -> List[str]:
        return [
            "produtibilidade_acumulada_calculo_earm",
            "produtibilidade_acumulada_calculo_earm_65",
            "produtibilidade_acumulada_calculo_econ",
            "produtibilidade_acumulada_calculo_altura_minima",
            "produtibilidade_acumulada_calculo_altura_65",
            "produtibilidade_acumulada_calculo_altura_maxima",
            "produtibilidade_acumulada_calculo_evaporacao_altura_minima",
            "produtibilidade_acumulada_calculo_evaporacao_altura_65",
            "produtibilidade_acumulada_calculo_evaporacao_altura_maxima",
        ]

    def __fecha_configuracao(
        self,
        df_usinas: pd.DataFrame,
        df_reservatorios: pd.DataFrame,
        df_acumuladas: pd.DataFrame,
        cfg_atual: int,
        df_atual: pd.DataFrame,
    ) -> pd.DataFrame:
        todas_usinas = list(
            set(
                df_usinas.index.tolist()
                + df_reservatorios.index.tolist()
                + df_acumuladas.index.tolist()
            )
        )
        todas_usinas.sort()
        df_agregado = pd.DataFrame(index=todas_usinas)
        df_agregado.loc[
            df_usinas.index,
            "produtibilidade_equivalente_volmin_volmax",
        ] = df_usinas["produtibilidade_equivalente_volmin_volmax"]
        for col in self.__colunas_produtibilidades_reservatorios():
            df_agregado.loc[
                df_reservatorios.index,
                col,
            ] = df_reservatorios[col]
        for col in self.__colunas_produtibilidades_acumuladas():
            df_agregado.loc[
                df_acumuladas.index,
                col,
            ] = df_acumuladas[col]
        df_agregado["configuracao"] = cfg_atual
        df_atual = pd.concat(
            [df_atual, df_agregado.reset_index()],
            ignore_index=True,
        )
        return df_atual

    # Override
    def read(self, file: IO, *args, **kwargs):
        cfg_atual = 0
        df_atual = pd.DataFrame()
        df_usinas = pd.DataFrame()
        df_reservatorios = pd.DataFrame()
        df_acumuladas = pd.DataFrame()
        while True:
            linha = file.readline()
            # Verifica se acabou:
            if "PRODUTIBILIDADES ACUMULADAS PARA CALCULO DE" in linha:
                if cfg_atual != 0:
                    df_atual = self.__fecha_configuracao(
                        df_usinas,
                        df_reservatorios,
                        df_acumuladas,
                        cfg_atual,
                        df_atual,
                    )
                self.data = df_atual.rename(columns={"index": "nome_usina"})[
                    [
                        "nome_usina",
                        "configuracao",
                        "produtibilidade_equivalente_volmin_volmax",
                    ]
                    + self.__colunas_produtibilidades_reservatorios()
                    + self.__colunas_produtibilidades_acumuladas()
                ]
                break
            if "CONFIGURACAO :" in linha:
                if cfg_atual != 0:
                    df_atual = self.__fecha_configuracao(
                        df_usinas,
                        df_reservatorios,
                        df_acumuladas,
                        cfg_atual,
                        df_atual,
                    )
                cfg_atual = self.__cfg_line.read(linha)[0]
            if "PRODUTIBILIDADES DAS USINAS (MW/m3/s)" in linha:
                df_usinas = self.__le_produtibilidade_usinas(file)
                df_usinas.set_index("nome_usina", inplace=True)
            if "USINA      PRODTM   PDTMIN   PDTMED   PDTMAX" in linha:
                df_reservatorios = self.__le_produtibilidade_reservatorios(
                    file
                )
                df_reservatorios.set_index("nome_usina", inplace=True)
            if "PRODUTIBILIDADES DOS RESERVATORIOS (MW/m3/s)" in linha:
                df_acumuladas = self.__le_produtibilidade_acumulada(file)
                df_acumuladas.set_index("nome_usina", inplace=True)
