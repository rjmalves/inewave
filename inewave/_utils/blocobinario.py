from abc import abstractmethod
from io import BufferedReader
from typing import Any, BinaryIO, Optional


class BlocoBinario:
    """
    Registro genérico dos arquivos do NEWAVE,
    especificado através de um mnemônico, com estados de leitura.
    """

    def __init__(self):
        self._dados: Any = None
        self._lido = False

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoBinario):
            return False
        bloco: BlocoBinario = o
        return self.dados == bloco.dados

    def le_bloco(self, arq: BufferedReader) -> Optional[bool]:
        """ """
        self._lido = True
        return self.le(arq)

    @abstractmethod
    def le(self, arq: BufferedReader):
        pass

    @abstractmethod
    def escreve(self, arq: BinaryIO):
        pass

    @property
    def concluido(self):
        return self._lido

    @property
    def encontrado(self):
        return not self._lido

    @property
    def dados(self) -> Any:
        """
        Retorna os dados lidos pelo registro.
        """
        return self._dados

    @dados.setter
    def dados(self, d: Any):
        self._dados = d
