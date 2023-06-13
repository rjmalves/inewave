from cfinterface.components.section import Section
from typing import IO, List, Dict, Union, Callable, Any
import numpy as np  # type: ignore
import numpy.typing as npt
import pandas as pd  # type: ignore
from enum import Enum


class VariavelOperacao(Enum):
    MERCADO = "MER"
    ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL = "EARMI"
    ENERGIA_NATURAL_AFLUENTE_ABSOLUTA = "ENAA"
    GERACAO_HIDRAULICA_CONTROLAVEL = "GHIDC"
    ENERGIA_VERTIDA = "EVER"
    ENERGIA_ARMAZENADA_ABSOLUTA_FINAL = "EARMF"
    ENERGIA_NATURAL_AFLUENTE_FIO_BRUTA = "ENAFB"
    ENERGIA_EVAPORADA = "EVAP"
    ENERGIA_ENCHIMENTO_VOLUME_MORTO = "EVMOR"
    GERACAO_TERMICA = "GTER"
    DEFICIT = "DEF"
    VALOR_AGUA = "VAGUA"
    CUSTO_MARGINAL_OPERACAO = "CMO"
    GERACAO_HIDRAULICA_FIO_LIQUIDA = "GHIDFL"
    PERDAS_GERACAO_HIDRAULICA_FIO = "PGHIDF"
    INTERCAMBIO = "INT"
    EXCESSO = "EXC"
    ENERGIA_NATURAL_AFLUENTE_BRUTA = "ENAB"
    ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL_CORRIGIDA = "ENAC"
    GERACAO_HIDRAULICA_MAXIMA = "GHIDMAX"
    ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO = "ENACD"
    ENERGIA_AFLUENTE_FIO_DESVIO = "ENAFD"
    BENEFICIO_INTERCAMBIO = "BINT"
    FATOR_CORRECAO_ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL = "FCENA"
    VIOLACAO_CURVA_AVERSAO = "VVMINOP"
    ACIONAMENTO_CURVA_AVERSAO = "AVMINOP"
    PENALIDADE_CURVA_AVERSAO = "PVMINOP"
    CUSTO_OPERACAO = "COP"
    CUSTO_GERACAO_TERMICA = "CTER"
    BENEFICIO_AGRUPAMENTO_INTERCAMBIO = "BAGRINT"
    ENERGIA_NATURAL_AFLUENTE_FIO = "ENAF"
    BENEFICIO_DESPACHO_GNL = "BGNL"
    VIOLACAO_GERACAO_HIRAULICA_MINIMA = "VGHIDMIN"
    VIOLACAO_ENERGIA_VAZAO_MINIMA = "VEVMIN"
    INVASAO_SAR = "ISAR"
    ACIONAMENTO_SAR = "ASAR"
    PENALIDADE_SAR = "PSAR"
    GERACAO_HIDRAULICA_MAXIMA_CONSIDERANDO_RE = "GHIDMAXR"
    VOLUME_ARMAZENADO_ABSOLUTO_FINAL = "VARMF"
    GERACAO_HIDRAULICA_USINA = "GHIDU"
    VOLUME_TURBINADO = "VTUR"
    VOLUME_VERTIDO = "VVER"
    VIOLACAO_GERACAO_HIDRAULICA_MINIMA_USINA = "VGHIDMINU"
    ENCHIMENTO_VOLUME_MORTO_USINA = "VMORU"
    VIOLACAO_DEFLUENCIA_MINIMA = "VDEFMIN"
    VOLUME_DESVIO_USINA = "VOLDU"
    VOLUME_DESVIO_POSITIVO_USINA = "VOLDPU"
    VOLUME_DESVIO_NEGATIVO_USINA = "VOLDNU"
    ##
    VIOLACAO_FPHA = "VFPHA"
    VAZAO_AFLUENTE = "QAFL"
    VAZAO_INCREMENTAL = "QINC"
    VOLUME_ARMAZENADO_PERCENTUAL_FINAL = "VARPF"
    GEOL_GSOL_OLD = "GEOL_GSOL_OLD"
    VIOLACAO_GEE = "VIOLACAO_GEE"
    CUSTO_VIOLACAO_ENERGIA_VAZAO_MINIMA = "CVEVMIN"
    CUSTO_ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO = "CENACD"
    CUSTO_ENERGIA_AFLUENTE_FIO_DESVIO = "CENAFD"
    CUSTO_VIOLACAO_GERACAO_HIDRAULICA_MINIMA = "CVGHIDMIN"
    SOMA_ENERGIA_NATURAL_AFLUENTE_12_MESES = "ENA12"
    SOMA_VAZAO_AFLUENTE_12_MESES = "QAFL12"
    GERACAO_EOLICA = "GEOL"
    VELOCIDADE_VENTO = "VENTO"
    VIOLACAO_FUNCAO_PRODUCAO_EOLICA = "VFPEOL"
    VIOLACAO_DEFLUENCIA_MAXIMA = "VDEFMAX"
    VIOLACAO_TURBINAMENTO_MINIMO = "VTURMIN"
    VIOLACAO_TURBINAMENTO_MAXIMO = "VTURMAX"
    VIOLACAO_LPP_TURBINAMENTO_MAXIMO = "VLPPTURMAX"
    VIOLACAO_LPP_DEFLUENCIA_MAXIMA = "VLPPDEFMAX"
    VIOLACAO_LPP_TURBINAMENTO_MAXIMO_USINA = "VLPPTURMAXU"
    VIOLACAO_LPP_DEFLUENCIA_MAXIMA_USINA = "VLPPDEFMAXU"
    RHS_LPP_TURBINAMENTO_MAXIMO = "RHSLPPTURMAX"
    RHS_LPP_DEFLUENCIA_MAXIMA = "RHSLPPDEFMAX"
    RHS_LPP_TURBINAMENTO_MAXIMO_USINA = "RHSLPPTURMAXU"
    RHS_LPP_DEFLUENCIA_MAXIMA_USINA = "RHSLPPDEFMAXU"
    VIOLACAO_RESTRICOES_ELETRICAS_ESPECIAIS = "VREESP"
    CUSTO_RESTRICOES_ELETRICAS_ESPECIAIS = "CREESP"
    VOLUME_ARMAZENADO_ABSOLUTO_INICIAL = "VARMI"
    VALOR_AGUA_USINA = "VAGUAU"
    VOLUME_EVAPORADO = "VEVAP"
    VOLUME_BOMBEADO = "VBOMB"
    CONSUMO_ENERGIA_ESTACAO_BOMBEAMENTO = "EBOMB"
    VOLUME_CANAL_DESVIO_USINA = "VOLCDU"


