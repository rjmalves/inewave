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
                b for i, b in enumerate(self.data.of_type(bloco)) if i == indice
            )
        except StopIteration:
            return None

    @property
    def nome_caso(self) -> Optional[str]:
        """
        Configuração da linha número 1 do arquivo `dger.dat`.
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
    def tipo_execucao(self) -> int:
        """
        Configuração da linha número 2 do arquivo `dger.dat`.
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
    def duracao_periodo(self) -> int:
        """
        Configuração da linha número 3 do arquivo `dger.dat`.
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
    def num_anos_estudo(self) -> int:
        """
        Configuração da linha número 4 do arquivo `dger.dat`.
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
    def mes_inicio_pre_estudo(self) -> int:
        """
        Configuração da linha número 5 do arquivo `dger.dat`.
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
    def mes_inicio_estudo(self) -> int:
        """
        Configuração da linha número 6 do arquivo `dger.dat`.
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
    def ano_inicio_estudo(self) -> int:
        """
        Configuração da linha número 7 do arquivo `dger.dat`.
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
    def num_anos_pre_estudo(self) -> int:
        """
        Configuração da linha número 8 do arquivo `dger.dat`.
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
    def num_anos_pos_estudo(self) -> int:
        """
        Configuração da linha número 9 do arquivo `dger.dat`.
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
    def num_anos_pos_sim_final(self) -> int:
        """
        Configuração da linha número 10 do arquivo `dger.dat`.
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
    def imprime_dados(self) -> int:
        """
        Configuração da linha número 11 do arquivo `dger.dat`.
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
    def imprime_mercados(self) -> int:
        """
        Configuração da linha número 12 do arquivo `dger.dat`.
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
    def imprime_energias(self) -> int:
        """
        Configuração da linha número 13 do arquivo `dger.dat`.
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
    def imprime_modelo_estocastico(self) -> int:
        """
        Configuração da linha número 14 do arquivo `dger.dat`.
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
    def imprime_subsistema(self) -> int:
        """
        Configuração da linha número 15 do arquivo `dger.dat`.
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
    def num_max_iteracoes(self) -> int:
        """
        Configuração da linha número 16 do arquivo `dger.dat`.
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
    def num_forwards(self) -> int:
        """
        Configuração da linha número 17 do arquivo `dger.dat`.
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
    def num_aberturas(self) -> List[int]:
        """
        Configuração da linha número 18 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoNumAberturas, 0)
        if b is not None:
            return b.valor
        return None

    @num_aberturas.setter
    def num_aberturas(self, dado: List[int]):
        b = self.__bloco_por_tipo(BlocoNumAberturas, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_series_sinteticas(self) -> int:
        """
        Configuração da linha número 19 do arquivo `dger.dat`.
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
    def ordem_maxima_parp(self) -> int:
        """
        Configuração da linha número 20 do arquivo `dger.dat`.
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
    def ano_inicial_historico(self) -> int:
        """
        Configuração da linha número 21 do arquivo `dger.dat`.
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
    def tamanho_registro_arquivo_historico(self) -> int:
        """
        Configuração da linha número 21 do arquivo `dger.dat`.
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
    def calcula_volume_inicial(self) -> int:
        """
        Configuração da linha número 22 do arquivo `dger.dat`.
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
    def volume_inicial_por_subsistema(self) -> List[float]:
        """
        Configuração das linhas número 23 e 24 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoVolInicialSubsistema, 0)
        if b is not None:
            return b.valores
        return None

    @volume_inicial_por_subsistema.setter
    def volume_inicial_por_subsistema(self, dado: List[float]):
        b = self.__bloco_por_tipo(BlocoVolInicialSubsistema, 0)
        if b is not None:
            b.valores = dado

    @property
    def tolerancia(self) -> float:
        """
        Configuração da linha número 25 do arquivo `dger.dat`.
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
    def taxa_de_desconto(self) -> float:
        """
        Configuração da linha número 26 do arquivo `dger.dat`.
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
    def tipo_simulacao_final(self) -> int:
        """
        Configuração da linha número 27 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoTipoSimFinal, 0)
        if b is not None:
            return b.valor
        return None

    @tipo_simulacao_final.setter
    def tipo_simulacao_final(self, dado: int):
        b = self.__bloco_por_tipo(BlocoTipoSimFinal, 0)
        if b is not None:
            b.valor = dado

    @property
    def impressao_operacao(self) -> int:
        """
        Configuração da linha número 28 do arquivo `dger.dat`.
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
    def impressao_convergencia(self) -> int:
        """
        Configuração da linha número 29 do arquivo `dger.dat`.
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
    def intervalo_para_gravar(self) -> int:
        """
        Configuração da linha número 30 do arquivo `dger.dat`.
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
    def num_minimo_iteracoes(self) -> int:
        """
        Configuração da linha número 31 do arquivo `dger.dat`.
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
    def racionamento_preventivo(self) -> str:
        """
        Configuração da linha número 32 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoRacionamentoPreventivo, 0)
        if b is not None:
            return b.valor
        return None

    @racionamento_preventivo.setter
    def racionamento_preventivo(self, dado: str):
        b = self.__bloco_por_tipo(BlocoRacionamentoPreventivo, 0)
        if b is not None:
            b.valor = dado

    @property
    def num_anos_manutencao_utes(self) -> int:
        """
        Configuração da linha número 33 do arquivo `dger.dat`.
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
    def tendencia_hidrologica(self) -> List[int]:
        """
        Configuração da linha número 34 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoTendenciaHidrologica, 0)
        if b is not None:
            return b.valores
        return None

    @tendencia_hidrologica.setter
    def tendencia_hidrologica(self, dado: List[int]):
        b = self.__bloco_por_tipo(BlocoTendenciaHidrologica, 0)
        if b is not None:
            b.valores = dado

    @property
    def restricao_itaipu(self) -> int:
        """
        Configuração da linha número 35 do arquivo `dger.dat`.
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
    def bid(self) -> int:
        """
        Configuração da linha número 36 do arquivo `dger.dat`.
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
    def perdas_rede_transmissao(self) -> int:
        """
        Configuração da linha número 37 do arquivo `dger.dat`.
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
    def el_nino(self) -> int:
        """
        Configuração da linha número 38 do arquivo `dger.dat`.
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
    def enso(self) -> int:
        """
        Configuração da linha número 39 do arquivo `dger.dat`.
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
    def duracao_por_patamar(self) -> int:
        """
        Configuração da linha número 40 do arquivo `dger.dat`.
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
    def outros_usos_da_agua(self) -> int:
        """
        Configuração da linha número 41 do arquivo `dger.dat`.
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
    def correcao_desvio(self) -> int:
        """
        Configuração da linha número 42 do arquivo `dger.dat`.
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
    def curva_aversao(self) -> int:
        """
        Configuração da linha número 43 do arquivo `dger.dat`.
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
    def tipo_geracao_enas(self) -> int:
        """
        Configuração da linha número 44 do arquivo `dger.dat`.
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
    def risco_deficit(self) -> List[float]:
        """
        Configuração da linha número 45 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoRiscoDeficit, 0)
        if b is not None:
            return b.valores
        return None

    @risco_deficit.setter
    def risco_deficit(self, dado: List[float]):
        b = self.__bloco_por_tipo(BlocoRiscoDeficit, 0)
        if b is not None:
            b.valores = dado

    @property
    def iteracao_para_simulacao_final(self) -> int:
        """
        Configuração da linha número 46 do arquivo `dger.dat`.
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
    def agrupamento_livre(self) -> int:
        """
        Configuração da linha número 47 do arquivo `dger.dat`.
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
    def equalizacao_penal_itercambio(self) -> int:
        """
        Configuração da linha número 48 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoEqualizacaoPenalInt, 0)
        if b is not None:
            return b.valor
        return None

    @equalizacao_penal_itercambio.setter
    def equalizacao_penal_itercambio(self, dado: int):
        b = self.__bloco_por_tipo(BlocoEqualizacaoPenalInt, 0)
        if b is not None:
            b.valor = dado

    @property
    def representacao_submotorizacao(self) -> int:
        """
        Configuração da linha número 49 do arquivo `dger.dat`.
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
    def ordenacao_automatica(self) -> int:
        """
        Configuração da linha número 50 do arquivo `dger.dat`.
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
    def considera_carga_adicional(self) -> int:
        """
        Configuração da linha número 51 do arquivo `dger.dat`.
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
    def delta_zsup(self) -> float:
        """
        Configuração da linha número 52 do arquivo `dger.dat`.
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
    def delta_zinf(self) -> float:
        """
        Configuração da linha número 53 do arquivo `dger.dat`.
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
    def deltas_consecutivos(self) -> int:
        """
        Configuração da linha número 54 do arquivo `dger.dat`.
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
    def despacho_antecipado_gnl(self) -> int:
        """
        Configuração da linha número 55 do arquivo `dger.dat`.
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
    def modif_automatica_adterm(self) -> int:
        """
        Configuração da linha número 56 do arquivo `dger.dat`.
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
    def considera_ghmin(self) -> int:
        """
        Configuração da linha número 57 do arquivo `dger.dat`.
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
    def simulacao_final_com_data(self) -> int:
        """
        Configuração da linha número 58 do arquivo `dger.dat`.
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
    def gerenciamento_pls(self) -> List[int]:
        """
        Configuração da linha número 59 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            return b.valores
        return None

    @gerenciamento_pls.setter
    def gerenciamento_pls(self, dado: List[int]):
        b = self.__bloco_por_tipo(BlocoGerenciamentoPLs, 0)
        if b is not None:
            b.valores = dado

    @property
    def sar(self) -> int:
        """
        Configuração da linha número 60 do arquivo `dger.dat`.
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
    def cvar(self) -> int:
        """
        Configuração da linha número 61 do arquivo `dger.dat`.
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
    def considera_zsup_min_convergencia(self) -> int:
        """
        Configuração da linha número 62 do arquivo `dger.dat`.
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
    def desconsidera_vazao_minima(self) -> int:
        """
        Configuração da linha número 63 do arquivo `dger.dat`.
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
    def restricoes_eletricas(self) -> int:
        """
        Configuração da linha número 64 do arquivo `dger.dat`.
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
    def selecao_de_cortes(self) -> int:
        """
        Configuração da linha número 65 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoSelecaoCortes, 0)
        if b is not None:
            return b.valor
        return None

    @selecao_de_cortes.setter
    def selecao_de_cortes(self, dado: int):
        b = self.__bloco_por_tipo(BlocoSelecaoCortes, 0)
        if b is not None:
            b.valor = dado

    @property
    def janela_de_cortes(self) -> int:
        """
        Configuração da linha número 66 do arquivo `dger.dat`.
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
    def reamostragem_cenarios(self) -> List[int]:
        """
        Configuração da linha número 67 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoReamostragemCenarios, 0)
        if b is not None:
            return b.valor
        return None

    @reamostragem_cenarios.setter
    def reamostragem_cenarios(self, dado: List[int]):
        b = self.__bloco_por_tipo(BlocoReamostragemCenarios, 0)
        if b is not None:
            b.valor = dado

    @property
    def converge_no_zero(self) -> int:
        """
        Configuração da linha número 68 do arquivo `dger.dat`.
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
    def consulta_fcf(self) -> int:
        """
        Configuração da linha número 69 do arquivo `dger.dat`.
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
    def impressao_ena(self) -> int:
        """
        Configuração da linha número 70 do arquivo `dger.dat`.
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
    def impressao_cortes_ativos_sim_final(self) -> str:
        """
        Configuração da linha número 71 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoImpressaoCortesAtivosSimFinal, 0)
        if b is not None:
            return b.valor
        return None

    @impressao_cortes_ativos_sim_final.setter
    def impressao_cortes_ativos_sim_final(self, dado: str):
        b = self.__bloco_por_tipo(BlocoImpressaoCortesAtivosSimFinal, 0)
        if b is not None:
            b.valor = dado

    @property
    def representacao_agregacao(self) -> int:
        """
        Configuração da linha número 72 do arquivo `dger.dat`.
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
    def matriz_correlacao_espacial(self) -> int:
        """
        Configuração da linha número 73 do arquivo `dger.dat`.
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
    def desconsidera_convergencia_estatistica(self) -> int:
        """
        Configuração da linha número 74 do arquivo `dger.dat`.
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
    def momento_reamostragem(self) -> int:
        """
        Configuração da linha número 75 do arquivo `dger.dat`.
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
    def mantem_arquivos_energias(self) -> int:
        """
        Configuração da linha número 76 do arquivo `dger.dat`.
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
    def inicio_teste_convergencia(self) -> int:
        """
        Configuração da linha número 77 do arquivo `dger.dat`.
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
    def sazonaliza_vmint(self) -> int:
        """
        Configuração da linha número 78 do arquivo `dger.dat`.
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
    def sazonaliza_vmaxt(self) -> int:
        """
        Configuração da linha número 79 do arquivo `dger.dat`.
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
    def sazonaliza_vminp(self) -> int:
        """
        Configuração da linha número 80 do arquivo `dger.dat`.
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
    def sazonaliza_cfuga_cmont(self) -> int:
        """
        Configuração da linha número 81 do arquivo `dger.dat`.
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
    def restricoes_emissao_gee(self) -> int:
        """
        Configuração da linha número 82 do arquivo `dger.dat`.
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
    def afluencia_anual_parp(self) -> int:
        """
        Configuração da linha número 83 do arquivo `dger.dat`.
        """
        b = self.__bloco_por_tipo(BlocoAfluenciaAnualPARp, 0)
        if b is not None:
            return b.valor
        return None

    @afluencia_anual_parp.setter
    def afluencia_anual_parp(self, dado: int):
        b = self.__bloco_por_tipo(BlocoAfluenciaAnualPARp, 0)
        if b is not None:
            b.valor = dado

    @property
    def restricoes_fornecimento_gas(self) -> int:
        """
        Configuração da linha número 84 do arquivo `dger.dat`.
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
    def memoria_calculo_cortes(self) -> int:
        """
        Configuração da linha número 85 do arquivo `dger.dat`.
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
    def considera_geracao_eolica(self) -> int:
        """
        Configuração da linha número 86 do arquivo `dger.dat`.
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
    def penalidade_corte_geracao_eolica(self) -> float:
        """
        Configuração da linha número 86 do arquivo `dger.dat`.
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
    def compensacao_correlacao_cruzada(self) -> int:
        """
        Configuração da linha número 87 do arquivo `dger.dat`.
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
