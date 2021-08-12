from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.arquivo import Arquivo
from inewave.newave.modelos.eafpast import BlocoEafPast, LeituraEafPast
from inewave._utils.escrita import Escrita

import pandas as pd  # type: ignore


class EafPast(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes às
    vazões anteriores ao período de planejamento por REE.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que são usadas juntos das contidas no arquivo `vazoes.dat`.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)
        # Interpreta o resultado da leitura
        val = True
        msg = "Erro na criação de EafPast: "
        if len(dados.blocos) == 1:
            bloco = dados.blocos[0]
            if isinstance(bloco, BlocoEafPast):
                self.__bloco = bloco
            else:
                msg += (f"O bloco deve ser do tipo {BlocoEafPast}, " +
                        f"mas foi fornecido do tipo {type(bloco)}")
                val = False
        else:
            msg += "Deve ser fornecido exatamente 1 bloco para EafPast"
            val = False
        if not val:
            raise TypeError(msg)

    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="eafpast.dat") -> 'EafPast':
        leitor = LeituraEafPast(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="eafpast.dat"):
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    @property
    def tendencia(self) -> pd.DataFrame:
        return self.__bloco._dados

    @tendencia.setter
    def tendencia(self, df: pd.DataFrame):
        self.__bloco._dados = df
