from typing import Callable, IO


class Bloco:
    """
    Bloco genérico de um arquivo do NEWAVE,
    especificado através de uma string de início e uma
    de terminação, com estados de leitura.
    """
    def __init__(self,
                 str_inicio: str,
                 str_final: str,
                 obrigatorio: bool,
                 funcao_leitura: Callable[[IO,
                                           str],
                                          None]):
        self._str_inicio = str_inicio
        self._str_final = str_final
        self._obrigatorio = obrigatorio
        self._funcao_leitura = funcao_leitura
        self._encontrado = False
        self._lido = False
        self._linha_inicio = ""

    def e_inicio_de_bloco(self, linha: str) -> bool:
        """
        Verifica se uma linha é início do bloco.
        """
        return (self._str_inicio in linha
                and not self._encontrado)

    def inicia_bloco(self, linha: str) -> bool:
        """
        Inicia um bloco com uma linha.
        """
        if not self._encontrado:
            self._encontrado = True
            self._linha_inicio = linha
        return self._encontrado and not self._lido

    def le_bloco(self, arq: IO) -> None:
        """
        """
        self._lido = True
        return self._funcao_leitura(arq,
                                    self._linha_inicio)

    @property
    def concluido(self):
        if self._obrigatorio:
            return self._lido
        else:
            return True

    @property
    def encontrado(self):
        return self._encontrado and not self._lido