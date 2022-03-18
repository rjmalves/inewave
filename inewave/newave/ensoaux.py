from inewave._utils.arquivo import ArquivoBlocos
from inewave._utils.dadosarquivo import DadosArquivoBlocos
from inewave._utils.escritablocos import EscritaBlocos

from inewave.newave.modelos.ensoaux import LeituraENSOAux


class ENSOAux(ArquivoBlocos):
    """
    Armazena os dados de entrada do NEWAVE referentes ao arquivo ENSO 2.

    **Parâmetros**

    """

    def __init__(self, dados: DadosArquivoBlocos) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ensoaux.dat"
    ) -> "ENSOAux":
        """ """
        leitor = LeituraENSOAux(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ensoaux.dat"):
        """ """
        escritor = EscritaBlocos(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)
