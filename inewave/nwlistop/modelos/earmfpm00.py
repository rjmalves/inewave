from typing import Dict
import numpy as np  # type: ignore
from inewave.config import NUM_CENARIOS, MESES


class Earmfpm00:
    """
    Armazena os dados das saídas referentes às energias
    armazenadas finais, por submercado e em % da energia armazenável máxima.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmfpm00x.out`, onde x varia conforme o
    submercado em questão.

    **Parâmetros**

    - mes_pmo: `int`
    - ano_pmo: `int`
    - versao_newave: `str`
    - submercado: `str`
    - energias_armazenadas: `Dict[int, np.ndarray]`

    """
    def __init__(self,
                 mes_pmo: int,
                 ano_pmo: int,
                 versao_newave: str,
                 submercado: str,
                 energias_armazenadas: Dict[int,
                                            np.ndarray]):
        self.mes_pmo = mes_pmo
        self.ano_pmo = ano_pmo
        self.versao_newave = versao_newave
        self.submercado = submercado
        self.energias_armazenadas = energias_armazenadas

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre Earmfpm00 avalia todos os valores, exceto
        a versão do NEWAVE.
        """
        if not isinstance(o, Earmfpm00):
            return False
        eaf: Earmfpm00 = o
        eq_mes_pmo = self.mes_pmo == eaf.mes_pmo
        eq_ano_pmo = self.ano_pmo == eaf.ano_pmo
        eq_submercado = self.submercado == eaf.submercado
        eq_e = all([np.array_equal(e, f)
                    for (e, f) in zip(self.energias_armazenadas.values(),
                                      eaf.energias_armazenadas.values())
                    ])
        return eq_mes_pmo and eq_ano_pmo and eq_submercado and eq_e

    @property
    def energias_por_ano(self) -> Dict[int, np.ndarray]:
        """
        Energias armazenadas para cada ano e em cada cenário, para
        todos os meses, organizadas primeiramente por ano.

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [ano] e retorna um np.ndarray com os valores
        de EARM para todos os cenários e meses, naquele ano.

        """
        return self.energias_armazenadas

    @property
    def energias_por_ano_e_mes(self) -> Dict[int,
                                             Dict[int, np.ndarray]]:
        """
        Energias armazenadas para cada ano e mês em cada cenário,
        para todos os meses, organizadas primeiramente por ano.

        **Retorna**

        `Dict[int, Dict[int, np.ndarray]]`

        **Sobre**

        O acesso é feito com [ano][mes] e retorna um np.ndarray com os
        valores de EARM para todos os cenários, naquele ano e mês.

        """
        energias: Dict[int,
                       Dict[int, np.ndarray]] = {}
        anos_estudo = list(self.energias_armazenadas.keys())
        n_meses = len(MESES)
        # Cria e inicializa os objetos a serem retornados
        for a in anos_estudo:
            energias[a] = {m: np.array([])
                           for m in range(1, n_meses + 1)}
        # Preenche com os valores
        for a, tabela in self.energias_armazenadas.items():
            for m in range(1, n_meses + 1):
                col = m - 1
                energias[a][m] = tabela[:, col]
        return energias

    @property
    def energias_por_ano_e_cenario(self) -> Dict[int,
                                                 Dict[int, np.ndarray]]:
        """
        Energias armazenadas para cada ano e cenário, para todos os
        meses, organizadas primeiramente por ano.

        **Retorna**

        `Dict[int, Dict[int, np.ndarray]]`

        **Sobre**

        O acesso é feito com [ano][cenario] e retorna um np.ndarray com os
        valores de EARM para todos os meses, naquele ano e cenário.

        """
        energias: Dict[int,
                       Dict[int, np.ndarray]] = {}
        anos_estudo = list(self.energias_armazenadas.keys())
        # Cria e inicializa os objetos a serem retornados
        for a in anos_estudo:
            energias[a] = {c: np.array([])
                           for c in range(NUM_CENARIOS)}
        # Preenche com os valores
        for a, tabela in self.energias_armazenadas.items():
            for c in range(NUM_CENARIOS):
                energias[a][c] = tabela[c, :]
        return energias
