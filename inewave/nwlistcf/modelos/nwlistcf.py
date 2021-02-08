from typing import Dict
import numpy as np  # type: ignore


class RegistroNwlistcf:
    """
    Armazena as informações de um registro da FCF do NEWAVE.

    ** Parâmetros **

    - ireg: `int`
    - rhs:  `float`
    - tabela: `np.ndarray`

    """

    __slots__ = ["ireg",
                 "rhs",
                 "tabela"]

    def __init__(self,
                 ireg: int,
                 rhs: float,
                 tabela: np.ndarray):
        self.ireg = ireg
        self.rhs = rhs
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre RegistroNwlistcf avalia todos os
        valores.
        """
        if not isinstance(o, RegistroNwlistcf):
            return False
        reg: RegistroNwlistcf = o
        eq_ireg = self.ireg == reg.ireg
        eq_rhs = self.rhs == reg.rhs
        eq_tab = np.array_equal(self.tabela, reg.tabela)

        return all([eq_ireg,
                    eq_rhs,
                    eq_tab])


class Nwlistcf:
    """
    Armazena os dados dos cortes construídos pelo NEWAVE existentes
    no arquivo `nwlistcf.rel` do NWLISTCF.

    Esta classe armazena os cortes da FCF de cada uma das variáveis,
    para cada registro e REE dentro do registro.

    Cada registro possui um modelo próprio, armazenando os coeficientes
    dos hiperplanos em uma array específica.

    **Parâmetros**

    - registros: `Dict[int, Dict[int, RegistroNwlistcf]]`

    """
    def __init__(self,
                 registros: Dict[int, Dict[int, RegistroNwlistcf]]):
        self.registros = registros

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre Nwlistcf avalia todos os registros.
        """
        if not isinstance(o, Nwlistcf):
            return False
        nw: Nwlistcf = o
        if self.registros.keys() != nw.registros.keys():
            return False
        for (p1, p2) in zip(self.registros.values(),
                            nw.registros.values()):
            if p1.keys() != p2.keys():
                return False
            for (r1, r2) in zip(p1.values(),
                                p2.values()):
                if r1 != r2:
                    return False
        return True
