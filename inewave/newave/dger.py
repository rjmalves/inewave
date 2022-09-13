from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional, List


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
from inewave.newave.modelos.dger import BlocoCompensacaoCorrelacaoCruzada
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


class DGer(SectionFile):
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
        BlocoCompensacaoCorrelacaoCruzada,
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
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="dger.dat") -> "DGer":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dger.dat"):
        self.write(diretorio, nome_arquivo)

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    @property
    def nome_caso(self) -> Optional[str]:
        """
        Configuração da linha número 1 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: str
        """
        b = self.__bloco_por_tipo(BlocoNomeCaso, 0)
        if b is not None:
            return b.valor
        return None

    @nome_caso.setter
    def nome_caso(self, dado: str):
        b = self.__bloco_por_tipo(BlocoNomeCaso, 0)
        if b is not None:
            b.valor = dado

    @property
    def tipo_execucao(self) -> Optional[int]:
        """
        Configuração da linha número 2 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoTipoExecucao, 0)
        if b is not None:
            return b.valor
        return None

    @tipo_execucao.setter
    def tipo_execucao(self, dado: int):
        b = self.__bloco_por_tipo(BlocoTipoExecucao, 0)
        if b is not None:
            b.valor = dado

    @property
    def duracao_periodo(self) -> Optional[int]:
        """
        Configuração da linha número 3 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoDuracaoPeriodo, 0)
        if b is not None:
            return b.valor
        return None

    @duracao_periodo.setter
    def duracao_periodo(self, dado: int):
        b = self.__bloco_por_tipo(BlocoDuracaoPeriodo, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_anos_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 4 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumAnosEstudo, 0)
        if b is not None:
            return b.valor
        return None

    @num_anos_estudo.setter
    def num_anos_estudo(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumAnosEstudo, 0)
        if b is not None:
            b.valor = dado

    @property
    def mes_inicio_pre_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 5 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoMesInicioPreEstudo, 0)
        if b is not None:
            return b.valor
        return None

    @mes_inicio_pre_estudo.setter
    def mes_inicio_pre_estudo(self, dado: int):
        b = self.__bloco_por_tipo(BlocoMesInicioPreEstudo, 0)
        if b is not None:
            b.valor = dado

    @property
    def mes_inicio_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 6 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoMesInicioEstudo, 0)
        if b is not None:
            return b.valor
        return None

    @mes_inicio_estudo.setter
    def mes_inicio_estudo(self, dado: int):
        b = self.__bloco_por_tipo(BlocoMesInicioEstudo, 0)
        if b is not None:
            b.valor = dado

    @property
    def ano_inicio_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 7 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoAnoInicioEstudo, 0)
        if b is not None:
            return b.valor
        return None

    @ano_inicio_estudo.setter
    def ano_inicio_estudo(self, dado: int):
        b = self.__bloco_por_tipo(BlocoAnoInicioEstudo, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_anos_pre_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 8 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumAnosPreEstudo, 0)
        if b is not None:
            return b.valor
        return None

    @num_anos_pre_estudo.setter
    def num_anos_pre_estudo(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumAnosPreEstudo, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_anos_pos_estudo(self) -> Optional[int]:
        """
        Configuração da linha número 9 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumAnosPosEstudo, 0)
        if b is not None:
            return b.valor
        return None

    @num_anos_pos_estudo.setter
    def num_anos_pos_estudo(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumAnosPosEstudo, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_anos_pos_sim_final(self) -> Optional[int]:
        """
        Configuração da linha número 10 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumAnosPosEstudoSimFinal, 0)
        if b is not None:
            return b.valor
        return None

    @num_anos_pos_sim_final.setter
    def num_anos_pos_sim_final(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumAnosPosEstudoSimFinal, 0)
        if b is not None:
            b.valor = dado

    @property
    def imprime_dados(self) -> Optional[int]:
        """
        Configuração da linha número 11 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImprimeDados, 0)
        if b is not None:
            return b.valor
        return None

    @imprime_dados.setter
    def imprime_dados(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImprimeDados, 0)
        if b is not None:
            b.valor = dado

    @property
    def imprime_mercados(self) -> Optional[int]:
        """
        Configuração da linha número 12 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImprimeMercados, 0)
        if b is not None:
            return b.valor
        return None

    @imprime_mercados.setter
    def imprime_mercados(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImprimeMercados, 0)
        if b is not None:
            b.valor = dado

    @property
    def imprime_energias(self) -> Optional[int]:
        """
        Configuração da linha número 13 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImprimeEnergias, 0)
        if b is not None:
            return b.valor
        return None

    @imprime_energias.setter
    def imprime_energias(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImprimeEnergias, 0)
        if b is not None:
            b.valor = dado

    @property
    def imprime_modelo_estocastico(self) -> Optional[int]:
        """
        Configuração da linha número 14 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImprimeModeloEstocastico, 0)
        if b is not None:
            return b.valor
        return None

    @imprime_modelo_estocastico.setter
    def imprime_modelo_estocastico(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImprimeModeloEstocastico, 0)
        if b is not None:
            b.valor = dado

    @property
    def imprime_subsistema(self) -> Optional[int]:
        """
        Configuração da linha número 15 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImprimeSubsistema, 0)
        if b is not None:
            return b.valor
        return None

    @imprime_subsistema.setter
    def imprime_subsistema(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImprimeSubsistema, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_max_iteracoes(self) -> Optional[int]:
        """
        Configuração da linha número 16 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumMaxIteracoes, 0)
        if b is not None:
            return b.valor
        return None

    @num_max_iteracoes.setter
    def num_max_iteracoes(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumMaxIteracoes, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_forwards(self) -> Optional[int]:
        """
        Configuração da linha número 17 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumForwards, 0)
        if b is not None:
            return b.valor
        return None

    @num_forwards.setter
    def num_forwards(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumForwards, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_aberturas(self) -> Optional[int]:
        """
        Configuração da linha número 18 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumAberturas, 0)
        if b is not None:
            return b.valor
        return None

    @num_aberturas.setter
    def num_aberturas(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumAberturas, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_series_sinteticas(self) -> Optional[int]:
        """
        Configuração da linha número 19 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumSeriesSinteticas, 0)
        if b is not None:
            return b.valor
        return None

    @num_series_sinteticas.setter
    def num_series_sinteticas(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumSeriesSinteticas, 0)
        if b is not None:
            b.valor = dado

    @property
    def ordem_maxima_parp(self) -> Optional[int]:
        """
        Configuração da linha número 20 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoOrdemMaximaPARp, 0)
        if b is not None:
            return b.valor
        return None

    @ordem_maxima_parp.setter
    def ordem_maxima_parp(self, dado: int):
        b = self.__bloco_por_tipo(BlocoOrdemMaximaPARp, 0)
        if b is not None:
            b.valor = dado

    @property
    def ano_inicial_historico(self) -> Optional[int]:
        """
        Configuração da linha número 21 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoAnoInicialHistorico, 0)
        if b is not None:
            return b.ano_inicial
        return None

    @ano_inicial_historico.setter
    def ano_inicial_historico(self, dado: int):
        b = self.__bloco_por_tipo(BlocoAnoInicialHistorico, 0)
        if b is not None:
            b.ano_inicial = dado

    @property
    def tamanho_registro_arquivo_historico(self) -> Optional[int]:
        """
        Configuração da linha número 21 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoAnoInicialHistorico, 0)
        if b is not None:
            return b.tamanho_registro_arquivo
        return None

    @tamanho_registro_arquivo_historico.setter
    def tamanho_registro_arquivo_historico(self, dado: int):
        b = self.__bloco_por_tipo(BlocoAnoInicialHistorico, 0)
        if b is not None:
            b.tamanho_registro_arquivo = dado

    @property
    def calcula_volume_inicial(self) -> Optional[int]:
        """
        Configuração da linha número 22 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoCalculaVolInicial, 0)
        if b is not None:
            return b.valor
        return None

    @calcula_volume_inicial.setter
    def calcula_volume_inicial(self, dado: int):
        b = self.__bloco_por_tipo(BlocoCalculaVolInicial, 0)
        if b is not None:
            b.valor = dado

    @property
    def volume_inicial_subsistema(self) -> List[Optional[float]]:
        """
        Configuração das linhas número 23 e 24 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoVolInicialSubsistema, 0)
        if b is not None:
            return b.valores
        return []

    @volume_inicial_subsistema.setter
    def volume_inicial_subsistema(self, dado: List[Optional[float]]):
        b = self.__bloco_por_tipo(BlocoVolInicialSubsistema, 0)
        if b is not None:
            b.valores = dado

    @property
    def tolerancia(self) -> Optional[float]:
        """
        Configuração da linha número 25 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoTolerancia, 0)
        if b is not None:
            return b.valor
        return None

    @tolerancia.setter
    def tolerancia(self, dado: float):
        b = self.__bloco_por_tipo(BlocoTolerancia, 0)
        if b is not None:
            b.valor = dado

    @property
    def taxa_de_desconto(self) -> Optional[float]:
        """
        Configuração da linha número 26 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoTaxaDesconto, 0)
        if b is not None:
            return b.valor
        return None

    @taxa_de_desconto.setter
    def taxa_de_desconto(self, dado: float):
        b = self.__bloco_por_tipo(BlocoTaxaDesconto, 0)
        if b is not None:
            b.valor = dado

    @property
    def tipo_simulacao_final(self) -> Optional[int]:
        """
        Configuração do primeiro campo da linha número 27
        do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoTipoSimFinal, 0)
        if b is not None:
            return b.valor[0]
        return None

    @tipo_simulacao_final.setter
    def tipo_simulacao_final(self, dado: int):
        b = self.__bloco_por_tipo(BlocoTipoSimFinal, 0)
        if b is not None:
            b.valor = [dado] + [b.valor[1]]

    @property
    def agregacao_simulacao_final(self) -> Optional[int]:
        """
        Configuração do segundo campo da linha número 27
        do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoTipoSimFinal, 0)
        if b is not None:
            return b.valor[1]
        return None

    @agregacao_simulacao_final.setter
    def agregacao_simulacao_final(self, dado: int):
        b = self.__bloco_por_tipo(BlocoTipoSimFinal, 0)
        if b is not None:
            b.valor = [b.valor[0]] + [dado]

    @property
    def impressao_operacao(self) -> Optional[int]:
        """
        Configuração da linha número 28 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImpressaoOperacao, 0)
        if b is not None:
            return b.valor
        return None

    @impressao_operacao.setter
    def impressao_operacao(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImpressaoOperacao, 0)
        if b is not None:
            b.valor = dado

    @property
    def impressao_convergencia(self) -> Optional[int]:
        """
        Configuração da linha número 29 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImpressaoConvergencia, 0)
        if b is not None:
            return b.valor
        return None

    @impressao_convergencia.setter
    def impressao_convergencia(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImpressaoConvergencia, 0)
        if b is not None:
            b.valor = dado

    @property
    def intervalo_para_gravar(self) -> Optional[int]:
        """
        Configuração da linha número 30 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoIntervaloGravar, 0)
        if b is not None:
            return b.valor
        return None

    @intervalo_para_gravar.setter
    def intervalo_para_gravar(self, dado: int):
        b = self.__bloco_por_tipo(BlocoIntervaloGravar, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_minimo_iteracoes(self) -> Optional[int]:
        """
        Configuração da linha número 31 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoMinIteracoes, 0)
        if b is not None:
            return b.valor
        return None

    @num_minimo_iteracoes.setter
    def num_minimo_iteracoes(self, dado: int):
        b = self.__bloco_por_tipo(BlocoMinIteracoes, 0)
        if b is not None:
            b.valor = dado

    @property
    def racionamento_preventivo(self) -> Optional[int]:
        """
        Configuração da linha número 32 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoRacionamentoPreventivo, 0)
        if b is not None:
            return b.valor
        return None

    @racionamento_preventivo.setter
    def racionamento_preventivo(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRacionamentoPreventivo, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_anos_manutencao_utes(self) -> Optional[int]:
        """
        Configuração da linha número 33 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoNumAnosManutUTE, 0)
        if b is not None:
            return b.valor
        return None

    @num_anos_manutencao_utes.setter
    def num_anos_manutencao_utes(self, dado: int):
        b = self.__bloco_por_tipo(BlocoNumAnosManutUTE, 0)
        if b is not None:
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
        b = self.__bloco_por_tipo(BlocoTendenciaHidrologica, 0)
        if b is not None:
            return b.considera_tendencia_hidrologica_calculo_politica
        return None

    @considera_tendencia_hidrologica_calculo_politica.setter
    def considera_tendencia_hidrologica_calculo_politica(self, dado: int):
        b = self.__bloco_por_tipo(BlocoTendenciaHidrologica, 0)
        if b is not None:
            b.considera_tendencia_hidrologica_calculo_politica = dado

    @property
    def considera_tendencia_hidrologica_sim_final(self) -> Optional[int]:
        """
        Configuração da linha número 34 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoTendenciaHidrologica, 0)
        if b is not None:
            return b.considera_tendencia_hidrologica_sim_final
        return None

    @considera_tendencia_hidrologica_sim_final.setter
    def considera_tendencia_hidrologica_sim_final(self, dado: int):
        b = self.__bloco_por_tipo(BlocoTendenciaHidrologica, 0)
        if b is not None:
            b.considera_tendencia_hidrologica_sim_final = dado

    @property
    def restricao_itaipu(self) -> Optional[int]:
        """
        Configuração da linha número 35 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoRestricaoItaipu, 0)
        if b is not None:
            return b.valor
        return None

    @restricao_itaipu.setter
    def restricao_itaipu(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRestricaoItaipu, 0)
        if b is not None:
            b.valor = dado

    @property
    def bid(self) -> Optional[int]:
        """
        Configuração da linha número 36 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoBid, 0)
        if b is not None:
            return b.valor
        return None

    @bid.setter
    def bid(self, dado: int):
        b = self.__bloco_por_tipo(BlocoBid, 0)
        if b is not None:
            b.valor = dado

    @property
    def perdas_rede_transmissao(self) -> Optional[int]:
        """
        Configuração da linha número 37 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoPerdasTransmissao, 0)
        if b is not None:
            return b.valor
        return None

    @perdas_rede_transmissao.setter
    def perdas_rede_transmissao(self, dado: int):
        b = self.__bloco_por_tipo(BlocoPerdasTransmissao, 0)
        if b is not None:
            b.valor = dado

    @property
    def el_nino(self) -> Optional[int]:
        """
        Configuração da linha número 38 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoElNino, 0)
        if b is not None:
            return b.valor
        return None

    @el_nino.setter
    def el_nino(self, dado: int):
        b = self.__bloco_por_tipo(BlocoElNino, 0)
        if b is not None:
            b.valor = dado

    @property
    def enso(self) -> Optional[int]:
        """
        Configuração da linha número 39 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoEnso, 0)
        if b is not None:
            return b.valor
        return None

    @enso.setter
    def enso(self, dado: int):
        b = self.__bloco_por_tipo(BlocoEnso, 0)
        if b is not None:
            b.valor = dado

    @property
    def duracao_por_patamar(self) -> Optional[int]:
        """
        Configuração da linha número 40 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoDuracaoPorPatamar, 0)
        if b is not None:
            return b.valor
        return None

    @duracao_por_patamar.setter
    def duracao_por_patamar(self, dado: int):
        b = self.__bloco_por_tipo(BlocoDuracaoPorPatamar, 0)
        if b is not None:
            b.valor = dado

    @property
    def outros_usos_da_agua(self) -> Optional[int]:
        """
        Configuração da linha número 41 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoOutrosUsosAgua, 0)
        if b is not None:
            return b.valor
        return None

    @outros_usos_da_agua.setter
    def outros_usos_da_agua(self, dado: int):
        b = self.__bloco_por_tipo(BlocoOutrosUsosAgua, 0)
        if b is not None:
            b.valor = dado

    @property
    def correcao_desvio(self) -> Optional[int]:
        """
        Configuração da linha número 42 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoCorrecaoDesvio, 0)
        if b is not None:
            return b.valor
        return None

    @correcao_desvio.setter
    def correcao_desvio(self, dado: int):
        b = self.__bloco_por_tipo(BlocoCorrecaoDesvio, 0)
        if b is not None:
            b.valor = dado

    @property
    def curva_aversao(self) -> Optional[int]:
        """
        Configuração da linha número 43 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoCurvaAversao, 0)
        if b is not None:
            return b.valor
        return None

    @curva_aversao.setter
    def curva_aversao(self, dado: int):
        b = self.__bloco_por_tipo(BlocoCurvaAversao, 0)
        if b is not None:
            b.valor = dado

    @property
    def tipo_geracao_enas(self) -> Optional[int]:
        """
        Configuração da linha número 44 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoTipoGeracaoENA, 0)
        if b is not None:
            return b.valor
        return None

    @tipo_geracao_enas.setter
    def tipo_geracao_enas(self, dado: int):
        b = self.__bloco_por_tipo(BlocoTipoGeracaoENA, 0)
        if b is not None:
            b.valor = dado

    @property
    def primeira_profundidade_risco_deficit(self) -> Optional[float]:
        """
        Configuração da linha número 45 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: float
        """
        b = self.__bloco_por_tipo(BlocoRiscoDeficit, 0)
        if b is not None:
            return b.primeira_profundidade_risco_deficit
        return None

    @primeira_profundidade_risco_deficit.setter
    def primeira_profundidade_risco_deficit(self, dado: float):
        b = self.__bloco_por_tipo(BlocoRiscoDeficit, 0)
        if b is not None:
            b.primeira_profundidade_risco_deficit = dado

    @property
    def segunda_profundidade_risco_deficit(self) -> Optional[float]:
        """
        Configuração da linha número 45 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: float
        """
        b = self.__bloco_por_tipo(BlocoRiscoDeficit, 0)
        if b is not None:
            return b.segunda_profundidade_risco_deficit
        return None

    @segunda_profundidade_risco_deficit.setter
    def segunda_profundidade_risco_deficit(self, dado: float):
        b = self.__bloco_por_tipo(BlocoRiscoDeficit, 0)
        if b is not None:
            b.segunda_profundidade_risco_deficit = dado

    @property
    def iteracao_para_simulacao_final(self) -> Optional[int]:
        """
        Configuração da linha número 46 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoIteracaoParaSimFinal, 0)
        if b is not None:
            return b.valor
        return None

    @iteracao_para_simulacao_final.setter
    def iteracao_para_simulacao_final(self, dado: int):
        b = self.__bloco_por_tipo(BlocoIteracaoParaSimFinal, 0)
        if b is not None:
            b.valor = dado

    @property
    def agrupamento_livre(self) -> Optional[int]:
        """
        Configuração da linha número 47 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoAgrupamentoLivre, 0)
        if b is not None:
            return b.valor
        return None

    @agrupamento_livre.setter
    def agrupamento_livre(self, dado: int):
        b = self.__bloco_por_tipo(BlocoAgrupamentoLivre, 0)
        if b is not None:
            b.valor = dado

    @property
    def equalizacao_penal_intercambio(self) -> Optional[int]:
        """
        Configuração da linha número 48 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoEqualizacaoPenalInt, 0)
        if b is not None:
            return b.valor
        return None

    @equalizacao_penal_intercambio.setter
    def equalizacao_penal_intercambio(self, dado: int):
        b = self.__bloco_por_tipo(BlocoEqualizacaoPenalInt, 0)
        if b is not None:
            b.valor = dado

    @property
    def representacao_submotorizacao(self) -> Optional[int]:
        """
        Configuração da linha número 49 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoRepresentacaoSubmot, 0)
        if b is not None:
            return b.valor
        return None

    @representacao_submotorizacao.setter
    def representacao_submotorizacao(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRepresentacaoSubmot, 0)
        if b is not None:
            b.valor = dado

    @property
    def ordenacao_automatica(self) -> Optional[int]:
        """
        Configuração da linha número 50 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoOrdenacaoAutomatica, 0)
        if b is not None:
            return b.valor
        return None

    @ordenacao_automatica.setter
    def ordenacao_automatica(self, dado: int):
        b = self.__bloco_por_tipo(BlocoOrdenacaoAutomatica, 0)
        if b is not None:
            b.valor = dado

    @property
    def considera_carga_adicional(self) -> Optional[int]:
        """
        Configuração da linha número 51 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoConsideraCargaAdicional, 0)
        if b is not None:
            return b.valor
        return None

    @considera_carga_adicional.setter
    def considera_carga_adicional(self, dado: int):
        b = self.__bloco_por_tipo(BlocoConsideraCargaAdicional, 0)
        if b is not None:
            b.valor = dado

    @property
    def delta_zsup(self) -> Optional[float]:
        """
        Configuração da linha número 52 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: float
        """
        b = self.__bloco_por_tipo(BlocoDeltaZSUP, 0)
        if b is not None:
            return b.valor
        return None

    @delta_zsup.setter
    def delta_zsup(self, dado: float):
        b = self.__bloco_por_tipo(BlocoDeltaZSUP, 0)
        if b is not None:
            b.valor = dado

    @property
    def delta_zinf(self) -> Optional[float]:
        """
        Configuração da linha número 53 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: float
        """
        b = self.__bloco_por_tipo(BlocoDeltaZINF, 0)
        if b is not None:
            return b.valor
        return None

    @delta_zinf.setter
    def delta_zinf(self, dado: float):
        b = self.__bloco_por_tipo(BlocoDeltaZINF, 0)
        if b is not None:
            b.valor = dado

    @property
    def deltas_consecutivos(self) -> Optional[int]:
        """
        Configuração da linha número 54 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoDeltasConsecutivos, 0)
        if b is not None:
            return b.valor
        return None

    @deltas_consecutivos.setter
    def deltas_consecutivos(self, dado: int):
        b = self.__bloco_por_tipo(BlocoDeltasConsecutivos, 0)
        if b is not None:
            b.valor = dado

    @property
    def despacho_antecipado_gnl(self) -> Optional[int]:
        """
        Configuração da linha número 55 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoDespachoAntecipadoGNL, 0)
        if b is not None:
            return b.valor
        return None

    @despacho_antecipado_gnl.setter
    def despacho_antecipado_gnl(self, dado: int):
        b = self.__bloco_por_tipo(BlocoDespachoAntecipadoGNL, 0)
        if b is not None:
            b.valor = dado

    @property
    def modif_automatica_adterm(self) -> Optional[int]:
        """
        Configuração da linha número 56 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoModifAutomaticaAdTerm, 0)
        if b is not None:
            return b.valor
        return None

    @modif_automatica_adterm.setter
    def modif_automatica_adterm(self, dado: int):
        b = self.__bloco_por_tipo(BlocoModifAutomaticaAdTerm, 0)
        if b is not None:
            b.valor = dado

    @property
    def considera_ghmin(self) -> Optional[int]:
        """
        Configuração da linha número 57 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoGeracaoHidraulicaMin, 0)
        if b is not None:
            return b.valor
        return None

    @considera_ghmin.setter
    def considera_ghmin(self, dado: int):
        b = self.__bloco_por_tipo(BlocoGeracaoHidraulicaMin, 0)
        if b is not None:
            b.valor = dado

    @property
    def simulacao_final_com_data(self) -> Optional[int]:
        """
        Configuração da linha número 58 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoSimFinalComData, 0)
        if b is not None:
            return b.valor
        return None

    @simulacao_final_com_data.setter
    def simulacao_final_com_data(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSimFinalComData, 0)
        if b is not None:
            b.valor = dado

    @property
    def utiliza_gerenciamento_pls(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            return b.utiliza_gerenciamento_pls
        return None

    @utiliza_gerenciamento_pls.setter
    def utiliza_gerenciamento_pls(self, dado: int):
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            b.utiliza_gerenciamento_pls = dado

    @property
    def comunicacao_dois_niveis(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            return b.comunicacao_dois_niveis
        return None

    @comunicacao_dois_niveis.setter
    def comunicacao_dois_niveis(self, dado: int):
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            b.comunicacao_dois_niveis = dado

    @property
    def armazenamento_local_arquivos_temporarios(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            return b.armazenamento_local_arquivos_temporarios
        return None

    @armazenamento_local_arquivos_temporarios.setter
    def armazenamento_local_arquivos_temporarios(self, dado: int):
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            b.armazenamento_local_arquivos_temporarios = dado

    @property
    def alocacao_memoria_ena(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            return b.alocacao_memoria_ena
        return None

    @alocacao_memoria_ena.setter
    def alocacao_memoria_ena(self, dado: int):
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            b.alocacao_memoria_ena = dado

    @property
    def alocacao_memoria_cortes(self) -> Optional[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            return b.alocacao_memoria_cortes
        return None

    @alocacao_memoria_cortes.setter
    def alocacao_memoria_cortes(self, dado: int):
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            b.alocacao_memoria_cortes = dado

    @property
    def sar(self) -> Optional[int]:
        """
        Configuração da linha número 60 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoSAR, 0)
        if b is not None:
            return b.valor
        return None

    @sar.setter
    def sar(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSAR, 0)
        if b is not None:
            b.valor = dado

    @property
    def cvar(self) -> Optional[int]:
        """
        Configuração da linha número 61 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoCVAR, 0)
        if b is not None:
            return b.valor
        return None

    @cvar.setter
    def cvar(self, dado: int):
        b = self.__bloco_por_tipo(BlocoCVAR, 0)
        if b is not None:
            b.valor = dado

    @property
    def considera_zsup_min_convergencia(self) -> Optional[int]:
        """
        Configuração da linha número 62 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoZSUPMinConvergencia, 0)
        if b is not None:
            return b.valor
        return None

    @considera_zsup_min_convergencia.setter
    def considera_zsup_min_convergencia(self, dado: int):
        b = self.__bloco_por_tipo(BlocoZSUPMinConvergencia, 0)
        if b is not None:
            b.valor = dado

    @property
    def desconsidera_vazao_minima(self) -> Optional[int]:
        """
        Configuração da linha número 63 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoDesconsideraVazaoMinima, 0)
        if b is not None:
            return b.valor
        return None

    @desconsidera_vazao_minima.setter
    def desconsidera_vazao_minima(self, dado: int):
        b = self.__bloco_por_tipo(BlocoDesconsideraVazaoMinima, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricoes_eletricas(self) -> Optional[int]:
        """
        Configuração da linha número 64 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoRestricoesEletricas, 0)
        if b is not None:
            return b.valor
        return None

    @restricoes_eletricas.setter
    def restricoes_eletricas(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRestricoesEletricas, 0)
        if b is not None:
            b.valor = dado

    @property
    def selecao_de_cortes_backward(self) -> Optional[int]:
        """
        Configuração do primeiro campo da linha número 65 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoSelecaoCortes, 0)
        if b is not None:
            return b.considera_na_backward
        return None

    @selecao_de_cortes_backward.setter
    def selecao_de_cortes_backward(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSelecaoCortes, 0)
        if b is not None:
            b.considera_na_backward = dado

    @property
    def selecao_de_cortes_forward(self) -> Optional[int]:
        """
        Configuração do segundo campo da linha número 65 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoSelecaoCortes, 0)
        if b is not None:
            return b.considera_na_forward
        return None

    @selecao_de_cortes_forward.setter
    def selecao_de_cortes_forward(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSelecaoCortes, 0)
        if b is not None:
            b.considera_na_forward = dado

    @property
    def janela_de_cortes(self) -> Optional[int]:
        """
        Configuração da linha número 66 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoJanelaCortes, 0)
        if b is not None:
            return b.valor
        return None

    @janela_de_cortes.setter
    def janela_de_cortes(self, dado: int):
        b = self.__bloco_por_tipo(BlocoJanelaCortes, 0)
        if b is not None:
            b.valor = dado

    @property
    def considera_reamostragem_cenarios(self) -> Optional[int]:
        """
        Configuração da linha número 67 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoReamostragemCenarios, 0)
        if b is not None:
            return b.considera_reamostragem_cenarios
        return None

    @considera_reamostragem_cenarios.setter
    def considera_reamostragem_cenarios(self, dado: int):
        b = self.__bloco_por_tipo(BlocoReamostragemCenarios, 0)
        if b is not None:
            b.considera_reamostragem_cenarios = dado

    @property
    def tipo_reamostragem_cenarios(self) -> Optional[int]:
        """
        Configuração da linha número 67 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoReamostragemCenarios, 0)
        if b is not None:
            return b.tipo_reamostragem_cenarios
        return None

    @tipo_reamostragem_cenarios.setter
    def tipo_reamostragem_cenarios(self, dado: int):
        b = self.__bloco_por_tipo(BlocoReamostragemCenarios, 0)
        if b is not None:
            b.tipo_reamostragem_cenarios = dado

    @property
    def passo_reamostragem_cenarios(self) -> Optional[int]:
        """
        Configuração da linha número 67 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoReamostragemCenarios, 0)
        if b is not None:
            return b.passo_reamostragem_cenarios
        return None

    @passo_reamostragem_cenarios.setter
    def passo_reamostragem_cenarios(self, dado: int):
        b = self.__bloco_por_tipo(BlocoReamostragemCenarios, 0)
        if b is not None:
            b.passo_reamostragem_cenarios = dado

    @property
    def converge_no_zero(self) -> Optional[int]:
        """
        Configuração da linha número 68 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoConvergeNoZero, 0)
        if b is not None:
            return b.valor
        return None

    @converge_no_zero.setter
    def converge_no_zero(self, dado: int):
        b = self.__bloco_por_tipo(BlocoConvergeNoZero, 0)
        if b is not None:
            b.valor = dado

    @property
    def consulta_fcf(self) -> Optional[int]:
        """
        Configuração da linha número 69 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoConsultaFCF, 0)
        if b is not None:
            return b.valor
        return None

    @consulta_fcf.setter
    def consulta_fcf(self, dado: int):
        b = self.__bloco_por_tipo(BlocoConsultaFCF, 0)
        if b is not None:
            b.valor = dado

    @property
    def impressao_ena(self) -> Optional[int]:
        """
        Configuração da linha número 70 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImpressaoENA, 0)
        if b is not None:
            return b.valor
        return None

    @impressao_ena.setter
    def impressao_ena(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImpressaoENA, 0)
        if b is not None:
            b.valor = dado

    @property
    def impressao_cortes_ativos_sim_final(self) -> Optional[int]:
        """
        Configuração da linha número 71 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoImpressaoCortesAtivosSimFinal, 0)
        if b is not None:
            return b.valor
        return None

    @impressao_cortes_ativos_sim_final.setter
    def impressao_cortes_ativos_sim_final(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImpressaoCortesAtivosSimFinal, 0)
        if b is not None:
            b.valor = dado

    @property
    def representacao_agregacao(self) -> Optional[int]:
        """
        Configuração da linha número 72 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoRepresentacaoAgregacao, 0)
        if b is not None:
            return b.valor
        return None

    @representacao_agregacao.setter
    def representacao_agregacao(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRepresentacaoAgregacao, 0)
        if b is not None:
            b.valor = dado

    @property
    def matriz_correlacao_espacial(self) -> Optional[int]:
        """
        Configuração da linha número 73 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoMatrizCorrelacaoEspacial, 0)
        if b is not None:
            return b.valor
        return None

    @matriz_correlacao_espacial.setter
    def matriz_correlacao_espacial(self, dado: int):
        b = self.__bloco_por_tipo(BlocoMatrizCorrelacaoEspacial, 0)
        if b is not None:
            b.valor = dado

    @property
    def desconsidera_convergencia_estatistica(self) -> Optional[int]:
        """
        Configuração da linha número 74 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoDesconsideraConvEstatistica, 0)
        if b is not None:
            return b.valor
        return None

    @desconsidera_convergencia_estatistica.setter
    def desconsidera_convergencia_estatistica(self, dado: int):
        b = self.__bloco_por_tipo(BlocoDesconsideraConvEstatistica, 0)
        if b is not None:
            b.valor = dado

    @property
    def momento_reamostragem(self) -> Optional[int]:
        """
        Configuração da linha número 75 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoMomentoReamostragem, 0)
        if b is not None:
            return b.valor
        return None

    @momento_reamostragem.setter
    def momento_reamostragem(self, dado: int):
        b = self.__bloco_por_tipo(BlocoMomentoReamostragem, 0)
        if b is not None:
            b.valor = dado

    @property
    def mantem_arquivos_energias(self) -> Optional[int]:
        """
        Configuração da linha número 76 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoMantemArquivosEnergias, 0)
        if b is not None:
            return b.valor
        return None

    @mantem_arquivos_energias.setter
    def mantem_arquivos_energias(self, dado: int):
        b = self.__bloco_por_tipo(BlocoMantemArquivosEnergias, 0)
        if b is not None:
            b.valor = dado

    @property
    def inicio_teste_convergencia(self) -> Optional[int]:
        """
        Configuração da linha número 77 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoInicioTesteConvergencia, 0)
        if b is not None:
            return b.valor
        return None

    @inicio_teste_convergencia.setter
    def inicio_teste_convergencia(self, dado: int):
        b = self.__bloco_por_tipo(BlocoInicioTesteConvergencia, 0)
        if b is not None:
            b.valor = dado

    @property
    def sazonaliza_vmint(self) -> Optional[int]:
        """
        Configuração da linha número 78 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoSazonalizarVminT, 0)
        if b is not None:
            return b.valor
        return None

    @sazonaliza_vmint.setter
    def sazonaliza_vmint(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSazonalizarVminT, 0)
        if b is not None:
            b.valor = dado

    @property
    def sazonaliza_vmaxt(self) -> Optional[int]:
        """
        Configuração da linha número 79 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoSazonalizarVmaxT, 0)
        if b is not None:
            return b.valor
        return None

    @sazonaliza_vmaxt.setter
    def sazonaliza_vmaxt(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSazonalizarVmaxT, 0)
        if b is not None:
            b.valor = dado

    @property
    def sazonaliza_vminp(self) -> Optional[int]:
        """
        Configuração da linha número 80 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoSazonalizarVminP, 0)
        if b is not None:
            return b.valor
        return None

    @sazonaliza_vminp.setter
    def sazonaliza_vminp(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSazonalizarVminP, 0)
        if b is not None:
            b.valor = dado

    @property
    def sazonaliza_cfuga_cmont(self) -> Optional[int]:
        """
        Configuração da linha número 81 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoSazonalizarCfugaCmont, 0)
        if b is not None:
            return b.valor
        return None

    @sazonaliza_cfuga_cmont.setter
    def sazonaliza_cfuga_cmont(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSazonalizarCfugaCmont, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricoes_emissao_gee(self) -> Optional[int]:
        """
        Configuração da linha número 82 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoRestricoesEmissaoGEE, 0)
        if b is not None:
            return b.valor
        return None

    @restricoes_emissao_gee.setter
    def restricoes_emissao_gee(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRestricoesEmissaoGEE, 0)
        if b is not None:
            b.valor = dado

    @property
    def consideracao_media_anual_afluencias(self) -> Optional[int]:
        """
        Configuração da linha número 83 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoAfluenciaAnualPARp, 0)
        if b is not None:
            return b.consideracao_media_anual_afluencias
        return None

    @consideracao_media_anual_afluencias.setter
    def consideracao_media_anual_afluencias(self, dado: int):
        b = self.__bloco_por_tipo(BlocoAfluenciaAnualPARp, 0)
        if b is not None:
            b.consideracao_media_anual_afluencias = dado

    @property
    def reducao_automatica_ordem(self) -> Optional[int]:
        """
        Configuração da linha número 83 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoAfluenciaAnualPARp, 0)
        if b is not None:
            return b.reducao_automatica_ordem
        return None

    @reducao_automatica_ordem.setter
    def reducao_automatica_ordem(self, dado: int):
        b = self.__bloco_por_tipo(BlocoAfluenciaAnualPARp, 0)
        if b is not None:
            b.reducao_automatica_ordem = dado

    @property
    def restricoes_fornecimento_gas(self) -> Optional[int]:
        """
        Configuração da linha número 84 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoRestricoesFornecGas, 0)
        if b is not None:
            return b.valor
        return None

    @restricoes_fornecimento_gas.setter
    def restricoes_fornecimento_gas(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRestricoesFornecGas, 0)
        if b is not None:
            b.valor = dado

    @property
    def memoria_calculo_cortes(self) -> Optional[int]:
        """
        Configuração da linha número 85 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoMemCalculoCortes, 0)
        if b is not None:
            return b.valor
        return None

    @memoria_calculo_cortes.setter
    def memoria_calculo_cortes(self, dado: int):
        b = self.__bloco_por_tipo(BlocoMemCalculoCortes, 0)
        if b is not None:
            b.valor = dado

    @property
    def considera_geracao_eolica(self) -> Optional[int]:
        """
        Configuração da linha número 86 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoGeracaoEolica, 0)
        if b is not None:
            return b.considera
        return None

    @considera_geracao_eolica.setter
    def considera_geracao_eolica(self, dado: int):
        b = self.__bloco_por_tipo(BlocoGeracaoEolica, 0)
        if b is not None:
            b.considera = dado

    @property
    def penalidade_corte_geracao_eolica(self) -> Optional[float]:
        """
        Configuração da linha número 86 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoGeracaoEolica, 0)
        if b is not None:
            return b.penalidade
        return None

    @penalidade_corte_geracao_eolica.setter
    def penalidade_corte_geracao_eolica(self, dado: float):
        b = self.__bloco_por_tipo(BlocoGeracaoEolica, 0)
        if b is not None:
            b.penalidade = dado

    @property
    def compensacao_correlacao_cruzada(self) -> Optional[int]:
        """
        Configuração da linha número 87 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int
        """
        b = self.__bloco_por_tipo(BlocoCompensacaoCorrelacaoCruzada, 0)
        if b is not None:
            return b.valor
        return None

    @compensacao_correlacao_cruzada.setter
    def compensacao_correlacao_cruzada(self, dado: int):
        b = self.__bloco_por_tipo(BlocoCompensacaoCorrelacaoCruzada, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricao_turbinamento(self) -> Optional[int]:
        """
        Configuração da linha número 88 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoConsideracaoTurbinamentoMinimoMaximo, 0)
        if b is not None:
            return b.valor
        return None

    @restricao_turbinamento.setter
    def restricao_turbinamento(self, dado: int):
        b = self.__bloco_por_tipo(BlocoConsideracaoTurbinamentoMinimoMaximo, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricao_defluencia(self) -> Optional[int]:
        """
        Configuração da linha número 89 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoConsideracaoDefluenciaMaxima, 0)
        if b is not None:
            return b.valor
        return None

    @restricao_defluencia.setter
    def restricao_defluencia(self, dado: int):
        b = self.__bloco_por_tipo(BlocoConsideracaoDefluenciaMaxima, 0)
        if b is not None:
            b.valor = dado

    @property
    def aproveitamento_bases_backward(self) -> Optional[int]:
        """
        Configuração da linha número 90 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoAproveitamentoBasePLsBackward, 0)
        if b is not None:
            return b.valor
        return None

    @aproveitamento_bases_backward.setter
    def aproveitamento_bases_backward(self, dado: int):
        b = self.__bloco_por_tipo(BlocoAproveitamentoBasePLsBackward, 0)
        if b is not None:
            b.valor = dado

    @property
    def impressao_estados_geracao_cortes(self) -> Optional[int]:
        """
        Configuração da linha número 91 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoImpressaoEstadosGeracaoCortes, 0)
        if b is not None:
            return b.valor
        return None

    @impressao_estados_geracao_cortes.setter
    def impressao_estados_geracao_cortes(self, dado: int):
        b = self.__bloco_por_tipo(BlocoImpressaoEstadosGeracaoCortes, 0)
        if b is not None:
            b.valor = dado

    @property
    def semente_forward(self) -> Optional[int]:
        """
        Configuração da linha número 92 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoSementeForward, 0)
        if b is not None:
            return b.valor
        return None

    @semente_forward.setter
    def semente_forward(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSementeForward, 0)
        if b is not None:
            b.valor = dado

    @property
    def semente_backward(self) -> Optional[int]:
        """
        Configuração da linha número 93 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoSementeBackward, 0)
        if b is not None:
            return b.valor
        return None

    @semente_backward.setter
    def semente_backward(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSementeBackward, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricao_lpp_turbinamento_maximo_ree(self) -> Optional[int]:
        """
        Configuração da linha número 94 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoRestricaoLPPTurbinamentoMaximoREE, 0)
        if b is not None:
            return b.valor
        return None

    @restricao_lpp_turbinamento_maximo_ree.setter
    def restricao_lpp_turbinamento_maximo_ree(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRestricaoLPPTurbinamentoMaximoREE, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricao_lpp_defluencia_maxima_ree(self) -> Optional[int]:
        """
        Configuração da linha número 95 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoRestricaoLPPDefluenciaMaximaREE, 0)
        if b is not None:
            return b.valor
        return None

    @restricao_lpp_defluencia_maxima_ree.setter
    def restricao_lpp_defluencia_maxima_ree(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRestricaoLPPDefluenciaMaximaREE, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricao_lpp_turbinamento_maximo_uhe(self) -> Optional[int]:
        """
        Configuração da linha número 96 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoRestricaoLPPTurbinamentoMaximoUHE, 0)
        if b is not None:
            return b.valor
        return None

    @restricao_lpp_turbinamento_maximo_uhe.setter
    def restricao_lpp_turbinamento_maximo_uhe(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRestricaoLPPTurbinamentoMaximoUHE, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricao_lpp_defluencia_maxima_uhe(self) -> Optional[int]:
        """
        Configuração da linha número 97 do arquivo `dger.dat`.

        :return: O valor do campo
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoRestricaoLPPDefluenciaMaximaUHE, 0)
        if b is not None:
            return b.valor
        return None

    @restricao_lpp_defluencia_maxima_uhe.setter
    def restricao_lpp_defluencia_maxima_uhe(self, dado: int):
        b = self.__bloco_por_tipo(BlocoRestricaoLPPDefluenciaMaximaUHE, 0)
        if b is not None:
            b.valor = dado
