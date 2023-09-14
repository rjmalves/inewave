from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional, List


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
from inewave.newave.modelos.dger import BlocoMemCalculoCortes
from inewave.newave.modelos.dger import BlocoGeracaoEolica

# from inewave.newave.modelos.dger import BlocoCompensacaoCorrelacaoCruzada
from inewave.newave.modelos.dger import (
    BlocoConsideracaoTurbinamentoMinimoMaximo,
)
from inewave.newave.modelos.dger import BlocoConsideracaoDefluenciaMaxima
from inewave.newave.modelos.dger import BlocoAproveitamentoBasePLsBackward
from inewave.newave.modelos.dger import BlocoImpressaoEstadosGeracaoCortes
from inewave.newave.modelos.dger import BlocoSementeForward
from inewave.newave.modelos.dger import BlocoSementeBackward
from inewave.newave.modelos.dger import BlocoRestricaoLPPTurbinamentoMaximoREE
from inewave.newave.modelos.dger import BlocoRestricaoLPPDefluenciaMaximaREE
from inewave.newave.modelos.dger import BlocoRestricaoLPPTurbinamentoMaximoUHE
from inewave.newave.modelos.dger import BlocoRestricaoLPPDefluenciaMaximaUHE
from inewave.newave.modelos.dger import BlocoRestricoesEletricasEspeciais
from inewave.newave.modelos.dger import BlocoFuncaoProducaoUHE
from inewave.newave.modelos.dger import BlocoFCFPosEstudo
from inewave.newave.modelos.dger import BlocoEstacoesBombeamento
from inewave.newave.modelos.dger import BlocoCanalDesvio
from inewave.newave.modelos.dger import BlocoRHQ
from inewave.newave.modelos.dger import BlocoRHV
from inewave.newave.modelos.dger import BlocoTratamentoCortes


