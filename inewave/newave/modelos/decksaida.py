from .cortes import Cortes
from .cortesh import CortesH
from .pmo import PMO
from inewave.newave.parp import PARp
from .forward import Forward
from .forwardh import ForwardH


class DeckSaida:
    """
    Armazena todos os dados de saída do NEWAVE.

    Esta classe lida com informações de saída do NEWAVE e
    é relacionada a um diretório, que deve conter
    um deck de saída do NEWAVE (unix-like).

    **Parâmetros**

    """

    def __init__(self,
                 cortes: Cortes,
                 cortesh: CortesH,
                 pmo: PMO,
                 parp: PARp,
                 forward: Forward,
                 forwardh: ForwardH) -> None:
        self.cortes = cortes
        self.cortesh = cortesh
        self.pmo = pmo
        self.parp = parp
        self.forward = forward
        self.forwardh = forwardh
