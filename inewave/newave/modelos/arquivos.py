from typing import List


class Arquivos:
    """
    Armazena os dados de entrada do NEWAVE referentes ao arquivo
    `arquivos.dat`.

    Esta classe lida com informações de entrada do NEWAVE e
    que deve se referir aos nomes dos demais arquivos de entrada
    utilizados para o caso em questão.

    **Parâmetros**

    - dados_gerais: `str`
    - subsistema: `str`
    - config_hidraulica: `str`
    - modif_usinas_hidraulicas: `str`
    - config_termica: `str`
    - classes_termicas: `str`
    - expansao_hidraulica: `str`
    - expansao_termica: `str`
    - patamares_mercado: `str`
    - cortes: `str`
    - cabecalho_cortes: `str`
    - relatorio_convergencia: `str`
    - series_sinteticas: `str`
    - relatorio_forward: `str`
    - cabecalho_forward: `str`
    - series_historicas: `str`
    - manutencao_programada_termicas: `str`
    - despacho_hidrotermico: `str`
    - tendencia_hidrologica: `str`
    - dados_itaipu: `str`
    - demanda_bidding: `str`
    - cargas_adicionais: `str`
    - fatores_perdas: `str`
    - patamares_geracao_termica_min: `str`
    - enso_1: `str`
    - enso_2: `str`
    - desvio_agua: `str`
    - penalidade_por_desvio: `str`
    - curva_guia_penalidade_vmin: `str`
    - agrupamento_livre_intercambios: `str`
    - antecipacao_despacho_gnl: `str`
    - geracao_hidraulica_min: `str`
    - aversao_risco_sar: `str`
    - aversao_risco_cvar: `str`
    - reservatorios_equivalentes_energia: `str`
    - restricoes_eletricas: `str`
    - tecnologias: `str`
    - dados_aberturas: `str`
    - emissoes_gee: `str`
    - restricoes_gas: `str`
    """

    __slots__ = [
                 "dados_gerais",
                 "subsistema",
                 "config_hidraulica",
                 "modif_usinas_hidraulicas",
                 "config_termica",
                 "dados_termicas",
                 "classes_termicas",
                 "expansao_hidraulica",
                 "expansao_termica",
                 "patamares_mercado",
                 "cortes",
                 "cabecalho_cortes",
                 "relatorio_convergencia",
                 "series_sinteticas",
                 "relatorio_forward",
                 "cabecalho_forward",
                 "series_historicas",
                 "manutencao_programada_termicas",
                 "despacho_hidrotermico",
                 "tendencia_hidrologica",
                 "dados_itaipu",
                 "demanda_bidding",
                 "cargas_adicionais",
                 "fatores_perdas",
                 "patamares_geracao_termica_min",
                 "enso_1",
                 "enso_2",
                 "desvio_agua",
                 "penalidade_por_desvio",
                 "curva_guia_penalidade_vmin",
                 "agrupamento_livre_intercambios",
                 "antecipacao_despacho_gnl",
                 "geracao_hidraulica_min",
                 "aversao_risco_sar",
                 "aversao_risco_cvar",
                 "eservatorios_equival_energia",
                 "restricoes_eletricas",
                 "tecnologias",
                 "dados_aberturas",
                 "emissoes_gee",
                 "restricoes_gas"
                ]

    legendas = [
                "DADOS GERAIS                :",
                "DADOS DOS SUBSIST/SUBMERCADO:",
                "CONFIGURACAO HIDRAULICA     :",
                "ALTERACAO DADOS USINAS HIDRO:",
                "CONFIGURACAO TERMICA        :",
                "DADOS DAS USINAS TERMICAS   :",
                "DADOS DAS CLASSES TERMICAS  :",
                "DADOS DE EXPANSAO HIDRAULICA:",
                "ARQUIVO DE EXPANSAO TERMICA :",
                "ARQUIVO DE PATAMARES MERCADO:",
                "ARQUIVO DE CORTES DE BENDERS:",
                "ARQUIVO DE CABECALHO CORTES :",
                "RELATORIO DE CONVERGENCIA   :",
                "RELATORIO DE E. SINTETICAS  :",
                "RELATORIO DETALHADO FORWARD :",
                "ARQUIVO DE CABECALHO FORWARD:",
                "ARQUIVO DE S.HISTORICAS S.F.:",
                "ARQUIVO DE MANUT.PROG. UTE'S:",
                "ARQUIVO P/DESPACHO HIDROTERM:",
                "ARQUIVO C/TEND. HIDROLOGICA :",
                "ARQUIVO C/DADOS DE ITAIPU   :",
                "ARQUIVO C/DEMAND S. BIDDING :",
                "ARQUIVO C/CARGAS ADICIONAIS :",
                "ARQUIVO C/FATORES DE PERDAS :",
                "ARQUIVO C/PATAMARES GTMIN   :",
                "ARQUIVO ENSO 1              :",
                "ARQUIVO ENSO 2              :",
                "ARQUIVO DSVAGUA             :",
                "ARQUIVO P/PENALID. POR DESV.:",
                "ARQUIVO C.GUIA / PENAL.VMINT:",
                "ARQUIVO AGRUPAMENTO LIVRE   :",
                "ARQUIVO ANTEC.DESP.GNL      :",
                "ARQUIVO GER. HIDR. MIN.     :",
                "ARQUIVO AVERSAO RISCO - SAR :",
                "ARQUIVO AVERSAO RISCO - CVAR:",
                "DADOS DOS RESER.EQ.ENERGIA  :",
                "DADOS DOS REST. ELETRICAS   :",
                "ARQUIVO DE TECNOLOGIAS      :",
                "DADOS DE ABERTURAS          :",
                "ARQUIVO DE EMISSOES GEE     :",
                "ARQUIVO DE RESTRICAO DE GAS :"
               ]

    def __init__(self,
                 dados_gerais: str,
                 subsistema: str,
                 config_hidraulica: str,
                 modif_usinas_hidraulicas: str,
                 config_termica: str,
                 dados_termicas: str,
                 classes_termicas: str,
                 expansao_hidraulica: str,
                 expansao_termica: str,
                 patamares_mercado: str,
                 cortes: str,
                 cabecalho_cortes: str,
                 relatorio_convergencia: str,
                 series_sinteticas: str,
                 relatorio_forward: str,
                 cabecalho_forward: str,
                 series_historicas: str,
                 manutencao_programada_termicas: str,
                 despacho_hidrotermico: str,
                 tendencia_hidrologica: str,
                 dados_itaipu: str,
                 demanda_bidding: str,
                 cargas_adicionais: str,
                 fatores_perdas: str,
                 patamares_geracao_termica_min: str,
                 enso_1: str,
                 enso_2: str,
                 desvio_agua: str,
                 penalidade_por_desvio: str,
                 curva_guia_penalidade_vmin: str,
                 agrupamento_livre_intercambios: str,
                 antecipacao_despacho_gnl: str,
                 geracao_hidraulica_min: str,
                 aversao_risco_sar: str,
                 aversao_risco_cvar: str,
                 reservatorios_equival_energia: str,
                 restricoes_eletricas: str,
                 tecnologias: str,
                 dados_aberturas: str,
                 emissoes_gee: str,
                 restricoes_gas: str):
        self.dados_gerais = dados_gerais
        self.subsistema = subsistema
        self.config_hidraulica = config_hidraulica
        self.modif_usinas_hidraulicas = modif_usinas_hidraulicas
        self.config_termica = config_termica
        self.dados_termicas = dados_termicas
        self.classes_termicas = classes_termicas
        self.expansao_hidraulica = expansao_hidraulica
        self.expansao_termica = expansao_termica
        self.patamares_mercado = patamares_mercado
        self.cortes = cortes
        self.cabecalho_cortes = cabecalho_cortes
        self.relatorio_convergencia = relatorio_convergencia
        self.series_sinteticas = series_sinteticas
        self.relatorio_forward = relatorio_forward
        self.cabecalho_forward = cabecalho_forward
        self.series_historicas = series_historicas
        self.manutencao_programada_termicas = manutencao_programada_termicas
        self.despacho_hidrotermico = despacho_hidrotermico
        self.tendencia_hidrologica = tendencia_hidrologica
        self.dados_itaipu = dados_itaipu
        self.demanda_bidding = demanda_bidding
        self.cargas_adicionais = cargas_adicionais
        self.fatores_perdas = fatores_perdas
        self.patamares_geracao_termica_min = patamares_geracao_termica_min
        self.enso_1 = enso_1
        self.enso_2 = enso_2
        self.desvio_agua = desvio_agua
        self.penalidade_por_desvio = penalidade_por_desvio
        self.curva_guia_penalidade_vmin = curva_guia_penalidade_vmin
        self.agrupamento_livre_intercambios = agrupamento_livre_intercambios
        self.antecipacao_despacho_gnl = antecipacao_despacho_gnl
        self.geracao_hidraulica_min = geracao_hidraulica_min
        self.aversao_risco_sar = aversao_risco_sar
        self.aversao_risco_cvar = aversao_risco_cvar
        self.eservatorios_equival_energia = reservatorios_equival_energia
        self.restricoes_eletricas = restricoes_eletricas
        self.tecnologias = tecnologias
        self.dados_aberturas = dados_aberturas
        self.emissoes_gee = emissoes_gee
        self.restricoes_gas = restricoes_gas

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre Caso avalia o único campo.
        """
        if not isinstance(o, Arquivos):
            return False
        arquivos: Arquivos = o
        dif = False
        for s1, s2 in zip(self.__slots__,
                          arquivos.__slots__):
            if s1 != s2 or getattr(self, s1) != getattr(arquivos, s2):
                dif = True
                break
        return not dif

    @classmethod
    def constroi_de_lista(cls, nomes_arquivos: List[str]) -> 'Arquivos':
        nomes = tuple(nomes_arquivos)
        return cls(*nomes)
