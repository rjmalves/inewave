# Inclui os membros

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .abertura import Abertura as Abertura
    from .adterm import Adterm as Adterm
    from .agrint import Agrint as Agrint
    from .arquivos import Arquivos as Arquivos
    from .avl_cortesfpha_nwv import AvlCortesFpha as AvlCortesFpha
    from .avl_desvfpha_s import AvlDesvFphaS as AvlDesvFphaS
    from .avl_desvfpha_v_q import AvlDesvFphaVQ as AvlDesvFphaVQ
    from .bid import BID as BID
    from .cadic import Cadic as Cadic
    from .caso import Caso as Caso
    from .clasgas import Clasgas as Clasgas
    from .clast import Clast as Clast
    from .confhd import Confhd as Confhd
    from .conft import Conft as Conft
    from .cortes import Cortes as Cortes
    from .cortese import Cortese as Cortese
    from .cortesh import Cortesh as Cortesh
    from .curva import Curva as Curva
    from .cvar import Cvar as Cvar
    from .dger import Dger as Dger
    from .dsvagua import Dsvagua as Dsvagua
    from .eafpast import Eafpast as Eafpast
    from .eco_fpha import EcoFpha as EcoFpha
    from .eliminacao_cortes import EliminacaoCortes as EliminacaoCortes
    from .elnino import ElNino as ElNino
    from .enavazb import Enavazb as Enavazb
    from .enavazf import Enavazf as Enavazf
    from .energiab import Energiab as Energiab
    from .energiaf import Energiaf as Energiaf
    from .energias import Energias as Energias
    from .engnat import Engnat as Engnat
    from .ensoaux import ENSOAux as ENSOAux
    from .evap_avl_desv import EvapAvlDesv as EvapAvlDesv
    from .evap_cortes import EvapCortes as EvapCortes
    from .evap_eco import EvapEco as EvapEco
    from .exph import Exph as Exph
    from .expt import Expt as Expt
    from .forward import Forward as Forward
    from .forwarh import Forwarh as Forwarh
    from .fpha_avl_desv_s import FphaAvlDesvS as FphaAvlDesvS
    from .fpha_avl_desv_v_q import FphaAvlDesvVQ as FphaAvlDesvVQ
    from .fpha_cortes import FphaCortes as FphaCortes
    from .fpha_eco import FphaEco as FphaEco
    from .gee import GEE as GEE
    from .ghmin import Ghmin as Ghmin
    from .gtminpat import Gtminpat as Gtminpat
    from .hidr import Hidr as Hidr
    from .itaipu import Itaipu as Itaipu
    from .manutt import Manutt as Manutt
    from .modif import Modif as Modif
    from .newavetim import Newavetim as Newavetim
    from .nwv_avl_evap import NwvAvlEvap as NwvAvlEvap
    from .nwv_cortes_evap import NwvCortesEvap as NwvCortesEvap
    from .nwv_eco_evap import NwvEcoEvap as NwvEcoEvap
    from .parp import Parp as Parp
    from .parpeol import Parpeol as Parpeol
    from .parpvaz import Parpvaz as Parpvaz
    from .patamar import Patamar as Patamar
    from .penalid import Penalid as Penalid
    from .perda import Perda as Perda
    from .pmo import Pmo as Pmo
    from .re import Re as Re
    from .ree import Ree as Ree
    from .sar import Sar as Sar
    from .selcor import Selcor as Selcor
    from .shist import Shist as Shist
    from .sistema import Sistema as Sistema
    from .tecno import Tecno as Tecno
    from .term import Term as Term
    from .vazaob import Vazaob as Vazaob
    from .vazaof import Vazaof as Vazaof
    from .vazaos import Vazaos as Vazaos
    from .vazinat import Vazinat as Vazinat
    from .vazoes import Vazoes as Vazoes
    from .vazpast import Vazpast as Vazpast
    from .volref_saz import VolrefSaz as VolrefSaz

_LAZY_IMPORTS: dict[str, str] = {
    # Deprecated
    "AvlCortesFpha": "avl_cortesfpha_nwv",
    "AvlDesvFphaS": "avl_desvfpha_s",
    "AvlDesvFphaVQ": "avl_desvfpha_v_q",
    "EcoFpha": "eco_fpha",
    "NwvAvlEvap": "nwv_avl_evap",
    "NwvCortesEvap": "nwv_cortes_evap",
    "NwvEcoEvap": "nwv_eco_evap",
    "Abertura": "abertura",
    "Adterm": "adterm",
    "Agrint": "agrint",
    "Arquivos": "arquivos",
    "BID": "bid",
    "Cadic": "cadic",
    "Caso": "caso",
    "Clasgas": "clasgas",
    "Clast": "clast",
    "Confhd": "confhd",
    "Conft": "conft",
    "Cortes": "cortes",
    "Cortese": "cortese",
    "Cortesh": "cortesh",
    "Curva": "curva",
    "Cvar": "cvar",
    "Dger": "dger",
    "Dsvagua": "dsvagua",
    "Eafpast": "eafpast",
    "EliminacaoCortes": "eliminacao_cortes",
    "ElNino": "elnino",
    "ENSOAux": "ensoaux",
    "Exph": "exph",
    "Expt": "expt",
    "Forward": "forward",
    "Forwarh": "forwarh",
    "GEE": "gee",
    "Ghmin": "ghmin",
    "Gtminpat": "gtminpat",
    "Hidr": "hidr",
    "Itaipu": "itaipu",
    "Manutt": "manutt",
    "Modif": "modif",
    "Newavetim": "newavetim",
    "Parp": "parp",
    "Parpvaz": "parpvaz",
    "Parpeol": "parpeol",
    "Patamar": "patamar",
    "Penalid": "penalid",
    "Perda": "perda",
    "Pmo": "pmo",
    "Re": "re",
    "Ree": "ree",
    "Sar": "sar",
    "Shist": "shist",
    "Selcor": "selcor",
    "Sistema": "sistema",
    "Tecno": "tecno",
    "Term": "term",
    "Vazoes": "vazoes",
    "Vazpast": "vazpast",
    "VolrefSaz": "volref_saz",
    "FphaCortes": "fpha_cortes",
    "FphaAvlDesvS": "fpha_avl_desv_s",
    "FphaAvlDesvVQ": "fpha_avl_desv_v_q",
    "FphaEco": "fpha_eco",
    "EvapAvlDesv": "evap_avl_desv",
    "EvapCortes": "evap_cortes",
    "EvapEco": "evap_eco",
    "Energiaf": "energiaf",
    "Energiab": "energiab",
    "Energias": "energias",
    "Enavazf": "enavazf",
    "Enavazb": "enavazb",
    "Engnat": "engnat",
    "Vazaof": "vazaof",
    "Vazaob": "vazaob",
    "Vazaos": "vazaos",
    "Vazinat": "vazinat",
}

__all__ = sorted(_LAZY_IMPORTS.keys())


def __getattr__(name: str) -> Any:
    if name in _LAZY_IMPORTS:
        module = importlib.import_module(f".{_LAZY_IMPORTS[name]}", __name__)
        value = getattr(module, name)
        globals()[name] = value  # cache for subsequent access
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return __all__
