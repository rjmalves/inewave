from inewave._utils.dadosarquivo import DadosArquivoBlocos
from inewave._utils.arquivo import ArquivoBlocos
from inewave._utils.escritablocos import EscritaBlocos

from inewave.newave.modelos.term import LeituraTerm, BlocoTermUTE

import pandas as pd  # type: ignore


class Term(ArquivoBlocos):
    """
    Armazena os dados de entrada do NEWAVE referentes aos dados das
    usinas térmicas.

    **Parâmetros**

    """

    def __init__(self, dados: DadosArquivoBlocos) -> None:
        super().__init__(dados)
        # Interpreta o resultado da leitura
        val = True
        msg = "Erro na criação de Term: "
        if len(dados.blocos) == 1:
            bloco = dados.blocos[0]
            if isinstance(bloco, BlocoTermUTE):
                self.__bloco = bloco
            else:
                msg += (
                    f"O bloco deve ser do tipo {BlocoTermUTE}, "
                    + f"mas foi fornecido do tipo {type(bloco)}"
                )
                val = False
        else:
            msg += "Deve ser fornecido exatamente 1 bloco para Term"
            val = False
        if not val:
            raise TypeError(msg)

    # Override
    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="term.dat") -> "Term":
        """ """
        leitor = LeituraTerm(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="term.dat"):
        """ """
        escritor = EscritaBlocos(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    @property
    def usinas(self) -> pd.DataFrame:
        return self.__bloco.dados

    @usinas.setter
    def usinas(self, d: pd.DataFrame):
        self.__bloco.dados = d
