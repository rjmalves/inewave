from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita
from inewave.newave.modelos.sistema import LeituraSistema

import pandas as pd  # type: ignore


class Sistema(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações
    dos subsistemas (submercados).

    **Parâmetros**

    """

    def __init__(self,
                 dados: DadosArquivo) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="sistema.dat") -> 'Sistema':
        """
        """
        leitor = LeituraSistema(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="sistema.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

    @property
    def custo_deficit(self) -> pd.DataFrame:
        """
        Tabela com os custos de déficit por patamar
        de déficit por subsistema.

        **Retorna**

        `pd.DataFrame`

        **Sobre**

        """
        return self._blocos[0].dados[1]

    @custo_deficit.setter
    def custo_deficit(self, custo: pd.DataFrame):
        """
        """
        self._blocos[0].dados[1] = custo

    @property
    def limites_intercambio(self) -> pd.DataFrame:
        """
        Tabela com os limites de intercâmbio entre
        subsistemas por mês/ano de estudo.

        **Retorna**

        `pd.DataFrame`

        **Sobre**

        """
        return self._blocos[1].dados

    @limites_intercambio.setter
    def limites_intercambio(self, limite: pd.DataFrame):
        """
        """
        self._blocos[1].dados = limite

    @property
    def mercado_energia(self) -> pd.DataFrame:
        """
        Tabela com os valores de mercado de energia
        (demanda) por mês/ano de estudo e por subsistema.

        **Retorna**

        `pd.DataFrame`

        **Sobre**

        """
        return self._blocos[2].dados

    @mercado_energia.setter
    def mercado_energia(self, merc: pd.DataFrame):
        """
        """
        self._blocos[2].dados = merc

    @property
    def geracao_usinas_nao_simuladas(self) -> pd.DataFrame:
        """
        Tabela com os valores de geração de pequenas usinas
        previstas para cada mês/ano de estudo e cada
        subsistema.

        **Retorna**

        `pd.DataFrame`

        **Sobre**

        """
        return self._blocos[3].dados

    @geracao_usinas_nao_simuladas.setter
    def geracao_usinas_nao_simuladas(self,
                                     ger: pd.DataFrame):
        """
        """
        self._blocos[3].dados = ger
