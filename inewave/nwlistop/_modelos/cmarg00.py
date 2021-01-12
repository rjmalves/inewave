from typing import Dict
import numpy as np  # type: ignore
from inewave.newave._modelos.patamar import Patamar
from inewave.config import NUM_PATAMARES, NUM_CENARIOS, MESES


class Cmarg00:
    """
    Classe responsável por lidar com o armazenamento dos dados das
    saídas do NWListOP referentes aos custos marginais de operação
    por patamar, por submercado: cmarg00x.out.
    """
    def __init__(self,
                 mes_pmo: int,
                 ano_pmo: int,
                 versao_newave: str,
                 submercado: str,
                 custos_patamares: Dict[int,
                                        np.ndarray]):
        self.mes_pmo = mes_pmo
        self.ano_pmo = ano_pmo
        self.versao_newave = versao_newave
        self.submercado = submercado
        self.custos_patamares = custos_patamares

    def custos_medios_por_ano(self,
                              patamar: Patamar) -> Dict[int,
                                                        np.ndarray]:
        """
        Retorna os custos médios para cada ano de estudo e mês.
        Recebe um objeto Patamar para realizar a ponderação de
        cada cenários pelos devidos valores. O acesso é feito com
        [ano] e a saída é uma array 2-D do numpy com os valores
        médios de cada cenário e mês.
        """
        patamares_anos = patamar.patamares_por_ano
        # Confere se os anos de estudo do objeto Patamar fornecido
        # são os mesmos do cmarg00
        if patamar.anos_estudo != list(self.custos_patamares.keys()):
            raise Exception("Objeto Patamar incompatível com Cmarg00")
        # Inicializa a variável que irá conter os custos médios
        n_meses = len(MESES)
        custos: Dict[int, np.ndarray] = {a: np.zeros((NUM_CENARIOS,
                                                      n_meses))
                                         for a in patamar.anos_estudo}
        # Para cada cenário, calcula o custo médio em relação aos
        # patamares
        for a in patamar.anos_estudo:
            for i in range(NUM_CENARIOS):
                li = i * NUM_PATAMARES
                lf = li + NUM_PATAMARES
                janela: np.ndarray = self.custos_patamares[a][li:lf, :]
                custos[a][i, :] = np.inner(janela.T,
                                           patamares_anos[a].T)[:, 0]
        return custos

    def custos_medios_por_ano_e_mes(self,
                                    patamar: Patamar) -> Dict[int,
                                                              np.ndarray]:
        """
        Retorna os custos médios para cada ano de estudo e mês.
        Recebe um objeto Patamar para realizar a ponderação de
        cada cenários pelos devidos valores. O acesso é feito com
        [ano][mes] e a saída é uma array do numpy com os valores
        médios de cada cenário.
        """
        patamares_anos = patamar.patamares_por_ano
        # Confere se os anos de estudo do objeto Patamar fornecido
        # são os mesmos do cmarg00
        if patamar.anos_estudo != list(self.custos_patamares.keys()):
            raise Exception("Objeto Patamar incompatível com Cmarg00")

        n_meses = len(MESES)
        # Variável auxiliar para cálculo mais rápido
        custos_ano: Dict[int, np.ndarray] = {a: np.zeros((NUM_CENARIOS,
                                                          n_meses))
                                             for a in patamar.anos_estudo}
        # Para cada cenário, calcula o custo médio em relação aos
        # patamares
        for a in patamar.anos_estudo:
            for i in range(NUM_CENARIOS):
                li = i * NUM_PATAMARES
                lf = li + NUM_PATAMARES
                janela: np.ndarray = self.custos_patamares[a][li:lf, :]
                custos_ano[a][i, :] = np.inner(janela.T,
                                               patamares_anos[a].T)[:, 0]
        # Inicializa a variável que irá conter os custos médios
        custos: Dict[int,
                     Dict[int,
                          np.ndarray]] = {a: {}
                                          for a in patamar.anos_estudo}
        # Separa os custos em cada mês e retorna
        for a in patamar.anos_estudo:
            for m in range(1, n_meses + 1):
                custos[a][m] = custos_ano[a][:, m - 1]
        return custos

    @property
    def custos_por_patamar(self) -> Dict[int,
                                         Dict[int,
                                              Dict[int, np.ndarray]]]:
        """
        Retorna os custos obtidos para cada ano, mês e em cada cenário,
        organizados primeiramente por patamar. O acesso é feito
        com [patamar][ano][mes] e retorna um np.ndarray.
        """
        custos: Dict[int,
                     Dict[int,
                          Dict[int, np.ndarray]]] = {}
        patamares = list(range(1, NUM_PATAMARES + 1))
        anos_estudo = list(self.custos_patamares.keys())
        n_meses = len(MESES)
        # Cria e inicializa os objetos a serem retornados
        for p in patamares:
            if p not in custos:
                custos[p] = {a: {m: np.zeros(NUM_CENARIOS,)
                                 for m in range(1, n_meses + 1)}
                             for a in anos_estudo}
        # Preenche com os valores
        for a, tabela in self.custos_patamares.items():
            for p in patamares:
                for c in range(NUM_CENARIOS):
                    for m in range(1, n_meses + 1):
                        lin = NUM_PATAMARES * c + p - 1
                        col = m - 1
                        custos[p][a][m][c] = tabela[lin, col]
        return custos
