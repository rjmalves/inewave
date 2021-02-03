# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO, MESES, REES, ORDEM_MAX_PARP
from inewave.newave.modelos.parp import PARp
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO, Dict, Tuple


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
    str_inicio_serie = "SERIE  DE ENERGIAS DO REE"
    str_inicio_ordens = "ORDEM FINAL DO MODELO AUTORREGRESSIVO"
    str_fim_serie = "CORRELOGRAMO"
    str_fim_coefs = "SERIE DE RUIDOS"
    str_fim_parp = "////////////////////"

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # PARp default, depois é substituído
        self.parp = PARp({}, {}, {})

    def le_arquivo(self) -> PARp:
        """
        Faz a leitura do arquivo `parp.dat`.
        """
        try:
            caminho = os.path.join(self.diretorio, "parp.dat")
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
        achou_series = False
        achou_ordens_coefs = False
        leu_series = False
        leu_ordens_coefs = False
        leu_rees = {i: False for i in range(1, len(REES) + 1)}
        ree = 0
        linha = ""
        # Variáveis para armazenar os componentes do PARp, que será
        # construído quando acabar a leitura
        n_meses = len(MESES)
        series: Dict[int, np.ndarray] = {i: np.zeros((100,
                                                      n_meses + 1,
                                                      100))
                                         for i in range(1,
                                                        len(REES) + 1)}
        ordens: Dict[int, np.ndarray] = {i: np.zeros((MAX_ANOS_ESTUDO,
                                                      n_meses + 1),
                                                     dtype=np.int32)
                                         for i in range(1,
                                                        len(REES) + 1)}
        n_linhas_coefs = MAX_ANOS_ESTUDO * n_meses
        coefs: Dict[int, np.ndarray] = {i: np.zeros((n_linhas_coefs,
                                                     ORDEM_MAX_PARP,
                                                     2))
                                        for i in range(1,
                                                       len(REES) + 1)}

        while True:
            # Decide se lê uma linha nova ou usa a última lida
            linha = self._le_linha_com_backup(arq)
            if self._fim_arquivo(linha):
                self.parp = PARp(ordens, coefs, series)
                break
            # Verifica se terminou de ler tudo sobre uma REE
            # e reseta as flags
            if leu_ordens_coefs and leu_series:
                leu_ordens_coefs = False
                leu_series = False
                leu_rees[ree] = True
            # Condição para iniciar uma leitura de dados
            if not achou_series and not leu_series:
                achou = LeituraPARp.str_inicio_serie in linha
                achou_series = achou
                if achou:
                    self._configura_backup()
            if not achou_ordens_coefs and not leu_ordens_coefs:
                achou = LeituraPARp.str_inicio_ordens in linha
                achou_ordens_coefs = achou
            # Quando achar, le cada parte adequadamente
            if achou_series:
                ree = self._le_series(arq, series)
                achou_series = False
                leu_series = True
            if achou_ordens_coefs:
                self._le_ordens_coefs(arq,
                                      ree,
                                      ordens,
                                      coefs)
                achou_ordens_coefs = False
                leu_ordens_coefs = True

        return self.parp

    def _le_series(self,
                   arq: IO,
                   series: Dict[int, np.ndarray]) -> int:
        """
        Lê as tabelas de séries de energia para uma REE.
        """
        ree = 0
        cfg = 0
        achou = False
        while True:
            # Confere se a leitura não acabou
            linha = self._le_linha_com_backup(arq)
            if LeituraPARp.str_fim_serie in linha:
                series[ree] = series[ree][:, :, :cfg]
                break
            # Senão, lê mais uma tabela
            if not achou:
                achou = LeituraPARp.str_inicio_serie in linha
                if achou:
                    self._configura_backup()
                continue
            if achou:
                self._configura_backup()
                ree, cfg = self._le_tabela_serie(arq, series)
                achou = False
        return ree

    def _le_tabela_serie(self,
                         arq: IO,
                         series: Dict[int, np.ndarray]
                         ) -> Tuple[int, int]:
        """
        """
        # Lê a linha do backup para descobrir a REE
        linha = self._le_linha_com_backup(arq)
        str_ree = linha.split("REE")[1][:16].strip()
        ree = REES.index(str_ree) + 1
        # Descobre a configuração
        cfg = int(linha.split("CONFIGURACAO No.")[1][:-2].strip())
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
            if len(linha) < 3 or "MEDIA AMOSTRAL DAS ENERGIAS" in linha:
                series[ree] = series[ree][:i, :, :]
                return ree, cfg
            # Senão, lê mais uma linha
            # Ano
            series[ree][i, 0, cfg-1] = int(linha[:4])
            # Energias de cada mês
            ci = 5
            nc = 9
            for j in range(n_meses):
                cf = ci + nc
                series[ree][i, j+1, cfg-1] = float(linha[ci:cf])
                ci = cf + 2
            i += 1

    def _le_ordens_coefs(self,
                         arq: IO,
                         ree: int,
                         ordens: Dict[int, np.ndarray],
                         coefs: Dict[int, np.ndarray]):
        """
        Lê as informações das ordens e dos coeficientes do PAR(p).
        """
        n_anos = self._le_tabela_ordens(arq, ree, ordens)
        self._le_coeficientes(arq, ree, coefs, n_anos)

    def _le_tabela_ordens(self,
                          arq: IO,
                          ree: int,
                          ordens: Dict[int, np.ndarray]
                          ) -> int:
        """
        Retorna o número de anos de estudo válidos (sem POS).
        """
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
                         ree: int,
                         coefs: Dict[int, np.ndarray],
                         n_anos: int):
        i = 0
        n_meses = len(MESES)
        while True:
            linha = self._le_linha_com_backup(arq)
            # Verifica se a leitura dos coeficientes já não terminou
            if LeituraPARp.str_fim_coefs in linha or i == n_anos * n_meses:
                coefs[ree] = coefs[ree][:i, :, :]
                break
            # Senão, lê mais uma tabela de coeficientes
            self._le_tabela_coeficientes(arq, ree, coefs, i)
            i += 1

    def _le_tabela_coeficientes(self,
                                arq: IO,
                                ree: int,
                                coefs: Dict[int, np.ndarray],
                                i: int):
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
            if lin == 2:
                break
            if achou:
                ci = 0
                nc = 9
                for j in range(ordem):
                    cf = ci + nc
                    coefs[ree][i, j, lin] = float(linha[ci:cf])
                    ci = cf + 2
                lin += 1

    def _fim_arquivo(self, linha: str) -> bool:
        return LeituraPARp.str_fim_parp in linha
