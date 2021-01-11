from typing import Dict
import numpy as np  # type: ignore
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
                        if p == 1 and c == 0 and a == 1995:
                            print(f" m = {m} lin = {lin} col = {col}")
                            print(f"tabela = {tabela[lin, :]}")
                        custos[p][a][m][c] = tabela[lin, col]
        return custos