class Dger(SectionFile):
    """
    Classe para armazenar dados gerais de uma execução do NEWAVE.

    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoNomeCaso,
        BlocoTipoExecucao,
        BlocoDuracaoPeriodo,
        BlocoNumAnosEstudo,
        BlocoMesInicioPreEstudo,
        BlocoMesInicioEstudo,
        BlocoAnoInicioEstudo,
        BlocoNumAnosPreEstudo,
        BlocoNumAnosPosEstudo,
        BlocoNumAnosPosEstudoSimFinal,
        BlocoImprimeDados,
        BlocoImprimeMercados,
        BlocoImprimeEnergias,
        BlocoImprimeModeloEstocastico,
        BlocoImprimeSubsistema,
        BlocoNumMaxIteracoes,
        BlocoNumForwards,
        BlocoNumAberturas,
        BlocoNumSeriesSinteticas,
        BlocoOrdemMaximaPARp,
        BlocoAnoInicialHistorico,
        BlocoCalculaVolInicial,
        BlocoVolInicialSubsistema,
        BlocoTolerancia,
        BlocoTaxaDesconto,
        BlocoTipoSimFinal,
        BlocoImpressaoOperacao,
        BlocoImpressaoConvergencia,
        BlocoIntervaloGravar,
        BlocoMinIteracoes,
        BlocoRacionamentoPreventivo,
        BlocoNumAnosManutUTE,
        BlocoTendenciaHidrologica,
        BlocoRestricaoItaipu,
        BlocoBid,
        BlocoPerdasTransmissao,
        BlocoElNino,
        BlocoEnso,
        BlocoDuracaoPorPatamar,
        BlocoOutrosUsosAgua,
        BlocoCorrecaoDesvio,
        BlocoCurvaAversao,
        BlocoTipoGeracaoENA,
        BlocoRiscoDeficit,
        BlocoIteracaoParaSimFinal,
        BlocoAgrupamentoLivre,
        BlocoEqualizacaoPenalInt,
        BlocoRepresentacaoSubmot,
        BlocoOrdenacaoAutomatica,
        BlocoConsideraCargaAdicional,
        BlocoDeltaZSUP,
        BlocoDeltaZINF,
        BlocoDeltasConsecutivos,
        BlocoDespachoAntecipadoGNL,
        BlocoModifAutomaticaAdTerm,
        BlocoGeracaoHidraulicaMin,
        BlocoSimFinalComData,
        BlocoGerenciamentoPLs,
        BlocoSAR,
        BlocoCVAR,
        BlocoZSUPMinConvergencia,
        BlocoDesconsideraVazaoMinima,
        BlocoRestricoesEletricas,
        BlocoSelecaoCortes,
        BlocoJanelaCortes,
        BlocoReamostragemCenarios,
        BlocoConvergeNoZero,
        BlocoConsultaFCF,
        BlocoImpressaoENA,
        BlocoImpressaoCortesAtivosSimFinal,
        BlocoRepresentacaoAgregacao,
        BlocoMatrizCorrelacaoEspacial,
        BlocoDesconsideraConvEstatistica,
        BlocoMomentoReamostragem,
        BlocoMantemArquivosEnergias,
        BlocoInicioTesteConvergencia,
        BlocoSazonalizarVminT,
        BlocoSazonalizarVmaxT,
        BlocoSazonalizarVminP,
        BlocoSazonalizarCfugaCmont,
        BlocoRestricoesEmissaoGEE,
        BlocoAfluenciaAnualPARp,
        BlocoRestricoesFornecGas,
        BlocoMemCalculoCortes,
        BlocoGeracaoEolica,
        # BlocoCompensacaoCorrelacaoCruzada,
        BlocoConsideracaoTurbinamentoMinimoMaximo,
        BlocoConsideracaoDefluenciaMaxima,
        BlocoAproveitamentoBasePLsBackward,
        BlocoImpressaoEstadosGeracaoCortes,
        BlocoSementeForward,
        BlocoSementeBackward,
        BlocoRestricaoLPPTurbinamentoMaximoREE,
        BlocoRestricaoLPPDefluenciaMaximaREE,
        BlocoRestricaoLPPTurbinamentoMaximoUHE,
        BlocoRestricaoLPPDefluenciaMaximaUHE,
        BlocoRestricoesEletricasEspeciais,
        BlocoFuncaoProducaoUHE,
        BlocoFCFPosEstudo,
        BlocoEstacoesBombeamento,
        BlocoCanalDesvio,
        BlocoRHQ,
        BlocoRHV,
        BlocoTratamentoCortes,
    ]

    @property
    def nome_caso(self) -> Optional[str]:
        """
        Configuração da linha número 1 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: str
        """
        b = self.data.get_sections_of_type(BlocoNomeCaso)
        if isinstance(b, BlocoNomeCaso):
            return b.valor
        return None

    @nome_caso.setter
    def nome_caso(self, dado: str):
        b = self.data.get_sections_of_type(BlocoNomeCaso)
        if isinstance(b, BlocoNomeCaso):
            b.valor = dado

    @property
    def tipo_execucao(self) -> Optional[int]:
        """
        Configuração da linha número 2 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoTipoExecucao)
        if isinstance(b, BlocoTipoExecucao):
            return b.valor
        return None

    @tipo_execucao.setter
    def tipo_execucao(self, dado: int):
        b = self.data.get_sections_of_type(BlocoTipoExecucao)
        if isinstance(b, BlocoTipoExecucao):
            b.valor = dado

    @property
    def duracao_periodo(self) -> Optional[int]:
        """
        Configuração da linha número 3 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoDuracaoPeriodo)
        if isinstance(b, BlocoDuracaoPeriodo):
            return b.valor
        return None

    @duracao_periodo.setter
    def duracao_periodo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoDuracaoPeriodo)
        if isinstance(b, BlocoDuracaoPeriodo):
            b.valor = dado

    @property
    def num_anos_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 4 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumAnosEstudo)
        if isinstance(b, BlocoNumAnosEstudo):
            return b.valor
        return None

    @num_anos_estudo.setter
    def num_anos_estudo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumAnosEstudo)
        if isinstance(b, BlocoNumAnosEstudo):
            b.valor = dado

    @property
    def mes_inicio_pre_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 5 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoMesInicioPreEstudo)
        if isinstance(b, BlocoMesInicioPreEstudo):
            return b.valor
        return None

    @mes_inicio_pre_estudo.setter
    def mes_inicio_pre_estudo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoMesInicioPreEstudo)
        if isinstance(b, BlocoMesInicioPreEstudo):
            b.valor = dado

    @property
    def mes_inicio_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 6 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoMesInicioEstudo)
        if isinstance(b, BlocoMesInicioEstudo):
            return b.valor
        return None

    @mes_inicio_estudo.setter
    def mes_inicio_estudo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoMesInicioEstudo)
        if isinstance(b, BlocoMesInicioEstudo):
            b.valor = dado

    @property
    def ano_inicio_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 7 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoAnoInicioEstudo)
        if isinstance(b, BlocoAnoInicioEstudo):
            return b.valor
        return None

    @ano_inicio_estudo.setter
    def ano_inicio_estudo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoAnoInicioEstudo)
        if isinstance(b, BlocoAnoInicioEstudo):
            b.valor = dado

    @property
    def num_anos_pre_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 8 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumAnosPreEstudo)
        if isinstance(b, BlocoNumAnosPreEstudo):
            return b.valor
        return None

    @num_anos_pre_estudo.setter
    def num_anos_pre_estudo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumAnosPreEstudo)
        if isinstance(b, BlocoNumAnosPreEstudo):
            b.valor = dado

    @property
    def num_anos_pos_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 9 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumAnosPosEstudo)
        if isinstance(b, BlocoNumAnosPosEstudo):
            return b.valor
        return None

    @num_anos_pos_estudo.setter
    def num_anos_pos_estudo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumAnosPosEstudo)
        if isinstance(b, BlocoNumAnosPosEstudo):
            b.valor = dado

    @property
    def num_anos_pos_sim_final(self) -> Optional[int]:
        """
        Configuração da linha número 10 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumAnosPosEstudoSimFinal)
        if isinstance(b, BlocoNumAnosPosEstudoSimFinal):
            return b.valor
        return None

    @num_anos_pos_sim_final.setter
    def num_anos_pos_sim_final(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumAnosPosEstudoSimFinal)
        if isinstance(b, BlocoNumAnosPosEstudoSimFinal):
            b.valor = dado

    @property
    def imprime_dados(self) -> Optional[int]:
        """
        Configuração da linha número 11 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImprimeDados)
        if isinstance(b, BlocoImprimeDados):
            return b.valor
        return None

    @imprime_dados.setter
    def imprime_dados(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImprimeDados)
        if isinstance(b, BlocoImprimeDados):
            b.valor = dado

    @property
    def imprime_mercados(self) -> Optional[int]:
        """
        Configuração da linha número 12 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImprimeMercados)
        if isinstance(b, BlocoImprimeMercados):
            return b.valor
        return None

    @imprime_mercados.setter
    def imprime_mercados(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImprimeMercados)
        if isinstance(b, BlocoImprimeMercados):
            b.valor = dado

    @property
    def imprime_energias(self) -> Optional[int]:
        """
        Configuração da linha número 13 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImprimeEnergias)
        if isinstance(b, BlocoImprimeEnergias):
            return b.valor
        return None

    @imprime_energias.setter
    def imprime_energias(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImprimeEnergias)
        if isinstance(b, BlocoImprimeEnergias):
            b.valor = dado

    @property
    def imprime_modelo_estocastico(self) -> Optional[int]:
        """
        Configuração da linha número 14 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImprimeModeloEstocastico)
        if isinstance(b, BlocoImprimeModeloEstocastico):
            return b.valor
        return None

    @imprime_modelo_estocastico.setter
    def imprime_modelo_estocastico(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImprimeModeloEstocastico)
        if isinstance(b, BlocoImprimeModeloEstocastico):
            b.valor = dado

    @property
    def imprime_subsistema(self) -> Optional[int]:
        """
        Configuração da linha número 15 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImprimeSubsistema)
        if isinstance(b, BlocoImprimeSubsistema):
            return b.valor
        return None

    @imprime_subsistema.setter
    def imprime_subsistema(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImprimeSubsistema)
        if isinstance(b, BlocoImprimeSubsistema):
            b.valor = dado

    @property
    def num_max_iteracoes(self) -> Optional[int]:
        """
        Configuração da linha número 16 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumMaxIteracoes)
        if isinstance(b, BlocoNumMaxIteracoes):
            return b.valor
        return None

    @num_max_iteracoes.setter
    def num_max_iteracoes(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumMaxIteracoes)
        if isinstance(b, BlocoNumMaxIteracoes):
            b.valor = dado

    @property
    def num_forwards(self) -> Optional[int]:
        """
        Configuração da linha número 17 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumForwards)
        if isinstance(b, BlocoNumForwards):
            return b.valor
        return None

    @num_forwards.setter
    def num_forwards(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumForwards)
        if isinstance(b, BlocoNumForwards):
            b.valor = dado

    @property
    def num_aberturas(self) -> Optional[int]:
        """
        Configuração da linha número 18 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumAberturas)
        if isinstance(b, BlocoNumAberturas):
            return b.valor
        return None

    @num_aberturas.setter
    def num_aberturas(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumAberturas)
        if isinstance(b, BlocoNumAberturas):
            b.valor = dado

    @property
    def num_series_sinteticas(self) -> Optional[int]:
        """
        Configuração da linha número 19 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumSeriesSinteticas)
        if isinstance(b, BlocoNumSeriesSinteticas):
            return b.valor
        return None

    @num_series_sinteticas.setter
    def num_series_sinteticas(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumSeriesSinteticas)
        if isinstance(b, BlocoNumSeriesSinteticas):
            b.valor = dado

    @property
    def ordem_maxima_parp(self) -> Optional[int]:
        """
        Configuração da linha número 20 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoOrdemMaximaPARp)
        if isinstance(b, BlocoOrdemMaximaPARp):
            return b.valor
        return None

    @ordem_maxima_parp.setter
    def ordem_maxima_parp(self, dado: int):
        b = self.data.get_sections_of_type(BlocoOrdemMaximaPARp)
        if isinstance(b, BlocoOrdemMaximaPARp):
            b.valor = dado

    @property
    def ano_inicial_historico(self) -> Optional[int]:
        """
        Configuração da linha número 21 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoAnoInicialHistorico)
        if isinstance(b, BlocoAnoInicialHistorico):
            return b.ano_inicial
        return None

    @ano_inicial_historico.setter
    def ano_inicial_historico(self, dado: int):
        b = self.data.get_sections_of_type(BlocoAnoInicialHistorico)
        if isinstance(b, BlocoAnoInicialHistorico):
            b.ano_inicial = dado

    @property
    def tamanho_registro_arquivo_historico(self) -> Optional[int]:
        """
        Configuração da linha número 21 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoAnoInicialHistorico)
        if isinstance(b, BlocoAnoInicialHistorico):
            return b.tamanho_registro_arquivo
        return None

    @tamanho_registro_arquivo_historico.setter
    def tamanho_registro_arquivo_historico(self, dado: int):
        b = self.data.get_sections_of_type(BlocoAnoInicialHistorico)
        if isinstance(b, BlocoAnoInicialHistorico):
            b.tamanho_registro_arquivo = dado

    @property
    def calcula_volume_inicial(self) -> Optional[int]:
        """
        Configuração da linha número 22 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoCalculaVolInicial)
        if isinstance(b, BlocoCalculaVolInicial):
            return b.valor
        return None

    @calcula_volume_inicial.setter
    def calcula_volume_inicial(self, dado: int):
        b = self.data.get_sections_of_type(BlocoCalculaVolInicial)
        if isinstance(b, BlocoCalculaVolInicial):
            b.valor = dado

    @property
    def volume_inicial_subsistema(self) -> List[Optional[float]]:
        """
        Configuração das linhas número 23 e 24 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoVolInicialSubsistema)
        if isinstance(b, BlocoVolInicialSubsistema):
            return b.valores
        return []

    @volume_inicial_subsistema.setter
    def volume_inicial_subsistema(self, dado: List[Optional[float]]):
        b = self.data.get_sections_of_type(BlocoVolInicialSubsistema)
        if isinstance(b, BlocoVolInicialSubsistema):
            b.valores = dado

    @property
    def tolerancia(self) -> Optional[float]:
        """
        Configuração da linha número 25 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoTolerancia)
        if isinstance(b, BlocoTolerancia):
            return b.valor
        return None

    @tolerancia.setter
    def tolerancia(self, dado: float):
        b = self.data.get_sections_of_type(BlocoTolerancia)
        if isinstance(b, BlocoTolerancia):
            b.valor = dado

    @property
    def taxa_de_desconto(self) -> Optional[float]:
        """
        Configuração da linha número 26 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoTaxaDesconto)
        if isinstance(b, BlocoTaxaDesconto):
            return b.valor
        return None

    @taxa_de_desconto.setter
    def taxa_de_desconto(self, dado: float):
        b = self.data.get_sections_of_type(BlocoTaxaDesconto)
        if isinstance(b, BlocoTaxaDesconto):
            b.valor = dado

    @property
    def tipo_simulacao_final(self) -> Optional[int]:
        """
        Configuração do primeiro campo da linha número 27
        do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoTipoSimFinal)
        if isinstance(b, BlocoTipoSimFinal):
            return b.valor[0]
        return None

    @tipo_simulacao_final.setter
    def tipo_simulacao_final(self, dado: int):
        b = self.data.get_sections_of_type(BlocoTipoSimFinal)
        if isinstance(b, BlocoTipoSimFinal):
            b.valor = [dado] + [b.valor[1]]

    @property
    def agregacao_simulacao_final(self) -> Optional[int]:
        """
        Configuração do segundo campo da linha número 27
        do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoTipoSimFinal)
        if isinstance(b, BlocoTipoSimFinal):
            return b.valor[1]
        return None

    @agregacao_simulacao_final.setter
    def agregacao_simulacao_final(self, dado: int):
        b = self.data.get_sections_of_type(BlocoTipoSimFinal)
        if isinstance(b, BlocoTipoSimFinal):
            b.valor = [b.valor[0]] + [dado]

    @property
    def impressao_operacao(self) -> Optional[int]:
        """
        Configuração da linha número 28 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImpressaoOperacao)
        if isinstance(b, BlocoImpressaoOperacao):
            return b.valor
        return None

    @impressao_operacao.setter
    def impressao_operacao(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImpressaoOperacao)
        if isinstance(b, BlocoImpressaoOperacao):
            b.valor = dado

    @property
    def impressao_convergencia(self) -> Optional[int]:
        """
        Configuração da linha número 29 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImpressaoConvergencia)
        if isinstance(b, BlocoImpressaoConvergencia):
            return b.valor
        return None

    @impressao_convergencia.setter
    def impressao_convergencia(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImpressaoConvergencia)
        if isinstance(b, BlocoImpressaoConvergencia):
            b.valor = dado

    @property
    def intervalo_para_gravar(self) -> Optional[int]:
        """
        Configuração da linha número 30 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoIntervaloGravar)
        if isinstance(b, BlocoIntervaloGravar):
            return b.valor
        return None

    @intervalo_para_gravar.setter
    def intervalo_para_gravar(self, dado: int):
        b = self.data.get_sections_of_type(BlocoIntervaloGravar)
        if isinstance(b, BlocoIntervaloGravar):
            b.valor = dado

    @property
    def num_minimo_iteracoes(self) -> Optional[int]:
        """
        Configuração da linha número 31 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoMinIteracoes)
        if isinstance(b, BlocoMinIteracoes):
            return b.valor
        return None

    @num_minimo_iteracoes.setter
    def num_minimo_iteracoes(self, dado: int):
        b = self.data.get_sections_of_type(BlocoMinIteracoes)
        if isinstance(b, BlocoMinIteracoes):
            b.valor = dado

    @property
    def racionamento_preventivo(self) -> Optional[int]:
        """
        Configuração da linha número 32 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoRacionamentoPreventivo)
        if isinstance(b, BlocoRacionamentoPreventivo):
            return b.valor
        return None

    @racionamento_preventivo.setter
    def racionamento_preventivo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRacionamentoPreventivo)
        if isinstance(b, BlocoRacionamentoPreventivo):
            b.valor = dado

    @property
    def num_anos_manutencao_utes(self) -> Optional[int]:
        """
        Configuração da linha número 33 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoNumAnosManutUTE)
        if isinstance(b, BlocoNumAnosManutUTE):
            return b.valor
        return None

    @num_anos_manutencao_utes.setter
    def num_anos_manutencao_utes(self, dado: int):
        b = self.data.get_sections_of_type(BlocoNumAnosManutUTE)
        if isinstance(b, BlocoNumAnosManutUTE):
            b.valor = dado

    @property
    def considera_tendencia_hidrologica_calculo_politica(
        self,
    ) -> Optional[int]:
        """
        Configuração da linha número 34 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoTendenciaHidrologica)
        if isinstance(b, BlocoTendenciaHidrologica):
            return b.considera_tendencia_hidrologica_calculo_politica
        return None

    @considera_tendencia_hidrologica_calculo_politica.setter
    def considera_tendencia_hidrologica_calculo_politica(self, dado: int):
        b = self.data.get_sections_of_type(BlocoTendenciaHidrologica)
        if isinstance(b, BlocoTendenciaHidrologica):
            b.considera_tendencia_hidrologica_calculo_politica = dado

    @property
    def considera_tendencia_hidrologica_sim_final(self) -> Optional[int]:
        """
        Configuração da linha número 34 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoTendenciaHidrologica)
        if isinstance(b, BlocoTendenciaHidrologica):
            return b.considera_tendencia_hidrologica_sim_final
        return None

    @considera_tendencia_hidrologica_sim_final.setter
    def considera_tendencia_hidrologica_sim_final(self, dado: int):
        b = self.data.get_sections_of_type(BlocoTendenciaHidrologica)
        if isinstance(b, BlocoTendenciaHidrologica):
            b.considera_tendencia_hidrologica_sim_final = dado

    @property
    def restricao_itaipu(self) -> Optional[int]:
        """
        Configuração da linha número 35 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoRestricaoItaipu)
        if isinstance(b, BlocoRestricaoItaipu):
            return b.valor
        return None

    @restricao_itaipu.setter
    def restricao_itaipu(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRestricaoItaipu)
        if isinstance(b, BlocoRestricaoItaipu):
            b.valor = dado

    @property
    def bid(self) -> Optional[int]:
        """
        Configuração da linha número 36 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoBid)
        if isinstance(b, BlocoBid):
            return b.valor
        return None

    @bid.setter
    def bid(self, dado: int):
        b = self.data.get_sections_of_type(BlocoBid)
        if isinstance(b, BlocoBid):
            b.valor = dado

    @property
    def perdas_rede_transmissao(self) -> Optional[int]:
        """
        Configuração da linha número 37 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoPerdasTransmissao)
        if isinstance(b, BlocoPerdasTransmissao):
            return b.valor
        return None

    @perdas_rede_transmissao.setter
    def perdas_rede_transmissao(self, dado: int):
        b = self.data.get_sections_of_type(BlocoPerdasTransmissao)
        if isinstance(b, BlocoPerdasTransmissao):
            b.valor = dado

    @property
    def el_nino(self) -> Optional[int]:
        """
        Configuração da linha número 38 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoElNino)
        if isinstance(b, BlocoElNino):
            return b.valor
        return None

    @el_nino.setter
    def el_nino(self, dado: int):
        b = self.data.get_sections_of_type(BlocoElNino)
        if isinstance(b, BlocoElNino):
            b.valor = dado

    @property
    def enso(self) -> Optional[int]:
        """
        Configuração da linha número 39 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoEnso)
        if isinstance(b, BlocoEnso):
            return b.valor
        return None

    @enso.setter
    def enso(self, dado: int):
        b = self.data.get_sections_of_type(BlocoEnso)
        if isinstance(b, BlocoEnso):
            b.valor = dado

    @property
    def duracao_por_patamar(self) -> Optional[int]:
        """
        Configuração da linha número 40 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoDuracaoPorPatamar)
        if isinstance(b, BlocoDuracaoPorPatamar):
            return b.valor
        return None

    @duracao_por_patamar.setter
    def duracao_por_patamar(self, dado: int):
        b = self.data.get_sections_of_type(BlocoDuracaoPorPatamar)
        if isinstance(b, BlocoDuracaoPorPatamar):
            b.valor = dado

    @property
    def outros_usos_da_agua(self) -> Optional[int]:
        """
        Configuração da linha número 41 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoOutrosUsosAgua)
        if isinstance(b, BlocoOutrosUsosAgua):
            return b.valor
        return None

    @outros_usos_da_agua.setter
    def outros_usos_da_agua(self, dado: int):
        b = self.data.get_sections_of_type(BlocoOutrosUsosAgua)
        if isinstance(b, BlocoOutrosUsosAgua):
            b.valor = dado

    @property
    def correcao_desvio(self) -> Optional[int]:
        """
        Configuração da linha número 42 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoCorrecaoDesvio)
        if isinstance(b, BlocoCorrecaoDesvio):
            return b.valor
        return None

    @correcao_desvio.setter
    def correcao_desvio(self, dado: int):
        b = self.data.get_sections_of_type(BlocoCorrecaoDesvio)
        if isinstance(b, BlocoCorrecaoDesvio):
            b.valor = dado

    @property
    def curva_aversao(self) -> Optional[int]:
        """
        Configuração da linha número 43 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoCurvaAversao)
        if isinstance(b, BlocoCurvaAversao):
            return b.valor
        return None

    @curva_aversao.setter
    def curva_aversao(self, dado: int):
        b = self.data.get_sections_of_type(BlocoCurvaAversao)
        if isinstance(b, BlocoCurvaAversao):
            b.valor = dado

    @property
    def tipo_geracao_enas(self) -> Optional[int]:
        """
        Configuração da linha número 44 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoTipoGeracaoENA)
        if isinstance(b, BlocoTipoGeracaoENA):
            return b.valor
        return None

    @tipo_geracao_enas.setter
    def tipo_geracao_enas(self, dado: int):
        b = self.data.get_sections_of_type(BlocoTipoGeracaoENA)
        if isinstance(b, BlocoTipoGeracaoENA):
            b.valor = dado

    @property
    def primeira_profundidade_risco_deficit(self) -> Optional[float]:
        """
        Configuração da linha número 45 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: float
        """
        b = self.data.get_sections_of_type(BlocoRiscoDeficit)
        if isinstance(b, BlocoRiscoDeficit):
            return b.primeira_profundidade_risco_deficit
        return None

    @primeira_profundidade_risco_deficit.setter
    def primeira_profundidade_risco_deficit(self, dado: float):
        b = self.data.get_sections_of_type(BlocoRiscoDeficit)
        if isinstance(b, BlocoRiscoDeficit):
            b.primeira_profundidade_risco_deficit = dado

    @property
    def segunda_profundidade_risco_deficit(self) -> Optional[float]:
        """
        Configuração da linha número 45 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: float
        """
        b = self.data.get_sections_of_type(BlocoRiscoDeficit)
        if isinstance(b, BlocoRiscoDeficit):
            return b.segunda_profundidade_risco_deficit
        return None

    @segunda_profundidade_risco_deficit.setter
    def segunda_profundidade_risco_deficit(self, dado: float):
        b = self.data.get_sections_of_type(BlocoRiscoDeficit)
        if isinstance(b, BlocoRiscoDeficit):
            b.segunda_profundidade_risco_deficit = dado

    @property
    def iteracao_para_simulacao_final(self) -> Optional[int]:
        """
        Configuração da linha número 46 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoIteracaoParaSimFinal)
        if isinstance(b, BlocoIteracaoParaSimFinal):
            return b.valor
        return None

    @iteracao_para_simulacao_final.setter
    def iteracao_para_simulacao_final(self, dado: int):
        b = self.data.get_sections_of_type(BlocoIteracaoParaSimFinal)
        if isinstance(b, BlocoIteracaoParaSimFinal):
            b.valor = dado

    @property
    def agrupamento_livre(self) -> Optional[int]:
        """
        Configuração da linha número 47 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoAgrupamentoLivre)
        if isinstance(b, BlocoAgrupamentoLivre):
            return b.valor
        return None

    @agrupamento_livre.setter
    def agrupamento_livre(self, dado: int):
        b = self.data.get_sections_of_type(BlocoAgrupamentoLivre)
        if isinstance(b, BlocoAgrupamentoLivre):
            b.valor = dado

    @property
    def equalizacao_penal_intercambio(self) -> Optional[int]:
        """
        Configuração da linha número 48 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoEqualizacaoPenalInt)
        if isinstance(b, BlocoEqualizacaoPenalInt):
            return b.valor
        return None

    @equalizacao_penal_intercambio.setter
    def equalizacao_penal_intercambio(self, dado: int):
        b = self.data.get_sections_of_type(BlocoEqualizacaoPenalInt)
        if isinstance(b, BlocoEqualizacaoPenalInt):
            b.valor = dado

    @property
    def representacao_submotorizacao(self) -> Optional[int]:
        """
        Configuração da linha número 49 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoRepresentacaoSubmot)
        if isinstance(b, BlocoRepresentacaoSubmot):
            return b.valor
        return None

    @representacao_submotorizacao.setter
    def representacao_submotorizacao(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRepresentacaoSubmot)
        if isinstance(b, BlocoRepresentacaoSubmot):
            b.valor = dado

    @property
    def ordenacao_automatica(self) -> Optional[int]:
        """
        Configuração da linha número 50 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoOrdenacaoAutomatica)
        if isinstance(b, BlocoOrdenacaoAutomatica):
            return b.valor
        return None

    @ordenacao_automatica.setter
    def ordenacao_automatica(self, dado: int):
        b = self.data.get_sections_of_type(BlocoOrdenacaoAutomatica)
        if isinstance(b, BlocoOrdenacaoAutomatica):
            b.valor = dado

    @property
    def considera_carga_adicional(self) -> Optional[int]:
        """
        Configuração da linha número 51 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoConsideraCargaAdicional)
        if isinstance(b, BlocoConsideraCargaAdicional):
            return b.valor
        return None

    @considera_carga_adicional.setter
    def considera_carga_adicional(self, dado: int):
        b = self.data.get_sections_of_type(BlocoConsideraCargaAdicional)
        if isinstance(b, BlocoConsideraCargaAdicional):
            b.valor = dado

    @property
    def delta_zsup(self) -> Optional[float]:
        """
        Configuração da linha número 52 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: float
        """
        b = self.data.get_sections_of_type(BlocoDeltaZSUP)
        if isinstance(b, BlocoDeltaZSUP):
            return b.valor
        return None

    @delta_zsup.setter
    def delta_zsup(self, dado: float):
        b = self.data.get_sections_of_type(BlocoDeltaZSUP)
        if isinstance(b, BlocoDeltaZSUP):
            b.valor = dado

    @property
    def delta_zinf(self) -> Optional[float]:
        """
        Configuração da linha número 53 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: float
        """
        b = self.data.get_sections_of_type(BlocoDeltaZINF)
        if isinstance(b, BlocoDeltaZINF):
            return b.valor
        return None

    @delta_zinf.setter
    def delta_zinf(self, dado: float):
        b = self.data.get_sections_of_type(BlocoDeltaZINF)
        if isinstance(b, BlocoDeltaZINF):
            b.valor = dado

    @property
    def deltas_consecutivos(self) -> Optional[int]:
        """
        Configuração da linha número 54 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoDeltasConsecutivos)
        if isinstance(b, BlocoDeltasConsecutivos):
            return b.valor
        return None

    @deltas_consecutivos.setter
    def deltas_consecutivos(self, dado: int):
        b = self.data.get_sections_of_type(BlocoDeltasConsecutivos)
        if isinstance(b, BlocoDeltasConsecutivos):
            b.valor = dado

    @property
    def despacho_antecipado_gnl(self) -> Optional[int]:
        """
        Configuração da linha número 55 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoDespachoAntecipadoGNL)
        if isinstance(b, BlocoDespachoAntecipadoGNL):
            return b.valor
        return None

    @despacho_antecipado_gnl.setter
    def despacho_antecipado_gnl(self, dado: int):
        b = self.data.get_sections_of_type(BlocoDespachoAntecipadoGNL)
        if isinstance(b, BlocoDespachoAntecipadoGNL):
            b.valor = dado

    @property
    def modif_automatica_adterm(self) -> Optional[int]:
        """
        Configuração da linha número 56 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoModifAutomaticaAdTerm)
        if isinstance(b, BlocoModifAutomaticaAdTerm):
            return b.valor
        return None

    @modif_automatica_adterm.setter
    def modif_automatica_adterm(self, dado: int):
        b = self.data.get_sections_of_type(BlocoModifAutomaticaAdTerm)
        if isinstance(b, BlocoModifAutomaticaAdTerm):
            b.valor = dado

    @property
    def considera_ghmin(self) -> Optional[int]:
        """
        Configuração da linha número 57 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoGeracaoHidraulicaMin)
        if isinstance(b, BlocoGeracaoHidraulicaMin):
            return b.valor
        return None

    @considera_ghmin.setter
    def considera_ghmin(self, dado: int):
        b = self.data.get_sections_of_type(BlocoGeracaoHidraulicaMin)
        if isinstance(b, BlocoGeracaoHidraulicaMin):
            b.valor = dado

    @property
    def simulacao_final_com_data(self) -> Optional[int]:
        """
        Configuração da linha número 58 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoSimFinalComData)
        if isinstance(b, BlocoSimFinalComData):
            return b.valor
        return None

    @simulacao_final_com_data.setter
    def simulacao_final_com_data(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSimFinalComData)
        if isinstance(b, BlocoSimFinalComData):
            b.valor = dado

    @property
    def utiliza_gerenciamento_pls(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            return b.utiliza_gerenciamento_pls
        return None

    @utiliza_gerenciamento_pls.setter
    def utiliza_gerenciamento_pls(self, dado: int):
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            b.utiliza_gerenciamento_pls = dado

    @property
    def comunicacao_dois_niveis(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            return b.comunicacao_dois_niveis
        return None

    @comunicacao_dois_niveis.setter
    def comunicacao_dois_niveis(self, dado: int):
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            b.comunicacao_dois_niveis = dado

    @property
    def armazenamento_local_arquivos_temporarios(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            return b.armazenamento_local_arquivos_temporarios
        return None

    @armazenamento_local_arquivos_temporarios.setter
    def armazenamento_local_arquivos_temporarios(self, dado: int):
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            b.armazenamento_local_arquivos_temporarios = dado

    @property
    def alocacao_memoria_ena(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            return b.alocacao_memoria_ena
        return None

    @alocacao_memoria_ena.setter
    def alocacao_memoria_ena(self, dado: int):
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            b.alocacao_memoria_ena = dado

    @property
    def alocacao_memoria_cortes(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            return b.alocacao_memoria_cortes
        return None

    @alocacao_memoria_cortes.setter
    def alocacao_memoria_cortes(self, dado: int):
        b = self.data.get_sections_of_type(BlocoGerenciamentoPLs)
        if isinstance(b, BlocoGerenciamentoPLs):
            b.alocacao_memoria_cortes = dado

    @property
    def sar(self) -> Optional[int]:
        """
        Configuração da linha número 60 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoSAR)
        if isinstance(b, BlocoSAR):
            return b.valor
        return None

    @sar.setter
    def sar(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSAR)
        if isinstance(b, BlocoSAR):
            b.valor = dado

    @property
    def cvar(self) -> Optional[int]:
        """
        Configuração da linha número 61 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoCVAR)
        if isinstance(b, BlocoCVAR):
            return b.valor
        return None

    @cvar.setter
    def cvar(self, dado: int):
        b = self.data.get_sections_of_type(BlocoCVAR)
        if isinstance(b, BlocoCVAR):
            b.valor = dado

    @property
    def considera_zsup_min_convergencia(self) -> Optional[int]:
        """
        Configuração da linha número 62 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoZSUPMinConvergencia)
        if isinstance(b, BlocoZSUPMinConvergencia):
            return b.valor
        return None

    @considera_zsup_min_convergencia.setter
    def considera_zsup_min_convergencia(self, dado: int):
        b = self.data.get_sections_of_type(BlocoZSUPMinConvergencia)
        if isinstance(b, BlocoZSUPMinConvergencia):
            b.valor = dado

    @property
    def desconsidera_vazao_minima(self) -> Optional[int]:
        """
        Configuração da linha número 63 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoDesconsideraVazaoMinima)
        if isinstance(b, BlocoDesconsideraVazaoMinima):
            return b.valor
        return None

    @desconsidera_vazao_minima.setter
    def desconsidera_vazao_minima(self, dado: int):
        b = self.data.get_sections_of_type(BlocoDesconsideraVazaoMinima)
        if isinstance(b, BlocoDesconsideraVazaoMinima):
            b.valor = dado

    @property
    def restricoes_eletricas(self) -> Optional[int]:
        """
        Configuração da linha número 64 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoRestricoesEletricas)
        if isinstance(b, BlocoRestricoesEletricas):
            return b.valor
        return None

    @restricoes_eletricas.setter
    def restricoes_eletricas(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRestricoesEletricas)
        if isinstance(b, BlocoRestricoesEletricas):
            b.valor = dado

    @property
    def selecao_de_cortes_backward(self) -> Optional[int]:
        """
        Configuração do primeiro campo da linha número 65 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoSelecaoCortes)
        if isinstance(b, BlocoSelecaoCortes):
            return b.considera_na_backward
        return None

    @selecao_de_cortes_backward.setter
    def selecao_de_cortes_backward(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSelecaoCortes)
        if isinstance(b, BlocoSelecaoCortes):
            b.considera_na_backward = dado

    @property
    def selecao_de_cortes_forward(self) -> Optional[int]:
        """
        Configuração do segundo campo da linha número 65 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoSelecaoCortes)
        if isinstance(b, BlocoSelecaoCortes):
            return b.considera_na_forward
        return None

    @selecao_de_cortes_forward.setter
    def selecao_de_cortes_forward(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSelecaoCortes)
        if isinstance(b, BlocoSelecaoCortes):
            b.considera_na_forward = dado

    @property
    def janela_de_cortes(self) -> Optional[int]:
        """
        Configuração da linha número 66 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoJanelaCortes)
        if isinstance(b, BlocoJanelaCortes):
            return b.valor
        return None

    @janela_de_cortes.setter
    def janela_de_cortes(self, dado: int):
        b = self.data.get_sections_of_type(BlocoJanelaCortes)
        if isinstance(b, BlocoJanelaCortes):
            b.valor = dado

    @property
    def considera_reamostragem_cenarios(self) -> Optional[int]:
        """
        Configuração da linha número 67 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoReamostragemCenarios)
        if isinstance(b, BlocoReamostragemCenarios):
            return b.considera_reamostragem_cenarios
        return None

    @considera_reamostragem_cenarios.setter
    def considera_reamostragem_cenarios(self, dado: int):
        b = self.data.get_sections_of_type(BlocoReamostragemCenarios)
        if isinstance(b, BlocoReamostragemCenarios):
            b.considera_reamostragem_cenarios = dado

    @property
    def tipo_reamostragem_cenarios(self) -> Optional[int]:
        """
        Configuração da linha número 67 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoReamostragemCenarios)
        if isinstance(b, BlocoReamostragemCenarios):
            return b.tipo_reamostragem_cenarios
        return None

    @tipo_reamostragem_cenarios.setter
    def tipo_reamostragem_cenarios(self, dado: int):
        b = self.data.get_sections_of_type(BlocoReamostragemCenarios)
        if isinstance(b, BlocoReamostragemCenarios):
            b.tipo_reamostragem_cenarios = dado

    @property
    def passo_reamostragem_cenarios(self) -> Optional[int]:
        """
        Configuração da linha número 67 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoReamostragemCenarios)
        if isinstance(b, BlocoReamostragemCenarios):
            return b.passo_reamostragem_cenarios
        return None

    @passo_reamostragem_cenarios.setter
    def passo_reamostragem_cenarios(self, dado: int):
        b = self.data.get_sections_of_type(BlocoReamostragemCenarios)
        if isinstance(b, BlocoReamostragemCenarios):
            b.passo_reamostragem_cenarios = dado

    @property
    def converge_no_zero(self) -> Optional[int]:
        """
        Configuração da linha número 68 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoConvergeNoZero)
        if isinstance(b, BlocoConvergeNoZero):
            return b.valor
        return None

    @converge_no_zero.setter
    def converge_no_zero(self, dado: int):
        b = self.data.get_sections_of_type(BlocoConvergeNoZero)
        if isinstance(b, BlocoConvergeNoZero):
            b.valor = dado

    @property
    def consulta_fcf(self) -> Optional[int]:
        """
        Configuração da linha número 69 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoConsultaFCF)
        if isinstance(b, BlocoConsultaFCF):
            return b.valor
        return None

    @consulta_fcf.setter
    def consulta_fcf(self, dado: int):
        b = self.data.get_sections_of_type(BlocoConsultaFCF)
        if isinstance(b, BlocoConsultaFCF):
            b.valor = dado

    @property
    def impressao_ena(self) -> Optional[int]:
        """
        Configuração da linha número 70 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImpressaoENA)
        if isinstance(b, BlocoImpressaoENA):
            return b.valor
        return None

    @impressao_ena.setter
    def impressao_ena(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImpressaoENA)
        if isinstance(b, BlocoImpressaoENA):
            b.valor = dado

    @property
    def impressao_cortes_ativos_sim_final(self) -> Optional[int]:
        """
        Configuração da linha número 71 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoImpressaoCortesAtivosSimFinal)
        if isinstance(b, BlocoImpressaoCortesAtivosSimFinal):
            return b.valor
        return None

    @impressao_cortes_ativos_sim_final.setter
    def impressao_cortes_ativos_sim_final(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImpressaoCortesAtivosSimFinal)
        if isinstance(b, BlocoImpressaoCortesAtivosSimFinal):
            b.valor = dado

    @property
    def representacao_agregacao(self) -> Optional[int]:
        """
        Configuração da linha número 72 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoRepresentacaoAgregacao)
        if isinstance(b, BlocoRepresentacaoAgregacao):
            return b.valor
        return None

    @representacao_agregacao.setter
    def representacao_agregacao(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRepresentacaoAgregacao)
        if isinstance(b, BlocoRepresentacaoAgregacao):
            b.valor = dado

    @property
    def matriz_correlacao_espacial(self) -> Optional[int]:
        """
        Configuração da linha número 73 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoMatrizCorrelacaoEspacial)
        if isinstance(b, BlocoMatrizCorrelacaoEspacial):
            return b.valor
        return None

    @matriz_correlacao_espacial.setter
    def matriz_correlacao_espacial(self, dado: int):
        b = self.data.get_sections_of_type(BlocoMatrizCorrelacaoEspacial)
        if isinstance(b, BlocoMatrizCorrelacaoEspacial):
            b.valor = dado

    @property
    def desconsidera_convergencia_estatistica(self) -> Optional[int]:
        """
        Configuração da linha número 74 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoDesconsideraConvEstatistica)
        if isinstance(b, BlocoDesconsideraConvEstatistica):
            return b.valor
        return None

    @desconsidera_convergencia_estatistica.setter
    def desconsidera_convergencia_estatistica(self, dado: int):
        b = self.data.get_sections_of_type(BlocoDesconsideraConvEstatistica)
        if isinstance(b, BlocoDesconsideraConvEstatistica):
            b.valor = dado

    @property
    def momento_reamostragem(self) -> Optional[int]:
        """
        Configuração da linha número 75 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoMomentoReamostragem)
        if isinstance(b, BlocoMomentoReamostragem):
            return b.valor
        return None

    @momento_reamostragem.setter
    def momento_reamostragem(self, dado: int):
        b = self.data.get_sections_of_type(BlocoMomentoReamostragem)
        if isinstance(b, BlocoMomentoReamostragem):
            b.valor = dado

    @property
    def mantem_arquivos_energias(self) -> Optional[int]:
        """
        Configuração da linha número 76 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoMantemArquivosEnergias)
        if isinstance(b, BlocoMantemArquivosEnergias):
            return b.valor
        return None

    @mantem_arquivos_energias.setter
    def mantem_arquivos_energias(self, dado: int):
        b = self.data.get_sections_of_type(BlocoMantemArquivosEnergias)
        if isinstance(b, BlocoMantemArquivosEnergias):
            b.valor = dado

    @property
    def inicio_teste_convergencia(self) -> Optional[int]:
        """
        Configuração da linha número 77 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoInicioTesteConvergencia)
        if isinstance(b, BlocoInicioTesteConvergencia):
            return b.valor
        return None

    @inicio_teste_convergencia.setter
    def inicio_teste_convergencia(self, dado: int):
        b = self.data.get_sections_of_type(BlocoInicioTesteConvergencia)
        if isinstance(b, BlocoInicioTesteConvergencia):
            b.valor = dado

    @property
    def sazonaliza_vmint(self) -> Optional[int]:
        """
        Configuração da linha número 78 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoSazonalizarVminT)
        if isinstance(b, BlocoSazonalizarVminT):
            return b.valor
        return None

    @sazonaliza_vmint.setter
    def sazonaliza_vmint(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSazonalizarVminT)
        if isinstance(b, BlocoSazonalizarVminT):
            b.valor = dado

    @property
    def sazonaliza_vmaxt(self) -> Optional[int]:
        """
        Configuração da linha número 79 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoSazonalizarVmaxT)
        if isinstance(b, BlocoSazonalizarVmaxT):
            return b.valor
        return None

    @sazonaliza_vmaxt.setter
    def sazonaliza_vmaxt(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSazonalizarVmaxT)
        if isinstance(b, BlocoSazonalizarVmaxT):
            b.valor = dado

    @property
    def sazonaliza_vminp(self) -> Optional[int]:
        """
        Configuração da linha número 80 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoSazonalizarVminP)
        if isinstance(b, BlocoSazonalizarVminP):
            return b.valor
        return None

    @sazonaliza_vminp.setter
    def sazonaliza_vminp(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSazonalizarVminP)
        if isinstance(b, BlocoSazonalizarVminP):
            b.valor = dado

    @property
    def sazonaliza_cfuga_cmont(self) -> Optional[int]:
        """
        Configuração da linha número 81 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoSazonalizarCfugaCmont)
        if isinstance(b, BlocoSazonalizarCfugaCmont):
            return b.valor
        return None

    @sazonaliza_cfuga_cmont.setter
    def sazonaliza_cfuga_cmont(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSazonalizarCfugaCmont)
        if isinstance(b, BlocoSazonalizarCfugaCmont):
            b.valor = dado

    @property
    def restricoes_emissao_gee(self) -> Optional[int]:
        """
        Configuração da linha número 82 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoRestricoesEmissaoGEE)
        if isinstance(b, BlocoRestricoesEmissaoGEE):
            return b.valor
        return None

    @restricoes_emissao_gee.setter
    def restricoes_emissao_gee(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRestricoesEmissaoGEE)
        if isinstance(b, BlocoRestricoesEmissaoGEE):
            b.valor = dado

    @property
    def consideracao_media_anual_afluencias(self) -> Optional[int]:
        """
        Configuração da linha número 83 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoAfluenciaAnualPARp)
        if isinstance(b, BlocoAfluenciaAnualPARp):
            return b.consideracao_media_anual_afluencias
        return None

    @consideracao_media_anual_afluencias.setter
    def consideracao_media_anual_afluencias(self, dado: int):
        b = self.data.get_sections_of_type(BlocoAfluenciaAnualPARp)
        if isinstance(b, BlocoAfluenciaAnualPARp):
            b.consideracao_media_anual_afluencias = dado

    @property
    def reducao_automatica_ordem(self) -> Optional[int]:
        """
        Configuração da linha número 83 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoAfluenciaAnualPARp)
        if isinstance(b, BlocoAfluenciaAnualPARp):
            return b.reducao_automatica_ordem
        return None

    @reducao_automatica_ordem.setter
    def reducao_automatica_ordem(self, dado: int):
        b = self.data.get_sections_of_type(BlocoAfluenciaAnualPARp)
        if isinstance(b, BlocoAfluenciaAnualPARp):
            b.reducao_automatica_ordem = dado

    @property
    def restricoes_fornecimento_gas(self) -> Optional[int]:
        """
        Configuração da linha número 84 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoRestricoesFornecGas)
        if isinstance(b, BlocoRestricoesFornecGas):
            return b.valor
        return None

    @restricoes_fornecimento_gas.setter
    def restricoes_fornecimento_gas(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRestricoesFornecGas)
        if isinstance(b, BlocoRestricoesFornecGas):
            b.valor = dado

    @property
    def memoria_calculo_cortes(self) -> Optional[int]:
        """
        Configuração da linha número 85 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoMemCalculoCortes)
        if isinstance(b, BlocoMemCalculoCortes):
            return b.valor
        return None

    @memoria_calculo_cortes.setter
    def memoria_calculo_cortes(self, dado: int):
        b = self.data.get_sections_of_type(BlocoMemCalculoCortes)
        if isinstance(b, BlocoMemCalculoCortes):
            b.valor = dado

    @property
    def considera_geracao_eolica(self) -> Optional[int]:
        """
        Configuração da linha número 86 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoGeracaoEolica)
        if isinstance(b, BlocoGeracaoEolica):
            return b.considera
        return None

    @considera_geracao_eolica.setter
    def considera_geracao_eolica(self, dado: int):
        b = self.data.get_sections_of_type(BlocoGeracaoEolica)
        if isinstance(b, BlocoGeracaoEolica):
            b.considera = dado

    @property
    def penalidade_corte_geracao_eolica(self) -> Optional[float]:
        """
        Configuração da linha número 86 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.data.get_sections_of_type(BlocoGeracaoEolica)
        if isinstance(b, BlocoGeracaoEolica):
            return b.penalidade
        return None

    @penalidade_corte_geracao_eolica.setter
    def penalidade_corte_geracao_eolica(self, dado: float):
        b = self.data.get_sections_of_type(BlocoGeracaoEolica)
        if isinstance(b, BlocoGeracaoEolica):
            b.penalidade = dado

    # TODO - restaurar em versões futuras
    # @property
    # def compensacao_correlacao_cruzada(self) -> Optional[int]:
    #     """
    #     Configuração da linha número 87 do arquivo `dger.dat`.

    #     :return: O valor do campo
    #     :rtype: int
    #     """
    #     b = self.data.get_sections_of_type(BlocoCompensacaoCorrelacaoCruzada)
    #     if isinstance(b, BlocoCompensacaoCorrelacaoCruzada):
    #         return b.valor
    #     return None

    # @compensacao_correlacao_cruzada.setter
    # def compensacao_correlacao_cruzada(self, dado: int):
    #     b = self.data.get_sections_of_type(BlocoCompensacaoCorrelacaoCruzada)
    #     if isinstance(b, BlocoCompensacaoCorrelacaoCruzada):
    #         b.valor = dado

    @property
    def restricao_turbinamento(self) -> Optional[int]:
        """
        Configuração da linha número 87 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(
            BlocoConsideracaoTurbinamentoMinimoMaximo
        )
        if isinstance(b, BlocoConsideracaoTurbinamentoMinimoMaximo):
            return b.valor
        return None

    @restricao_turbinamento.setter
    def restricao_turbinamento(self, dado: int):
        b = self.data.get_sections_of_type(
            BlocoConsideracaoTurbinamentoMinimoMaximo
        )
        if isinstance(b, BlocoConsideracaoTurbinamentoMinimoMaximo):
            b.valor = dado

    @property
    def restricao_defluencia(self) -> Optional[int]:
        """
        Configuração da linha número 88 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoConsideracaoDefluenciaMaxima)
        if isinstance(b, BlocoConsideracaoDefluenciaMaxima):
            return b.valor
        return None

    @restricao_defluencia.setter
    def restricao_defluencia(self, dado: int):
        b = self.data.get_sections_of_type(BlocoConsideracaoDefluenciaMaxima)
        if isinstance(b, BlocoConsideracaoDefluenciaMaxima):
            b.valor = dado

    @property
    def aproveitamento_bases_backward(self) -> Optional[int]:
        """
        Configuração da linha número 89 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoAproveitamentoBasePLsBackward)
        if isinstance(b, BlocoAproveitamentoBasePLsBackward):
            return b.valor
        return None

    @aproveitamento_bases_backward.setter
    def aproveitamento_bases_backward(self, dado: int):
        b = self.data.get_sections_of_type(BlocoAproveitamentoBasePLsBackward)
        if isinstance(b, BlocoAproveitamentoBasePLsBackward):
            b.valor = dado

    @property
    def impressao_estados_geracao_cortes(self) -> Optional[int]:
        """
        Configuração da linha número 90 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoImpressaoEstadosGeracaoCortes)
        if isinstance(b, BlocoImpressaoEstadosGeracaoCortes):
            return b.valor
        return None

    @impressao_estados_geracao_cortes.setter
    def impressao_estados_geracao_cortes(self, dado: int):
        b = self.data.get_sections_of_type(BlocoImpressaoEstadosGeracaoCortes)
        if isinstance(b, BlocoImpressaoEstadosGeracaoCortes):
            b.valor = dado

    @property
    def semente_forward(self) -> Optional[int]:
        """
        Configuração da linha número 91 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoSementeForward)
        if isinstance(b, BlocoSementeForward):
            return b.valor
        return None

    @semente_forward.setter
    def semente_forward(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSementeForward)
        if isinstance(b, BlocoSementeForward):
            b.valor = dado

    @property
    def semente_backward(self) -> Optional[int]:
        """
        Configuração da linha número 92 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoSementeBackward)
        if isinstance(b, BlocoSementeBackward):
            return b.valor
        return None

    @semente_backward.setter
    def semente_backward(self, dado: int):
        b = self.data.get_sections_of_type(BlocoSementeBackward)
        if isinstance(b, BlocoSementeBackward):
            b.valor = dado

    @property
    def restricao_lpp_turbinamento_maximo_ree(self) -> Optional[int]:
        """
        Configuração da linha número 93 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(
            BlocoRestricaoLPPTurbinamentoMaximoREE
        )
        if isinstance(b, BlocoRestricaoLPPTurbinamentoMaximoREE):
            return b.valor
        return None

    @restricao_lpp_turbinamento_maximo_ree.setter
    def restricao_lpp_turbinamento_maximo_ree(self, dado: int):
        b = self.data.get_sections_of_type(
            BlocoRestricaoLPPTurbinamentoMaximoREE
        )
        if isinstance(b, BlocoRestricaoLPPTurbinamentoMaximoREE):
            b.valor = dado

    @property
    def restricao_lpp_defluencia_maxima_ree(self) -> Optional[int]:
        """
        Configuração da linha número 94 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(
            BlocoRestricaoLPPDefluenciaMaximaREE
        )
        if isinstance(b, BlocoRestricaoLPPDefluenciaMaximaREE):
            return b.valor
        return None

    @restricao_lpp_defluencia_maxima_ree.setter
    def restricao_lpp_defluencia_maxima_ree(self, dado: int):
        b = self.data.get_sections_of_type(
            BlocoRestricaoLPPDefluenciaMaximaREE
        )
        if isinstance(b, BlocoRestricaoLPPDefluenciaMaximaREE):
            b.valor = dado

    @property
    def restricao_lpp_turbinamento_maximo_uhe(self) -> Optional[int]:
        """
        Configuração da linha número 95 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(
            BlocoRestricaoLPPTurbinamentoMaximoUHE
        )
        if isinstance(b, BlocoRestricaoLPPTurbinamentoMaximoUHE):
            return b.valor
        return None

    @restricao_lpp_turbinamento_maximo_uhe.setter
    def restricao_lpp_turbinamento_maximo_uhe(self, dado: int):
        b = self.data.get_sections_of_type(
            BlocoRestricaoLPPTurbinamentoMaximoUHE
        )
        if isinstance(b, BlocoRestricaoLPPTurbinamentoMaximoUHE):
            b.valor = dado

    @property
    def restricao_lpp_defluencia_maxima_uhe(self) -> Optional[int]:
        """
        Configuração da linha número 96 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(
            BlocoRestricaoLPPDefluenciaMaximaUHE
        )
        if isinstance(b, BlocoRestricaoLPPDefluenciaMaximaUHE):
            return b.valor
        return None

    @restricao_lpp_defluencia_maxima_uhe.setter
    def restricao_lpp_defluencia_maxima_uhe(self, dado: int):
        b = self.data.get_sections_of_type(
            BlocoRestricaoLPPDefluenciaMaximaUHE
        )
        if isinstance(b, BlocoRestricaoLPPDefluenciaMaximaUHE):
            b.valor = dado

    @property
    def restricoes_eletricas_especiais(self) -> Optional[int]:
        """
        Configuração da linha número 97 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoRestricoesEletricasEspeciais)
        if isinstance(b, BlocoRestricoesEletricasEspeciais):
            return b.valor
        return None

    @restricoes_eletricas_especiais.setter
    def restricoes_eletricas_especiais(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRestricoesEletricasEspeciais)
        if isinstance(b, BlocoRestricoesEletricasEspeciais):
            b.valor = dado

    @property
    def funcao_producao_uhe(self) -> Optional[int]:
        """
        Configuração da linha número 98 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoFuncaoProducaoUHE)
        if isinstance(b, BlocoFuncaoProducaoUHE):
            return b.valor
        return None

    @funcao_producao_uhe.setter
    def funcao_producao_uhe(self, dado: int):
        b = self.data.get_sections_of_type(BlocoFuncaoProducaoUHE)
        if isinstance(b, BlocoFuncaoProducaoUHE):
            b.valor = dado

    @property
    def fcf_pos_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 99 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoFCFPosEstudo)
        if isinstance(b, BlocoFCFPosEstudo):
            return b.valor
        return None

    @fcf_pos_estudo.setter
    def fcf_pos_estudo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoFCFPosEstudo)
        if isinstance(b, BlocoFCFPosEstudo):
            b.valor = dado

    @property
    def estacoes_bombeamento(self) -> Optional[int]:
        """
        Configuração da linha número 100 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoEstacoesBombeamento)
        if isinstance(b, BlocoEstacoesBombeamento):
            return b.valor
        return None

    @estacoes_bombeamento.setter
    def estacoes_bombeamento(self, dado: int):
        b = self.data.get_sections_of_type(BlocoEstacoesBombeamento)
        if isinstance(b, BlocoEstacoesBombeamento):
            b.valor = dado

    @property
    def canal_desvio(self) -> Optional[int]:
        """
        Configuração da linha número 101 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoCanalDesvio)
        if isinstance(b, BlocoCanalDesvio):
            return b.valor
        return None

    @canal_desvio.setter
    def canal_desvio(self, dado: int):
        b = self.data.get_sections_of_type(BlocoCanalDesvio)
        if isinstance(b, BlocoCanalDesvio):
            b.valor = dado

    @property
    def restricoes_rhq(self) -> Optional[int]:
        """
        Configuração da linha número 102 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoRHQ)
        if isinstance(b, BlocoRHQ):
            return b.valor
        return None

    @restricoes_rhq.setter
    def restricoes_rhq(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRHQ)
        if isinstance(b, BlocoRHQ):
            b.valor = dado

    @property
    def restricoes_rhv(self) -> Optional[int]:
        """
        Configuração da linha número 103 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoRHV)
        if isinstance(b, BlocoRHV):
            return b.valor
        return None

    @restricoes_rhv.setter
    def restricoes_rhv(self, dado: int):
        b = self.data.get_sections_of_type(BlocoRHV)
        if isinstance(b, BlocoRHV):
            b.valor = dado

    @property
    def gera_arquivo_cortes_unico(self) -> Optional[int]:
        """
        Configuração da linha número 104 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoTratamentoCortes)
        if isinstance(b, BlocoTratamentoCortes):
            return b.gera_arquivo_unico
        return None

    @gera_arquivo_cortes_unico.setter
    def gera_arquivo_cortes_unico(self, dado: int):
        b = self.data.get_sections_of_type(BlocoTratamentoCortes)
        if isinstance(b, BlocoTratamentoCortes):
            b.gera_arquivo_unico = dado

    @property
    def mantem_arquivos_cortes_por_periodo(self) -> Optional[int]:
        """
        Configuração da linha número 104 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoTratamentoCortes)
        if isinstance(b, BlocoTratamentoCortes):
            return b.mantem_arquivos_por_periodo
        return None

    @mantem_arquivos_cortes_por_periodo.setter
    def mantem_arquivos_cortes_por_periodo(self, dado: int):
        b = self.data.get_sections_of_type(BlocoTratamentoCortes)
        if isinstance(b, BlocoTratamentoCortes):
            b.mantem_arquivos_por_periodo = dado

    @property
    def periodos_manutencao_cortes(self) -> List[Optional[int]]:
        """
        Configuração da linha número 104 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: list[int | None]
        """
        b = self.data.get_sections_of_type(BlocoTratamentoCortes)
        if isinstance(b, BlocoTratamentoCortes):
            return b.periodos_cortes
        return [None]

    @periodos_manutencao_cortes.setter
    def periodos_manutencao_cortes(self, dado: List[Optional[int]]):
        b = self.data.get_sections_of_type(BlocoTratamentoCortes)
        if isinstance(b, BlocoTratamentoCortes):
            b.periodos_cortes = dado
