from typing import Dict
import numpy as np  # type: ignore


class RegistroEstado:
    """
    Armazena as informações de um registro visitado pelo NEWAVE
    em algum período de alguma simulação.

    ** Parâmetros **

    - ireg: `int`
    - itec: `int`
    - simc: `int`
    - itef: `int`
    - fobj: `int`
    - tabela: `np.ndarray`

    """

    __slots__ = ["ireg",
                 "itec",
                 "simc",
                 "itef",
                 "fobj",
                 "tabela"]

    def __init__(self,
                 ireg: int,
                 itec: int,
                 simc: int,
                 itef: int,
                 fobj: float,
                 tabela: np.ndarray):
        self.ireg = ireg
        self.itec = itec
        self.simc = simc
        self.itef = itef
        self.fobj = fobj
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre RegistroEstado avalia todos os
        valores.
        """
        if not isinstance(o, RegistroEstado):
            return False
        reg: RegistroEstado = o
        eq_ireg = self.ireg == reg.ireg
        eq_itec = self.itec == reg.itec
        eq_simc = self.simc == reg.simc
        eq_itef = self.itef == reg.itef
        eq_fobj = self.fobj == reg.fobj
        eq_tab = np.array_equal(self.tabela, reg.tabela)

        return all([eq_ireg,
                    eq_itec,
                    eq_simc,
                    eq_itef,
                    eq_fobj,
                    eq_tab])


class Estados:
    """
    Armazena os dados dos estados visitados pelo NEWAVE existentes
    no arquivo `estados.rel` do NWLISTCF.

    Esta classe armazena os estados de cada uma das variáveis envolvidas
    no problema e da função objetivo, para cada registro e REE dentro
    do registro.

    Cada registro possui um modelo próprio, armazenando os estados das
    variáveis em uma array específica.

    **Parâmetros**

    - registros: `Dict[int, Dict[int, RegistroEstado]]`

    """
    def __init__(self,
                 registros: Dict[int, Dict[int, RegistroEstado]]):
        self.registros = registros

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre Estados avalia todos os registros.
        """
        if not isinstance(o, Estados):
            return False
        est: Estados = o
        if self.registros.keys() != est.registros.keys():
            return False
        for (p1, p2) in zip(self.registros.values(),
                            est.registros.values()):
            if p1.keys() != p2.keys():
                return False
            for (r1, r2) in zip(p1.values(),
                                p2.values()):
                if r1 != r2:
                    return False
        return True
