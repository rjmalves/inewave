from abc import abstractmethod
from typing import Any, IO, Optional


class Bloco:
    """
    Bloco genérico de um arquivo do NEWAVE,
    especificado através de uma string de início e uma
    de terminação, com estados de leitura.
    """
    def __init__(self,
                 str_inicio: str,
                 str_final: str,
                 obrigatorio: bool):
        self._str_inicio = str_inicio
        self._str_final = str_final
        self._obrigatorio = obrigatorio
        self._dados: Any = None
        self._encontrado = False
        self._ordem = 0
        self._lido = False
        self._linha_inicio = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Bloco):
            return False
        bloco: Bloco = o
        return self.dados == bloco.dados

    def e_inicio_de_bloco(self, linha: str) -> bool:
        """
        Verifica se uma linha é início do bloco.
        """
        return (self._str_inicio in linha
                and not self._encontrado)

    def inicia_bloco(self,
                     linha: str,
                     ordem: int) -> bool:
        """
        Inicia um bloco com uma linha.
        """
        if not self._encontrado:
            self._encontrado = True
            self._linha_inicio = linha
            self._ordem = ordem
        return self._encontrado and not self._lido

    def le_bloco(self,
                 arq: IO) -> Optional[bool]:
        """
        """
        self._lido = True
        return self.le(arq)

    @abstractmethod
    def le(self, arq: IO):
        pass

    @abstractmethod
    def escreve(self, arq: IO):
        pass

    @property
    def concluido(self):
        if self._obrigatorio:
            return self._lido
        else:
            return True

    @property
    def encontrado(self):
        return self._encontrado and not self._lido

    @property
    def dados(self) -> Any:
        """
        Retorna os dados lidos pelo bloco.
        """
        return self._dados

    @dados.setter
    def dados(self, d: Any):
        self._dados = d
