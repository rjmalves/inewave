from typing import List
import numpy as np  # type: ignore


class Patamar:
    """
    Classe responsável por lidar com o armazenamento dos dados de
    entrada do NEWAVE referentes aos patamares de carga por submercado,
    localizados no arquivo patamar.dat.
    """
    def __init__(self,
                 num_patamares: int,
                 anos_estudo: List[int],
                 patamares: np.ndarray):
        self.num_patamares = num_patamares
        self.anos_estudo = anos_estudo
        self.patamares = patamares
