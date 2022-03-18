from abc import abstractmethod
from typing import Any, List
from io import BufferedReader
import os
from traceback import print_exc

from inewave._utils.blocobinario import BlocoBinario
from .dadosarquivo import DadosArquivoBinarios


class LeituraBinario:
    """
    Classe com utilidades gerais para leitura de arquivos
    binários do DECOMP.
    """

    def __init__(self, diretorio: str):
        self._diretorio = diretorio
        self._blocos: List[BlocoBinario] = []
        self._dados: Any = None

    def _lista_arquivos_por_chave(self, chave: str) -> List[str]:
        """
        Retorna a lista de caminhos completos para os arquivos em um
        diretório, desde que tenham uma certa chave no nome.
        """
        return [f for f in os.listdir(self._diretorio) if chave in f]

    def _le_blocos_encontrados(
        self, arq: BufferedReader, blocos: List[BlocoBinario]
    ):
        """
        Faz a leitura dos blocos encontrados até o momento e que
        ainda não foram lidos.
        """
        for i, b in enumerate(blocos):
            if not b.concluido:
                return b.le_bloco(arq)

    def _le_blocos_arquivo(self, arq: BufferedReader):
        """
        Faz a leitura dos blocos de dados do arquivo.
        """
        self._blocos = self._cria_blocos_leitura()
        while True:
            # Decide se acabou o arquivo binário
            b = arq.peek(1)  # noqa
            if self._fim_arquivo(b):
                self._prepara_dados_saida()
                break
            # Lê mais um bloco
            self._le_blocos_encontrados(arq, self._blocos)

    def _le_arquivo_em_diretorio(
        self, diretorio: str, nome_arquivo: str
    ) -> None:
        """
        Faz a leitura do arquivo em um diretorio.
        """
        try:
            caminho = os.path.join(diretorio, nome_arquivo)
            with open(caminho, "rb") as arq:
                self._le_blocos_arquivo(arq)  # type: ignore
        except Exception:
            print_exc()

    @abstractmethod
    def _cria_blocos_leitura(self) -> List[BlocoBinario]:
        """
        Método que cria a lista de blocos a serem lidos no arquivo.
        Implementa o Factory Pattern.
        """
        pass

    def _prepara_dados_saida(self):
        """
        Trata os dados obtidos do arquivo para ser retornado.
        """
        self._blocos = [b for b in self._blocos if b.concluido]

    def _fim_arquivo(self, b: bytes) -> bool:
        """
        Método que deve ser implementado para cada arquivo, com o
        conteúdo da linha que indica o fim do próprio, para impedir loops
        de leitura eterna.
        """
        return not b

    def le_arquivo(self, nome_arquivo: str) -> DadosArquivoBinarios:
        """
        Método para ler um arquivo e retornar o objeto
        devido da classe em particular.
        """
        self._le_arquivo_em_diretorio(self._diretorio, nome_arquivo)
        return DadosArquivoBinarios(self._blocos)

    @property
    def dados(self) -> Any:
        """
        Dados de leitura obtidos pelo blocos, organizados
        para realizar a criação do objeto associado.
        """
        return self._dados
