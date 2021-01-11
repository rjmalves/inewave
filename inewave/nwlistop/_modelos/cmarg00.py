from typing import Dict
import numpy as np  # type: ignore


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
