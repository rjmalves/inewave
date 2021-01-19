from enum import Enum
from typing import List, Tuple


class EnumComInferencia(Enum):
    """
    Classe base para os enums com inferência
    do enum a partir do valor dado
    """
    @classmethod
    def infere_valor(cls, v: int):
        """
        Construtor do enum a partir do valor
        """
        for e in cls:
            if e.value == v:
                return e
        return None


class EnumTipoExecucao(EnumComInferencia):
    r"""
    - COMPLETA:
    - SIMULACAO_FINAL
    """
    COMPLETA = 0
    SIMULACAO_FINAL = 1


class EnumTipoSimulacaoFinal(EnumComInferencia):
    r"""
    - NAO_SIMULA
    - SERIES_SINTETICAS
    - SERIE_HISTORICA
    - CONSISTENCIA_DADOS
    """
    NAO_SIMULA = 0
    SERIES_SINTETICAS = 1
    SERIE_HISTORICA = 2
    CONSISTENCIA_DADOS = 3


class EnumImpressaoOperacao(EnumComInferencia):
    r"""
    - SINOPSE
    - OPERACAO_DETALHADA
    """
    SINOPSE = 0
    OPERACAO_DETALHADA = 1


class EnumImpressaoConvergencia(EnumComInferencia):
    r"""
    - CONVERGENCIA_FINAL
    - CONVERGENCIA_TOTAL
    """
    CONVERGENCIA_FINAL = 0
    CONVERGENCIA_TOTAL = 1


class EnumTamanhoArquivoVazoes(EnumComInferencia):
    r"""
    - PALAVRAS_320
    - PALAVRAS_600
    """
    PALAVRAS_320 = 0
    PALAVRAS_600 = 1


class EnumTendenciaHidrologica(EnumComInferencia):
    r"""
    - NAO_LER
    - LER_POR_REE
    - LER_POR_POSTO
    """
    NAO_LER = 0
    LER_POR_REE = 1
    LER_POR_POSTO = 2


class EnumDuracaoPatamar(EnumComInferencia):
    r"""
    - SAZONAL
    - VARIAVEL_POR_ANO
    """
    SAZONAL = 0
    VARIAVEL_POR_ANO = 1


class EnumCorrecaoEnergiaDesvio(EnumComInferencia):
    r"""
    - CONSTANTE
    - VARIAVEL_COM_ARMAZENAMENTO
    """
    CONSTANTE = 0
    VARIAVEL_COM_ARMAZENAMENTO = 1


class EnumTipoGeracaoENAs(EnumComInferencia):
    r"""
    - RESIDUOS_IGUAIS_FW_BW
    - COMPENSACAO_CORR_CRUZADA_BW
    - COMPENSACAO_CORR_CRUZADA_FW_BW
    """
    RESIDUOS_IGUAIS_FW_BW = 0
    COMPENSACAO_CORR_CRUZADA_BW = 1
    COMPENSACAO_CORR_CRUZADA_FW_BW = 2


class EnumRepresentacaoSubmotorizacao(EnumComInferencia):
    r"""
    - NAO_CONSIDERA
    - SUBSISTEMA
    - USINA
    """
    NAO_CONSIDERA = 0
    SUBSISTEMA = 1
    USINA = 2


class EnumCVAR(EnumComInferencia):
    r"""
    - NAO_CONSIDERA
    - CONSTANTE_NO_TEMPO
    - VARIAVEL_NO_TEMPO
    """
    NAO_CONSIDERA = 0
    CONSTANTE_NO_TEMPO = 1
    VARIAVEL_NO_TEMPO = 2


class EnumTipoReamostragem(EnumComInferencia):
    r"""
    - RECOMBINACAO
    - PLENA
    """
    RECOMBINACAO = 0
    PLENA = 1


class EnumRepresentanteAgregacao(EnumComInferencia):
    r"""
    - MAIS_PROXIMO
    - CENTROIDE
    """
    MAIS_PROXIMO = 0
    CENTROIDE = 1


class EnumMatrizCorrelacaoEspacial(EnumComInferencia):
    r"""
    - ANUAL
    - MENSAL
    """
    ANUAL = 0
    MENSAL = 1


