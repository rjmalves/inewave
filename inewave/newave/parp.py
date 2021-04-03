# Imports do próprio módulo
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO, MESES, REES, ORDEM_MAX_PARP
from inewave.newave.modelos.parp import PARp
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from copy import deepcopy
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
        series_energia = Bloco(LeituraPARp.str_inicio_serie,
                               LeituraPARp.str_fim_serie,
                               True,
                               self._le_series
                               )
        return [series_energia]

    def _verifica_inicio_blocos(self,
                                linha: str,
                                blocos: List[Bloco]) -> bool:
        """
        Verifica se a linha atual é a linha de início de algum
        dos blocos a serem lidos.
        """
        return any([b.inicio_bloco(linha) for b in blocos])

    def _le_blocos_encontrados(self,
                               arq: IO,
                               blocos: List[Bloco],
                               *args):
        """
        Faz a leitura dos blocos encontrados até o momento e que
        ainda não foram lidos.
        """
        for b in blocos:
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
        achou_correl_parc = False
        achou_ordens_o_coefs = False
        achou_ordens_f_coefs = False
        achou_medias = False
        achou_correl_cruz = False
        achou_correl_esp_a = False
        achou_correl_esp_m = False
        leu_correl_parc = False
        leu_ordens_o_coefs = False
        leu_ordens_f_coefs = False
        leu_medias = False
        leu_correl_cruz = False
        leu_rees = {i: False for i in range(1, len(REES) + 1)}
        ultima_cfg_lida = 0
        linha = ""
        # Variáveis para armazenar os componentes do PARp, que será
        # construído quando acabar a leitura

        while True:
            # Decide se lê uma linha nova ou usa a última lida
            linha = self._le_linha_com_backup(arq)
            self._verifica_inicio_blocos(linha, blocos)
            if self._fim_arquivo(linha):
                # Limpa as correls_esp_a e correl_esp_m com apenas as
                # cfgs lidas
                cfgs_lidas = list(range(1, ultima_cfg_lida + 1))
                for i in range(100):
                    if i not in cfgs_lidas:
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
            # Verifica se terminou de ler tudo sobre uma REE
            # e reseta as flags
            if all([leu_ordens_f_coefs,
                    leu_correl_parc]) and all([b.concluido for b in blocos]):
                leu_ordens_o_coefs = False
                leu_ordens_f_coefs = False
                leu_correl_parc = False
                leu_medias = False
                leu_correl_cruz = False
                leu_rees[self._ree_atual] = True
            # Condição para iniciar uma leitura de dados
            self._le_blocos_encontrados(arq, blocos)
            if not achou_correl_parc and not leu_correl_parc:
                achou = LeituraPARp.str_inicio_correl_parc in linha
                achou_correl_parc = achou
            if not achou_ordens_o_coefs and not leu_ordens_o_coefs:
                achou = LeituraPARp.str_inicio_ordens_o in linha
                achou_ordens_o_coefs = achou
            if not achou_ordens_f_coefs and not leu_ordens_f_coefs:
                achou = LeituraPARp.str_inicio_ordens_f in linha
                achou_ordens_f_coefs = achou
            if not achou_medias and not leu_medias:
                achou = LeituraPARp.str_inicio_media in linha
                achou_medias = achou
                if achou:
                    self._configura_backup()
            if not achou_correl_cruz and not leu_correl_cruz:
                achou = LeituraPARp.str_inicio_correl_cruz in linha
                achou_correl_cruz = achou
            if not achou_correl_esp_a:
                achou = LeituraPARp.str_inicio_correl_esp_a in linha
                achou_correl_esp_a = achou
                if achou:
                    self._configura_backup()
            if not achou_correl_esp_m:
                achou = LeituraPARp.str_inicio_correl_esp_m in linha
                achou_correl_esp_m = achou
                if achou:
                    self._configura_backup()
            # Quando achar, le cada parte adequadamente
            if achou_correl_parc:
                self._le_tabela_correlograma(arq)
                achou_correl_parc = False
                leu_correl_parc = True
            if achou_ordens_o_coefs:
                self._le_ordens_originais(arq)
                achou_ordens_o_coefs = False
                leu_ordens_o_coefs = True
            if achou_ordens_f_coefs:
                self._le_ordens_finais_e_coefs(arq)
                achou_ordens_f_coefs = False
                leu_ordens_f_coefs = True
            if achou_medias:
                self._le_medias(arq)
                achou_medias = False
                leu_medias = True
            if achou_correl_cruz:
                self._le_tabela_correl_cruzada(arq)
                achou_correl_cruz = False
                leu_correl_cruz = True
            if achou_correl_esp_a:
                ultima_cfg_lida = self._le_tabela_correl_esp_a(arq)
                achou_correl_esp_a = False
            if achou_correl_esp_m:
                self._le_tabelas_correl_esp_m(arq)
                achou_correl_esp_m = False

        return self.parp

    def _le_series(self,
                   arq: IO,
                   cabecalho: str) -> None:
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
            if linha[8:11] == "JAN" and cfg_tmp != cfg_lida:
                self._le_tabela_serie(arq)
                cfg_lida = self._cfg_atual

    def _le_medias(self,
                   arq: IO):
        """
        Lê as tabelas de séries de energia para uma REE.
        """
        ree = self._ree_atual
        ind_ano = 0
        achou = False
        acabou = False
        while True:
            # Confere se a leitura não acabou
            linha = self._le_linha_com_backup(arq)
            if LeituraPARp.str_inicio_correl_cruz in linha or acabou:
                self._configura_backup()
                self.medias[ree] = self.medias[ree][:, :, :ind_ano]
                break
            # Senão, lê mais uma tabela
            if not achou:
                achou = LeituraPARp.str_inicio_media in linha
                if achou:
                    self._configura_backup()
                continue
            if achou:
                self._configura_backup()
                if self._le_tabela_media(arq, ind_ano):
                    ind_ano += 1
                else:
                    acabou = True
                achou = False

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
        print(cfg)
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
                                arq: IO):
        """
        """
        ree = self._ree_atual
        # Salta 2 linhas
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        # Lê a tabela
        i = 0
        n_meses = len(MESES)
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
            for j in range(n_meses - 1):
                cf = ci + nc
                self.correl_p[ree][i, j+1] = float(linha[ci:cf])
                ci = cf + 2
            i += 1

    def _le_tabela_correl_cruzada(self,
                                  arq: IO):
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
                         ind_ano: int,
                         ) -> bool:
        """
        """
        ree = self._ree_atual
        # Lê a linha do backup para descobrir o ano
        linha = self._le_linha_com_backup(arq)
        str_ano = linha.split("ANO:")[1].strip()
        # Se é um ano de pós estudo, ignora
        if not str_ano.isnumeric():
            return False
        # Salta 5 linhas
        self._le_linha_com_backup(arq)
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
                                  arq: IO):
        """
        Lê as informações das ordens e dos coeficientes do PAR(p).
        """
        n_anos = self._le_tabela_ordens(arq, self.ordens_f)
        self._le_coeficientes(arq, n_anos)

    def _le_ordens_originais(self,
                             arq: IO):
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
                         n_anos: int):
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
                                arq: IO) -> int:
        """
        """
        # Lê a linha do backup para descobrir a configuração
        self._configura_backup()
        linha = self._le_linha_com_backup(arq)
        str_cfg = linha.split("No:")[1].strip()
        # Descobre a configuração
        cfg = int(str_cfg)
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
                return cfg
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
                                 arq: IO):
        """
        """
        # Lê a linha do backup para descobrir a configuração
        self._configura_backup()
        linha = self._le_linha_com_backup(arq)
        str_cfg = linha.split("No:")[1].strip()
        # Descobre a configuração
        cfg = int(str_cfg)
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
                return cfg
            # Senão, procura e lê mais uma tabela
            if "MES" in linha:
                self._configura_backup()
                self._le_tabela_correl_esp_m(arq,
                                             cfg)
                i += 1

    def _le_tabela_correl_esp_m(self,
                                arq: IO,
                                cfg: int):
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
                self.correl_esp_m[cfg][ree_linha,
                                       i,
                                       j] = float(linha[ci:cf])
                ci = cf + 6
            i += 1

    def _fim_arquivo(self, linha: str) -> bool:
        return LeituraPARp.str_fim_parp in linha
