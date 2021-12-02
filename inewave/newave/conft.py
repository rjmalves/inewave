from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita
from inewave.newave.modelos.conft import LeituraConfT, BlocoConfUTE

import pandas as pd  # type: ignore


class ConfT(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações das
    usinas térmicas.

    **Parâmetros**

    """

    def __init__(self,
                 dados: DadosArquivo) -> None:
        super().__init__(dados)
        # Interpreta o resultado da leitura
        val = True
        msg = "Erro na criação de ConfT: "
        if len(dados.blocos) == 1:
            bloco = dados.blocos[0]
            if isinstance(bloco, BlocoConfUTE):
                self.__bloco = bloco
            else:
                msg += (f"O bloco deve ser do tipo {BlocoConfUTE}, " +
                        f"mas foi fornecido do tipo {type(bloco)}")
                val = False
        else:
            msg += "Deve ser fornecido exatamente 1 bloco para ConfT"
            val = False
        if not val:
            raise TypeError(msg)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="conft.dat") -> 'ConfT':
        """
        """
        leitor = LeituraConfT(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="conft.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

    @property
    def usinas(self) -> pd.DataFrame:
        return self.__bloco.dados

    @usinas.setter
    def usinas(self, d: pd.DataFrame):
        self.__bloco.dados = d
