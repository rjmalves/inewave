from inewave._utils.arquivo import Arquivo
from .caso import Caso
from .arquivos import Arquivos
from .dger import DGer
from .sistema import Sistema
from .confhd import Confhd
from .modif import Modif
from .conft import ConfT
from .term import Term
from .clast import ClasT
from .exph import Exph
from .expt import Expt
from .patamar import Patamar
from .shist import Shist
from .manutt import ManutT
from .vazpast import VazPast
from .itaipu import Itaipu
from .bid import BID
from .cadic import CAdic
from .perda import Perda
from .gtminpat import GTMinPat
from .elnino import ElNino
from .ensoaux import ENSOAux
from .dsvagua import DSVAgua
from .penalid import Penalid
from .curva import Curva
from .agrint import AgrInt
from .adterm import AdTerm
from .ghmin import GHMin
from .sar import SAR
from .cvar import CVAR
from .ree import REE
from .re import RE
from .tecno import Tecno
from .abertura import Abertura
from .gee import GEE
from .clasgas import ClasGas

from typing import List, Type


class DeckEntrada:
    """
    Armazena todos os dados de entrada do NEWAVE.

    Esta classe lida com informações de entrada do NEWAVE e
    é relacionada a um diretório, que deve conter
    um deck de entrada do NEWAVE (unix-like).

    **Parâmetros**

    """

    modelos_arquivos: List[Type[Arquivo]] = [
                                             Caso,
                                             Arquivos,
                                             DGer,
                                             Sistema,
                                             Confhd,
                                             Modif,
                                             ConfT,
                                             Term,
                                             ClasT,
                                             Exph,
                                             Expt,
                                             Patamar,
                                             Shist,
                                             ManutT,
                                             VazPast,
                                             Itaipu,
                                             BID,
                                             CAdic,
                                             Perda,
                                             GTMinPat,
                                             ElNino,
                                             ENSOAux,
                                             DSVAgua,
                                             Penalid,
                                             Curva,
                                             AgrInt,
                                             AdTerm,
                                             GHMin,
                                             SAR,
                                             CVAR,
                                             REE,
                                             RE,
                                             Tecno,
                                             Abertura,
                                             GEE,
                                             ClasGas
                                            ]

    def __init__(self,
                 arquivos: List[Arquivo]) -> None:
        self.__arquivos_deck = arquivos

    @classmethod
    def le_deck(cls, diretorio: str):
        # Lê o arquivo caso.dat no diretorio, para saber os
        # nomes dos arquivos
        caso = Caso.le_arquivo(diretorio)
        # Lê o arquivos.dat no diretorio
        arquivos = Arquivos.le_arquivo(diretorio, caso.arquivo)
        # Lê os demais arquivos
        arquivos_deck = [t.le_arquivo(diretorio, n) for t, n in
                         zip(DeckEntrada.modelos_arquivos[2:],
                             arquivos.arquivos_entrada)]

        return cls([caso, arquivos] + arquivos_deck)

    def escreve_deck(self, diretorio: str):
        nomes_arquivos = self.arquivos.arquivos_entrada
        nomes_arquivos = ["caso.dat", self.caso.arquivo] + nomes_arquivos
        for arq, nome in zip(self.__arquivos_deck, nomes_arquivos):
            arq.escreve_arquivo(diretorio, nome)

    def __obtem_arquivo_por_indice(self, indice: int):
        return self.__arquivos_deck[indice]

    @property
    def caso(self) -> Caso:
        return self.__obtem_arquivo_por_indice(0)

    @property
    def arquivos(self) -> Arquivos:
        return self.__obtem_arquivo_por_indice(1)
