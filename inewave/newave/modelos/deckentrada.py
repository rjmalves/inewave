from .dger import DGer
from .sistema import Sistema
from .confhd import Confhd
from .modif import Modif
from .conft import Conft
from .term import Term
from .clast import Clast
from .exph import Exph
from .expt import Expt
from .patamar import Patamar
from .shist import Shist
from .manutt import Manutt
from .vazpast import VazPast
from .cadic import CAdic
from .perda import Perda
from .gtminpat import GTMinPat
from .dsvagua import DSVAgua
from .penalid import Penalid
from .curva import Curva
from .agrint import AgrInt
from .adterm import AdTerm
from .ghmin import GhMin
from .sar import SAR
from .cvar import CVAR
from .ree import REE
from .re import RE
from .tecno import Tecno
from .abertura import Abertura
from .gee import GEE
from .clasgas import ClasGas


class DeckEntrada:
    """
    Armazena todos os dados de entrada do NEWAVE.

    Esta classe lida com informações de entrada do NEWAVE e
    é relacionada a um diretório, que deve conter
    um deck de entrada do NEWAVE (unix-like).

    **Parâmetros**

    """

    def __init__(self,
                 dger: DGer,
                 sistema: Sistema,
                 confhd: Confhd,
                 modif: Modif,
                 conft: Conft,
                 term: Term,
                 clast: Clast,
                 exph: Exph,
                 expt: Expt,
                 patamar: Patamar,
                 shist: Shist,
                 manutt: Manutt,
                 vazpast: VazPast,
                 cadic: CAdic,
                 perda: Perda,
                 gtminpat: GTMinPat,
                 dsvagua: DSVAgua,
                 penalid: Penalid,
                 curva: Curva,
                 agrint: AgrInt,
                 adterm: AdTerm,
                 ghmin: GhMin,
                 sar: SAR,
                 cvar: CVAR,
                 ree: REE,
                 re: RE,
                 tecno: Tecno,
                 abertura: Abertura,
                 gee: GEE,
                 clasgas: ClasGas) -> None:
        self.dger = dger
        self.sistema = sistema
        self.confhd = confhd
        self.modif = modif
        self.conft = conft
        self.term = term
        self.clast = clast
        self.exph = exph
        self.expt = expt
        self.patamar = patamar
        self.shist = shist
        self.manutt = manutt
        self.vazpast = vazpast
        self.cadic = cadic
        self.perda = perda
        self.gtminpat = gtminpat
        self.dsvagua = dsvagua
        self.penalid = penalid
        self.curva = curva
        self.agrint = agrint
        self.adterm = adterm
        self.ghmin = ghmin
        self.sar = sar
        self.cvar = cvar
        self.ree = ree
        self.re = re
        self.tecno = tecno
        self.abertura = abertura
        self.gee = gee
        self.clasgas = clasgas
