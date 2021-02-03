from typing import Dict
import numpy as np  # type: ignore
from inewave.newave.modelos.patamar import Patamar
from inewave.config import NUM_PATAMARES, NUM_CENARIOS, MESES


class Cmarg00:
    """
    Armazena os dados das saídas referentes aos custos marginais de operação
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cmarg00x.out`, onde x varia conforme o
    submercado em questão.

    **Parâmetros**

    - mes_pmo: `int`
    - ano_pmo: `int`
    - versao_newave: `str`
    - submercado: `str`
    - custos_patamares: `Dict[int, np.ndarray]`

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

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre Cmarg00 avalia todos os valores, exceto
        a versão do NEWAVE.
        """
        if not isinstance(o, Cmarg00):
            return False
        cmarg: Cmarg00 = o
        eq_mes_pmo = self.mes_pmo == cmarg.mes_pmo
        eq_ano_pmo = self.ano_pmo == cmarg.ano_pmo
        eq_submercado = self.submercado == cmarg.submercado
        eq_custos = all([np.array_equal(c1, c2)
                         for (c1, c2) in zip(self.custos_patamares.values(),
                                             cmarg.custos_patamares.values())
                         ])
        return eq_mes_pmo and eq_ano_pmo and eq_submercado and eq_custos

    def custos_medios_por_ano(self,
                              patamar: Patamar) -> Dict[int,
                                                        np.ndarray]:
        """
        Custos médios para cada ano de estudo.

        **Parâmetros**

        `Patamar`

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

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
                                    p: Patamar) -> Dict[int,
                                                        Dict[int,
                                                             np.ndarray]]:
        """
        Custos médios para cada ano de estudo e mês.

        **Parâmetros**

        `Patamar`

        **Retorna**

        `Dict[int, Dict[int, np.ndarray]]`

        **Sobre**

        Recebe um objeto Patamar para realizar a ponderação de
        cada cenários pelos devidos valores. O acesso é feito com
        [ano][mes] e a saída é uma array do numpy com os valores
        médios de cada cenário.
        """
        custos_ano = self.custos_medios_por_ano(p)
        n_meses = len(MESES)
        # Inicializa a variável que irá conter os custos médios por mês
        custos: Dict[int,
                     Dict[int,
                          np.ndarray]] = {a: {}
                                          for a in p.anos_estudo}
        # Separa os custos em cada mês e retorna
        for a in p.anos_estudo:
            for m in range(1, n_meses + 1):
                custos[a][m] = custos_ano[a][:, m - 1]
        return custos

    @property
    def custos_por_patamar(self) -> Dict[int,
                                         Dict[int,
                                              Dict[int, np.ndarray]]]:
        """
        Custos obtidos para cada ano, mês e em cada cenário,
        organizados primeiramente por patamar.

        **Retorna**

        `Dict[int, Dict[int, Dict[int, np.ndarray]]]`

        **Sobre**

        O acesso é feito
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

    @property
    def custos_por_ano(self) -> Dict[int,
                                     Dict[int, np.ndarray]]:
        """
        Custos obtidos para cada ano e em cada cenário, para
        todos os meses, organizados primeiramente por ano.

        **Retorna**

        `Dict[int, Dict[int,  np.ndarray]]`

        **Sobre**

        O acesso é feito
        com [patamar][ano] e retorna um np.ndarray com os valores de
        custos para todos os cenários e meses, naquele patamar e ano.
        """
        custos: Dict[int,
                     Dict[int, np.ndarray]] = {}
        patamares = list(range(1, NUM_PATAMARES + 1))
        anos_estudo = list(self.custos_patamares.keys())
        n_meses = len(MESES)
        # Cria e inicializa os objetos a serem retornados
        for p in patamares:
            if p not in custos:
                custos[p] = {a:  np.zeros((NUM_CENARIOS, n_meses))
                             for a in anos_estudo}
        # Preenche com os valores
        for a, tabela in self.custos_patamares.items():
            for p in patamares:
                for c in range(NUM_CENARIOS):
                    lin = NUM_PATAMARES * c + p - 1
                    custos[p][a][c, :] = tabela[lin, :]
        return custos

    @property
    def custos_por_ano_e_mes(self) -> Dict[int,
                                           Dict[int,
                                                Dict[int, np.ndarray]]]:
        """
        Custos obtidos para cada ano, mês e em cada cenário,
        organizados primeiramente por ano e mês.

        **Retorna**

        `Dict[int, Dict[int, Dict[int, np.ndarray]]]`

        **Sobre**

        O acesso é feito com
        [patamar][ano][mes] e retorna um np.ndarray com os valores de
        custos para todos os cenários, naquele patamar.
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
