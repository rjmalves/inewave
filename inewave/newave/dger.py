from inewave._utils.bloco import Bloco
from typing import Any, Type, List
from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita
from inewave.newave.modelos.dger import BlocoMesInicioEstudo, BlocoNomeCaso
from inewave.newave.modelos.dger import BlocoTipoExecucao
from inewave.newave.modelos.dger import BlocoDuracaoPeriodo
from inewave.newave.modelos.dger import BlocoNumAnosEstudo
from inewave.newave.modelos.dger import BlocoMesInicioPreEstudo
from inewave.newave.modelos.dger import BlocoAnoInicioEstudo
from inewave.newave.modelos.dger import BlocoNumAnosPreEstudo
from inewave.newave.modelos.dger import BlocoNumAnosPosEstudo
from inewave.newave.modelos.dger import BlocoNumAnosPosEstudoSimFinal
from inewave.newave.modelos.dger import BlocoImprimeDados
from inewave.newave.modelos.dger import BlocoImprimeMercados
from inewave.newave.modelos.dger import BlocoImprimeEnergias
from inewave.newave.modelos.dger import BlocoImprimeModeloEstocastico
from inewave.newave.modelos.dger import BlocoImprimeSubsistema
from inewave.newave.modelos.dger import BlocoNumMaxIteracoes
from inewave.newave.modelos.dger import BlocoNumForwards
from inewave.newave.modelos.dger import BlocoNumAberturas
from inewave.newave.modelos.dger import BlocoNumSeriesSinteticas
from inewave.newave.modelos.dger import BlocoOrdemMaximaPARp
from inewave.newave.modelos.dger import BlocoAnoInicialHistorico
from inewave.newave.modelos.dger import BlocoCalculaVolInicial
from inewave.newave.modelos.dger import BlocoVolInicialSubsistema
from inewave.newave.modelos.dger import BlocoTolerancia
from inewave.newave.modelos.dger import BlocoTaxaDesconto
from inewave.newave.modelos.dger import BlocoTipoSimFinal
from inewave.newave.modelos.dger import BlocoImpressaoOperacao
from inewave.newave.modelos.dger import BlocoImpressaoConvergencia
from inewave.newave.modelos.dger import BlocoIntervaloGravar
from inewave.newave.modelos.dger import BlocoMinIteracoes
from inewave.newave.modelos.dger import BlocoRacionamentoPreventivo
from inewave.newave.modelos.dger import BlocoNumAnosManutUTE
from inewave.newave.modelos.dger import BlocoTendenciaHidrologica
from inewave.newave.modelos.dger import BlocoRestricaoItaipu
from inewave.newave.modelos.dger import BlocoBid
from inewave.newave.modelos.dger import BlocoPerdasTransmissao
from inewave.newave.modelos.dger import BlocoElNino
from inewave.newave.modelos.dger import BlocoEnso
from inewave.newave.modelos.dger import BlocoDuracaoPorPatamar
from inewave.newave.modelos.dger import BlocoOutrosUsosAgua
from inewave.newave.modelos.dger import BlocoCorrecaoDesvio
from inewave.newave.modelos.dger import BlocoCurvaAversao
from inewave.newave.modelos.dger import BlocoTipoGeracaoENA
from inewave.newave.modelos.dger import BlocoRiscoDeficit
from inewave.newave.modelos.dger import BlocoIteracaoParaSimFinal
from inewave.newave.modelos.dger import BlocoAgrupamentoLivre
from inewave.newave.modelos.dger import BlocoEqualizacaoPenalInt
from inewave.newave.modelos.dger import BlocoRepresentacaoSubmot
from inewave.newave.modelos.dger import BlocoOrdenacaoAutomatica
from inewave.newave.modelos.dger import BlocoConsideraCargaAdicional
from inewave.newave.modelos.dger import BlocoDeltaZSUP
from inewave.newave.modelos.dger import BlocoDeltaZINF
from inewave.newave.modelos.dger import BlocoDeltasConsecutivos
from inewave.newave.modelos.dger import BlocoDespachoAntecipadoGNL
from inewave.newave.modelos.dger import BlocoModifAutomaticaAdTerm
from inewave.newave.modelos.dger import BlocoGeracaoHidraulicaMin
from inewave.newave.modelos.dger import BlocoSimFinalComData
from inewave.newave.modelos.dger import BlocoGerenciamentoPLs
from inewave.newave.modelos.dger import BlocoSAR
from inewave.newave.modelos.dger import BlocoCVAR
from inewave.newave.modelos.dger import BlocoZSUPMinConvergencia
from inewave.newave.modelos.dger import BlocoDesconsideraVazaoMinima
from inewave.newave.modelos.dger import BlocoRestricoesEletricas
from inewave.newave.modelos.dger import BlocoSelecaoCortes
from inewave.newave.modelos.dger import BlocoJanelaCortes
from inewave.newave.modelos.dger import BlocoReamostragemCenarios
from inewave.newave.modelos.dger import BlocoConvergeNoZero
from inewave.newave.modelos.dger import BlocoConsultaFCF
from inewave.newave.modelos.dger import BlocoImpressaoENA
from inewave.newave.modelos.dger import BlocoImpressaoCortesAtivosSimFinal
from inewave.newave.modelos.dger import BlocoRepresentacaoAgregacao
from inewave.newave.modelos.dger import BlocoMatrizCorrelacaoEspacial
from inewave.newave.modelos.dger import BlocoDesconsideraConvEstatistica
from inewave.newave.modelos.dger import BlocoMomentoReamostragem
from inewave.newave.modelos.dger import BlocoMantemArquivosEnergias
from inewave.newave.modelos.dger import BlocoInicioTesteConvergencia
from inewave.newave.modelos.dger import BlocoSazonalizarVminT
from inewave.newave.modelos.dger import BlocoSazonalizarVmaxT
from inewave.newave.modelos.dger import BlocoSazonalizarVminP
from inewave.newave.modelos.dger import BlocoSazonalizarCfugaCmont
from inewave.newave.modelos.dger import BlocoRestricoesEmissaoGEE
from inewave.newave.modelos.dger import BlocoAfluenciaAnualPARp
from inewave.newave.modelos.dger import BlocoRestricoesFornecGas
from inewave.newave.modelos.dger import BlocoIncertezaGeracaoEolica
from inewave.newave.modelos.dger import BlocoIncertezaGeracaoSolar
from inewave.newave.modelos.dger import BlocoRepresentacaoIncerteza
from inewave.newave.modelos.dger import LeituraDGer


