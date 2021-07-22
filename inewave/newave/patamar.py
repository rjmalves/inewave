from inewave.newave.modelos.patamar import LeituraPatamar
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.arquivo import Arquivo
from inewave._utils.escrita import Escrita
from inewave.config import MESES_DF

from typing import Dict
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class Patamar(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    patamares de carga por submercado.

    Esta classe pode lidar com um número qualquer de patamares
    de carga, desde que as informações fornecidas a ela por meio
    da tabela de valores seja compatível com o parâmetro `num_patamares`
    da mesma.

    A tabela de patamares de carga é armazenada através de uma array
    em `NumPy`, para otimizar cálculos futuros e espaço ocupado
    em memória. A tabela interna é transformada em dicionários
    e outras estruturas de dados mais palpáveis através das propriedades
    da própria classe.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)
        # Interpreta o resultado da leitura
        val = True
        msg = "Erro na criação de Patamar: "
        if len(dados.blocos) != 3:
            msg += "Devem ser fornecidos exatamente 2 blocos para Patamar"
            val = False
        if not val:
            raise TypeError(msg)

    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="patamar.dat") -> 'Patamar':
        """
        """
        leitor = LeituraPatamar(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="patamar.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

    @property
    def duracao_mensal_patamares(self) -> pd.DataFrame:
        """
        Tabela de duração mensal dos patamares de carga.

        **Retorna**

        `pd.DataFrame`

        **Sobre**

        """
        return self._blocos[0].dados

    @duracao_mensal_patamares.setter
    def duracao_mensal_patamares(self, duracao: pd.DataFrame):
        self._blocos[0].dados = duracao

    @property
    def carga_patamares(self) -> pd.DataFrame:
        """
        Tabela de carga em p.u. dos patamares de carga.

        **Retorna**

        `pd.DataFrame`

        **Sobre**

        """
        return self._blocos[1].dados

    @carga_patamares.setter
    def carga_patamares(self, carga: pd.DataFrame):
        self._blocos[1].dados = carga

    @property
    def intercambio_patamares(self) -> pd.DataFrame:
        """
        Tabela de intercambios em p.u. dos patamares de carga.

        **Retorna**

        `pd.DataFrame`

        **Sobre**

        """
        return self._blocos[2].dados

    @intercambio_patamares.setter
    def intercambio_patamares(self, inter: pd.DataFrame):
        self._blocos[2].dados = inter

    @property
    def patamares_por_ano(self) -> Dict[int, np.ndarray]:
        """
        Valores contidos na tabela de duração dos patamares, organizados
        por ano.

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [ano] e o valor fornecido
        é uma array 2-D do `NumPy` com os valores dos patamares para todo
        os meses de um ano, semelhante a uma linha do arquivo patamar.dat.
        """
        patamares_ano: Dict[int, np.ndarray] = {}
        # Preenche com os valores
        duracoes = self.duracao_mensal_patamares
        anos = self.anos_estudo
        for i, a in enumerate(anos):
            patamares_ano[a] = duracoes.loc[duracoes["Ano"] == a,
                                            MESES_DF].to_numpy()
        return patamares_ano

    @property
    def anos_estudo(self) -> np.ndarray:
        """
        Lista com os anos de estudo descritos no Patamar.

        **Retorna**

        `np.ndarray`

        """
        duracoes = self.duracao_mensal_patamares
        return np.array(list(set(list(duracoes["Ano"]))))
