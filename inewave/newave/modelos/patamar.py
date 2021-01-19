from typing import List, Dict
import numpy as np  # type: ignore
from inewave.config import MESES


class Patamar:
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

    **Parâmetros**

    - num_patamares: `int`
    - anos_estudo: `List[int]`
    - paramares: `np.ndarray`

    """
    def __init__(self,
                 num_patamares: int,
                 anos_estudo: List[int],
                 patamares: np.ndarray):
        self.num_patamares = num_patamares
        self.anos_estudo = anos_estudo
        self.patamares = patamares

    @property
    def patamares_por_ano(self) -> Dict[int, np.ndarray]:
        """
        Valores contidos na tabela de patamares, organizados
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
        for i, a in enumerate(self.anos_estudo):
            li = self.num_patamares * i
            lf = li + self.num_patamares
            patamares_ano[a] = self.patamares[li:lf, :]
        return patamares_ano

    @property
    def patamares_por_ano_e_mes(self) -> Dict[int, Dict[int, np.ndarray]]:
        """
        Valores contidos na tabela de patamares, organizados por ano e mês.

        **Retorna**

        `Dict[int, Dict[int, np.ndarray]]`

        **Sobre**

        O acesso é feito com [ano][mes] e o valor fornecido
        é uma array do numpy com os valores para os patamares 1, 2, ... .
        """
        patamares_ano: Dict[int, Dict[int, np.ndarray]] = {}
        n_meses = len(MESES)
        # Cria e inicializa os objetos
        for a in self.anos_estudo:
            patamares_ano[a] = {m: np.zeros(self.num_patamares,)
                                for m in range(1, n_meses + 1)}
        # Preenche com os valores
        for i, a in enumerate(self.anos_estudo):
            for m in range(1, n_meses + 1):
                li = self.num_patamares * i
                lf = li + self.num_patamares
                col = m - 1
                patamares_ano[a][m] = self.patamares[li:lf, col]
        return patamares_ano
