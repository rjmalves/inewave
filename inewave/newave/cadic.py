from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita
from inewave.newave.modelos.cadic import LeituraCAdic

import pandas as pd  # type: ignore


class CAdic(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes às cargas
    adicionais.

    **Parâmetros**

    """

    def __init__(self,
                 dados: DadosArquivo) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="c_adic.dat") -> 'CAdic':
        """
        """
        leitor = LeituraCAdic(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="c_adic.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

    @property
    def cargas_adicionais(self) -> pd.DataFrame:
        """
        Tabela com as cargas adicionais por mês/ano e por subsistema
        para cada razão de carga adicional.

        **Retorna**

        `pd.DataFrame`

        **Sobre**
        """
        return self._blocos[0].dados

    @cargas_adicionais.setter
    def cargas_adicionais(self, carga: pd.DataFrame):
        self._blocos[0].dados = carga
