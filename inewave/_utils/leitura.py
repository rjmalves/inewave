from abc import abstractmethod
from typing import Any, IO, List, Dict
import os
import pandas as pd  # type: ignore
from traceback import print_exc

from inewave._utils.bloco import Bloco
from .dadosarquivo import DadosArquivo


class Leitura:
    """
    Classe com utilidades gerais para leitura de arquivos
    do NEWAVE.
    """
    def __init__(self,
                 diretorio: str):
        self._usa_backup = False
        self._linha_backup = ""
        self._diretorio = diretorio
        self._linhas_fora_blocos: Dict[int, str] = {}
        self._blocos: List[Bloco] = []
        self._dados: Any = None

    def _le_linha_com_backup(self, arq: IO) -> str:
        """
        Faz uma leitura de linha de um arquivo, mas com a opção de usar
        um backup de leitura anterior sinalizado anteriormente.
        """
        linha = ""
        if self._usa_backup:
            self._usa_backup = False
            linha = self._linha_backup
        else:
            linha = arq.readline()
            self._linha_backup = linha
        return linha

    def _configura_backup(self):
        """
        Prepara a próxima leitura para ser uma feita a partir de um
        backup armazenado.
        """
        self._usa_backup = True

    def _lista_arquivos_por_chave(self, chave: str) -> List[str]:
        """
        Retorna a lista de caminhos completos para os arquivos em um
        diretório, desde que tenham uma certa chave no nome.
        """
        return [f for f in os.listdir(self._diretorio) if chave in f]

    def _verifica_inicio_blocos(self,
                                linha: str,
                                ordem: int,
                                blocos: List[Bloco]) -> bool:
        """
        Verifica se a linha atual é a linha de início de algum
        dos blocos a serem lidos.
        """
        for i, b in enumerate(blocos):
            if b.e_inicio_de_bloco(linha):
                return b.inicia_bloco(linha, ordem)

        self._linhas_fora_blocos[ordem] = linha
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

    def _le_blocos_arquivo(self, arq: IO):
        """
        Faz a leitura dos blocos de dados do arquivo.
        """
        self._blocos = self._cria_blocos_leitura()
        linha = ""
        i = 0
        while True:
            # Decide se lê uma linha nova ou usa a última lida
            linha = self._le_linha_com_backup(arq)
            if self._fim_arquivo(linha):
                self._prepara_dados_saida()
                break

            self._verifica_inicio_blocos(linha, i, self._blocos)
            # Caso a função de leitura retorne True, é configurado
            #  o backup da linha atual.
            bkp = self._le_blocos_encontrados(arq, self._blocos)
            if bkp:
                self._linha_backup = bkp
                self._configura_backup()
            i += 1

    def _le_arquivo_em_diretorio(self,
                                 diretorio: str,
                                 nome_arquivo: str) -> None:
        """
        Faz a leitura do arquivo em um diretorio.
        """
        try:
            caminho = os.path.join(diretorio, nome_arquivo)
            with open(caminho, "r") as arq:
                self._le_blocos_arquivo(arq)
        except Exception:
            print_exc()

    @abstractmethod
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Método que cria a lista de blocos a serem lidos no arquivo.
        Implementa o Factory Pattern.
        """
        pass

    def _prepara_dados_saida(self):
        """
        Trata os dados obtidos do arquivo para ser retornado.
        """
        self._blocos = [b for b in self._blocos
                        if b.concluido]

    def _fim_arquivo(self, linha: str) -> bool:
        """
        Método que deve ser implementado para cada arquivo, com o
        conteúdo da linha que indica o fim do próprio, para impedir loops
        de leitura eterna.
        """
        return len(linha) == 0

    def le_arquivo(self, nome_arquivo: str) -> DadosArquivo:
        """
        Método para ler um arquivo e retornar o objeto
        devido da classe em particular.
        """
        self._le_arquivo_em_diretorio(self._diretorio,
                                      nome_arquivo)
        return DadosArquivo(self._blocos,
                            self._linhas_fora_blocos)

    @property
    def dados(self) -> Any:
        """
        Dados de leitura obtidos pelo blocos, organizados
        para realizar a criação do objeto associado.
        """
        return self._dados


class LeituraCSV:
    """
    Classe com utilidades gerais para leitura de arquivos
    .csv do NEWAVE.
    """
    def __init__(self,
                 diretorio: str):
        self._diretorio = diretorio
        self._dados = pd.DataFrame()

    def _le_tabela_arquivo(self, caminho: str):
        """
        Faz a leitura dos blocos de dados do arquivo.
        """
        self._dados = pd.read_csv(caminho,
                                  sep=",",
                                  encoding="utf-8",
                                  index_col=1)

    def _le_arquivo_em_diretorio(self,
                                 diretorio: str,
                                 nome_arquivo: str) -> None:
        """
        Faz a leitura do arquivo em um diretorio.
        """
        try:
            caminho = os.path.join(diretorio, nome_arquivo)
            self._le_tabela_arquivo(caminho)
            self.processa_dados_lidos()
        except Exception:
            print_exc()

    def le_arquivo(self, nome_arquivo: str) -> pd.DataFrame:
        """
        Método para ler um arquivo e retornar o objeto
        devido da classe em particular.
        """
        self._le_arquivo_em_diretorio(self._diretorio,
                                      nome_arquivo)
        return self._dados

    @abstractmethod
    def processa_dados_lidos(self):
        """
        """
        pass

    @property
    def dados(self) -> pd.DataFrame:
        """
        Dados de leitura obtidos pelo blocos, organizados
        para realizar a criação do objeto associado.
        """
        return self._dados