class SecaoDadosForward(Section):
    """
    Registro com os resultados da operação do modelo NEWAVE.
    """

    VARIAVEIS: List[VariavelOperacao] = [
        VariavelOperacao.MERCADO,
        VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL,
        VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_ABSOLUTA,
        VariavelOperacao.GERACAO_HIDRAULICA_CONTROLAVEL,
        VariavelOperacao.ENERGIA_VERTIDA,
        VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_FINAL,
        VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO_BRUTA,
        VariavelOperacao.ENERGIA_EVAPORADA,
        VariavelOperacao.ENERGIA_ENCHIMENTO_VOLUME_MORTO,
        VariavelOperacao.GERACAO_TERMICA,
        VariavelOperacao.DEFICIT,
        VariavelOperacao.VALOR_AGUA,
        VariavelOperacao.CUSTO_MARGINAL_OPERACAO,
        VariavelOperacao.GERACAO_HIDRAULICA_FIO_LIQUIDA,
        VariavelOperacao.PERDAS_GERACAO_HIDRAULICA_FIO,
        VariavelOperacao.INTERCAMBIO,
        VariavelOperacao.EXCESSO,
        VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_BRUTA,
        VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL_CORRIGIDA,
        VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA,
        VariavelOperacao.ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO,
        VariavelOperacao.ENERGIA_AFLUENTE_FIO_DESVIO,
        VariavelOperacao.BENEFICIO_INTERCAMBIO,
        VariavelOperacao.FATOR_CORRECAO_ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL,
        VariavelOperacao.VIOLACAO_CURVA_AVERSAO,
        VariavelOperacao.ACIONAMENTO_CURVA_AVERSAO,
        VariavelOperacao.PENALIDADE_CURVA_AVERSAO,
        VariavelOperacao.CUSTO_OPERACAO,
        VariavelOperacao.CUSTO_GERACAO_TERMICA,
        VariavelOperacao.BENEFICIO_AGRUPAMENTO_INTERCAMBIO,
        VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO,
        VariavelOperacao.BENEFICIO_DESPACHO_GNL,
        VariavelOperacao.VIOLACAO_GERACAO_HIRAULICA_MINIMA,
        VariavelOperacao.VIOLACAO_ENERGIA_VAZAO_MINIMA,
        VariavelOperacao.INVASAO_SAR,
        VariavelOperacao.ACIONAMENTO_SAR,
        VariavelOperacao.PENALIDADE_SAR,
        VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA_CONSIDERANDO_RE,
        VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_FINAL,
        VariavelOperacao.GERACAO_HIDRAULICA_USINA,
        VariavelOperacao.VOLUME_TURBINADO,
        VariavelOperacao.VOLUME_VERTIDO,
        VariavelOperacao.VIOLACAO_GERACAO_HIDRAULICA_MINIMA_USINA,
        VariavelOperacao.ENCHIMENTO_VOLUME_MORTO_USINA,
        VariavelOperacao.VIOLACAO_DEFLUENCIA_MINIMA,
        VariavelOperacao.VOLUME_DESVIO_USINA,
        VariavelOperacao.VOLUME_DESVIO_POSITIVO_USINA,
        VariavelOperacao.VOLUME_DESVIO_NEGATIVO_USINA,
        VariavelOperacao.VIOLACAO_FPHA,
        VariavelOperacao.VAZAO_AFLUENTE,
        VariavelOperacao.VAZAO_INCREMENTAL,
        VariavelOperacao.VOLUME_ARMAZENADO_PERCENTUAL_FINAL,
        VariavelOperacao.GEOL_GSOL_OLD,
        VariavelOperacao.VIOLACAO_GEE,
        VariavelOperacao.CUSTO_VIOLACAO_ENERGIA_VAZAO_MINIMA,
        VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO,
        VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_FIO_DESVIO,
        VariavelOperacao.CUSTO_VIOLACAO_GERACAO_HIDRAULICA_MINIMA,
        VariavelOperacao.SOMA_ENERGIA_NATURAL_AFLUENTE_12_MESES,
        VariavelOperacao.SOMA_VAZAO_AFLUENTE_12_MESES,
        VariavelOperacao.GERACAO_EOLICA,
        VariavelOperacao.VELOCIDADE_VENTO,
        VariavelOperacao.VIOLACAO_FUNCAO_PRODUCAO_EOLICA,
        VariavelOperacao.VIOLACAO_DEFLUENCIA_MAXIMA,
        VariavelOperacao.VIOLACAO_TURBINAMENTO_MAXIMO,
        VariavelOperacao.VIOLACAO_TURBINAMENTO_MINIMO,
        VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO,
        VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA,
        VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO_USINA,
        VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA_USINA,
        VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO,
        VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA,
        VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO_USINA,
        VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA_USINA,
        VariavelOperacao.VIOLACAO_RESTRICOES_ELETRICAS_ESPECIAIS,
        VariavelOperacao.CUSTO_RESTRICOES_ELETRICAS_ESPECIAIS,
        VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_INICIAL,
        VariavelOperacao.VALOR_AGUA_USINA,
        VariavelOperacao.VOLUME_EVAPORADO,
        VariavelOperacao.VOLUME_BOMBEADO,
        VariavelOperacao.CONSUMO_ENERGIA_ESTACAO_BOMBEAMENTO,
        VariavelOperacao.VOLUME_CANAL_DESVIO_USINA,
    ]

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.data: Dict[VariavelOperacao, Union[np.ndarray, pd.DataFrame]] = {}

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosForward):
            return False
        bloco: SecaoDadosForward = o
        if not all(
            [
                isinstance(self.data, dict),
                isinstance(bloco.data, dict),
            ]
        ):
            return False
        else:
            if not all(
                [isinstance(b, pd.DataFrame) for b in self.data.values()]
                + [isinstance(b, pd.DataFrame) for b in o.data.values()]
            ):
                return False
            else:
                return all(
                    [
                        (k1 == k2) and v1.equals(v2)  # type: ignore
                        for (k1, v1), (k2, v2) in zip(
                            self.data.items(), bloco.data.items()
                        )
                    ]
                )

    def __le_e_atribui_int(
        self, file: IO, destino: np.ndarray, tamanho: int, indice: int
    ):
        offset = tamanho * indice
        destino[offset : offset + tamanho] = np.frombuffer(
            file.read(tamanho * 4),
            dtype=np.int32,
            count=tamanho,
        )

    def __le_e_atribui_float(
        self, file: IO, destino: np.ndarray, tamanho: int, indice: int
    ):
        offset = tamanho * indice
        destino[offset : offset + tamanho] = np.frombuffer(
            file.read(tamanho * 4),
            dtype=np.float32,
            count=tamanho,
        )

    def __inicializa_variaveis(
        self, numero_estagios: int, numero_forwards: int
    ):
        # Variáveis que sempre existem
        self.__estagios_df = np.repeat(
            np.arange(1, numero_estagios + 1), numero_forwards
        )
        self.__cenarios_df = np.tile(
            np.arange(1, numero_forwards + 1), numero_estagios
        )
        self.__num_simulacoes = numero_estagios * numero_forwards
        self.estagio = np.zeros((1 * self.__num_simulacoes,), dtype=np.int32)
        # Variáveis que variam com a versão do modelo
        mapa_variaveis: Dict[
            VariavelOperacao, Callable[[Any], npt.NDArray[np.float32]]
        ] = {
            VariavelOperacao.MERCADO: lambda _: np.zeros(
                (self.numero_submercados * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_ABSOLUTA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_CONTROLAVEL: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.ENERGIA_VERTIDA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
            ),
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_FINAL: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO_BRUTA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
            ),
            VariavelOperacao.ENERGIA_EVAPORADA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
            ),
            VariavelOperacao.ENERGIA_ENCHIMENTO_VOLUME_MORTO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
            ),
            VariavelOperacao.GERACAO_TERMICA: lambda _: np.zeros(
                (
                    2
                    * self.total_classes_termicas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.DEFICIT: lambda _: np.zeros(
                (
                    self.numero_submercados
                    * self.numero_patamares_deficit
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VALOR_AGUA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.CUSTO_MARGINAL_OPERACAO: lambda _: np.zeros(
                (
                    self.numero_submercados
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_FIO_LIQUIDA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.PERDAS_GERACAO_HIDRAULICA_FIO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.INTERCAMBIO: lambda _: np.zeros(
                (
                    self.numero_total_submercados
                    * (self.numero_total_submercados - 1)
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.EXCESSO: lambda _: np.zeros(
                (
                    self.numero_submercados
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_BRUTA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL_CORRIGIDA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.ENERGIA_AFLUENTE_FIO_DESVIO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.BENEFICIO_INTERCAMBIO: lambda _: np.zeros(
                (
                    self.numero_total_submercados
                    * (self.numero_total_submercados - 1)
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.FATOR_CORRECAO_ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL: lambda _: np.zeros(  # noqa
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_CURVA_AVERSAO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.ACIONAMENTO_CURVA_AVERSAO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.PENALIDADE_CURVA_AVERSAO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.CUSTO_OPERACAO: lambda _: np.zeros(
                (1 * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.CUSTO_GERACAO_TERMICA: lambda _: np.zeros(
                (self.numero_submercados * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.BENEFICIO_AGRUPAMENTO_INTERCAMBIO: lambda _: np.zeros(
                (
                    self.numero_patamares_carga
                    * self.numero_agrupamentos_intercambio
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.BENEFICIO_DESPACHO_GNL: lambda _: np.zeros(
                (
                    self.numero_submercados
                    * self.numero_patamares_carga
                    * self.lag_maximo_usinas_gnl
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_GERACAO_HIRAULICA_MINIMA: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_ENERGIA_VAZAO_MINIMA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.INVASAO_SAR: lambda _: np.zeros(
                (1 * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.ACIONAMENTO_SAR: lambda _: np.zeros(
                (1 * self.__num_simulacoes,),
                dtype=np.int32,
            ),
            VariavelOperacao.PENALIDADE_SAR: lambda _: np.zeros(
                (1 * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA_CONSIDERANDO_RE: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_FINAL: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_USINA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_TURBINADO: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_VERTIDO: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_GERACAO_HIDRAULICA_MINIMA_USINA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.ENCHIMENTO_VOLUME_MORTO_USINA: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_DEFLUENCIA_MINIMA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_DESVIO_USINA: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_DESVIO_POSITIVO_USINA: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_DESVIO_NEGATIVO_USINA: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_FPHA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VAZAO_AFLUENTE: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VAZAO_INCREMENTAL: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.GEOL_GSOL_OLD: lambda _: np.zeros(
                (
                    2
                    * self.numero_submercados
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_GEE: lambda _: np.zeros(
                (1 * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_PERCENTUAL_FINAL: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.CUSTO_VIOLACAO_ENERGIA_VAZAO_MINIMA: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_FIO_DESVIO: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.CUSTO_VIOLACAO_GERACAO_HIDRAULICA_MINIMA: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.SOMA_ENERGIA_NATURAL_AFLUENTE_12_MESES: lambda _: np.zeros(
                (self.numero_rees * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.SOMA_VAZAO_AFLUENTE_12_MESES: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.GERACAO_EOLICA: lambda _: np.zeros(
                (
                    self.numero_parques_eolicos_equivalentes
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VELOCIDADE_VENTO: lambda _: np.zeros(
                (
                    self.numero_parques_eolicos_equivalentes
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_FUNCAO_PRODUCAO_EOLICA: lambda _: np.zeros(
                (
                    self.numero_parques_eolicos_equivalentes
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_DEFLUENCIA_MAXIMA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_TURBINAMENTO_MINIMO: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_TURBINAMENTO_MAXIMO: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO_USINA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA_USINA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA: lambda _: np.zeros(
                (
                    self.numero_rees
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO_USINA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA_USINA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VIOLACAO_RESTRICOES_ELETRICAS_ESPECIAIS: lambda _: np.zeros(
                (
                    self.numero_restricoes_eletricas_especiais
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.CUSTO_RESTRICOES_ELETRICAS_ESPECIAIS: lambda _: np.zeros(
                (
                    self.numero_restricoes_eletricas_especiais
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_INICIAL: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VALOR_AGUA_USINA: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_EVAPORADO: lambda _: np.zeros(
                (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_BOMBEADO: lambda _: np.zeros(
                (
                    self.numero_estacoes_bombeamento
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.CONSUMO_ENERGIA_ESTACAO_BOMBEAMENTO: lambda _: np.zeros(
                (
                    self.numero_estacoes_bombeamento
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
            VariavelOperacao.VOLUME_CANAL_DESVIO_USINA: lambda _: np.zeros(
                (
                    self.numero_usinas_hidreletricas
                    * self.numero_patamares_carga
                    * self.__num_simulacoes,
                ),
                dtype=np.float32,
            ),
        }
        for v in self.__class__.VARIAVEIS:
            self.data[v] = mapa_variaveis[v](v)

    def __le_registro(
        self,
        file: IO,
        offset: int,
        indice: int,
    ):
        file.seek(offset)
        self.__le_e_atribui_int(file, self.estagio, 1, indice)
        # Variáveis que variam com a versão do modelo
        mapa_variaveis: Dict[VariavelOperacao, Callable] = {
            VariavelOperacao.MERCADO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.MERCADO],
                self.numero_submercados,
                indice,
            ),
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL
                ],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_ABSOLUTA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_ABSOLUTA],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_CONTROLAVEL: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.GERACAO_HIDRAULICA_CONTROLAVEL],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.ENERGIA_VERTIDA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ENERGIA_VERTIDA],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_FINAL: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_FINAL],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO_BRUTA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO_BRUTA],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.ENERGIA_EVAPORADA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ENERGIA_EVAPORADA],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.ENERGIA_ENCHIMENTO_VOLUME_MORTO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ENERGIA_ENCHIMENTO_VOLUME_MORTO],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.GERACAO_TERMICA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.GERACAO_TERMICA],
                2 * self.total_classes_termicas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.DEFICIT: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.DEFICIT],
                self.numero_submercados
                * self.numero_patamares_deficit
                * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VALOR_AGUA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VALOR_AGUA],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.CUSTO_MARGINAL_OPERACAO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.CUSTO_MARGINAL_OPERACAO],
                self.numero_submercados * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_FIO_LIQUIDA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.GERACAO_HIDRAULICA_FIO_LIQUIDA],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.PERDAS_GERACAO_HIDRAULICA_FIO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.PERDAS_GERACAO_HIDRAULICA_FIO],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.INTERCAMBIO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.INTERCAMBIO],
                self.numero_total_submercados
                * (self.numero_total_submercados - 1)
                * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.EXCESSO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.EXCESSO],
                self.numero_submercados * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_BRUTA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_BRUTA],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL_CORRIGIDA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL_CORRIGIDA
                ],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO
                ],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.ENERGIA_AFLUENTE_FIO_DESVIO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ENERGIA_AFLUENTE_FIO_DESVIO],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.BENEFICIO_INTERCAMBIO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.BENEFICIO_INTERCAMBIO],
                self.numero_total_submercados
                * (self.numero_total_submercados - 1)
                * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.FATOR_CORRECAO_ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.FATOR_CORRECAO_ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL
                ],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.VIOLACAO_CURVA_AVERSAO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_CURVA_AVERSAO],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.ACIONAMENTO_CURVA_AVERSAO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ACIONAMENTO_CURVA_AVERSAO],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.PENALIDADE_CURVA_AVERSAO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.PENALIDADE_CURVA_AVERSAO],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.CUSTO_OPERACAO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.CUSTO_OPERACAO],
                1,
                indice,
            ),
            VariavelOperacao.CUSTO_GERACAO_TERMICA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.CUSTO_GERACAO_TERMICA],
                self.numero_submercados,
                indice,
            ),
            VariavelOperacao.BENEFICIO_AGRUPAMENTO_INTERCAMBIO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.BENEFICIO_AGRUPAMENTO_INTERCAMBIO],
                self.numero_patamares_carga
                * self.numero_agrupamentos_intercambio,
                indice,
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.BENEFICIO_DESPACHO_GNL: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.BENEFICIO_DESPACHO_GNL],
                self.numero_submercados
                * self.numero_patamares_carga
                * self.lag_maximo_usinas_gnl,
                indice,
            ),
            VariavelOperacao.VIOLACAO_GERACAO_HIRAULICA_MINIMA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_GERACAO_HIRAULICA_MINIMA],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_ENERGIA_VAZAO_MINIMA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_ENERGIA_VAZAO_MINIMA],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.INVASAO_SAR: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.INVASAO_SAR],
                1,
                indice,
            ),
            VariavelOperacao.ACIONAMENTO_SAR: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ACIONAMENTO_SAR],
                1,
                indice,
            ),
            VariavelOperacao.PENALIDADE_SAR: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.PENALIDADE_SAR],
                1,
                indice,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA_CONSIDERANDO_RE: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA_CONSIDERANDO_RE
                ],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_FINAL: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_FINAL],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_USINA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.GERACAO_HIDRAULICA_USINA],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VOLUME_TURBINADO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_TURBINADO],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VOLUME_VERTIDO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_VERTIDO],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_GERACAO_HIDRAULICA_MINIMA_USINA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.VIOLACAO_GERACAO_HIDRAULICA_MINIMA_USINA
                ],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.ENCHIMENTO_VOLUME_MORTO_USINA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.ENCHIMENTO_VOLUME_MORTO_USINA],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VIOLACAO_DEFLUENCIA_MINIMA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_DEFLUENCIA_MINIMA],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VOLUME_DESVIO_USINA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_DESVIO_USINA],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VOLUME_DESVIO_POSITIVO_USINA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_DESVIO_POSITIVO_USINA],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VOLUME_DESVIO_NEGATIVO_USINA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_DESVIO_NEGATIVO_USINA],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VIOLACAO_FPHA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_FPHA],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VAZAO_AFLUENTE: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VAZAO_AFLUENTE],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VAZAO_INCREMENTAL: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VAZAO_INCREMENTAL],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_PERCENTUAL_FINAL: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[VariavelOperacao.VOLUME_ARMAZENADO_PERCENTUAL_FINAL],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.GEOL_GSOL_OLD: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.GEOL_GSOL_OLD],
                2 * self.numero_submercados * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_GEE: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_GEE],
                1,
                indice,
            ),
            VariavelOperacao.CUSTO_VIOLACAO_ENERGIA_VAZAO_MINIMA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.CUSTO_VIOLACAO_ENERGIA_VAZAO_MINIMA
                ],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO
                ],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_FIO_DESVIO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_FIO_DESVIO],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.CUSTO_VIOLACAO_GERACAO_HIDRAULICA_MINIMA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.CUSTO_VIOLACAO_GERACAO_HIDRAULICA_MINIMA
                ],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.SOMA_ENERGIA_NATURAL_AFLUENTE_12_MESES: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.SOMA_ENERGIA_NATURAL_AFLUENTE_12_MESES
                ],
                self.numero_rees,
                indice,
            ),
            VariavelOperacao.SOMA_VAZAO_AFLUENTE_12_MESES: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.SOMA_VAZAO_AFLUENTE_12_MESES],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.GERACAO_EOLICA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.GERACAO_EOLICA],
                self.numero_parques_eolicos_equivalentes
                * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VELOCIDADE_VENTO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VELOCIDADE_VENTO],
                self.numero_parques_eolicos_equivalentes,
                indice,
            ),
            VariavelOperacao.VIOLACAO_FUNCAO_PRODUCAO_EOLICA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_FUNCAO_PRODUCAO_EOLICA],
                self.numero_parques_eolicos_equivalentes
                * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_DEFLUENCIA_MAXIMA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_DEFLUENCIA_MAXIMA],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_TURBINAMENTO_MAXIMO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_TURBINAMENTO_MAXIMO],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_TURBINAMENTO_MINIMO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_TURBINAMENTO_MINIMO],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO_USINA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO_USINA
                ],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA_USINA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA_USINA
                ],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA],
                self.numero_rees * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO_USINA: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO_USINA],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA_USINA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA_USINA],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VIOLACAO_RESTRICOES_ELETRICAS_ESPECIAIS: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.VIOLACAO_RESTRICOES_ELETRICAS_ESPECIAIS
                ],
                self.numero_restricoes_eletricas_especiais
                * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.CUSTO_RESTRICOES_ELETRICAS_ESPECIAIS: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.CUSTO_RESTRICOES_ELETRICAS_ESPECIAIS
                ],
                self.numero_restricoes_eletricas_especiais
                * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_INICIAL: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_INICIAL],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VALOR_AGUA_USINA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VALOR_AGUA_USINA],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VOLUME_EVAPORADO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_EVAPORADO],
                self.numero_usinas_hidreletricas,
                indice,
            ),
            VariavelOperacao.VOLUME_BOMBEADO: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_BOMBEADO],
                self.numero_estacoes_bombeamento * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.CONSUMO_ENERGIA_ESTACAO_BOMBEAMENTO: lambda _: self.__le_e_atribui_float(  # noqa
                file,
                self.data[
                    VariavelOperacao.CONSUMO_ENERGIA_ESTACAO_BOMBEAMENTO
                ],
                self.numero_estacoes_bombeamento * self.numero_patamares_carga,
                indice,
            ),
            VariavelOperacao.VOLUME_CANAL_DESVIO_USINA: lambda _: self.__le_e_atribui_float(
                file,
                self.data[VariavelOperacao.VOLUME_CANAL_DESVIO_USINA],
                self.numero_usinas_hidreletricas * self.numero_patamares_carga,
                indice,
            ),
        }
        for v in self.__class__.VARIAVEIS:
            mapa_variaveis[v](v)

    def __converte_array_em_dataframe(
        self,
        variavel: np.ndarray,
        colunas_identificacao: dict,
        num_elementos: int,
    ):
        return pd.DataFrame(
            data={
                **{
                    "estagio": np.repeat(self.__estagios_df, num_elementos),
                    "cenario": np.repeat(self.__cenarios_df, num_elementos),
                },
                **colunas_identificacao,
                **{"valor": variavel},
            }
        )

    def __converte_array_submercado(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "submercado": np.tile(
                    self.nomes_submercados, self.__num_simulacoes
                )
            },
            self.numero_submercados,
        )

    def __converte_array_submercado_patamar(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "submercado": np.tile(
                    np.repeat(
                        self.nomes_submercados, self.numero_patamares_carga
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.tile(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.numero_submercados,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.numero_submercados * self.numero_patamares_carga,
        )

    def __converte_array_ree(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )

    def __converte_array_ree_patamar(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "ree": np.tile(
                    np.repeat(
                        self.nomes_rees,
                        self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.tile(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.numero_rees,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.numero_rees * self.numero_patamares_carga,
        )

    def __converte_array_ute_patamar(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "usina": np.tile(
                    np.tile(
                        self.nomes_classes_termicas,
                        self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.repeat(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.total_classes_termicas,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.total_classes_termicas * self.numero_patamares_carga,
        )

    def __converte_array_submercado_patamardeficit_patamar(
        self, variavel: np.ndarray
    ):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "submercado": np.tile(
                    np.repeat(
                        self.nomes_submercados,
                        self.numero_patamares_deficit
                        * self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamarDeficit": np.tile(
                    np.tile(
                        np.arange(1, self.numero_patamares_deficit + 1),
                        self.numero_patamares_carga * self.numero_submercados,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.tile(
                        np.repeat(
                            np.arange(1, self.numero_patamares_carga + 1),
                            self.numero_patamares_deficit,
                        ),
                        self.numero_submercados,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.numero_submercados
            * self.numero_patamares_deficit
            * self.numero_patamares_carga,
        )

    def __converte_array_par_submercados_patamar(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "submercadoDe": np.tile(
                    np.tile(
                        self.nomes_submercados_totais[:-1],
                        self.numero_total_submercados
                        * self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "submercadoPara": np.tile(
                    np.tile(
                        np.repeat(
                            self.nomes_submercados_totais,
                            self.numero_total_submercados - 1,
                        ),
                        self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.tile(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.numero_total_submercados
                        * (self.numero_total_submercados - 1),
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.numero_total_submercados
            * (self.numero_total_submercados - 1)
            * self.numero_patamares_carga,
        )

    def __converte_array_agrupamentointercambio_patamar(
        self, variavel: np.ndarray
    ):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "agrupamentoIntercambio": np.tile(
                    np.repeat(
                        np.arange(1, self.numero_agrupamentos_intercambio + 1),
                        self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.arange(1, self.numero_patamares_carga + 1),
                    self.numero_agrupamentos_intercambio
                    * self.__num_simulacoes,
                ),
            },
            self.numero_agrupamentos_intercambio * self.numero_patamares_carga,
        )

    def __converte_array_laggnl_submercado_patamar(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "lag": np.tile(
                    np.arange(1, self.lag_maximo_usinas_gnl + 1),
                    self.numero_patamares_carga
                    * self.numero_submercados
                    * self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.repeat(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.lag_maximo_usinas_gnl,
                    ),
                    self.numero_submercados * self.__num_simulacoes,
                ),
                "submercado": np.tile(
                    np.repeat(
                        self.nomes_submercados,
                        self.lag_maximo_usinas_gnl
                        * self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.lag_maximo_usinas_gnl
            * self.numero_submercados
            * self.numero_patamares_carga,
        )

    def __converte_array_uhe(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )

    def __converte_array_uhe_patamar(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "usina": np.tile(
                    np.repeat(
                        self.nomes_usinas_hidreletricas,
                        self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.tile(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.numero_usinas_hidreletricas,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
        )

    def __converte_array_pee(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "pee": np.tile(
                    self.nomes_parques_eolicos_equivalentes,
                    self.__num_simulacoes,
                )
            },
            self.numero_parques_eolicos_equivalentes,
        )

    def __converte_array_pee_patamar(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "pee": np.tile(
                    np.repeat(
                        self.nomes_parques_eolicos_equivalentes,
                        self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.tile(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.numero_parques_eolicos_equivalentes,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.numero_parques_eolicos_equivalentes
            * self.numero_patamares_carga,
        )

    def __converte_array_restricaoeletrica_patamar(self, variavel: np.ndarray):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "restricao": np.tile(
                    np.repeat(
                        np.arange(
                            1,
                            self.numero_restricoes_eletricas_especiais + 1,
                        ),
                        self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.tile(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.numero_restricoes_eletricas_especiais,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.numero_restricoes_eletricas_especiais
            * self.numero_patamares_carga,
        )

    def __converte_array_estacaobombeamento_patamar(
        self, variavel: np.ndarray
    ):
        return self.__converte_array_em_dataframe(
            variavel,
            {
                "estacao": np.tile(
                    np.repeat(
                        self.nomes_estacoes_bombeamento,
                        self.numero_patamares_carga,
                    ),
                    self.__num_simulacoes,
                ),
                "patamar": np.tile(
                    np.tile(
                        np.arange(1, self.numero_patamares_carga + 1),
                        self.numero_estacoes_bombeamento,
                    ),
                    self.__num_simulacoes,
                ),
            },
            self.numero_estacoes_bombeamento * self.numero_patamares_carga,
        )

    def __converte_arrays_em_dataframes(self):
        mapa_variaveis: Dict[VariavelOperacao, Callable] = {
            VariavelOperacao.MERCADO: lambda _: self.__converte_array_submercado(
                self.data[VariavelOperacao.MERCADO]
            ),
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL: lambda _: self.__converte_array_ree(  # noqa
                self.data[VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL]
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_ABSOLUTA: lambda _: self.__converte_array_ree(  # noqa
                self.data[VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_ABSOLUTA],
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_CONTROLAVEL: lambda _: self.__converte_array_ree_patamar(  # noqa
                self.data[VariavelOperacao.GERACAO_HIDRAULICA_CONTROLAVEL]
            ),
            VariavelOperacao.ENERGIA_VERTIDA: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.ENERGIA_VERTIDA]
            ),
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_FINAL: lambda _: self.__converte_array_ree(  # noqa
                self.data[VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_FINAL]
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO_BRUTA: lambda _: self.__converte_array_ree(  # noqa
                self.data[VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO_BRUTA]
            ),
            VariavelOperacao.ENERGIA_EVAPORADA: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.ENERGIA_EVAPORADA]
            ),
            VariavelOperacao.ENERGIA_ENCHIMENTO_VOLUME_MORTO: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.ENERGIA_ENCHIMENTO_VOLUME_MORTO]
            ),
            VariavelOperacao.GERACAO_TERMICA: lambda _: self.__converte_array_ute_patamar(
                self.data[VariavelOperacao.GERACAO_TERMICA][::2]
                + self.data[VariavelOperacao.GERACAO_TERMICA][1::2]
            ),
            VariavelOperacao.DEFICIT: lambda _: self.__converte_array_submercado_patamardeficit_patamar(  # noqa
                self.data[VariavelOperacao.DEFICIT]
            ),
            VariavelOperacao.VALOR_AGUA: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.VALOR_AGUA]
            ),
            VariavelOperacao.CUSTO_MARGINAL_OPERACAO: lambda _: self.__converte_array_submercado_patamar(  # noqa
                self.data[VariavelOperacao.CUSTO_MARGINAL_OPERACAO]
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_FIO_LIQUIDA: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.GERACAO_HIDRAULICA_FIO_LIQUIDA]
            ),
            VariavelOperacao.PERDAS_GERACAO_HIDRAULICA_FIO: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.PERDAS_GERACAO_HIDRAULICA_FIO]
            ),
            VariavelOperacao.INTERCAMBIO: lambda _: self.__converte_array_par_submercados_patamar(
                self.data[VariavelOperacao.INTERCAMBIO]
            ),
            VariavelOperacao.EXCESSO: lambda _: self.__converte_array_submercado_patamar(
                self.data[VariavelOperacao.EXCESSO]
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_BRUTA: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_BRUTA]
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL_CORRIGIDA: lambda _: self.__converte_array_ree(  # noqa
                self.data[
                    VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL_CORRIGIDA
                ]
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA: lambda _: self.__converte_array_ree_patamar(
                self.data[VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA]
            ),
            VariavelOperacao.ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO: lambda _: self.__converte_array_ree(  # noqa
                self.data[VariavelOperacao.ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO]
            ),
            VariavelOperacao.ENERGIA_AFLUENTE_FIO_DESVIO: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.ENERGIA_AFLUENTE_FIO_DESVIO]
            ),
            VariavelOperacao.BENEFICIO_INTERCAMBIO: lambda _: self.__converte_array_par_submercados_patamar(  # noqa
                self.data[VariavelOperacao.BENEFICIO_INTERCAMBIO]
            ),
            VariavelOperacao.FATOR_CORRECAO_ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL: lambda _: self.__converte_array_ree(  # noqa
                self.data[
                    VariavelOperacao.FATOR_CORRECAO_ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL
                ]
            ),
            VariavelOperacao.VIOLACAO_CURVA_AVERSAO: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.VIOLACAO_CURVA_AVERSAO]
            ),
            VariavelOperacao.ACIONAMENTO_CURVA_AVERSAO: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.ACIONAMENTO_CURVA_AVERSAO]
            ),
            VariavelOperacao.PENALIDADE_CURVA_AVERSAO: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.PENALIDADE_CURVA_AVERSAO]
            ),
            VariavelOperacao.CUSTO_OPERACAO: lambda _: self.__converte_array_em_dataframe(
                self.data[VariavelOperacao.CUSTO_OPERACAO],
                {},
                1,
            ),
            VariavelOperacao.CUSTO_GERACAO_TERMICA: lambda _: self.__converte_array_submercado(
                self.data[VariavelOperacao.CUSTO_GERACAO_TERMICA]
            ),
            VariavelOperacao.BENEFICIO_AGRUPAMENTO_INTERCAMBIO: lambda _: self.__converte_array_agrupamentointercambio_patamar(  # noqa
                self.data[VariavelOperacao.BENEFICIO_AGRUPAMENTO_INTERCAMBIO]
            ),
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO]
            ),
            VariavelOperacao.BENEFICIO_DESPACHO_GNL: lambda _: self.__converte_array_laggnl_submercado_patamar(  # noqa
                self.data[VariavelOperacao.BENEFICIO_DESPACHO_GNL]
            ),
            VariavelOperacao.VIOLACAO_GERACAO_HIRAULICA_MINIMA: lambda _: self.__converte_array_ree_patamar(  # noqa
                self.data[VariavelOperacao.VIOLACAO_GERACAO_HIRAULICA_MINIMA]
            ),
            VariavelOperacao.VIOLACAO_ENERGIA_VAZAO_MINIMA: lambda _: self.__converte_array_ree(
                self.data[VariavelOperacao.VIOLACAO_ENERGIA_VAZAO_MINIMA]
            ),
            VariavelOperacao.INVASAO_SAR: lambda _: self.__converte_array_em_dataframe(
                self.data[VariavelOperacao.INVASAO_SAR],
                {},
                1,
            ),
            VariavelOperacao.ACIONAMENTO_SAR: lambda _: self.__converte_array_em_dataframe(
                self.data[VariavelOperacao.ACIONAMENTO_SAR],
                {},
                1,
            ),
            VariavelOperacao.PENALIDADE_SAR: lambda _: self.__converte_array_em_dataframe(
                self.data[VariavelOperacao.PENALIDADE_SAR],
                {},
                1,
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA_CONSIDERANDO_RE: lambda _: self.__converte_array_ree_patamar(  # noqa
                self.data[
                    VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA_CONSIDERANDO_RE
                ]
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_FINAL: lambda _: self.__converte_array_uhe(  # noqa
                self.data[VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_FINAL]
            ),
            VariavelOperacao.GERACAO_HIDRAULICA_USINA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[VariavelOperacao.GERACAO_HIDRAULICA_USINA]
            ),
            VariavelOperacao.VOLUME_TURBINADO: lambda _: self.__converte_array_uhe_patamar(
                self.data[VariavelOperacao.VOLUME_TURBINADO]
            ),
            VariavelOperacao.VOLUME_VERTIDO: lambda _: self.__converte_array_uhe_patamar(
                self.data[VariavelOperacao.VOLUME_VERTIDO]
            ),
            VariavelOperacao.VIOLACAO_GERACAO_HIDRAULICA_MINIMA_USINA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[
                    VariavelOperacao.VIOLACAO_GERACAO_HIDRAULICA_MINIMA_USINA
                ]
            ),
            VariavelOperacao.ENCHIMENTO_VOLUME_MORTO_USINA: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.ENCHIMENTO_VOLUME_MORTO_USINA]
            ),
            VariavelOperacao.VIOLACAO_DEFLUENCIA_MINIMA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[VariavelOperacao.VIOLACAO_DEFLUENCIA_MINIMA]
            ),
            VariavelOperacao.VOLUME_DESVIO_USINA: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.VOLUME_DESVIO_USINA]
            ),
            VariavelOperacao.VOLUME_DESVIO_POSITIVO_USINA: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.VOLUME_DESVIO_POSITIVO_USINA]
            ),
            VariavelOperacao.VOLUME_DESVIO_NEGATIVO_USINA: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.VOLUME_DESVIO_NEGATIVO_USINA]
            ),
            VariavelOperacao.VIOLACAO_FPHA: lambda _: self.__converte_array_uhe_patamar(
                self.data[VariavelOperacao.VIOLACAO_FPHA]
            ),
            VariavelOperacao.VAZAO_AFLUENTE: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.VAZAO_AFLUENTE]
            ),
            VariavelOperacao.VAZAO_INCREMENTAL: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.VAZAO_INCREMENTAL]
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_PERCENTUAL_FINAL: lambda _: self.__converte_array_uhe(  # noqa
                self.data[VariavelOperacao.VOLUME_ARMAZENADO_PERCENTUAL_FINAL]
            ),
            VariavelOperacao.GEOL_GSOL_OLD: lambda _: pd.DataFrame(),
            VariavelOperacao.VIOLACAO_GEE: lambda _: pd.DataFrame(),
            VariavelOperacao.CUSTO_VIOLACAO_ENERGIA_VAZAO_MINIMA: lambda _: self.__converte_array_ree(  # noqa
                self.data[VariavelOperacao.CUSTO_VIOLACAO_ENERGIA_VAZAO_MINIMA]
            ),
            VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO: lambda _: self.__converte_array_ree(  # noqa
                self.data[
                    VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO
                ]
            ),
            VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_FIO_DESVIO: lambda _: self.__converte_array_ree(  # noqa
                self.data[VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_FIO_DESVIO]
            ),
            VariavelOperacao.CUSTO_VIOLACAO_GERACAO_HIDRAULICA_MINIMA: lambda _: self.__converte_array_ree_patamar(  # noqa
                self.data[
                    VariavelOperacao.CUSTO_VIOLACAO_GERACAO_HIDRAULICA_MINIMA
                ]
            ),
            VariavelOperacao.SOMA_ENERGIA_NATURAL_AFLUENTE_12_MESES: lambda _: self.__converte_array_ree(  # noqa
                self.data[
                    VariavelOperacao.SOMA_ENERGIA_NATURAL_AFLUENTE_12_MESES
                ]
            ),
            VariavelOperacao.SOMA_VAZAO_AFLUENTE_12_MESES: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.SOMA_VAZAO_AFLUENTE_12_MESES]
            ),
            VariavelOperacao.GERACAO_EOLICA: lambda _: self.__converte_array_pee_patamar(
                self.data[VariavelOperacao.GERACAO_EOLICA]
            ),
            VariavelOperacao.VELOCIDADE_VENTO: lambda _: self.__converte_array_pee(
                self.data[VariavelOperacao.VELOCIDADE_VENTO]
            ),
            VariavelOperacao.VIOLACAO_FUNCAO_PRODUCAO_EOLICA: lambda _: self.__converte_array_pee_patamar(  # noqa
                self.data[VariavelOperacao.VIOLACAO_FUNCAO_PRODUCAO_EOLICA]
            ),
            VariavelOperacao.VIOLACAO_DEFLUENCIA_MAXIMA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[VariavelOperacao.VIOLACAO_DEFLUENCIA_MAXIMA]
            ),
            VariavelOperacao.VIOLACAO_TURBINAMENTO_MAXIMO: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[VariavelOperacao.VIOLACAO_TURBINAMENTO_MAXIMO]
            ),
            VariavelOperacao.VIOLACAO_TURBINAMENTO_MINIMO: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[VariavelOperacao.VIOLACAO_TURBINAMENTO_MINIMO]
            ),
            VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO: lambda _: self.__converte_array_ree_patamar(  # noqa
                self.data[VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO]
            ),
            VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA: lambda _: self.__converte_array_ree_patamar(  # noqa
                self.data[VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA]
            ),
            VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO_USINA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[
                    VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO_USINA
                ]
            ),
            VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA_USINA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[
                    VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA_USINA
                ]
            ),
            VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO: lambda _: self.__converte_array_ree_patamar(  # noqa
                self.data[VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO]
            ),
            VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA: lambda _: self.__converte_array_ree_patamar(  # noqa
                self.data[VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA]
            ),
            VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO_USINA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO_USINA]
            ),
            VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA_USINA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA_USINA]
            ),
            VariavelOperacao.VIOLACAO_RESTRICOES_ELETRICAS_ESPECIAIS: lambda _: self.__converte_array_restricaoeletrica_patamar(  # noqa
                self.data[
                    VariavelOperacao.VIOLACAO_RESTRICOES_ELETRICAS_ESPECIAIS
                ]
            ),
            VariavelOperacao.CUSTO_RESTRICOES_ELETRICAS_ESPECIAIS: lambda _: self.__converte_array_restricaoeletrica_patamar(  # noqa
                self.data[
                    VariavelOperacao.CUSTO_RESTRICOES_ELETRICAS_ESPECIAIS
                ]
            ),
            VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_INICIAL: lambda _: self.__converte_array_uhe(  # noqa
                self.data[VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_INICIAL]
            ),
            VariavelOperacao.VALOR_AGUA_USINA: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.VALOR_AGUA_USINA]
            ),
            VariavelOperacao.VOLUME_EVAPORADO: lambda _: self.__converte_array_uhe(
                self.data[VariavelOperacao.VOLUME_EVAPORADO]
            ),
            VariavelOperacao.VOLUME_BOMBEADO: lambda _: self.__converte_array_estacaobombeamento_patamar(  # noqa
                self.data[VariavelOperacao.VOLUME_BOMBEADO]
            ),
            VariavelOperacao.CONSUMO_ENERGIA_ESTACAO_BOMBEAMENTO: lambda _: self.__converte_array_estacaobombeamento_patamar(  # noqa
                self.data[VariavelOperacao.CONSUMO_ENERGIA_ESTACAO_BOMBEAMENTO]
            ),
            VariavelOperacao.VOLUME_CANAL_DESVIO_USINA: lambda _: self.__converte_array_uhe_patamar(  # noqa
                self.data[VariavelOperacao.VOLUME_CANAL_DESVIO_USINA]
            ),
        }
        for v in self.__class__.VARIAVEIS:
            self.data[v] = mapa_variaveis[v](v)

        # Soma GTMIN e GTFLEX
        # TODO - talvez tenha uma diferença aqui, pois o NEWAVE
        # escreve por submercado. Para casos de PMO, as térmicas são
        # cadastradas por submercado no conft, então não deve
        # dar diferença. Os nomes deveriam ser fornecidos por
        # submercado já..

    def read(
        self,
        file: IO,
        tamanho_registro: int = 41264,
        numero_estagios: int = 60,
        numero_forwards: int = 200,
        numero_patamares_carga: int = 3,
        numero_patamares_deficit: int = 1,
        numero_agrupamentos_intercambio: int = 1,
        numero_classes_termicas_submercados: List[int] = [],
        lag_maximo_usinas_gnl: int = 2,
        numero_restricoes_eletricas_especiais: int = 0,
        nomes_submercados: List[str] = ["SUDESTE", "SUL", "NORDESTE", "NORTE"],
        nomes_submercados_totais: List[str] = [
            "SUDESTE",
            "SUL",
            "NORDESTE",
            "NORTE",
            "NOFICT1",
        ],
        nomes_rees: List[str] = [
            "SUDESTE",
            "MADEIRA",
            "TPIRES",
            "ITAIPU",
            "PARANA",
            "PRNPANEMA",
            "SUL",
            "IGUACU",
            "NORDESTE",
            "NORTE",
            "BMONTE",
            "MAN-AP",
        ],
        nomes_classes_termicas: List[str] = [],
        nomes_usinas_hidreletricas: List[str] = [],
        nomes_parques_eolicos_equivalentes: List[str] = [],
        nomes_estacoes_bombeamento: List[str] = [],
        *args,
        **kwargs,
    ):
        # Atribui variáveis locais
        self.numero_rees = len(nomes_rees)
        self.numero_submercados = len(nomes_submercados)
        self.numero_total_submercados = len(nomes_submercados_totais)
        self.numero_patamares_carga = numero_patamares_carga
        self.numero_patamares_deficit = numero_patamares_deficit
        self.numero_agrupamentos_intercambio = numero_agrupamentos_intercambio
        self.numero_classes_termicas_submercados = (
            numero_classes_termicas_submercados
        )
        self.total_classes_termicas = sum(
            self.numero_classes_termicas_submercados
        )
        self.numero_usinas_hidreletricas = len(nomes_usinas_hidreletricas)
        self.lag_maximo_usinas_gnl = lag_maximo_usinas_gnl
        self.numero_parques_eolicos_equivalentes = len(
            nomes_parques_eolicos_equivalentes
        )
        self.numero_restricoes_eletricas_especiais = (
            numero_restricoes_eletricas_especiais
        )
        self.numero_estacoes_bombeamento = len(nomes_estacoes_bombeamento)
        self.nomes_submercados = np.array(nomes_submercados)
        self.nomes_submercados_totais = np.array(nomes_submercados_totais)
        self.nomes_rees = np.array(nomes_rees)
        self.nomes_classes_termicas = np.array(nomes_classes_termicas)
        self.nomes_usinas_hidreletricas = np.array(nomes_usinas_hidreletricas)
        self.nomes_parques_eolicos_equivalentes = np.array(
            nomes_parques_eolicos_equivalentes
        )
        self.nomes_estacoes_bombeamento = np.array(nomes_estacoes_bombeamento)
        # Realiza leitura
        self.__inicializa_variaveis(numero_estagios, numero_forwards)
        for estagio in range(numero_estagios):
            for serie in range(numero_forwards):
                indice = estagio * numero_forwards + serie
                offset = tamanho_registro * indice
                self.__le_registro(file, offset, indice)
        self.__converte_arrays_em_dataframes()
