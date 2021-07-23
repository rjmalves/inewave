from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita
from inewave.newave.modelos.curva import LeituraCurva

import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class Curva(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes à curva para
    penalização por volume mínimo dos reservatórios.

    **Parâmetros**

    """

    def __init__(self,
                 dados: DadosArquivo) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="curva.dat") -> 'Curva':
        """
        """
        leitor = LeituraCurva(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="curva.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

    @property
    def configuracoes_penalizacao(self) -> np.ndarray:
        """
        Linha de configuração das opções de penalização do
        arquivo curva.dat.

        **Retorna**

        `np.ndarray`

        **Sobre**

        Retorna um array com três elementos:

        - O primeiro é o tipo de penalização: 0 - FIXA e 1 - MAXIMA
        - O segundo é o mês de penalização: entre 1 e 12
        - O terceiro é a sazonalização do VminP: 0 para não e 1 para sim
        """
        return self._blocos[0].dados

    @configuracoes_penalizacao.setter
    def configuracoes_penalizacao(self, config: np.ndarray):
        self._blocos[0].dados = config

    @property
    def penalidades_ree(self) -> pd.DataFrame:
        """
        Tabela com os custos de penalidades por violação de VminP
        em cada REE.

        **Retorna**

        `pd.DataFrame`

        **Sobre**
        """
        return self._blocos[1].dados

    @penalidades_ree.setter
    def penalidades_ree(self, penalidades: pd.DataFrame):
        self._blocos[1].dados = penalidades

    @property
    def curva_seguranca(self) -> pd.DataFrame:
        """
        Tabela com os valores da curva de segurança de operação
        para cada mês/ano de cada REE.

        **Retorna**

        `pd.DataFrame`

        **Sobre**
        """
        return self._blocos[2].dados

    @curva_seguranca.setter
    def curva_seguranca(self, curva: pd.DataFrame):
        self._blocos[2].dados = curva
