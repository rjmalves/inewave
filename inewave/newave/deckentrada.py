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
from .eafpast import EafPast
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
from os.path import join


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

        def le_vazpast_eafpast(nome: str):
            # Lê a primeira linha do arquivo
            with open(join(diretorio, nome), "r") as arq:
                # Se tiver a palavra "SISTEMA", é EafPast
                if "SISTEMA" in arq.readline():
                    arquivos_deck.append(EafPast.le_arquivo(diretorio, n))
                else:
                    arquivos_deck.append(VazPast.le_arquivo(diretorio, n))

        # Lê o arquivo caso.dat no diretorio, para saber os
        # nomes dos arquivos
        caso = Caso.le_arquivo(diretorio)
        # Lê o arquivos.dat no diretorio
        arquivos = Arquivos.le_arquivo(diretorio, caso.arquivo)
        # Lê os demais arquivos
        arquivos_deck: List[Arquivo] = []
        for t, n in zip(DeckEntrada.modelos_arquivos[2:],
                        arquivos.arquivos_entrada):
            # Pro caso do VazPast, também pode ser EafPast
            if t == VazPast:
                le_vazpast_eafpast(n)
            else:
                arquivos_deck.append(t.le_arquivo(diretorio, n))

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

    @property
    def dger(self) -> DGer:
        return self.__obtem_arquivo_por_indice(2)

    @property
    def sistema(self) -> Sistema:
        return self.__obtem_arquivo_por_indice(3)

    @property
    def confhd(self) -> Confhd:
        return self.__obtem_arquivo_por_indice(4)

    @property
    def modif(self) -> Modif:
        return self.__obtem_arquivo_por_indice(5)

    @property
    def conft(self) -> ConfT:
        return self.__obtem_arquivo_por_indice(6)

    @property
    def term(self) -> Term:
        return self.__obtem_arquivo_por_indice(7)

    @property
    def clast(self) -> ClasT:
        return self.__obtem_arquivo_por_indice(8)

    @property
    def exph(self) -> Exph:
        return self.__obtem_arquivo_por_indice(9)

    @property
    def expt(self) -> Expt:
        return self.__obtem_arquivo_por_indice(10)

    @property
    def patamar(self) -> Patamar:
        return self.__obtem_arquivo_por_indice(11)

    @property
    def shist(self) -> Shist:
        return self.__obtem_arquivo_por_indice(12)

    @property
    def manutt(self) -> ManutT:
        return self.__obtem_arquivo_por_indice(13)

    @property
    def eafpast(self) -> EafPast:
        if type(self.__obtem_arquivo_por_indice(14)) != EafPast:
            raise ValueError("Arquivo Eafpast não fornecido")
        return self.__obtem_arquivo_por_indice(14)

    @property
    def vazpast(self) -> VazPast:
        if type(self.__obtem_arquivo_por_indice(14)) != VazPast:
            raise ValueError("Arquivo VazPast não fornecido")
        return self.__obtem_arquivo_por_indice(14)

    @property
    def itaipu(self) -> Itaipu:
        return self.__obtem_arquivo_por_indice(15)

    @property
    def bid(self) -> BID:
        return self.__obtem_arquivo_por_indice(16)

    @property
    def cadic(self) -> CAdic:
        return self.__obtem_arquivo_por_indice(17)

    @property
    def perda(self) -> Perda:
        return self.__obtem_arquivo_por_indice(18)

    @property
    def gtminpat(self) -> GTMinPat:
        return self.__obtem_arquivo_por_indice(19)

    @property
    def elnino(self) -> ElNino:
        return self.__obtem_arquivo_por_indice(20)

    @property
    def ensoaux(self) -> ENSOAux:
        return self.__obtem_arquivo_por_indice(21)

    @property
    def dsvagua(self) -> DSVAgua:
        return self.__obtem_arquivo_por_indice(22)

    @property
    def penalid(self) -> Penalid:
        return self.__obtem_arquivo_por_indice(23)

    @property
    def curva(self) -> Curva:
        return self.__obtem_arquivo_por_indice(24)

    @property
    def agrint(self) -> AgrInt:
        return self.__obtem_arquivo_por_indice(25)

    @property
    def adterm(self) -> AdTerm:
        return self.__obtem_arquivo_por_indice(26)

    @property
    def ghmin(self) -> GHMin:
        return self.__obtem_arquivo_por_indice(27)

    @property
    def sar(self) -> SAR:
        return self.__obtem_arquivo_por_indice(28)

    @property
    def cvar(self) -> CVAR:
        return self.__obtem_arquivo_por_indice(29)

    @property
    def ree(self) -> REE:
        return self.__obtem_arquivo_por_indice(30)

    @property
    def re(self) -> RE:
        return self.__obtem_arquivo_por_indice(31)

    @property
    def tecno(self) -> Tecno:
        return self.__obtem_arquivo_por_indice(32)

    @property
    def abertura(self) -> Abertura:
        return self.__obtem_arquivo_por_indice(33)

    @property
    def gee(self) -> GEE:
        return self.__obtem_arquivo_por_indice(34)

    @property
    def clasgas(self) -> ClasGas:
        return self.__obtem_arquivo_por_indice(34)
