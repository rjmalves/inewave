# Imports do próprio módulo
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave.config import MAX_ANOS_ESTUDO, MAX_CONFIGURACOES
from inewave.config import MESES, REES, ORDEM_MAX_PARP
from inewave.newave.modelos.parp import PARp
# Imports de módulos externos
import numpy as np  # type: ignore
from copy import copy
from typing import IO, Dict, List


class LeituraPARp(Leitura):
    """
    Realiza a leitura do arquivo `parp.dat`
    existente em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `parp.dat`, construindo
    um objeto `PARp` cujas informações são as mesmas do parp.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `parp`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraPARp(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> parp = leitor.parp

    """
    # Marcadores de início dos blocos que são lidos
    str_inicio_serie = "SERIE  DE ENERGIAS DO REE"
    str_inicio_media = "SERIE MEDIA 12 MESES "
    str_inicio_correl_parc = "CORRELOGRAMO PARCIAL DA SERIE DE ENERGIAS"
    str_inicio_correl_cruz = "CORRELACAO CRUZADA VARIAVEL ANUAL"
    str_inicio_ordens_o = "ORDEM ORIGINAL DO MODELO AUTORREGRESSIVO"
    str_inicio_ordens_f = "ORDEM FINAL DO MODELO AUTORREGRESSIVO"
    str_inicio_correl_esp_a = "CORRELACAO ESPACIAL HISTORICA ANUAL"
    str_inicio_correl_esp_m = "CORRELACAO ESPACIAL HISTORICA MENSAL"
    # Marcadores de fim dos blocos que são lidos
    str_fim_serie = "CORRELOGRAMO"
    str_fim_coefs = "SERIE DE RUIDOS"
    str_fim_parp = "////////////////////"

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # PARp default, depois é substituído
        self.parp = PARp({}, {}, {}, {}, {}, {}, {}, {}, {})

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo parp.dat.
        """
        energia = Bloco(LeituraPARp.str_inicio_serie,
                        LeituraPARp.str_fim_serie,
                        True,
                        self._le_series
                        )
        correl_parcial = Bloco(LeituraPARp.str_inicio_correl_parc,
                               "",
                               True,
                               self._le_correlograma)
        ordens_finais_coefs = Bloco(LeituraPARp.str_inicio_ordens_f,
                                    LeituraPARp.str_fim_coefs,
                                    True,
                                    self._le_ordens_finais_e_coefs)
        ordens_originais = Bloco(LeituraPARp.str_inicio_ordens_o,
                                 "",
                                 False,
                                 self._le_ordens_originais)
        medias = Bloco(LeituraPARp.str_inicio_media,
                       "",
                       False,
                       self._le_medias)
        correl_cruz_media = Bloco(LeituraPARp.str_inicio_correl_cruz,
                                  "",
                                  False,
                                  self._le_correl_cruzada_media)
        correl_esp_anual = Bloco(LeituraPARp.str_inicio_correl_esp_a,
                                 "",
                                 True,
                                 self._le_correl_esp_anual)
        correl_esp_mensal = Bloco(LeituraPARp.str_inicio_correl_esp_m,
                                  "",
                                  True,
                                  self._le_correl_esp_mensal)

        # Repete os blocos para o número esperado de tabelas no arquivo
        series_energia = [copy(energia) for _ in range(len(REES))]
        series_correls = [copy(correl_parcial) for _ in range(len(REES))]
        series_ordens_finais_coefs = [copy(ordens_finais_coefs)
                                      for _ in range(len(REES))]
        series_ordens_originais = [copy(ordens_originais)
                                   for _ in range(len(REES))]
        series_medias = [copy(medias)
                         for _ in range(len(REES))]
        correls_cruzada_media = [copy(correl_cruz_media)
                                 for _ in range(len(REES))]
        correls_esp_anuais = [copy(correl_esp_anual)
                              for _ in range(MAX_CONFIGURACOES)]
        correls_esp_mensais = [copy(correl_esp_mensal)
                               for _ in range(MAX_CONFIGURACOES)]
        return [*series_energia,
                *series_correls,
                *series_ordens_finais_coefs,
                *series_ordens_originais,
                *series_medias,
                *correls_cruzada_media,
                *correls_esp_anuais,
                *correls_esp_mensais]

    # Override
    def _inicia_variaveis_leitura(self):
        """
        Inicia variáveis temporárias que são escritas durante
        a leitura do arquivo.
        """
        self._ree_atual = 0
        self._cfg_atual = 0
        self._ano_atual = ""
        self.series: Dict[int, np.ndarray] = {i: np.zeros((100,
                                                           len(MESES) + 1,
                                                           100))
                                              for i in range(1,
                                                             len(REES) + 1)}
        self.medias: Dict[int, np.ndarray] = {i: np.zeros((100,
                                                           len(MESES),
                                                           100))
                                              for i in range(1,
                                                             len(REES) + 1)}
        self.correl_p: Dict[int, np.ndarray] = {i: np.zeros((200,
                                                             len(MESES)))
                                                for i in range(1,
                                                               len(REES) + 1)}
        self.ordens_o: Dict[int, np.ndarray] = {i: np.zeros((MAX_ANOS_ESTUDO,
                                                             len(MESES) + 1),
                                                            dtype=np.int32)
                                                for i in range(1,
                                                               len(REES) + 1)}
        self.ordens_f: Dict[int, np.ndarray] = {i: np.zeros((MAX_ANOS_ESTUDO,
                                                             len(MESES) + 1),
                                                            dtype=np.int32)
                                                for i in range(1,
                                                               len(REES) + 1)}
        self.correl_c: Dict[int, np.ndarray] = {i: np.zeros((200,
                                                             len(MESES) + 1))
                                                for i in range(1,
                                                               len(REES) + 1)}
        n_linhas_coefs = MAX_ANOS_ESTUDO * len(MESES)
        self.coefs: Dict[int, np.ndarray] = {i: np.zeros((n_linhas_coefs,
                                                          ORDEM_MAX_PARP,
                                                          4))
                                             for i in range(1,
                                                            len(REES) + 1)}
        MAX_CFG = MAX_CONFIGURACOES
        self.correl_esp_a: Dict[int, np.ndarray] = {i: np.zeros((len(REES),
                                                                 len(REES)))
                                                    for i in range(1, MAX_CFG)}
        self.correl_esp_m: Dict[int, np.ndarray] = {i: np.zeros((len(REES),
                                                                 len(MESES),
                                                                 len(REES)))
                                                    for i in range(1, MAX_CFG)}

    # Override
    def _prepara_dados_saida(self):
        """
        Trata os dados obtidos do arquivo para ser retornado.
        """
        # Limpa as correls_esp_a e correl_esp_m com apenas as
        # cfgs lidas
        cfgs_nao_lidas = list(range(self._cfg_atual + 1,
                                    MAX_CONFIGURACOES))
        for i in cfgs_nao_lidas:
            self.correl_esp_a.pop(i)
            self.correl_esp_m.pop(i)
        # Cria o objeto parp completo
        self.parp = PARp(self.ordens_o,
                         self.ordens_f,
                         self.coefs,
                         self.series,
                         self.correl_p,
                         self.medias,
                         self.correl_c,
                         self.correl_esp_a,
                         self.correl_esp_m)

    # Override
    def _fim_arquivo(self, linha: str) -> bool:
        return LeituraPARp.str_fim_parp in linha

    # Override
    def le_arquivo(self, nome_arquivo="parp.dat") -> PARp:
        """
        Faz a leitura do arquivo `parp.dat`.
        """
        self._le_arquivo_em_diretorio(self.diretorio,
                                      nome_arquivo)
        return self.parp

    def _le_series(self,
                   arq: IO,
                   cabecalho: str = "") -> None:
        """
        Lê as tabelas de séries de energia para uma REE.
        """

        def _identifica_ree() -> int:
            """
            Processa uma linha e extrai o índice da REE.
            """
            ree = REES.index(cabecalho.split("REE")[1][:16].strip()) + 1
            self._ree_atual = ree
            return ree

        def _identifica_cfg(linha: str) -> int:
            """
            Processa uma linha e extrai o número da configuração.
            """
            self._cfg_atual = int(linha.split(STR_CFG)[1][:-2].strip())
            return self._cfg_atual

        def _le_tabela_serie():
            """
            Lê a tabela de séries de energia de uma configuração.
            """
            # Variáveis auxiliares
            ree = self._ree_atual  # PEP8
            cfg = self._cfg_atual  # PEP8
            regi = RegistroIn(4)  # PEP8
            regf = RegistroFn(9)  # PEP8
            i_linha = 0
            # Salta 1 linha
            self._le_linha_com_backup(arq)
            # Lê a tabela
            while True:
                linha = self._le_linha_com_backup(arq)
                # Verifica se a tabela já acabou
                if len(linha) < 3:  # Tolerância a caracteres especiais
                    self.series[ree] = self.series[ree][:i_linha, :, :]
                    break
                # Senão, lê mais uma linha
                # Ano
                self.series[ree][i_linha, 0, cfg-1] = regi.le_registro(linha,
                                                                       0)
                # Energias de cada mês
                self.series[ree][i_linha,
                                 1:,
                                 cfg-1] = regf.le_linha_tabela(linha,
                                                               5,
                                                               2,
                                                               len(MESES))
                i_linha += 1

        # Variáveis auxiliares
        STR_CFG = "CONFIGURACAO No."
        # Identifica o REE e a primeira cfg no cabeçalho
        _identifica_ree()
        _identifica_cfg(cabecalho)

        ultima_cfg_lida = 0
        while True:
            # Confere se a leitura não acabou
            linha = self._le_linha_com_backup(arq)
            if LeituraPARp.str_fim_serie in linha:
                ree = self._ree_atual  # PEP8
                self.series[ree] = self.series[ree][:,
                                                    :,
                                                    :self._cfg_atual]
                break
            # Atualiza a última cfg quando for a linha devida
            if STR_CFG in linha:
                _identifica_cfg(linha)
            # Se for um cabeçalho de tabela, começa a ler
            if linha[8:11] == "JAN" and self._cfg_atual != ultima_cfg_lida:
                _le_tabela_serie()
                ultima_cfg_lida = self._cfg_atual

    def _le_medias(self,
                   arq: IO,
                   cabecalho: str = ""):
        """
        Lê as tabelas de séries de energia para uma REE.
        """

        def _identifica_ano_estudo(linha: str):
            """
            Identifica o ano de estudo em questão.
            """
            # Não pode usar uma leitura simples de registro
            # pois pode ter "POS" no lugar
            if STR_ANO in linha:
                ano = linha.split(STR_ANO)[1].strip()
                self._ano_atual = (ano if ano.isnumeric()
                                   else str(int(self._ano_atual) + 1))

        def _le_tabela_media() -> bool:
            """
            Lê uma tabela de médias anuais.
            """
            # Variáveis auxiliares
            reg = RegistroFn(9)
            i_linha = 0
            # Salta 1 linha
            self._le_linha_com_backup(arq)
            # Lê a tabela
            while True:
                # Verifica se a tabela já acabou
                linha = self._le_linha_com_backup(arq)
                if len(linha) < 3:  # Tolerância a caracteres especiais
                    self.medias[ree] = self.medias[ree][:i_linha,
                                                        :,
                                                        :]
                    return True
                # Senão, lê mais uma linha
                self.medias[ree][i_linha,
                                 :,
                                 i_ano] = reg.le_linha_tabela(linha,
                                                              5,
                                                              2,
                                                              len(MESES))
                i_linha += 1

        # Variáveis auxiliares
        STR_ANO = "ANO:"
        ree = self._ree_atual
        i_ano = 0
        ultimo_ano_lido = ""
        # Identifica o primeiro ano no cabeçalho
        _identifica_ano_estudo(cabecalho)
        while True:
            # Confere se a leitura não acabou
            linha = self._le_linha_com_backup(arq)
            if (LeituraPARp.str_inicio_correl_cruz in linha):
                self._configura_backup()
                self.medias[ree] = self.medias[ree][:,
                                                    :,
                                                    :i_ano]
                break
            # Atualiza a detecção de uma nova tabela
            _identifica_ano_estudo(linha)
            # Se existe uma nova tabela, lê
            if linha[8:11] == "JAN" and ultimo_ano_lido != self._ano_atual:
                _le_tabela_media()
                i_ano += 1
                ultimo_ano_lido = self._ano_atual

    def _le_correlograma(self,
                         arq: IO,
                         cabecalho: str = "") -> None:
        """
        """
        # Variáveis auxiliares
        ree = self._ree_atual
        i_mes = 0
        regi = RegistroIn(4)
        regf = RegistroFn(8)
        # Salta 2 linhas
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        # Lê a tabela
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3 or not linha[5:9].isnumeric():
                self.correl_p[ree] = self.correl_p[ree][:i_mes, :]
                break
            # Senão, lê mais uma linha
            # Ano
            self.correl_p[ree][i_mes,
                               0] = regi.le_registro(linha,
                                                     5)
            # Correlação de cada mês
            self.correl_p[ree][i_mes,
                               1:] = regf.le_linha_tabela(linha,
                                                          11,
                                                          2,
                                                          len(MESES) - 1)
            i_mes += 1

    def _le_correl_cruzada_media(self,
                                 arq: IO,
                                 cabecalho: str = ""):
        """
        """
        # Variáveis auxiliares
        ree = self._ree_atual
        i_mes = 0
        regi = RegistroIn(4)
        regf = RegistroFn(8)
        # Salta 4 linhas
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        # Lê a tabela
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3 or not linha[5:9].isnumeric():
                self.correl_c[ree] = self.correl_c[ree][:i_mes, :]
                break
            # Senão, lê mais uma linha
            # Ano
            self.correl_c[ree][i_mes,
                               0] = regi.le_registro(linha,
                                                     5)
            # Correlação de cada mês
            self.correl_c[ree][i_mes,
                               1:] = regf.le_linha_tabela(linha,
                                                          11,
                                                          2,
                                                          len(MESES))
            i_mes += 1

    def _le_ordens_finais_e_coefs(self,
                                  arq: IO,
                                  cabecalho: str = "") -> None:
        """
        Lê as informações das ordens e dos coeficientes do PAR(p).
        """
        n_anos = self._le_tabela_ordens(arq, self.ordens_f)
        self._le_coeficientes(arq, n_anos)

    def _le_ordens_originais(self,
                             arq: IO,
                             cabecalho: str = "") -> None:
        """
        Lê a tabela de ordens originais do modelo.
        """
        self._le_tabela_ordens(arq, self.ordens_o)

    def _le_tabela_ordens(self,
                          arq: IO,
                          ordens: Dict[int, np.ndarray]
                          ) -> int:
        """
        Retorna o número de anos de estudo válidos (Sem PRE).
        """

        def _identifica_ano_estudo(linha: str):
            """
            Identifica o ano de estudo em questão.
            """
            # Não pode usar uma leitura simples de registro
            # pois pode ter "POS" no lugar
            ano = linha[32:36]
            self._ano_atual = (ano if ano.isnumeric()
                               else str(int(self._ano_atual) + 1))

        # Variáveis auxiliares
        ree = self._ree_atual
        i_ano = 0
        reg = RegistroIn(3)
        # Salta 3 linhas
        for _ in range(3):
            self._le_linha_com_backup(arq)
        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se a tabela já acabou
            if len(linha) < 3:  # Tolerância a caracteres especiais
                ordens[ree] = ordens[ree][:i_ano, :]
                break
            # Extrai o ano
            _identifica_ano_estudo(linha)
            ordens[ree][i_ano, 0] = int(self._ano_atual)
            # As ordens de cada mês
            ordens[ree][i_ano,
                        1:] = reg.le_linha_tabela(linha,
                                                  38,
                                                  2,
                                                  len(MESES))
            i_ano += 1
        return i_ano

    def _le_coeficientes(self,
                         arq: IO,
                         n_anos: int) -> None:

        def _extrai_ordem_modelo(linha: str):
            """
            """
            return int(linha.split("AR(")[1][:-2])

        def _le_tabela_coeficientes():

            def _le_coefs_periodo():
                """
                """
                for o in range(2):
                    linha = self._le_linha_com_backup(arq)
                    self.coefs[ree][i_coefs,
                                    :ordem,
                                    o] = regf.le_linha_tabela(linha,
                                                              0,
                                                              2,
                                                              ordem)

            def _le_coef_media():
                """
                """
                for o in range(2, 4):
                    linha = self._le_linha_com_backup(arq)
                    # Se não possui dados de média, não lê
                    if len(linha) < 2:
                        break
                    self.coefs[ree][i_coefs,
                                    0,
                                    o] = regf.le_registro(linha,
                                                          0)

            # Variaveis auxiliares
            ree = self._ree_atual
            regf = RegistroFn(9)
            linha = ""
            # Procura pelo cabeçalho dos coeficientes do período
            while "COEFICIENTES DA EQUACAO" not in linha:
                linha = self._le_linha_com_backup(arq)
            ordem = _extrai_ordem_modelo(linha)
            _le_coefs_periodo()
            _le_coef_media()

        n_periodos = n_anos * len(MESES)
        for i_coefs in range(n_periodos):
            _le_tabela_coeficientes()

        self.coefs[self._ree_atual] = self.coefs[self._ree_atual][:n_periodos,
                                                                  :,
                                                                  :]

    def _le_correl_esp_anual(self,
                             arq: IO,
                             cabecalho: str = "") -> None:
        """
        """

        def _identifica_configuracao():
            """
            Identifica a configuração associada à tabela.
            """
            self._cfg_atual = int(cabecalho.split("No:")[1].strip())

        def _extrai_ordem_rees(linha: str) -> List[int]:
            """
            Obtém a ordem de disposição das REEs nas colunas.
            """
            str_rees = [s for s in linha.split(" ") if len(s) > 1]
            return [REES.index(s) for s in str_rees]

        def _ordena_correls(correls: List[float],
                            idx: List[int]):
            """
            """
            return [correls[idx.index(i)]
                    for i in range(len(idx))]

        reg = RegistroFn(7)
        _identifica_configuracao()
        cfg = self._cfg_atual
        # Salta 1 linha
        self._le_linha_com_backup(arq)
        idx = _extrai_ordem_rees(self._le_linha_com_backup(arq))
        i_ree = 0
        # Lê a tabela
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3:  # Tolerância a caracteres especiais
                break
            # Senão, lê mais uma linha
            correls = reg.le_linha_tabela(linha, 18, 6, len(MESES))
            self.correl_esp_a[cfg][idx[i_ree],
                                   :] = _ordena_correls(correls,
                                                        idx)
            i_ree += 1

    def _le_correl_esp_mensal(self,
                              arq: IO,
                              cabecalho: str = "") -> None:
        """
        """

        def _identifica_configuracao():
            """
            Identifica a configuração associada à tabela.
            """
            self._cfg_atual = int(cabecalho.split("No:")[1].strip())

        def _le_tabela_correl_esp_m(cabecalho: str):
            """
            """

            def _extrai_ordem_rees(linha: str) -> List[int]:
                """
                Obtém a ordem de disposição das REEs nas colunas.
                """
                str_rees = [s for s in linha.split(" ") if len(s) > 1]
                return [REES.index(s) for s in str_rees]

            def _ordena_correls(correls: List[float],
                                idx: List[int]):
                """
                """
                return [correls[idx.index(i)]
                        for i in range(len(idx))]

            # Variáveis auxiliares
            rega = RegistroAn(12)
            regf = RegistroFn(7)
            idx = _extrai_ordem_rees(cabecalho[18:])
            # Lê a tabela
            i_ree = 0
            while True:
                # Verifica se a tabela já acabou
                linha = self._le_linha_com_backup(arq)
                if len(linha) < 3:  # Tolerância a caracteres especiais
                    break
                # Senão, lê mais uma linha
                # Identifica a REE da linha
                ree = REES.index(rega.le_registro(linha, 0))
                cor = regf.le_linha_tabela(linha, 18, 6, len(MESES))
                self.correl_esp_m[self._cfg_atual][ree,
                                                   i_ree,
                                                   :] = _ordena_correls(cor,
                                                                        idx)
                i_ree += 1

        _identifica_configuracao()
        # Salta 1 linha
        self._le_linha_com_backup(arq)
        # Lê a tabela
        i_tabela = 0
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if (LeituraPARp.str_inicio_correl_esp_a in linha or
                    self._fim_arquivo(linha)):
                break

            # Senão, procura e lê mais uma tabela
            if "MES" not in linha:
                continue

            _le_tabela_correl_esp_m(linha)
            i_tabela += 1

        self._configura_backup()
