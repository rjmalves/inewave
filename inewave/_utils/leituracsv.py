import os
from abc import abstractmethod
from traceback import print_exc
import pandas as pd  # type: ignore


class LeituraCSV:
    """
    Classe com utilidades gerais para leitura de arquivos
    .csv do NEWAVE.
    """

    def __init__(self, diretorio: str):
        self._diretorio = diretorio
        self._dados = pd.DataFrame()

    def _le_tabela_arquivo(self, caminho: str):
        """
        Faz a leitura dos blocos de dados do arquivo.
        """
        self._dados = pd.read_csv(
            caminho, sep=",", encoding="utf-8", index_col=1
        )

    def _le_arquivo_em_diretorio(
        self, diretorio: str, nome_arquivo: str
    ) -> None:
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
        self._le_arquivo_em_diretorio(self._diretorio, nome_arquivo)
        return self._dados

    @abstractmethod
    def processa_dados_lidos(self):
        """ """
        pass

    @property
    def dados(self) -> pd.DataFrame:
        """
        Dados de leitura obtidos pelo blocos, organizados
        para realizar a criação do objeto associado.
        """
        return self._dados
