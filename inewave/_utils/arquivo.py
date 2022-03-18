from abc import abstractmethod
from typing import List, TypeVar, Type
from .registronewave import RegistroNEWAVE
from .dadosarquivo import DadosArquivoBlocos
from .dadosarquivo import DadosArquivoRegistros
from .dadosarquivo import DadosArquivoBinarios


class ArquivoBlocos:
    """ """

    def __init__(self, dados: DadosArquivoBlocos) -> None:
        self._dados = dados

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre arquivos avalia os dados interpretados e
        também os comentários externos.
        """
        if not isinstance(o, ArquivoBlocos):
            return False
        arquivos: ArquivoBlocos = o
        dif = False
        for (i1, l1), (i2, l2) in zip(
            self._linhas_fora_blocos.items(),
            arquivos._linhas_fora_blocos.items(),
        ):
            if i1 != i2 or l1 != l2:
                dif = True
                break
        for b1, b2 in zip(self._blocos, arquivos._blocos):
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
    def le_arquivo(cls, diretorio: str, nome_arquivo="") -> "ArquivoBlocos":
        pass

    @abstractmethod
    def escreve_arquivo(self, diretorio: str, nome_arquivo=""):
        pass


class ArquivoRegistros:
    """ """

    T = TypeVar("T")

    def __init__(self, dados: DadosArquivoRegistros) -> None:
        self._dados = dados

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre arquivos avalia os dados interpretados e
        também os comentários externos.
        """
        if not isinstance(o, ArquivoRegistros):
            return False
        d: ArquivoRegistros = o
        dif = False
        for (i1, l1), (i2, l2) in zip(
            self.linhas_fora_registros.items(), d.linhas_fora_registros.items()
        ):
            if i1 != i2 or l1 != l2:
                dif = True
                break
        for b1, b2 in zip(self._registros, d._registros):
            if b1 != b2:
                dif = True
                break
        return not dif

    @property
    def linhas_fora_registros(self):
        return self._dados.linhas_fora_registros

    @property
    def _registros(self):
        return self._dados.registros

    def cria_registro(
        self, anterior: RegistroNEWAVE, registro: RegistroNEWAVE
    ) -> RegistroNEWAVE:
        return self._dados.cria_registro(anterior, registro)

    def deleta_registro(self, registro: RegistroNEWAVE) -> bool:
        return self._dados.deleta_registro(registro)

    def lista_registros(self, tipo: Type[T]) -> List[T]:
        return self._dados.lista_registros(tipo)

    @classmethod
    @abstractmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="") -> "ArquivoRegistros":
        pass

    @abstractmethod
    def escreve_arquivo(self, diretorio: str, nome_arquivo=""):
        pass


class ArquivoBinario:
    """ """

    def __init__(self, dados: DadosArquivoBinarios) -> None:
        self._dados = dados

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre arquivos avalia os dados interpretados e
        também os comentários externos.
        """
        if not isinstance(o, ArquivoBinario):
            return False
        d: ArquivoBinario = o
        dif = False
        for b1, b2 in zip(self._blocos, d._blocos):
            if b1 != b2:
                dif = True
                break
        return not dif

    @property
    def _blocos(self):
        return self._dados.blocos

    @classmethod
    @abstractmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="") -> "ArquivoBinario":
        pass

    @abstractmethod
    def escreve_arquivo(self, diretorio: str, nome_arquivo=""):
        pass
