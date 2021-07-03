
from typing import Dict, List

from.bloco import Bloco


class DadosArquivo:
    """
    """
    def __init__(self,
                 blocos: List[Bloco],
                 linhas_fora_blocos: Dict[int, str]) -> None:
        self.__blocos = blocos
        self.__linhas_fora_blocos = linhas_fora_blocos
        pass

    @property
    def blocos(self) -> List[Bloco]:
        return self.__blocos

    @property
    def linhas_fora_blocos(self) -> Dict[int, str]:
        return self.__linhas_fora_blocos
