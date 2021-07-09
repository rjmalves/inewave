from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.arquivo import Arquivo
from inewave.newave.modelos.vazpast import BlocoVazPast, LeituraVazPast
from inewave._utils.escrita import Escrita

import numpy as np  # type: ignore


class VazPast(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes às
    vazões anteriores ao período de planejamento.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que são usadas juntos das contidas no arquivo `vazoes.dat`.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)
        # Interpreta o resultado da leitura
        val = True
        msg = "Erro na criação de VazPast: "
        if len(dados.blocos) == 1:
            bloco = dados.blocos[0]
            if isinstance(bloco, BlocoVazPast):
                self.__bloco = bloco
            else:
                msg += (f"O bloco deve ser do tipo {BlocoVazPast}, " +
                        f"mas foi fornecido do tipo {type(bloco)}")
                val = False
        else:
            msg += "Deve ser fornecido exatamente 1 bloco para VazPast"
            val = False
        if not val:
            raise TypeError(msg)

    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="vazpast.dat") -> 'VazPast':
        leitor = LeituraVazPast(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="vazpast.dat"):
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    @property
    def postos(self) -> np.ndarray:
        return self.__bloco._dados[2][:, 0]

    @postos.setter
    def postos(self, posto: np.ndarray):
        if posto.shape != self.postos.shape:
            raise ValueError("Deve ser atribuído o mesmo número de postos.")
        self.__bloco._dados[2][:, 0] = posto

    @property
    def nomes_usinas(self) -> np.ndarray:
        return self.__bloco._dados[2][:, 1]

    @nomes_usinas.setter
    def nomes_usinas(self, nomes: np.ndarray):
        if nomes.shape != self.nomes_usinas.shape:
            raise ValueError("Deve ser atribuído o mesmo número de nomes.")
        self.__bloco._dados[2][:, 1] = nomes
