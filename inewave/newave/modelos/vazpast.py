from typing import List
import numpy as np  # type: ignore


class VazPast:
    """
    Armazena os dados de entrada do NEWAVE referentes às
    vazões anteriores ao período de planejamento.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que são usadas juntos das contidas no arquivo `vazoes.dat`.

    **Parâmetros**
    - mes_planejamento: `int`
    - ano_planejamento: `int`
    - postos: `List[int]`
    - nomes: `List[str]`
    - tabela: `np.ndarray`

    """
    def __init__(self,
                 mes_planejamento: int,
                 ano_planejamento: int,
                 postos: List[int],
                 nomes: List[str],
                 tabela: np.ndarray):
        self.mes_planejamento = mes_planejamento
        self.ano_planejamento = ano_planejamento
        self.postos = postos
        self.nomes = nomes
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre VazPast avalia todas as usinas.
        """
        if not isinstance(o, VazPast):
            return False
        vaz: VazPast = o
        eq_postos = self.postos == vaz.postos
        eq_nomes = self.nomes == vaz.nomes
        eq_tabela = np.array_equal(self.tabela, vaz.tabela)
        return eq_postos and eq_nomes and eq_tabela
