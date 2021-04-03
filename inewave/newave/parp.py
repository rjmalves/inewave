# Imports do próprio módulo
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO, MESES, REES, ORDEM_MAX_PARP
from inewave.newave.modelos.parp import PARp
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from copy import deepcopy, copy
from traceback import print_exc
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
                               self._le_tabela_correlograma)
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
                                  self._le_tabela_correl_cruzada)
        correl_esp_anual = Bloco(LeituraPARp.str_inicio_correl_esp_a,
                                 "",
                                 True,
                                 self._le_tabela_correl_esp_a)
        correl_esp_mensal = Bloco(LeituraPARp.str_inicio_correl_esp_m,
                                  "",
                                  True,
                                  self._le_tabelas_correl_esp_m)
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
        MAX_CFGS = 60
        correls_esp_anuais = [copy(correl_esp_anual)
                              for _ in range(MAX_CFGS)]
        correls_esp_mensais = [copy(correl_esp_mensal)
                               for _ in range(MAX_CFGS)]
        return [*series_energia,
                *series_correls,
                *series_ordens_finais_coefs,
                *series_ordens_originais,
                *series_medias,
                *correls_cruzada_media,
                *correls_esp_anuais,
                *correls_esp_mensais]

    def _verifica_inicio_blocos(self,
                                linha: str,
                                blocos: List[Bloco]) -> bool:
        """
        Verifica se a linha atual é a linha de início de algum
        dos blocos a serem lidos.
        """
        for i, b in enumerate(blocos):
            if b.e_inicio_de_bloco(linha):
                return b.inicia_bloco(linha)
        return False

    def _le_blocos_encontrados(self,
                               arq: IO,
                               blocos: List[Bloco],
                               *args):
        """
        Faz a leitura dos blocos encontrados até o momento e que
        ainda não foram lidos.
        """
        for i, b in enumerate(blocos):
            if b.encontrado:
                return b.le_bloco(arq, *args)

    def _inicia_variaveis_leitura(self):
        """
        Inicia variáveis temporárias que são escritas durante
        a leitura do arquivo.
        """
        self._ree_atual = 0
        self._cfg_atual = 0
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
        self.correl_esp_a: Dict[int, np.ndarray] = {i: np.zeros((len(REES),
                                                                 len(REES)))
                                                    for i in range(100)}
        self.correl_esp_m: Dict[int, np.ndarray] = {i: np.zeros((len(REES),
                                                                 len(MESES),
                                                                 len(REES)))
                                                    for i in range(100)}

    def le_arquivo(self, nome_arquivo="parp.dat") -> PARp:
        """
        Faz a leitura do arquivo `parp.dat`.
        """
        try:
            caminho = os.path.join(self.diretorio, nome_arquivo)
            with open(caminho, "r") as arq:
                self.parp = self._le_parp(arq)
                return self.parp
        except Exception:
            print_exc()
            return self.parp

    def _le_parp(self, arq: IO) -> PARp:
        """
        Faz a leitura do arquivo parp.dat.
        """
        blocos = self._cria_blocos_leitura()
        self._inicia_variaveis_leitura()
        linha = ""
        while True:
            # Decide se lê uma linha nova ou usa a última lida
            linha = self._le_linha_com_backup(arq)
            self._verifica_inicio_blocos(linha, blocos)
            if self._fim_arquivo(linha):
                # Limpa as correls_esp_a e correl_esp_m com apenas as
                # cfgs lidas
                cfgs_lidas = list(range(self._cfg_atual, 60))
                for i in cfgs_lidas:
                    self.correl_esp_a.pop(i)
                    self.correl_esp_m.pop(i)
                # Cria o objeto parp completo
                self.parp = PARp(deepcopy(self.ordens_o),
                                 deepcopy(self.ordens_f),
                                 deepcopy(self.coefs),
                                 deepcopy(self.series),
                                 deepcopy(self.correl_p),
                                 deepcopy(self.medias),
                                 deepcopy(self.correl_c),
                                 deepcopy(self.correl_esp_a),
                                 deepcopy(self.correl_esp_m))
                break

            self._le_blocos_encontrados(arq, blocos)

        return self.parp

    def _le_series(self,
                   arq: IO,
                   cabecalho: str = "") -> None:
        """
        Lê as tabelas de séries de energia para uma REE.
        """
        # Variáveis auxiliares
        STR_CFG = "CONFIGURACAO No."
        # Identifica o REE e a primeira cfg no cabeçalho
        str_ree = cabecalho.split("REE")[1][:16].strip()
        ree = REES.index(str_ree) + 1
        self._ree_atual = ree
        cfg_tmp = int(cabecalho.split(STR_CFG)[1][:-2].strip())
        self._cfg_atual = cfg_tmp
        cfg_lida = 0
        while True:
            # Confere se a leitura não acabou
            linha = self._le_linha_com_backup(arq)
            if LeituraPARp.str_fim_serie in linha:
                self.series[ree] = self.series[ree][:, :, :cfg_tmp]
                break
            # Atualiza a última cfg_tmp quando for a linha devida
            if STR_CFG in linha:
                cfg_tmp = int(linha.split(STR_CFG)[1][:-2].strip())
                self._cfg_atual = cfg_tmp
            # Se for um cabeçalho de tabela, começa a ler
            if linha[8:11] == "JAN" and self._cfg_atual != cfg_lida:
                self._le_tabela_serie(arq)
                cfg_lida = self._cfg_atual

    def _le_medias(self,
                   arq: IO,
                   cabecalho: str = ""):
        """
        Lê as tabelas de séries de energia para uma REE.
        """
        # Variáveis auxiliares
        STR_ANO = "ANO:"
        ree = self._ree_atual
        # Identifica o primeiro ano no cabeçalho
        str_ano = cabecalho.split(STR_ANO)[1].strip()
        ind_ano = 0
        str_ano_lido = ""
        acabou = False
        while True:
            # Confere se a leitura não acabou
            linha = self._le_linha_com_backup(arq)
            if LeituraPARp.str_inicio_correl_cruz in linha or acabou:
                self._configura_backup()
                print(ind_ano)
                self.medias[ree] = self.medias[ree][:, :, :ind_ano]
                break
            # Atualiza o ano lido quando for a linha devida
            if STR_ANO in linha:
                str_ano = linha.split(STR_ANO)[1].strip()
                if not str_ano.isnumeric():
                    acabou = True
            if (linha[8:11] == "JAN" and
                    str_ano_lido != str_ano and
                    not acabou):
                self._le_tabela_media(arq, ind_ano)
                ind_ano += 1
                str_ano_lido = str_ano

    def _le_tabela_serie(self,
                         arq: IO):
        """
        """
        ree = self._ree_atual
        cfg = self._cfg_atual
        # Salta 1 linha
        self._le_linha_com_backup(arq)
        # Lê a tabela
        i = 0
        n_meses = len(MESES)
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3 or "MEDIA AMOSTRAL DAS ENERGIAS" in linha:
                self.series[ree] = self.series[ree][:i, :, :]
                break
            # Senão, lê mais uma linha
            # Ano
            self.series[ree][i, 0, cfg-1] = int(linha[:4])
            # Energias de cada mês
            ci = 5
            nc = 9
            for j in range(n_meses):
                cf = ci + nc
                self.series[ree][i, j+1, cfg-1] = float(linha[ci:cf])
                ci = cf + 2
            i += 1

    def _le_tabela_correlograma(self,
                                arq: IO,
                                cabecalho: str = "") -> None:
        """
        """
        ree = self._ree_atual
        # Salta 2 linhas
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        # Lê a tabela
        i = 0
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3 or not linha[5:9].isnumeric():
                self.correl_p[ree] = self.correl_p[ree][:i, :]
                break
            # Senão, lê mais uma linha
            # Ano
            self.correl_p[ree][i, 0] = int(linha[5:9])
            # Correlação de cada mês
            ci = 11
            nc = 8
            for j in range(len(MESES) - 1):
                cf = ci + nc
                self.correl_p[ree][i, j+1] = float(linha[ci:cf])
                ci = cf + 2
            i += 1

    def _le_tabela_correl_cruzada(self,
                                  arq: IO,
                                  cabecalho: str = ""):
        """
        """
        ree = self._ree_atual
        # Salta 4 linhas
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        # Lê a tabela
        i = 0
        n_meses = len(MESES)
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3 or not linha[5:9].isnumeric():
                self.correl_c[ree] = self.correl_c[ree][:i, :]
                break
            # Senão, lê mais uma linha
            # Ano
            self.correl_c[ree][i, 0] = int(linha[5:9])
            # Correlação de cada mês
            ci = 11
            nc = 8
            for j in range(n_meses):
                cf = ci + nc
                self.correl_c[ree][i, j+1] = float(linha[ci:cf])
                ci = cf + 2
            i += 1

    def _le_tabela_media(self,
                         arq: IO,
                         ind_ano: int
                         ) -> bool:
        """
        """
        ree = self._ree_atual
        # Salta 1 linha
        self._le_linha_com_backup(arq)
        # Lê a tabela
        i = 0
        n_meses = len(MESES)
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3:
                self.medias[ree] = self.medias[ree][:i, :, :]
                return True
            # Senão, lê mais uma linha
            ci = 5
            nc = 9
            for j in range(n_meses):
                cf = ci + nc
                self.medias[ree][i, j, ind_ano] = float(linha[ci:cf])
                ci = cf + 2
            i += 1

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
        Retorna o número de anos de estudo válidos (sem POS).
        """
        ree = self._ree_atual
        # Salta 3 linhas
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        i = 0
        n_meses = len(MESES)
        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se a tabela já acabou
            if len(linha) < 3:
                ordens[ree] = ordens[ree][:i, :]
                break
            # Extrai o ano
            str_ano = linha[32:36]
            if not str_ano.isnumeric():
                continue
            ordens[ree][i, 0] = int(str_ano)
            # As ordens de cada mês
            ci = 38
            nc = 3
            for j in range(1, n_meses + 1):
                cf = ci + nc
                ordens[ree][i, j] = int(linha[ci:cf])
                ci = cf + 2
            i += 1
        return i

    def _le_coeficientes(self,
                         arq: IO,
                         n_anos: int) -> None:
        ree = self._ree_atual
        i = 0
        n_meses = len(MESES)
        while True:
            linha = self._le_linha_com_backup(arq)
            # Verifica se a leitura dos coeficientes já não terminou
            if LeituraPARp.str_fim_coefs in linha or i == n_anos * n_meses:
                self.coefs[ree] = self.coefs[ree][:i, :, :]
                break
            # Senão, lê mais uma tabela de coeficientes
            self._le_tabela_coeficientes(arq, i)
            i += 1

    def _le_tabela_coeficientes(self,
                                arq: IO,
                                i: int):
        ree = self._ree_atual
        achou = False
        ordem = 0
        lin = 0
        while True:
            linha = self._le_linha_com_backup(arq)
            if not achou:
                # Procura pela ordem do modelo
                if "COEFICIENTES DA EQUACAO" in linha:
                    achou = True
                    ordem = int(linha.split("AR(")[1][:-2])
                continue
            if lin == 4 or len(linha) < 2:
                break
            if achou:
                ci = 0
                nc = 9
                if lin < 2:
                    for j in range(ordem):
                        cf = ci + nc
                        self.coefs[ree][i, j, lin] = float(linha[ci:cf])
                        ci = cf + 2
                else:
                    self.coefs[ree][i, 0, lin] = float(linha[ci:cf])
                lin += 1

    def _le_tabela_correl_esp_a(self,
                                arq: IO,
                                cabecalho: str = "") -> None:
        """
        """
        str_cfg = cabecalho.split("No:")[1].strip()
        # Descobre a configuração
        self._cfg_atual = int(str_cfg)
        cfg = self._cfg_atual
        # Salta 1 linhas
        self._le_linha_com_backup(arq)
        linha = self._le_linha_com_backup(arq)
        # Descobre a ordem das REEs nas colunas
        str_rees = [s for s in linha.split(" ") if len(s) > 1]
        ordem_rees = [REES.index(s) + 1 for s in str_rees]
        # Lê a tabela
        i = 0
        n_meses = len(MESES)
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3:
                break
            # Senão, lê mais uma linha
            ci = 18
            nc = 7
            for j in range(n_meses):
                cf = ci + nc
                self.correl_esp_a[cfg][ordem_rees[i]-1,
                                       ordem_rees[j]-1] = float(linha[ci:cf])
                ci = cf + 6
            i += 1

    def _le_tabelas_correl_esp_m(self,
                                 arq: IO,
                                 cabecalho: str = "") -> None:
        """
        """
        str_cfg = cabecalho.split("No:")[1].strip()
        # Descobre a configuração
        self._cfg_atual = int(str_cfg)
        # Salta 1 linha
        self._le_linha_com_backup(arq)
        # Lê a tabela
        i = 0
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if (LeituraPARp.str_inicio_correl_esp_a in linha or
                    LeituraPARp.str_fim_parp in linha):
                self._configura_backup()
                break
            # Senão, procura e lê mais uma tabela
            if "MES" in linha:
                self._configura_backup()
                self._le_tabela_correl_esp_m(arq)
                i += 1

    def _le_tabela_correl_esp_m(self,
                                arq: IO):
        """
        """
        linha = self._le_linha_com_backup(arq)
        # Descobre a ordem das REEs nas colunas
        str_rees = [s for s in linha[18:].split(" ") if len(s) > 1]
        ordem_rees = [REES.index(s) for s in str_rees]
        # Lê a tabela
        i = 0
        while True:
            # Verifica se a tabela já acabou
            linha = self._le_linha_com_backup(arq)
            if len(linha) < 3:
                break
            # Senão, lê mais uma linha
            # Identifica a REE da linha
            ree_linha = REES.index(linha[:12].strip())
            ci = 18
            nc = 7
            for j in ordem_rees:
                cf = ci + nc
                self.correl_esp_m[self._cfg_atual][ree_linha,
                                                   i,
                                                   j] = float(linha[ci:cf])
                ci = cf + 6
            i += 1

    def _fim_arquivo(self, linha: str) -> bool:
        return LeituraPARp.str_fim_parp in linha