class DGer(Arquivo):
    """
    Classe para armazenar dados gerais de uma execução do NEWAVE.

    """
    def __init__(self, dados: DadosArquivo):
        super().__init__(dados)

    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="dger.dat") -> 'DGer':
        """
        """
        leitor = LeituraDGer(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="dger.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

    def __le_por_tipo(self, tipo: Type[Bloco]) -> Any:
        for d in self._dados.blocos:
            if isinstance(d, tipo):
                return d.dados
        # Se não tem o dado, lança erro
        raise ValueError(f" Não foi encontrado o dado do tipo {tipo}")

    def __escreve_por_tipo(self,
                           tipo: Type[Bloco],
                           dado: Any):
        for d in self._dados.blocos:
            if isinstance(d, tipo):
                d.dados = dado
                return
        # Se não tem o dado, lança erro
        raise ValueError(f" Não foi encontrado o dado do tipo {tipo}")

    @property
    def nome_caso(self) -> str:
        """
        Configuração da linha número 1 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNomeCaso)

    @nome_caso.setter
    def nome_caso(self, dado: str):
        self.__escreve_por_tipo(BlocoNomeCaso, dado)

    @property
    def tipo_execucao(self) -> int:
        """
        Configuração da linha número 2 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoTipoExecucao)

    @tipo_execucao.setter
    def tipo_execucao(self, dado: int):
        self.__escreve_por_tipo(BlocoTipoExecucao, dado)

    @property
    def duracao_periodo(self) -> int:
        """
        Configuração da linha número 3 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoDuracaoPeriodo)

    @duracao_periodo.setter
    def duracao_periodo(self, dado: int):
        self.__escreve_por_tipo(BlocoDuracaoPeriodo, dado)

    @property
    def num_anos_estudo(self) -> int:
        """
        Configuração da linha número 4 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumAnosEstudo)

    @num_anos_estudo.setter
    def num_anos_estudo(self, dado: int):
        self.__escreve_por_tipo(BlocoNumAnosEstudo, dado)

    @property
    def mes_inicio_pre_estudo(self) -> int:
        """
        Configuração da linha número 5 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoMesInicioPreEstudo)

    @mes_inicio_pre_estudo.setter
    def mes_inicio_pre_estudo(self, dado: int):
        self.__escreve_por_tipo(BlocoMesInicioPreEstudo, dado)

    @property
    def mes_inicio_estudo(self) -> int:
        """
        Configuração da linha número 6 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoMesInicioEstudo)

    @mes_inicio_estudo.setter
    def mes_inicio_estudo(self, dado: int):
        self.__escreve_por_tipo(BlocoMesInicioEstudo, dado)

    @property
    def ano_inicio_estudo(self) -> int:
        """
        Configuração da linha número 7 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoAnoInicioEstudo)

    @ano_inicio_estudo.setter
    def ano_inicio_estudo(self, dado: int):
        self.__escreve_por_tipo(BlocoAnoInicioEstudo, dado)

    @property
    def num_anos_pre_estudo(self) -> int:
        """
        Configuração da linha número 8 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumAnosPreEstudo)

    @num_anos_pre_estudo.setter
    def num_anos_pre_estudo(self, dado: int):
        self.__escreve_por_tipo(BlocoNumAnosPreEstudo, dado)

    @property
    def num_anos_pos_estudo(self) -> int:
        """
        Configuração da linha número 9 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumAnosPosEstudo)

    @num_anos_pos_estudo.setter
    def num_anos_pos_estudo(self, dado: int):
        self.__escreve_por_tipo(BlocoNumAnosPosEstudo, dado)

    @property
    def num_anos_pos_sim_final(self) -> int:
        """
        Configuração da linha número 10 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumAnosPosEstudoSimFinal)

    @num_anos_pos_sim_final.setter
    def num_anos_pos_sim_final(self, dado: int):
        self.__escreve_por_tipo(BlocoNumAnosPosEstudoSimFinal, dado)

    @property
    def imprime_dados(self) -> int:
        """
        Configuração da linha número 11 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImprimeDados)

    @imprime_dados.setter
    def imprime_dados(self, dado: int):
        self.__escreve_por_tipo(BlocoImprimeDados, dado)

    @property
    def imprime_mercados(self) -> int:
        """
        Configuração da linha número 12 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImprimeMercados)

    @imprime_mercados.setter
    def imprime_mercados(self, dado: int):
        self.__escreve_por_tipo(BlocoImprimeMercados, dado)

    @property
    def imprime_energias(self) -> int:
        """
        Configuração da linha número 13 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImprimeEnergias)

    @imprime_energias.setter
    def imprime_energias(self, dado: int):
        self.__escreve_por_tipo(BlocoImprimeEnergias, dado)

    @property
    def imprime_modelo_estocastico(self) -> int:
        """
        Configuração da linha número 14 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImprimeModeloEstocastico)

    @imprime_modelo_estocastico.setter
    def imprime_modelo_estocastico(self, dado: int):
        self.__escreve_por_tipo(BlocoImprimeModeloEstocastico, dado)

    @property
    def imprime_subsistema(self) -> int:
        """
        Configuração da linha número 15 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImprimeSubsistema)

    @imprime_subsistema.setter
    def imprime_subsistema(self, dado: int):
        self.__escreve_por_tipo(BlocoImprimeSubsistema, dado)

    @property
    def num_max_iteracoes(self) -> int:
        """
        Configuração da linha número 16 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumMaxIteracoes)

    @num_max_iteracoes.setter
    def num_max_iteracoes(self, dado: int):
        self.__escreve_por_tipo(BlocoNumMaxIteracoes, dado)

    @property
    def num_forwards(self) -> int:
        """
        Configuração da linha número 17 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumForwards)

    @num_forwards.setter
    def num_forwards(self, dado: int):
        self.__escreve_por_tipo(BlocoNumForwards, dado)

    @property
    def num_aberturas(self) -> List[int]:
        """
        Configuração da linha número 18 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumAberturas)

    @num_aberturas.setter
    def num_aberturas(self, dado: List[int]):
        self.__escreve_por_tipo(BlocoNumAberturas, dado)

    @property
    def num_series_sinteticas(self) -> int:
        """
        Configuração da linha número 19 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumSeriesSinteticas)

    @num_series_sinteticas.setter
    def num_series_sinteticas(self, dado: int):
        self.__escreve_por_tipo(BlocoNumSeriesSinteticas, dado)

    @property
    def ordem_maxima_parp(self) -> int:
        """
        Configuração da linha número 20 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoOrdemMaximaPARp)

    @ordem_maxima_parp.setter
    def ordem_maxima_parp(self, dado: int):
        self.__escreve_por_tipo(BlocoOrdemMaximaPARp, dado)

    @property
    def ano_inicial_historico(self) -> List[int]:
        """
        Configuração da linha número 21 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoAnoInicialHistorico)

    @ano_inicial_historico.setter
    def ano_inicial_historico(self, dado: List[int]):
        self.__escreve_por_tipo(BlocoAnoInicialHistorico, dado)

    @property
    def calcula_volume_inicial(self) -> int:
        """
        Configuração da linha número 22 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoCalculaVolInicial)

    @calcula_volume_inicial.setter
    def calcula_volume_inicial(self, dado: int):
        self.__escreve_por_tipo(BlocoCalculaVolInicial, dado)

    @property
    def volume_inicial_por_subsistema(self) -> List[float]:
        """
        Configuração das linhas número 23 e 24 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoVolInicialSubsistema)

    @volume_inicial_por_subsistema.setter
    def volume_inicial_por_subsistema(self, dado: List[float]):
        self.__escreve_por_tipo(BlocoVolInicialSubsistema, dado)

    @property
    def tolerancia(self) -> float:
        """
        Configuração da linha número 25 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoTolerancia)

    @tolerancia.setter
    def tolerancia(self, dado: float):
        self.__escreve_por_tipo(BlocoTolerancia, dado)

    @property
    def taxa_de_desconto(self) -> float:
        """
        Configuração da linha número 26 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoTaxaDesconto)

    @taxa_de_desconto.setter
    def taxa_de_desconto(self, dado: float):
        self.__escreve_por_tipo(BlocoTaxaDesconto, dado)

    @property
    def tipo_simulacao_final(self) -> int:
        """
        Configuração da linha número 27 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoTipoSimFinal)

    @tipo_simulacao_final.setter
    def tipo_simulacao_final(self, dado: int):
        self.__escreve_por_tipo(BlocoTipoSimFinal, dado)

    @property
    def impressao_operacao(self) -> int:
        """
        Configuração da linha número 28 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImpressaoOperacao)

    @impressao_operacao.setter
    def impressao_operacao(self, dado: int):
        self.__escreve_por_tipo(BlocoImpressaoOperacao, dado)

    @property
    def impressao_convergencia(self) -> int:
        """
        Configuração da linha número 29 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImpressaoConvergencia)

    @impressao_convergencia.setter
    def impressao_convergencia(self, dado: int):
        self.__escreve_por_tipo(BlocoImpressaoConvergencia, dado)

    @property
    def intervalo_para_gravar(self) -> int:
        """
        Configuração da linha número 30 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoIntervaloGravar)

    @intervalo_para_gravar.setter
    def intervalo_para_gravar(self, dado: int):
        self.__escreve_por_tipo(BlocoIntervaloGravar, dado)

    @property
    def num_minimo_iteracoes(self) -> int:
        """
        Configuração da linha número 31 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoMinIteracoes)

    @num_minimo_iteracoes.setter
    def num_minimo_iteracoes(self, dado: int):
        self.__escreve_por_tipo(BlocoMinIteracoes, dado)

    @property
    def racionamento_preventivo(self) -> str:
        """
        Configuração da linha número 32 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRacionamentoPreventivo)

    @racionamento_preventivo.setter
    def racionamento_preventivo(self, dado: str):
        self.__escreve_por_tipo(BlocoRacionamentoPreventivo, dado)

    @property
    def num_anos_manutencao_utes(self) -> int:
        """
        Configuração da linha número 33 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoNumAnosManutUTE)

    @num_anos_manutencao_utes.setter
    def num_anos_manutencao_utes(self, dado: int):
        self.__escreve_por_tipo(BlocoNumAnosManutUTE, dado)

    @property
    def tendencia_hidrologica(self) -> List[int]:
        """
        Configuração da linha número 34 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoTendenciaHidrologica)

    @tendencia_hidrologica.setter
    def tendencia_hidrologica(self, dado: List[int]):
        self.__escreve_por_tipo(BlocoTendenciaHidrologica, dado)

    @property
    def restricao_itaipu(self) -> int:
        """
        Configuração da linha número 35 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRestricaoItaipu)

    @restricao_itaipu.setter
    def restricao_itaipu(self, dado: int):
        self.__escreve_por_tipo(BlocoRestricaoItaipu, dado)

    @property
    def bid(self) -> int:
        """
        Configuração da linha número 36 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoBid)

    @bid.setter
    def bid(self, dado: int):
        self.__escreve_por_tipo(BlocoBid, dado)

    @property
    def perdas_rede_transmissao(self) -> int:
        """
        Configuração da linha número 37 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoPerdasTransmissao)

    @perdas_rede_transmissao.setter
    def perdas_rede_transmissao(self, dado: int):
        self.__escreve_por_tipo(BlocoPerdasTransmissao, dado)

    @property
    def el_nino(self) -> int:
        """
        Configuração da linha número 38 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoElNino)

    @el_nino.setter
    def el_nino(self, dado: int):
        self.__escreve_por_tipo(BlocoElNino, dado)

    @property
    def enso(self) -> int:
        """
        Configuração da linha número 39 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoEnso)

    @enso.setter
    def enso(self, dado: int):
        self.__escreve_por_tipo(BlocoEnso, dado)

    @property
    def duracao_por_patamar(self) -> int:
        """
        Configuração da linha número 40 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoDuracaoPorPatamar)

    @duracao_por_patamar.setter
    def duracao_por_patamar(self, dado: int):
        self.__escreve_por_tipo(BlocoDuracaoPorPatamar, dado)

    @property
    def outros_usos_da_agua(self) -> int:
        """
        Configuração da linha número 41 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoOutrosUsosAgua)

    @outros_usos_da_agua.setter
    def outros_usos_da_agua(self, dado: int):
        self.__escreve_por_tipo(BlocoOutrosUsosAgua, dado)

    @property
    def correcao_desvio(self) -> int:
        """
        Configuração da linha número 42 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoCorrecaoDesvio)

    @correcao_desvio.setter
    def correcao_desvio(self, dado: int):
        self.__escreve_por_tipo(BlocoCorrecaoDesvio, dado)

    @property
    def curva_aversao(self) -> int:
        """
        Configuração da linha número 43 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoCurvaAversao)

    @curva_aversao.setter
    def curva_aversao(self, dado: int):
        self.__escreve_por_tipo(BlocoCurvaAversao, dado)

    @property
    def tipo_geracao_enas(self) -> int:
        """
        Configuração da linha número 44 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoTipoGeracaoENA)

    @tipo_geracao_enas.setter
    def tipo_geracao_enas(self, dado: int):
        self.__escreve_por_tipo(BlocoTipoGeracaoENA, dado)

    @property
    def risco_deficit(self) -> List[float]:
        """
        Configuração da linha número 45 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRiscoDeficit)

    @risco_deficit.setter
    def risco_deficit(self, dado: List[float]):
        self.__escreve_por_tipo(BlocoRiscoDeficit, dado)

    @property
    def iteracao_para_simulacao_final(self) -> int:
        """
        Configuração da linha número 46 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoIteracaoParaSimFinal)

    @iteracao_para_simulacao_final.setter
    def iteracao_para_simulacao_final(self, dado: int):
        self.__escreve_por_tipo(BlocoIteracaoParaSimFinal, dado)

    @property
    def agrupamento_livre(self) -> int:
        """
        Configuração da linha número 47 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoAgrupamentoLivre)

    @agrupamento_livre.setter
    def agrupamento_livre(self, dado: int):
        self.__escreve_por_tipo(BlocoAgrupamentoLivre, dado)

    @property
    def equalizacao_penal_itercambio(self) -> int:
        """
        Configuração da linha número 48 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoEqualizacaoPenalInt)

    @equalizacao_penal_itercambio.setter
    def equalizacao_penal_itercambio(self, dado: int):
        self.__escreve_por_tipo(BlocoEqualizacaoPenalInt, dado)

    @property
    def representacao_submotorizacao(self) -> int:
        """
        Configuração da linha número 49 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRepresentacaoSubmot)

    @representacao_submotorizacao.setter
    def representacao_submotorizacao(self, dado: int):
        self.__escreve_por_tipo(BlocoRepresentacaoSubmot, dado)

    @property
    def ordenacao_automatica(self) -> int:
        """
        Configuração da linha número 50 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoOrdenacaoAutomatica)

    @ordenacao_automatica.setter
    def ordenacao_automatica(self, dado: int):
        self.__escreve_por_tipo(BlocoOrdenacaoAutomatica, dado)

    @property
    def considera_carga_adicional(self) -> int:
        """
        Configuração da linha número 51 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoConsideraCargaAdicional)

    @considera_carga_adicional.setter
    def considera_carga_adicional(self, dado: int):
        self.__escreve_por_tipo(BlocoConsideraCargaAdicional, dado)

    @property
    def delta_zsup(self) -> float:
        """
        Configuração da linha número 52 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoDeltaZSUP)

    @delta_zsup.setter
    def delta_zsup(self, dado: float):
        self.__escreve_por_tipo(BlocoDeltaZSUP, dado)

    @property
    def delta_zinf(self) -> float:
        """
        Configuração da linha número 53 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoDeltaZINF)

    @delta_zinf.setter
    def delta_zinf(self, dado: float):
        self.__escreve_por_tipo(BlocoDeltaZINF, dado)

    @property
    def deltas_consecutivos(self) -> int:
        """
        Configuração da linha número 54 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoDeltasConsecutivos)

    @deltas_consecutivos.setter
    def deltas_consecutivos(self, dado: int):
        self.__escreve_por_tipo(BlocoDeltasConsecutivos, dado)

    @property
    def despacho_antecipado_gnl(self) -> int:
        """
        Configuração da linha número 55 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoDespachoAntecipadoGNL)

    @despacho_antecipado_gnl.setter
    def despacho_antecipado_gnl(self, dado: int):
        self.__escreve_por_tipo(BlocoDespachoAntecipadoGNL, dado)

    @property
    def modif_automatica_adterm(self) -> int:
        """
        Configuração da linha número 56 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoModifAutomaticaAdTerm)

    @modif_automatica_adterm.setter
    def modif_automatica_adterm(self, dado: int):
        self.__escreve_por_tipo(BlocoModifAutomaticaAdTerm, dado)

    @property
    def considera_ghmin(self) -> int:
        """
        Configuração da linha número 57 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoGeracaoHidraulicaMin)

    @considera_ghmin.setter
    def considera_ghmin(self, dado: int):
        self.__escreve_por_tipo(BlocoGeracaoHidraulicaMin, dado)

    @property
    def simulacao_final_com_data(self) -> int:
        """
        Configuração da linha número 58 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoSimFinalComData)

    @simulacao_final_com_data.setter
    def simulacao_final_com_data(self, dado: int):
        self.__escreve_por_tipo(BlocoSimFinalComData, dado)

    @property
    def gerenciamento_pls(self) -> List[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoGerenciamentoPLs)

    @gerenciamento_pls.setter
    def gerenciamento_pls(self, dado: List[int]):
        self.__escreve_por_tipo(BlocoGerenciamentoPLs, dado)

    @property
    def sar(self) -> int:
        """
        Configuração da linha número 60 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoSAR)

    @sar.setter
    def sar(self, dado: int):
        self.__escreve_por_tipo(BlocoSAR, dado)

    @property
    def cvar(self) -> int:
        """
        Configuração da linha número 61 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoCVAR)

    @cvar.setter
    def cvar(self, dado: int):
        self.__escreve_por_tipo(BlocoCVAR, dado)

    @property
    def considera_zsup_min_convergencia(self) -> int:
        """
        Configuração da linha número 62 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoZSUPMinConvergencia)

    @considera_zsup_min_convergencia.setter
    def considera_zsup_min_convergencia(self, dado: int):
        self.__escreve_por_tipo(BlocoZSUPMinConvergencia, dado)

    @property
    def desconsidera_vazao_minima(self) -> int:
        """
        Configuração da linha número 63 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoDesconsideraVazaoMinima)

    @desconsidera_vazao_minima.setter
    def desconsidera_vazao_minima(self, dado: int):
        self.__escreve_por_tipo(BlocoDesconsideraVazaoMinima, dado)

    @property
    def restricoes_eletricas(self) -> int:
        """
        Configuração da linha número 64 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRestricoesEletricas)

    @restricoes_eletricas.setter
    def restricoes_eletricas(self, dado: int):
        self.__escreve_por_tipo(BlocoRestricoesEletricas, dado)

    @property
    def selecao_de_cortes(self) -> int:
        """
        Configuração da linha número 65 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoSelecaoCortes)

    @selecao_de_cortes.setter
    def selecao_de_cortes(self, dado: int):
        self.__escreve_por_tipo(BlocoSelecaoCortes, dado)

    @property
    def janela_de_cortes(self) -> int:
        """
        Configuração da linha número 66 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoJanelaCortes)

    @janela_de_cortes.setter
    def janela_de_cortes(self, dado: int):
        self.__escreve_por_tipo(BlocoJanelaCortes, dado)

    @property
    def reamostragem_cenarios(self) -> List[int]:
        """
        Configuração da linha número 67 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoReamostragemCenarios)

    @reamostragem_cenarios.setter
    def reamostragem_cenarios(self, dado: List[int]):
        self.__escreve_por_tipo(BlocoReamostragemCenarios, dado)

    @property
    def converge_no_zero(self) -> int:
        """
        Configuração da linha número 68 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoConvergeNoZero)

    @converge_no_zero.setter
    def converge_no_zero(self, dado: int):
        self.__escreve_por_tipo(BlocoConvergeNoZero, dado)

    @property
    def consulta_fcf(self) -> int:
        """
        Configuração da linha número 69 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoConsultaFCF)

    @consulta_fcf.setter
    def consulta_fcf(self, dado: int):
        self.__escreve_por_tipo(BlocoConsultaFCF, dado)

    @property
    def impressao_ena(self) -> int:
        """
        Configuração da linha número 70 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImpressaoENA)

    @impressao_ena.setter
    def impressao_ena(self, dado: int):
        self.__escreve_por_tipo(BlocoImpressaoENA, dado)

    @property
    def impressao_cortes_ativos_sim_final(self) -> str:
        """
        Configuração da linha número 71 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoImpressaoCortesAtivosSimFinal)

    @impressao_cortes_ativos_sim_final.setter
    def impressao_cortes_ativos_sim_final(self, dado: str):
        self.__escreve_por_tipo(BlocoImpressaoCortesAtivosSimFinal,
                                dado)

    @property
    def representacao_agregacao(self) -> int:
        """
        Configuração da linha número 72 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRepresentacaoAgregacao)

    @representacao_agregacao.setter
    def representacao_agregacao(self, dado: int):
        self.__escreve_por_tipo(BlocoRepresentacaoAgregacao, dado)

    @property
    def matriz_correlacao_espacial(self) -> int:
        """
        Configuração da linha número 73 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoMatrizCorrelacaoEspacial)

    @matriz_correlacao_espacial.setter
    def matriz_correlacao_espacial(self, dado: int):
        self.__escreve_por_tipo(BlocoMatrizCorrelacaoEspacial, dado)

    @property
    def desconsidera_convergencia_estatistica(self) -> int:
        """
        Configuração da linha número 74 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoDesconsideraConvEstatistica)

    @desconsidera_convergencia_estatistica.setter
    def desconsidera_convergencia_estatistica(self, dado: int):
        self.__escreve_por_tipo(BlocoDesconsideraConvEstatistica,
                                dado)

    @property
    def momento_reamostragem(self) -> int:
        """
        Configuração da linha número 75 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoMomentoReamostragem)

    @momento_reamostragem.setter
    def momento_reamostragem(self, dado: int):
        self.__escreve_por_tipo(BlocoMomentoReamostragem, dado)

    @property
    def mantem_arquivos_energias(self) -> int:
        """
        Configuração da linha número 76 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoMantemArquivosEnergias)

    @mantem_arquivos_energias.setter
    def mantem_arquivos_energias(self, dado: int):
        self.__escreve_por_tipo(BlocoMantemArquivosEnergias, dado)

    @property
    def inicio_teste_convergencia(self) -> int:
        """
        Configuração da linha número 77 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoInicioTesteConvergencia)

    @inicio_teste_convergencia.setter
    def inicio_teste_convergencia(self, dado: int):
        self.__escreve_por_tipo(BlocoInicioTesteConvergencia, dado)

    @property
    def sazonaliza_vmint(self) -> int:
        """
        Configuração da linha número 78 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoSazonalizarVminT)

    @sazonaliza_vmint.setter
    def sazonaliza_vmint(self, dado: int):
        self.__escreve_por_tipo(BlocoSazonalizarVminT, dado)

    @property
    def sazonaliza_vmaxt(self) -> int:
        """
        Configuração da linha número 79 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoSazonalizarVmaxT)

    @sazonaliza_vmaxt.setter
    def sazonaliza_vmaxt(self, dado: int):
        self.__escreve_por_tipo(BlocoSazonalizarVmaxT, dado)

    @property
    def sazonaliza_vminp(self) -> int:
        """
        Configuração da linha número 80 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoSazonalizarVminP)

    @sazonaliza_vminp.setter
    def sazonaliza_vminp(self, dado: int):
        self.__escreve_por_tipo(BlocoSazonalizarVminP, dado)

    @property
    def sazonaliza_cfuga_cmont(self) -> int:
        """
        Configuração da linha número 81 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoSazonalizarCfugaCmont)

    @sazonaliza_cfuga_cmont.setter
    def sazonaliza_cfuga_cmont(self, dado: int):
        self.__escreve_por_tipo(BlocoSazonalizarCfugaCmont, dado)

    @property
    def restricoes_emissao_gee(self) -> int:
        """
        Configuração da linha número 82 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRestricoesEmissaoGEE)

    @restricoes_emissao_gee.setter
    def restricoes_emissao_gee(self, dado: int):
        self.__escreve_por_tipo(BlocoRestricoesEmissaoGEE, dado)

    @property
    def afluencia_anual_parp(self) -> int:
        """
        Configuração da linha número 83 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoAfluenciaAnualPARp)

    @afluencia_anual_parp.setter
    def afluencia_anual_parp(self, dado: int):
        self.__escreve_por_tipo(BlocoAfluenciaAnualPARp, dado)

    @property
    def restricoes_fornecimento_gas(self) -> int:
        """
        Configuração da linha número 84 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRestricoesFornecGas)

    @restricoes_fornecimento_gas.setter
    def restricoes_fornecimento_gas(self, dado: int):
        self.__escreve_por_tipo(BlocoRestricoesFornecGas, dado)

    @property
    def incerteza_geracao_eolica(self) -> int:
        """
        Configuração da linha número 85 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoIncertezaGeracaoEolica)

    @incerteza_geracao_eolica.setter
    def incerteza_geracao_eolica(self, dado: int):
        self.__escreve_por_tipo(BlocoIncertezaGeracaoEolica, dado)

    @property
    def incerteza_geracao_solar(self) -> int:
        """
        Configuração da linha número 86 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoIncertezaGeracaoSolar)

    @incerteza_geracao_solar.setter
    def incerteza_geracao_solar(self, dado: int):
        self.__escreve_por_tipo(BlocoIncertezaGeracaoSolar, dado)

    @property
    def representacao_incertezas(self) -> int:
        """
        Configuração da linha número 87 do arquivo `dger.dat`.
        """
        return self.__le_por_tipo(BlocoRepresentacaoIncerteza)

    @representacao_incertezas.setter
    def representacao_incertezas(self, dado: int):
        self.__escreve_por_tipo(BlocoRepresentacaoIncerteza, dado)
