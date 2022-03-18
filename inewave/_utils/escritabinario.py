from inewave._utils.blocobinario import BlocoBinario
from .dadosarquivo import DadosArquivoBinarios

import os
from typing import BinaryIO, List
from traceback import print_exc


class EscritaBinario:
    """
    Classe com utilidades gerais para a escrita de arquivos
    binários do DECOMP.
    """

    def __init__(self, diretorio: str):
        self._diretorio = diretorio

    def _escreve_blocos(self, arq: BinaryIO, blocos: List[BlocoBinario]):
        for b in blocos:
            b.escreve(arq)

    def escreve_arquivo(self, dados: DadosArquivoBinarios, nome_arquivo: str):
        """ """
        try:
            if not os.path.exists(self._diretorio):
                os.makedirs(self._diretorio)
            caminho = os.path.join(self._diretorio, nome_arquivo)
            with open(caminho, "wb") as arq:
                self._escreve_blocos(arq, dados.blocos)
        except Exception as e:
            print_exc()
            raise e
