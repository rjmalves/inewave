import numpy as np  # type: ignore
from inewave._utils.dadosarquivo import DadosArquivoBlocos
from inewave._utils.arquivo import ArquivoBlocos
from inewave.newave.modelos.dsvagua import BlocoDsvUHE, LeituraDSVAgua
from inewave._utils.escritablocos import EscritaBlocos


class DSVAgua(ArquivoBlocos):
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    desvios de água por usina.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que podem ser modificadas através do arquivo `dsvagua.dat`.

    """

    def __init__(self, dados: DadosArquivoBlocos):
        super().__init__(dados)
        # Interpreta o resultado da leitura
        val = True
        msg = "Erro na criação de DSVAgua: "
        if len(dados.blocos) == 1:
            bloco = dados.blocos[0]
            if isinstance(bloco, BlocoDsvUHE):
                self.__bloco = bloco
            else:
                msg += (
                    f"O bloco deve ser do tipo {BlocoDsvUHE}, "
                    + f"mas foi fornecido do tipo {type(bloco)}"
                )
                val = False
        else:
            msg += "Deve ser fornecido exatamente 1 bloco para DSVAgua"
            val = False
        if not val:
            raise TypeError(msg)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dsvagua.dat"
    ) -> "DSVAgua":
        leitor = LeituraDSVAgua(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dsvagua.dat"):
        escritor = EscritaBlocos(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    @property
    def desvios(self) -> np.ndarray:
        return self.__bloco.dados
