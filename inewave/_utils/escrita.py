from .dadosarquivo import DadosArquivo
from .bloco import Bloco

import os
from typing import IO, List, Dict
from traceback import print_exc


class Escrita:
    """
    Classe com utilidades gerais para a escrita de arquivos
    do NEWAVE.
    """
    def __init__(self,
                 diretorio: str):
        self._diretorio = diretorio

    def _escreve_blocos_e_linhas(self,
                                 arq: IO,
                                 blocos: List[Bloco],
                                 linhas: Dict[int, str]):

        ordem_blocos = [b._ordem for b in blocos]
        ordem_linhas = list(linhas.keys())
        ordens = ordem_blocos + ordem_linhas
        num_ordens = max(ordens) if len(ordens) > 0 else 0
        num_itens = num_ordens + 1
        for i in range(num_itens):
            if i in ordem_blocos:
                blocos[ordem_blocos.index(i)].escreve(arq)
            elif i in ordem_linhas:
                arq.write(linhas[i])

    def escreve_arquivo(self,
                        dados: DadosArquivo,
                        nome_arquivo: str):
        """
        """
        try:
            if not os.path.exists(self._diretorio):
                os.makedirs(self._diretorio)
            caminho = os.path.join(self._diretorio, nome_arquivo)
            with open(caminho, "w") as arq:
                self._escreve_blocos_e_linhas(arq,
                                              dados.blocos,
                                              dados.linhas_fora_blocos)
        except Exception:
            print_exc()
