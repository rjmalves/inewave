from cfinterface.components.section import Section
from typing import IO, List
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class SecaoDadosForward(Section):
    """
    Registro com os resultados da operação
    """

    BYTES_FLOAT = 4
    BYTES_INT = 4

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosForward):
            return False
        bloco: SecaoDadosForward = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(bloco.data, list),
            ]
        ):
            return False
        else:
            return all([a.equals(b) for a, b in zip(self.data, bloco.data)])

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
        self.__estagios_df = np.repeat(
            np.arange(1, numero_estagios + 1), numero_forwards
        )
        self.__cenarios_df = np.tile(
            np.arange(1, numero_forwards + 1), numero_estagios
        )
        self.__num_simulacoes = numero_estagios * numero_forwards
        self.estagio = np.zeros((1 * self.__num_simulacoes,), dtype=np.int32)
        self.mercado_liquido = np.zeros(
            (self.numero_submercados * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.energia_armazenada_inicial = np.zeros(
            (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
        )
        self.energia_afluente_total = np.zeros(
            (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
        )
        self.geracao_hidraulica_controlavel = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.energia_vertida = np.zeros(
            (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
        )
        self.energia_armazenada_final = np.zeros(
            (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
        )
        self.energia_fio_dagua = np.zeros(
            (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
        )
        self.energia_evaporada = np.zeros(
            (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
        )
        self.energia_enchimento_volume_morto = np.zeros(
            (self.numero_rees * self.__num_simulacoes,), dtype=np.float32
        )
        self.geracao_termica = np.zeros(
            (
                2
                * self.total_classes_termicas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.deficit = np.zeros(
            (
                self.numero_submercados
                * self.numero_patamares_deficit
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.pi_balanco_hidrico = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.pi_balanco_demanda = np.zeros(
            (
                self.numero_submercados
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.geracao_fio_dagua_liquida = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.perdas_fio_dagua = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.intercambios = np.zeros(
            (
                self.numero_total_submercados
                * (self.numero_total_submercados - 1)
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.excesso = np.zeros(
            (
                self.numero_submercados
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.energia_afluente_bruta_sem_correcao = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.energia_afluente_controlavel_corrigida = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.geracao_hidraulica_maxima = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.energia_controlavel_referente_desvio = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.energia_fio_dagua_referente_desvio = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.beneficio_intercambio = np.zeros(
            (
                self.numero_total_submercados
                * (self.numero_total_submercados - 1)
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.fator_correcao_energia_controlavel = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.invasao_curva_aversao = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.acionamento_curva_aversao = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.penalidade_invasao_curva_aversao = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.custo_total_operacao = np.zeros(
            (1 * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.custo_geracao_termica = np.zeros(
            (self.numero_submercados * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.beneficio_agrupamento_intercambios = np.zeros(
            (
                self.numero_patamares_carga
                * self.numero_agrupamentos_intercambio
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.energia_afluente_fio_dagua = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.beneficio_despacho_gnl = np.zeros(
            (
                self.numero_submercados
                * self.numero_patamares_carga
                * self.lag_maximo_usinas_gnl
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_ghmin_ree = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_energia_vazao_minima = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.invasao_sar = np.zeros(
            (1 * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.acionamento_sar = np.zeros(
            (1 * self.__num_simulacoes,),
            dtype=np.int32,
        )
        self.penalidade_sar = np.zeros(
            (1 * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.capacidade_hidraulica_maxima_considerando_re = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.volume_armazenado_final = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.geracao_hidraulica_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.volume_turbinado_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.volume_vertido_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_ghmin_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.enchimento_volume_morto_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.violacao_vazao_minima_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.volume_desvio_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.volume_desvio_positivo_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.volume_desvio_negativo_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.violacao_fpha_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.vazao_afluente_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.vazao_incremental_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.volume_armazenado_final_percentual_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.custo_violacao_energia_vazao_minima = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.custo_desvio_agua_controlavel = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.custo_desvio_agua_fio_dagua = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.custo_violacao_ghmin = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.soma_afluencias_passadas_ree = np.zeros(
            (self.numero_rees * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.soma_afluencias_passadas_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.geracao_eolica_pee = np.zeros(
            (
                self.numero_parques_eolicos_equivalentes
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.vento_pee = np.zeros(
            (
                self.numero_parques_eolicos_equivalentes
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_funcao_producao_eolica_pee = np.zeros(
            (
                self.numero_parques_eolicos_equivalentes
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_vazao_maxima_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_turbinamento_maximo_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_turbinamento_minimo_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_lpp_turbinamento_maximo = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_lpp_defluencia_maxima = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_lpp_turbinamento_maximo_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_lpp_defluencia_maxima_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.rhs_lpp_turbinamento_maximo = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.rhs_lpp_defluencia_maxima = np.zeros(
            (
                self.numero_rees
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.rhs_lpp_turbinamento_maximo_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.rhs_lpp_defluencia_maxima_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.violacao_restricao_eletrica_especial = np.zeros(
            (
                self.numero_restricoes_eletricas_especiais
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.custo_restricao_eletrica_especial = np.zeros(
            (
                self.numero_restricoes_eletricas_especiais
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.volume_armazenado_inicial_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.lambda_balanco_hidrico_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.volume_evaporado_usina = np.zeros(
            (self.numero_usinas_hidreletricas * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.volume_bombeado_estacao_bombeamento = np.zeros(
            (self.numero_estacoes_bombeamento * self.__num_simulacoes,),
            dtype=np.float32,
        )
        self.consumo_energia_estacao_bombeamento = np.zeros(
            (
                self.numero_estacoes_bombeamento
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )
        self.volume_desvio_canal_desvio_usina = np.zeros(
            (
                self.numero_usinas_hidreletricas
                * self.numero_patamares_carga
                * self.__num_simulacoes,
            ),
            dtype=np.float32,
        )

    def __le_registro(
        self,
        file: IO,
        offset: int,
        indice: int,
    ):
        file.seek(offset)
        self.__le_e_atribui_int(file, self.estagio, 1, indice)
        self.__le_e_atribui_float(
            file, self.mercado_liquido, self.numero_submercados, indice
        )
        self.__le_e_atribui_float(
            file, self.energia_armazenada_inicial, self.numero_rees, indice
        )
        self.__le_e_atribui_float(
            file, self.energia_afluente_total, self.numero_rees, indice
        )
        self.__le_e_atribui_float(
            file,
            self.geracao_hidraulica_controlavel,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file, self.energia_vertida, self.numero_rees, indice
        )
        self.__le_e_atribui_float(
            file, self.energia_armazenada_final, self.numero_rees, indice
        )
        self.__le_e_atribui_float(
            file, self.energia_fio_dagua, self.numero_rees, indice
        )
        self.__le_e_atribui_float(
            file, self.energia_evaporada, self.numero_rees, indice
        )
        self.__le_e_atribui_float(
            file,
            self.energia_enchimento_volume_morto,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.geracao_termica,
            2 * self.total_classes_termicas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.deficit,
            self.numero_submercados
            * self.numero_patamares_deficit
            * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.pi_balanco_hidrico,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.pi_balanco_demanda,
            self.numero_submercados * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.geracao_fio_dagua_liquida,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.perdas_fio_dagua,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.intercambios,
            self.numero_total_submercados
            * (self.numero_total_submercados - 1)
            * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.excesso,
            self.numero_submercados * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.energia_afluente_bruta_sem_correcao,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.energia_afluente_controlavel_corrigida,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.geracao_hidraulica_maxima,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.energia_controlavel_referente_desvio,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.energia_fio_dagua_referente_desvio,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.beneficio_intercambio,
            self.numero_total_submercados
            * (self.numero_total_submercados - 1)
            * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.fator_correcao_energia_controlavel,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.invasao_curva_aversao,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.acionamento_curva_aversao,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.penalidade_invasao_curva_aversao,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.custo_total_operacao,
            1,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.custo_geracao_termica,
            self.numero_submercados,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.beneficio_agrupamento_intercambios,
            self.numero_patamares_carga * self.numero_agrupamentos_intercambio,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.energia_afluente_fio_dagua,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.beneficio_despacho_gnl,
            self.numero_submercados
            * self.numero_patamares_carga
            * self.lag_maximo_usinas_gnl,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_ghmin_ree,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_energia_vazao_minima,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.invasao_sar,
            1,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.acionamento_sar,
            1,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.penalidade_sar,
            1,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.capacidade_hidraulica_maxima_considerando_re,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_armazenado_final,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.geracao_hidraulica_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_turbinado_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_vertido_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_ghmin_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.enchimento_volume_morto_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_vazao_minima_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_desvio_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_desvio_positivo_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_desvio_negativo_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_fpha_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.vazao_afluente_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.vazao_incremental_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_armazenado_final_percentual_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        # Campos GEOL e GSOL antigos - ignorados
        np.frombuffer(
            file.read(
                2
                * self.numero_submercados
                * self.numero_patamares_carga
                * SecaoDadosForward.BYTES_FLOAT
            ),
            dtype=np.float32,
            count=2 * self.numero_submercados * self.numero_patamares_carga,
        )
        # Violação limites GEE - ignorado
        np.frombuffer(
            file.read(SecaoDadosForward.BYTES_FLOAT),
            dtype=np.float32,
            count=1,
        )[0]
        self.__le_e_atribui_float(
            file,
            self.custo_violacao_energia_vazao_minima,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.custo_desvio_agua_controlavel,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.custo_desvio_agua_fio_dagua,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.custo_violacao_ghmin,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.soma_afluencias_passadas_ree,
            self.numero_rees,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.soma_afluencias_passadas_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.geracao_eolica_pee,
            self.numero_parques_eolicos_equivalentes
            * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.vento_pee,
            self.numero_parques_eolicos_equivalentes,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_funcao_producao_eolica_pee,
            self.numero_parques_eolicos_equivalentes
            * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_vazao_maxima_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_turbinamento_maximo_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_turbinamento_minimo_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_lpp_turbinamento_maximo,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_lpp_defluencia_maxima,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_lpp_turbinamento_maximo_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_lpp_defluencia_maxima_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.rhs_lpp_turbinamento_maximo,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.rhs_lpp_defluencia_maxima,
            self.numero_rees * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.rhs_lpp_turbinamento_maximo_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.rhs_lpp_defluencia_maxima_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.violacao_restricao_eletrica_especial,
            self.numero_restricoes_eletricas_especiais
            * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.custo_restricao_eletrica_especial,
            self.numero_restricoes_eletricas_especiais
            * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_armazenado_inicial_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.lambda_balanco_hidrico_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_evaporado_usina,
            self.numero_usinas_hidreletricas,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_bombeado_estacao_bombeamento,
            self.numero_estacoes_bombeamento,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.consumo_energia_estacao_bombeamento,
            self.numero_estacoes_bombeamento * self.numero_patamares_carga,
            indice,
        )
        self.__le_e_atribui_float(
            file,
            self.volume_desvio_canal_desvio_usina,
            self.numero_usinas_hidreletricas * self.numero_patamares_carga,
            indice,
        )

    def __converte_array_em_dataframe(
        self,
        variavel: np.ndarray,
        colunas_identificacao: dict,
        num_elementos: int,
    ):
        # print([v.shape for k, v in colunas_identificacao.items()])
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

    def __converte_arrays_em_dataframes(self):
        self.mercado_liquido = self.__converte_array_em_dataframe(
            self.mercado_liquido,
            {
                "submercado": np.tile(
                    self.nomes_submercados, self.__num_simulacoes
                )
            },
            self.numero_submercados,
        )
        self.energia_armazenada_inicial = self.__converte_array_em_dataframe(
            self.energia_armazenada_inicial,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.energia_afluente_total = self.__converte_array_em_dataframe(
            self.energia_afluente_total,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.geracao_hidraulica_controlavel = (
            self.__converte_array_em_dataframe(
                self.geracao_hidraulica_controlavel,
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
        )
        self.energia_vertida = self.__converte_array_em_dataframe(
            self.energia_vertida,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.energia_armazenada_final = self.__converte_array_em_dataframe(
            self.energia_armazenada_final,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.energia_fio_dagua = self.__converte_array_em_dataframe(
            self.energia_fio_dagua,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.energia_evaporada = self.__converte_array_em_dataframe(
            self.energia_evaporada,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.energia_enchimento_volume_morto = (
            self.__converte_array_em_dataframe(
                self.energia_enchimento_volume_morto,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        # Soma GTMIN e GTFLEX
        self.geracao_termica = (
            self.geracao_termica[::2] + self.geracao_termica[1::2]
        )
        # TODO - talvez tenha uma diferença aqui, pois o NEWAVE
        # escreve por submercado. Para casos de PMO, as térmicas são
        # cadastradas por submercado no conft, então não deve
        # dar diferença. Os nomes deveriam ser fornecidos por
        # submercado já..
        self.geracao_termica = self.__converte_array_em_dataframe(
            self.geracao_termica,
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
        self.deficit = self.__converte_array_em_dataframe(
            self.deficit,
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
        self.pi_balanco_hidrico = self.__converte_array_em_dataframe(
            self.pi_balanco_hidrico,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.pi_balanco_demanda = self.__converte_array_em_dataframe(
            self.pi_balanco_demanda,
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
        self.geracao_fio_dagua_liquida = self.__converte_array_em_dataframe(
            self.geracao_fio_dagua_liquida,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.perdas_fio_dagua = self.__converte_array_em_dataframe(
            self.perdas_fio_dagua,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.intercambios = self.__converte_array_em_dataframe(
            self.intercambios,
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
        self.excesso = self.__converte_array_em_dataframe(
            self.excesso,
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
        self.energia_afluente_bruta_sem_correcao = (
            self.__converte_array_em_dataframe(
                self.energia_afluente_bruta_sem_correcao,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.energia_afluente_controlavel_corrigida = (
            self.__converte_array_em_dataframe(
                self.energia_afluente_controlavel_corrigida,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.geracao_hidraulica_maxima = self.__converte_array_em_dataframe(
            self.geracao_hidraulica_maxima,
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
        self.energia_controlavel_referente_desvio = (
            self.__converte_array_em_dataframe(
                self.energia_controlavel_referente_desvio,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.energia_fio_dagua_referente_desvio = (
            self.__converte_array_em_dataframe(
                self.energia_fio_dagua_referente_desvio,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.beneficio_intercambio = self.__converte_array_em_dataframe(
            self.beneficio_intercambio,
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
        self.fator_correcao_energia_controlavel = (
            self.__converte_array_em_dataframe(
                self.fator_correcao_energia_controlavel,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.invasao_curva_aversao = self.__converte_array_em_dataframe(
            self.invasao_curva_aversao,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.acionamento_curva_aversao = self.__converte_array_em_dataframe(
            self.acionamento_curva_aversao,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.penalidade_invasao_curva_aversao = (
            self.__converte_array_em_dataframe(
                self.penalidade_invasao_curva_aversao,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.custo_total_operacao = self.__converte_array_em_dataframe(
            self.custo_total_operacao,
            {},
            1,
        )
        self.custo_geracao_termica = self.__converte_array_em_dataframe(
            self.custo_geracao_termica,
            {
                "submercado": np.tile(
                    self.nomes_submercados, self.__num_simulacoes
                )
            },
            self.numero_submercados,
        )
        self.beneficio_agrupamento_intercambios = (
            self.__converte_array_em_dataframe(
                self.beneficio_agrupamento_intercambios,
                {
                    "agrupamentoIntercambio": np.tile(
                        np.repeat(
                            np.arange(
                                1, self.numero_agrupamentos_intercambio + 1
                            ),
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
                self.numero_agrupamentos_intercambio
                * self.numero_patamares_carga,
            )
        )
        self.energia_afluente_fio_dagua = self.__converte_array_em_dataframe(
            self.energia_afluente_fio_dagua,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.beneficio_despacho_gnl = self.__converte_array_em_dataframe(
            self.beneficio_despacho_gnl,
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
        self.violacao_ghmin_ree = self.__converte_array_em_dataframe(
            self.violacao_ghmin_ree,
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
        self.violacao_energia_vazao_minima = (
            self.__converte_array_em_dataframe(
                self.violacao_energia_vazao_minima,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.invasao_sar = self.__converte_array_em_dataframe(
            self.invasao_sar,
            {},
            1,
        )
        self.acionamento_sar = self.__converte_array_em_dataframe(
            self.acionamento_sar,
            {},
            1,
        )
        self.penalidade_sar = self.__converte_array_em_dataframe(
            self.penalidade_sar,
            {},
            1,
        )
        self.capacidade_hidraulica_maxima_considerando_re = (
            self.__converte_array_em_dataframe(
                self.capacidade_hidraulica_maxima_considerando_re,
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
        )
        self.volume_armazenado_final = self.__converte_array_em_dataframe(
            self.volume_armazenado_final,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )
        self.geracao_hidraulica_usina = self.__converte_array_em_dataframe(
            self.geracao_hidraulica_usina,
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
        self.volume_turbinado_usina = self.__converte_array_em_dataframe(
            self.volume_turbinado_usina,
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
        self.volume_vertido_usina = self.__converte_array_em_dataframe(
            self.volume_vertido_usina,
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
        self.violacao_ghmin_usina = self.__converte_array_em_dataframe(
            self.violacao_ghmin_usina,
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
        self.enchimento_volume_morto_usina = (
            self.__converte_array_em_dataframe(
                self.enchimento_volume_morto_usina,
                {
                    "usina": np.tile(
                        self.nomes_usinas_hidreletricas, self.__num_simulacoes
                    )
                },
                self.numero_usinas_hidreletricas,
            )
        )
        self.violacao_vazao_minima_usina = self.__converte_array_em_dataframe(
            self.violacao_vazao_minima_usina,
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
        self.volume_desvio_usina = self.__converte_array_em_dataframe(
            self.volume_desvio_usina,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )
        self.volume_desvio_positivo_usina = self.__converte_array_em_dataframe(
            self.volume_desvio_positivo_usina,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )
        self.volume_desvio_negativo_usina = self.__converte_array_em_dataframe(
            self.volume_desvio_negativo_usina,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )
        self.violacao_fpha_usina = self.__converte_array_em_dataframe(
            self.violacao_fpha_usina,
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
        self.vazao_afluente_usina = self.__converte_array_em_dataframe(
            self.vazao_afluente_usina,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )
        self.vazao_incremental_usina = self.__converte_array_em_dataframe(
            self.vazao_incremental_usina,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )
        self.volume_armazenado_final_percentual_usina = (
            self.__converte_array_em_dataframe(
                self.volume_armazenado_final_percentual_usina,
                {
                    "usina": np.tile(
                        self.nomes_usinas_hidreletricas, self.__num_simulacoes
                    )
                },
                self.numero_usinas_hidreletricas,
            )
        )
        self.custo_violacao_energia_vazao_minima = (
            self.__converte_array_em_dataframe(
                self.custo_violacao_energia_vazao_minima,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.custo_desvio_agua_controlavel = (
            self.__converte_array_em_dataframe(
                self.custo_desvio_agua_controlavel,
                {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
                self.numero_rees,
            )
        )
        self.custo_desvio_agua_fio_dagua = self.__converte_array_em_dataframe(
            self.custo_desvio_agua_fio_dagua,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.custo_violacao_ghmin = self.__converte_array_em_dataframe(
            self.custo_violacao_ghmin,
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
        self.soma_afluencias_passadas_ree = self.__converte_array_em_dataframe(
            self.soma_afluencias_passadas_ree,
            {"ree": np.tile(self.nomes_rees, self.__num_simulacoes)},
            self.numero_rees,
        )
        self.soma_afluencias_passadas_usina = (
            self.__converte_array_em_dataframe(
                self.soma_afluencias_passadas_usina,
                {
                    "usina": np.tile(
                        self.nomes_usinas_hidreletricas, self.__num_simulacoes
                    )
                },
                self.numero_usinas_hidreletricas,
            )
        )
        self.geracao_eolica_pee = self.__converte_array_em_dataframe(
            self.geracao_eolica_pee,
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
        self.vento_pee = self.__converte_array_em_dataframe(
            self.vento_pee,
            {
                "pee": np.tile(
                    self.nomes_parques_eolicos_equivalentes,
                    self.__num_simulacoes,
                )
            },
            self.numero_parques_eolicos_equivalentes,
        )
        self.violacao_funcao_producao_eolica_pee = (
            self.__converte_array_em_dataframe(
                self.violacao_funcao_producao_eolica_pee,
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
        )
        self.violacao_vazao_maxima_usina = self.__converte_array_em_dataframe(
            self.violacao_vazao_maxima_usina,
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
        self.violacao_turbinamento_maximo_usina = (
            self.__converte_array_em_dataframe(
                self.violacao_turbinamento_maximo_usina,
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
        )
        self.violacao_turbinamento_minimo_usina = (
            self.__converte_array_em_dataframe(
                self.violacao_turbinamento_minimo_usina,
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
        )
        self.violacao_lpp_turbinamento_maximo = (
            self.__converte_array_em_dataframe(
                self.violacao_lpp_turbinamento_maximo,
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
        )
        self.violacao_lpp_defluencia_maxima = (
            self.__converte_array_em_dataframe(
                self.violacao_lpp_defluencia_maxima,
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
        )
        self.violacao_lpp_turbinamento_maximo_usina = (
            self.__converte_array_em_dataframe(
                self.violacao_lpp_turbinamento_maximo_usina,
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
        )
        self.violacao_lpp_defluencia_maxima_usina = (
            self.__converte_array_em_dataframe(
                self.violacao_lpp_defluencia_maxima_usina,
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
        )
        self.rhs_lpp_turbinamento_maximo = self.__converte_array_em_dataframe(
            self.rhs_lpp_turbinamento_maximo,
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
        self.rhs_lpp_defluencia_maxima = self.__converte_array_em_dataframe(
            self.rhs_lpp_defluencia_maxima,
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
        self.rhs_lpp_turbinamento_maximo_usina = (
            self.__converte_array_em_dataframe(
                self.rhs_lpp_turbinamento_maximo_usina,
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
        )
        self.rhs_lpp_defluencia_maxima_usina = (
            self.__converte_array_em_dataframe(
                self.rhs_lpp_defluencia_maxima_usina,
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
        )
        self.violacao_restricao_eletrica_especial = (
            self.__converte_array_em_dataframe(
                self.violacao_restricao_eletrica_especial,
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
        )
        self.custo_restricao_eletrica_especial = (
            self.__converte_array_em_dataframe(
                self.custo_restricao_eletrica_especial,
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
        )
        self.volume_armazenado_inicial_usina = (
            self.__converte_array_em_dataframe(
                self.volume_armazenado_inicial_usina,
                {
                    "usina": np.tile(
                        self.nomes_usinas_hidreletricas, self.__num_simulacoes
                    )
                },
                self.numero_usinas_hidreletricas,
            )
        )
        self.lambda_balanco_hidrico_usina = self.__converte_array_em_dataframe(
            self.lambda_balanco_hidrico_usina,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )
        self.volume_evaporado_usina = self.__converte_array_em_dataframe(
            self.volume_evaporado_usina,
            {
                "usina": np.tile(
                    self.nomes_usinas_hidreletricas, self.__num_simulacoes
                )
            },
            self.numero_usinas_hidreletricas,
        )
        self.volume_bombeado_estacao_bombeamento = (
            self.__converte_array_em_dataframe(
                self.volume_bombeado_estacao_bombeamento,
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
        )
        self.consumo_energia_estacao_bombeamento = (
            self.__converte_array_em_dataframe(
                self.consumo_energia_estacao_bombeamento,
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
        )
        self.volume_desvio_canal_desvio_usina = (
            self.__converte_array_em_dataframe(
                self.volume_desvio_canal_desvio_usina,
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
        )

    def __cria_objeto_data(self):
        self.data = [
            self.estagio,
            self.mercado_liquido,
            self.energia_armazenada_inicial,
            self.energia_afluente_total,
            self.geracao_hidraulica_controlavel,
            self.energia_vertida,
            self.energia_armazenada_final,
            self.energia_fio_dagua,
            self.energia_evaporada,
            self.energia_enchimento_volume_morto,
            self.geracao_termica,
            self.deficit,
            self.pi_balanco_hidrico,
            self.pi_balanco_demanda,
            self.geracao_fio_dagua_liquida,
            self.perdas_fio_dagua,
            self.intercambios,
            self.excesso,
            self.energia_afluente_bruta_sem_correcao,
            self.energia_afluente_controlavel_corrigida,
            self.geracao_hidraulica_maxima,
            self.energia_controlavel_referente_desvio,
            self.energia_fio_dagua_referente_desvio,
            self.beneficio_intercambio,
            self.fator_correcao_energia_controlavel,
            self.invasao_curva_aversao,
            self.acionamento_curva_aversao,
            self.penalidade_invasao_curva_aversao,
            self.custo_total_operacao,
            self.custo_geracao_termica,
            self.beneficio_agrupamento_intercambios,
            self.energia_afluente_fio_dagua,
            self.beneficio_despacho_gnl,
            self.violacao_ghmin_ree,
            self.violacao_energia_vazao_minima,
            self.invasao_sar,
            self.acionamento_sar,
            self.penalidade_sar,
            self.capacidade_hidraulica_maxima_considerando_re,
            self.volume_armazenado_final,
            self.geracao_hidraulica_usina,
            self.volume_turbinado_usina,
            self.volume_vertido_usina,
            self.violacao_ghmin_usina,
            self.enchimento_volume_morto_usina,
            self.violacao_vazao_minima_usina,
            self.volume_desvio_usina,
            self.volume_desvio_positivo_usina,
            self.volume_desvio_negativo_usina,
            self.violacao_fpha_usina,
            self.vazao_afluente_usina,
            self.vazao_incremental_usina,
            self.volume_armazenado_final_percentual_usina,
            self.custo_violacao_energia_vazao_minima,
            self.custo_desvio_agua_controlavel,
            self.custo_desvio_agua_fio_dagua,
            self.custo_violacao_ghmin,
            self.soma_afluencias_passadas_ree,
            self.soma_afluencias_passadas_usina,
            self.geracao_eolica_pee,
            self.vento_pee,
            self.violacao_funcao_producao_eolica_pee,
            self.violacao_vazao_maxima_usina,
            self.violacao_turbinamento_maximo_usina,
            self.violacao_turbinamento_minimo_usina,
            self.violacao_lpp_turbinamento_maximo,
            self.violacao_lpp_defluencia_maxima,
            self.violacao_lpp_turbinamento_maximo_usina,
            self.violacao_lpp_defluencia_maxima_usina,
            self.rhs_lpp_turbinamento_maximo,
            self.rhs_lpp_defluencia_maxima,
            self.rhs_lpp_turbinamento_maximo_usina,
            self.rhs_lpp_defluencia_maxima_usina,
            self.violacao_restricao_eletrica_especial,
            self.custo_restricao_eletrica_especial,
            self.volume_armazenado_inicial_usina,
            self.lambda_balanco_hidrico_usina,
            self.volume_evaporado_usina,
            self.volume_bombeado_estacao_bombeamento,
            self.consumo_energia_estacao_bombeamento,
            self.volume_desvio_canal_desvio_usina,
        ]

    def read(
        self,
        file: IO,
        tamanho_registro: int = 41264,
        numero_estagios: int = 60,
        numero_forwards: int = 200,
        numero_rees: int = 12,
        numero_submercados: int = 4,
        numero_total_submercados: int = 5,
        numero_patamares_carga: int = 3,
        numero_patamares_deficit: int = 1,
        numero_agrupamentos_intercambio: int = 1,
        numero_classes_termicas_submercados: List[int] = [],
        numero_usinas_hidreletricas: int = 164,
        lag_maximo_usinas_gnl: int = 2,
        numero_parques_eolicos_equivalentes: int = 2,
        numero_restricoes_eletricas_especiais: int = 0,
        numero_estacoes_bombeamento: int = 0,
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
        self.numero_rees = numero_rees
        self.numero_submercados = numero_submercados
        self.numero_total_submercados = numero_total_submercados
        self.numero_patamares_carga = numero_patamares_carga
        self.numero_patamares_deficit = numero_patamares_deficit
        self.numero_agrupamentos_intercambio = numero_agrupamentos_intercambio
        self.numero_classes_termicas_submercados = (
            numero_classes_termicas_submercados
        )
        self.total_classes_termicas = sum(
            self.numero_classes_termicas_submercados
        )
        self.numero_usinas_hidreletricas = numero_usinas_hidreletricas
        self.lag_maximo_usinas_gnl = lag_maximo_usinas_gnl
        self.numero_parques_eolicos_equivalentes = (
            numero_parques_eolicos_equivalentes
        )
        self.numero_restricoes_eletricas_especiais = (
            numero_restricoes_eletricas_especiais
        )
        self.numero_estacoes_bombeamento = numero_estacoes_bombeamento
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
        self.__cria_objeto_data()
