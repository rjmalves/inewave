from abc import abstractmethod
from typing import IO, List
import os


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

    @abstractmethod
    def _fim_arquivo(self, linha: str) -> bool:
        """
        Método que deve ser implementado para cada arquivo, com o
        conteúdo da linha que indica o fim do próprio, para impedir loops
        de leitura eterna.
        """
        pass
