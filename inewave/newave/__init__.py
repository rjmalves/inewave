# Inclui os membros

import importlib
from typing import Any

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