class EnumMomentoReamostragem(EnumComInferencia):
    r"""
    - BW_ITER_CORRESPONDENTE
    - FW_ITER_CORRESPONDENTE
    """
    BW_ITER_CORRESPONDENTE = 0
    FW_ITER_CORRESPONDENTE = 1


class EnumInicioTesteConvergencia(EnumComInferencia):
    r"""
    - PRIMEIRA_ITERACAO
    - ITERACAO_MINIMA
    """
    PRIMEIRA_ITERACAO = 0
    ITERACAO_MINIMA = 1


class DGer:
    """
    Classe para armazenar dados gerais de uma execução do NEWAVE.

    Os parâmetros são fornecidos ao construtor na mesma ordem em
    que são definidos no arquivo `dger.dat`.

    Apesar disso, não é recomendado criar um arquivo com o construtor
    desta classe, e sim utilizar o método `DGer.dger_padrao()`,
    que fornece um objeto com valores em todos os campos,
    que podem ser modificados.

    **Parâmetros**

    - nome_estudo : `str`
    - tipo_execucao: `EnumTipoExecucao`
    - duracao_estagio_op: `int`
    - num_anos_estudo: `int`,
    - mes_inicio_pre_estudo: `int`,
    - mes_inicio_estudo: `int`,
    - ano_inicio_estudo: `int`,
    - num_anos_pre_estudo: `int`,
    - num_anos_pos_estudo: `int`,
    - num_anos_pos_sim_final: `int`,
    - imprime_dados_usinas: `bool`,
    - imprime_dados_mercados: `bool`,
    - imprime_dados_energias: `bool`,
    - imprime_dados_modelo: `bool`,
    - imprime_dados_rees: `bool`,
    - max_iteracoes: `int`,
    - num_sim_forward: `int`,
    - num_aberturas: `int`,
    - num_series_sinteticas: `int`,
    - ordem_maxima_parp: `int`,
    - ano_inicial_vaz_historicas: `int`,
    - tamanho_arq_vaz_historicas: `EnumTamanhoArquivoVazoes`,
    - calcula_vol_inicial: `bool`,
    - vol_inicial_subsistema: `List[float]`,
    - tolerancia: `float`,
    - taxa_de_desconto: `float`,
    - tipo_simulacao_final: `EnumTipoSimulacaoFinal`,
    - impressao_operacao: `EnumImpressaoOperacao`,
    - impressao_convergencia: `EnumImpressaoConvergencia`,
    - intervalo_gravacao_relatorio: `int`,
    - min_interacoes: `int`,
    - racionamento_preventivo: `bool`,
    - numero_anos_manutencao_UTEs: `int`,
    - tendencia_hidrologica: `EnumTendenciaHidrologica`,
    - restricoes_itaipu: `bool`,
    - bidding_demanda: `bool`,
    - perdas_transmissao: `bool`,
    - el_nino: `bool`,
    - enso: `bool`,
    - duracao_patamar: `EnumDuracaoPatamar`,
    - considera_desvio_dagua: `bool`,
    - correcao_energia_desvio: `EnumCorrecaoEnergiaDesvio`,
    - considera_curva_aversao: `bool`,
    - tipo_geracao_afluencias: `EnumTipoGeracaoENAs`,
    - profundidade_risco_deficit: `Tuple[float, float]`,
    - iteracao_sim_final: `int`,
    - agrupamento_livre_interc: `bool`,
    - equaliza_penalidades_interc: `bool`,
    - representa_submotor: `EnumRepresentacaoSubmotorizacao`,
    - ordenacao_automatica_subsist: `bool`,
    - considera_cargas_adicionais: `bool`,
    - delta_zsup: `float`,
    - delta_zinf: `float`,
    - deltas_consecutivos: `int`,
    - considera_despacho_gnl: `bool`,
    - modifica_auto_despacho_gnl: `bool`,
    - considera_ghmin: `bool`,
    - sim_final_com_data: `bool`,
    - gerenciador_externo: `bool`,
    - comunicacao_dois_niveis: `bool`,
    - armazenamento_local_temp: `bool`,
    - aloca_memoria_enas: `bool`,
    - aloca_memoria_cortes: `bool`,
    - sar: `bool`,
    - cvar: `EnumCVAR`,
    - convergencia_minimo_zsup: `bool`,
    - desconsidera_vazao_minima: `bool`,
    - considera_restricoes_elet: `bool`,
    - selecao_cortes_benders: `bool`,
    - janela_selecao_cortes: `bool`,
    - reamostragem: `bool`,
    - tipo_reamostragem: `EnumTipoReamostragem`,
    - passo_reamostragem: `int`,
    - considera_convergencia_no0: `bool`,
    - consulta_fcf: `bool`,
    - impressao_ena: `bool`,
    - impressao_cortes_ativos: `bool`,
    - representante_agregacao: `EnumRepresentanteAgregacao`,
    - matriz_corr_espacial: `EnumMatrizCorrelacaoEspacial`,
    - desconsidera_converg_estatist: `bool`,
    - momento_reamostragem: `EnumMomentoReamostragem`,
    - mantem_arquivos_ena: `bool`,
    - inicio_teste_convergencia: `EnumInicioTesteConvergencia`

    """
    def __init__(self,
                 nome_estudo: str,
                 tipo_execucao: EnumTipoExecucao,
                 duracao_estagio_op: int,
                 num_anos_estudo: int,
                 mes_inicio_pre_estudo: int,
                 mes_inicio_estudo: int,
                 ano_inicio_estudo: int,
                 num_anos_pre_estudo: int,
                 num_anos_pos_estudo: int,
                 num_anos_pos_sim_final: int,
                 imprime_dados_usinas: bool,
                 imprime_dados_mercados: bool,
                 imprime_dados_energias: bool,
                 imprime_dados_modelo: bool,
                 imprime_dados_rees: bool,
                 max_iteracoes: int,
                 num_sim_forward: int,
                 num_aberturas: int,
                 num_series_sinteticas: int,
                 ordem_maxima_parp: int,
                 ano_inicial_vaz_historicas: int,
                 tamanho_arq_vaz_historicas: EnumTamanhoArquivoVazoes,
                 calcula_vol_inicial: bool,
                 vol_inicial_subsistema: List[float],
                 tolerancia: float,
                 taxa_de_desconto: float,
                 tipo_simulacao_final: EnumTipoSimulacaoFinal,
                 impressao_operacao: EnumImpressaoOperacao,
                 impressao_convergencia: EnumImpressaoConvergencia,
                 intervalo_gravacao_relatorio: int,
                 min_interacoes: int,
                 racionamento_preventivo: bool,
                 numero_anos_manutencao_UTEs: int,
                 tendencia_hidrologica: EnumTendenciaHidrologica,
                 restricoes_itaipu: bool,
                 bidding_demanda: bool,
                 perdas_transmissao: bool,
                 el_nino: bool,
                 enso: bool,
                 duracao_patamar: EnumDuracaoPatamar,
                 considera_desvio_dagua: bool,
                 correcao_energia_desvio: EnumCorrecaoEnergiaDesvio,
                 considera_curva_aversao: bool,
                 tipo_geracao_afluencias: EnumTipoGeracaoENAs,
                 profundidade_risco_deficit: Tuple[float, float],
                 iteracao_sim_final: int,
                 agrupamento_livre_interc: bool,
                 equaliza_penalidades_interc: bool,
                 representa_submotor: EnumRepresentacaoSubmotorizacao,
                 ordenacao_automatica_subsist: bool,
                 considera_cargas_adicionais: bool,
                 delta_zsup: float,
                 delta_zinf: float,
                 deltas_consecutivos: int,
                 considera_despacho_gnl: bool,
                 modifica_auto_despacho_gnl: bool,
                 considera_ghmin: bool,
                 sim_final_com_data: bool,
                 gerenciador_externo: bool,
                 comunicacao_dois_niveis: bool,
                 armazenamento_local_temp: bool,
                 aloca_memoria_enas: bool,
                 aloca_memoria_cortes: bool,
                 sar: bool,
                 cvar: EnumCVAR,
                 convergencia_minimo_zsup: bool,
                 desconsidera_vazao_minima: bool,
                 considera_restricoes_elet: bool,
                 selecao_cortes_benders: bool,
                 janela_selecao_cortes: bool,
                 reamostragem: bool,
                 tipo_reamostragem: EnumTipoReamostragem,
                 passo_reamostragem: int,
                 considera_convergencia_no0: bool,
                 consulta_fcf: bool,
                 impressao_ena: bool,
                 impressao_cortes_ativos: bool,
                 representante_agregacao: EnumRepresentanteAgregacao,
                 matriz_corr_espacial: EnumMatrizCorrelacaoEspacial,
                 desconsidera_converg_estatist: bool,
                 momento_reamostragem: EnumMomentoReamostragem,
                 mantem_arquivos_ena: bool,
                 inicio_teste_convergencia: EnumInicioTesteConvergencia
                 ):

        self.nome_estudo = nome_estudo
        self.tipo_execucao = tipo_execucao
        self.duracao_estagio_op = duracao_estagio_op
        self.num_anos_estudo = num_anos_estudo
        self.mes_inicio_pre_estudo = mes_inicio_pre_estudo
        self.mes_inicio_estudo = mes_inicio_estudo
        self.ano_inicio_estudo = ano_inicio_estudo
        self.num_anos_pre_estudo = num_anos_pre_estudo
        self.num_anos_pos_estudo = num_anos_pos_estudo
        self.num_anos_pos_sim_final = num_anos_pos_sim_final
        self.imprime_dados_usinas = imprime_dados_usinas
        self.imprime_dados_mercados = imprime_dados_mercados
        self.imprime_dados_energias = imprime_dados_energias
        self.imprime_dados_modelo = imprime_dados_modelo
        self.imprime_dados_rees = imprime_dados_rees
        self.max_iteracoes = max_iteracoes
        self.num_sim_forward = num_sim_forward
        self.num_aberturas = num_aberturas
        self.num_series_sinteticas = num_series_sinteticas
        self.ordem_maxima_parp = ordem_maxima_parp
        self.ano_inicial_vaz_historicas = ano_inicial_vaz_historicas
        self.tamanho_arq_vaz_historicas = tamanho_arq_vaz_historicas
        self.calcula_vol_inicial = calcula_vol_inicial
        self.vol_inicial_subsistema = vol_inicial_subsistema
        self.tolerancia = tolerancia
        self.taxa_de_desconto = taxa_de_desconto
        self.tipo_simulacao_final = tipo_simulacao_final
        self.impressao_operacao = impressao_operacao
        self.impressao_convergencia = impressao_convergencia
        self.intervalo_gravacao_relatorio = intervalo_gravacao_relatorio
        self.min_interacoes = min_interacoes
        self.racionamento_preventivo = racionamento_preventivo
        self.numero_anos_manutencao_UTEs = numero_anos_manutencao_UTEs
        self.tendencia_hidrologica = tendencia_hidrologica
        self.restricoes_itaipu = restricoes_itaipu
        self.bidding_demanda = bidding_demanda
        self.perdas_transmissao = perdas_transmissao
        self.el_nino = el_nino
        self.enso = enso
        self.duracao_patamar = duracao_patamar
        self.considera_desvio_dagua = considera_desvio_dagua
        self.correcao_energia_desvio = correcao_energia_desvio
        self.considera_curva_aversao = considera_curva_aversao
        self.tipo_geracao_afluencias = tipo_geracao_afluencias
        self.profundidade_risco_deficit = profundidade_risco_deficit
        self.iteracao_sim_final = iteracao_sim_final
        self.agrupamento_livre_interc = agrupamento_livre_interc
        self.equaliza_penalidades_interc = equaliza_penalidades_interc
        self.representa_submotor = representa_submotor
        self.ordenacao_automatica_subsist = ordenacao_automatica_subsist
        self.considera_cargas_adicionais = considera_cargas_adicionais
        self.delta_zsup = delta_zsup
        self.delta_zinf = delta_zinf
        self.deltas_consecutivos = deltas_consecutivos
        self.considera_despacho_gnl = considera_despacho_gnl
        self.modifica_auto_despacho_gnl = modifica_auto_despacho_gnl
        self.considera_ghmin = considera_ghmin
        self.sim_final_com_data = sim_final_com_data
        self.gerenciador_externo = gerenciador_externo
        self.comunicacao_dois_niveis = comunicacao_dois_niveis
        self.armazenamento_local_temp = armazenamento_local_temp
        self.aloca_memoria_enas = aloca_memoria_enas
        self.aloca_memoria_cortes = aloca_memoria_cortes
        self.sar = sar
        self.cvar = cvar
        self.convergencia_minimo_zsup = convergencia_minimo_zsup
        self.desconsidera_vazao_minima = desconsidera_vazao_minima
        self.considera_restricoes_elet = considera_restricoes_elet
        self.selecao_cortes_benders = selecao_cortes_benders
        self.janela_selecao_cortes = janela_selecao_cortes
        self.reamostragem = reamostragem
        self.tipo_reamostragem = tipo_reamostragem
        self.passo_reamostragem = passo_reamostragem
        self.considera_convergencia_no0 = considera_convergencia_no0
        self.consulta_fcf = consulta_fcf
        self.impressao_ena = impressao_ena
        self.impressao_cortes_ativos = impressao_cortes_ativos
        self.representante_agregacao = representante_agregacao
        self.matriz_corr_espacial = matriz_corr_espacial
        self.desconsidera_converg_estatist = desconsidera_converg_estatist
        self.momento_reamostragem = momento_reamostragem
        self.mantem_arquivos_ena = mantem_arquivos_ena
        self.inicio_teste_convergencia = inicio_teste_convergencia

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre DGer avalia todos os campos,
        menos o nome do estudo.
        """
        if not isinstance(o, DGer):
            return False
        dger: DGer = o
        dif = False
        for (k, u), (_, v) in zip(self.__dict__.items(),
                                  dger.__dict__.items()):
            if k == "nome_estudo":
                continue
            if u != v:
                dif = True
                break
        return not dif

    @classmethod
    def dger_padrao(cls):
        """
        Retorna um DGer padrão, com valores em todos os campos.

        Devido ao grande número de parâmetros do objeto DGer, este
        método se fez necessário para possibilitar a geração de objetos
        de dados gerais em larga escala sem precisar configurar cada um
        dos parâmetros necessários no construtor.

        Desta forma, um objeto DGer pode ser instanciado e ter apenas
        os parâmetros que forem de interesse do usuário modificados,
        facilitando a realização de estudos.

        **Exemplos**

        >>> dger_com_sar = DGer.dger_padrao()
        >>> print(dger_padrao.sar)
        False
        >>> dger_com_sar.sar = True
        >>> print(dger_padrao.sar)
        True

        """
        return DGer("",
                    EnumTipoExecucao.COMPLETA,
                    1,
                    5,
                    1,
                    1,
                    2021,
                    0,
                    5,
                    0,
                    True,
                    True,
                    True,
                    True,
                    True,
                    45,
                    200,
                    20,
                    2000,
                    6,
                    1931,
                    EnumTamanhoArquivoVazoes.PALAVRAS_320,
                    True,
                    [0., 0., 0., 0.],
                    95.0,
                    12.0,
                    EnumTipoSimulacaoFinal.SERIES_SINTETICAS,
                    EnumImpressaoOperacao.OPERACAO_DETALHADA,
                    EnumImpressaoConvergencia.CONVERGENCIA_TOTAL,
                    1,
                    30,
                    False,
                    1,
                    EnumTendenciaHidrologica.LER_POR_POSTO,
                    False,
                    False,
                    False,
                    False,
                    False,
                    EnumDuracaoPatamar.VARIAVEL_POR_ANO,
                    True,
                    EnumCorrecaoEnergiaDesvio.VARIAVEL_COM_ARMAZENAMENTO,
                    True,
                    EnumTipoGeracaoENAs.RESIDUOS_IGUAIS_FW_BW,
                    (1.0, 2.5),
                    0,
                    True,
                    True,
                    EnumRepresentacaoSubmotorizacao.USINA,
                    False,
                    True,
                    10.0,
                    0.2,
                    3,
                    True,
                    True,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    False,
                    False,
                    True,
                    True,
                    False,
                    True,
                    EnumTipoReamostragem.PLENA,
                    0,
                    False,
                    False,
                    False,
                    False,
                    EnumRepresentanteAgregacao.CENTROIDE,
                    EnumMatrizCorrelacaoEspacial.MENSAL,
                    True,
                    EnumMomentoReamostragem.FW_ITER_CORRESPONDENTE,
                    False,
                    EnumInicioTesteConvergencia.ITERACAO_MINIMA
                    )
