from abc import abstractmethod
from .dadosarquivo import DadosArquivo


class Arquivo:
    """
    """
    def __init__(self,
                 dados: DadosArquivo) -> None:
        self._dados = dados

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre arquivos avalia os dados interpretados e
        também os comentários externos.
        """
        if not isinstance(o, Arquivo):
            return False
        arquivos: Arquivo = o
        dif = False
        for (i1, l1), (i2, l2) in zip(self._linhas_fora_blocos.items(),
                                      arquivos._linhas_fora_blocos.items()):
            if i1 != i2 or l1 != l2:
                dif = True
                break
        for b1, b2 in zip(self._blocos,
                          arquivos._blocos):
            if b1 != b2:
                dif = True
                break
        return not dif

    @property
    def _linhas_fora_blocos(self):
        return self._dados.linhas_fora_blocos

    @property
    def _blocos(self):
        return self._dados.blocos

    @classmethod
    @abstractmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="") -> 'Arquivo':
        pass

    @abstractmethod
    def escreve_arquivo(self, diretorio: str, nome_arquivo=""):
        pass
