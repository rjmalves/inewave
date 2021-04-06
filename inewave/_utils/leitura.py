from abc import abstractmethod
from typing import Any, IO, List
import os
from traceback import print_exc

from inewave._utils.bloco import Bloco


class Leitura:
    """
    Classe com utilidades gerais para leitura de arquivos
    do NEWAVE.
    """
    def __init__(self):
        self.usa_backup = False
        self.linha_backup = ""
        self.diretorio = ""

    def _le_linha_com_backup(self, arq: IO) -> str:
        """
        Faz uma leitura de linha de um arquivo, mas com a opção de usar
        um backup de leitura anterior sinalizado anteriormente.
        """
        linha = ""
        if self.usa_backup:
            self.usa_backup = False
            linha = self.linha_backup
        else:
            linha = arq.readline()
            self.linha_backup = linha
        return linha

    def _configura_backup(self):
        """
        Prepara a próxima leitura para ser uma feita a partir de um
        backup armazenado.
        """
        self.usa_backup = True

    def _lista_arquivos_por_chave(self, chave: str) -> List[str]:
        """
        Retorna a lista de caminhos completos para os arquivos em um
        diretório, desde que tenham uma certa chave no nome.
        """
        return [f for f in os.listdir(self.diretorio) if chave in f]

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

    def _le_blocos_arquivo(self, arq: IO):
        """
        Faz a leitura dos blocos de dados do arquivo.
        """
        blocos = self._cria_blocos_leitura()
        self._inicia_variaveis_leitura()
        linha = ""
        while True:
            # Decide se lê uma linha nova ou usa a última lida
            linha = self._le_linha_com_backup(arq)
            self._verifica_inicio_blocos(linha, blocos)

            if self._fim_arquivo(linha):
                self._prepara_dados_arquivo()
                break

            self._le_blocos_encontrados(arq, blocos)

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

    # @abstractmethod
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Método que cria a lista de blocos a serem lidos no arquivo.
        Implementa o Factory Pattern.
        """
        pass

    # @abstractmethod
    def _inicia_variaveis_leitura(self):
        """
        Inicia variáveis temporárias que são escritas durante
        a leitura do arquivo.
        """
        pass

    # @abstractmethod
    def _prepara_dados_saida(self):
        """
        Trata os dados obtidos do arquivo para ser retornado.
        """
        pass

    @abstractmethod
    def _fim_arquivo(self, linha: str) -> bool:
        """
        Método que deve ser implementado para cada arquivo, com o
        conteúdo da linha que indica o fim do próprio, para impedir loops
        de leitura eterna.
        """
        pass

    # @abstractmethod
    def le_arquivo(self, nome_arquivo: str) -> Any:
        """
        Método para ler um arquivo e retornar o objeto
        devido da classe em particular.
        """
        pass
