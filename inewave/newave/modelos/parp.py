from typing import Dict
import numpy as np  # type: ignore


class PARp:
    """
    Armazena os dados de saída do NEWAVE referentes aos modelos e às
    séries sintéticas de energia geradas pelo PAR(p).

    Esta classe lida com informações de saída do NEWAVE e
    cujas saídas devem ser compatíveis com as observadas através
    do NWLISTOP.

    **Parâmetros**

    - ordens: `Dict[int, np.ndarray]`
    - coeficientes: `Dict[int, np.ndarray]`
    - series: `Dict[int, np.ndarray]`

    """
    def __init__(self,
                 ordens: Dict[int, np.ndarray],
                 coeficientes: Dict[int, np.ndarray],
                 series: Dict[int, np.ndarray]):
        self.ordens = ordens
        self.coeficientes = coeficientes
        self.series = series

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre PARp avalia todos os campos.
        """
        if not isinstance(o, PARp):
            return False
        parp: PARp = o
        eq_ordens = all([np.array_equal(o1, o2)
                         for (o1, o2) in zip(self.ordens,
                                             parp.ordens)])
        eq_coefs = all([np.array_equal(c1, c2)
                        for (c1, c2) in zip(self.coeficientes,
                                            parp.coeficientes)])
        eq_series = all([np.array_equal(s1, s2)
                         for (s1, s2) in zip(self.series,
                                             parp.series)])
        return eq_ordens and eq_coefs and eq_series
