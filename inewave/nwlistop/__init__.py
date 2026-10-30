# Inclui os membros

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .c_v_rhq import CVRHQ as CVRHQ
    from .c_v_rhq_s import CVRHQs as CVRHQs
    from .c_v_rhv import CVRHV as CVRHV
    from .c_v_rhv_s import CVRHVs as CVRHVs
    from .cbomb import Cbomb as Cbomb
    from .cbombsin import Cbombsin as Cbombsin
    from .cdef import Cdef as Cdef
    from .cdefsin import Cdefsin as Cdefsin
    from .celetricas import Celetricas as Celetricas
    from .cmarg import Cmarg as Cmarg
    from .cmargmed import Cmargmed as Cmargmed
    from .coper import Coper as Coper
    from .corteolm import Corteolm as Corteolm
    from .cterm import Cterm as Cterm
    from .ctermsin import Ctermsin as Ctermsin
    from .custo_futuro import CustoFuturo as CustoFuturo
    from .cviol_eletrica import CviolEletrica as CviolEletrica
    from .cviol_eletricasin import CviolEletricasin as CviolEletricasin
    from .cviol_rhq import CviolRhq as CviolRhq
    from .cviol_rhq_sin import CviolRhqsin as CviolRhqsin
    from .cviol_rhv import CviolRhv as CviolRhv
    from .cviol_rhv_sin import CviolRhvsin as CviolRhvsin
    from .deficit import Def as Def
    from .defsin import Defsin as Defsin
    from .deletricas import Deletricas as Deletricas
    from .depminuh import Depminuh as Depminuh
    from .desvuh import Desvuh as Desvuh
    from .dfphauh import Dfphauh as Dfphauh
    from .dlppdfmax import Dlppdfmax as Dlppdfmax
    from .dlppdfmaxm import Dlppdfmaxm as Dlppdfmaxm
    from .dlppdfmaxs import Dlppdfmaxs as Dlppdfmaxs
    from .dlpptbmax import Dlpptbmax as Dlpptbmax
    from .dlpptbmaxm import Dlpptbmaxm as Dlpptbmaxm
    from .dlpptbmaxs import Dlpptbmaxs as Dlpptbmaxs
    from .dnegevap import Dnegevap as Dnegevap
    from .dposevap import Dposevap as Dposevap
    from .dtbmax import Dtbmax as Dtbmax
    from .dtbmin import Dtbmin as Dtbmin
    from .dvazmax import Dvazmax as Dvazmax
    from .eaf import Eaf as Eaf
    from .eafb import Eafb as Eafb
    from .eafbm import Eafbm as Eafbm
    from .eafbsin import Eafbsin as Eafbsin
    from .eafm import Eafm as Eafm
    from .earmf import Earmf as Earmf
    from .earmfm import Earmfm as Earmfm
    from .earmfp import Earmfp as Earmfp
    from .earmfpm import Earmfpm as Earmfpm
    from .earmfpsin import Earmfpsin as Earmfpsin
    from .earmfsin import Earmfsin as Earmfsin
    from .edesvc import Edesvc as Edesvc
    from .edesvcm import Edesvcm as Edesvcm
    from .edesvcsin import Edesvcsin as Edesvcsin
    from .evapo import Evapo as Evapo
    from .evapom import Evapom as Evapom
    from .evaporsin import Evaporsin as Evaporsin
    from .evert import Evert as Evert
    from .evertm import Evertm as Evertm
    from .evertsin import Evertsin as Evertsin
    from .exces import Exces as Exces
    from .excessin import Excessin as Excessin
    from .form_rhq import FormRHQ as FormRHQ
    from .form_rhv import FormRHV as FormRHV
    from .fteolm import Fteolm as Fteolm
    from .fteolsin import Fteolsin as Fteolsin
    from .geol import Geol as Geol
    from .geolm import Geolm as Geolm
    from .geolsin import Geolsin as Geolsin
    from .gh_fphexat import GhFphexat as GhFphexat
    from .ghidr import Ghidr as Ghidr
    from .ghidrm import Ghidrm as Ghidrm
    from .ghidrsin import Ghidrsin as Ghidrsin
    from .ghiduh import Ghiduh as Ghiduh
    from .ghmax import Ghmax as Ghmax
    from .ghmax_fpha import GhmaxFpha as GhmaxFpha
    from .ghmax_fphc import GhmaxFphc as GhmaxFphc
    from .ghmaxm import Ghmaxm as Ghmaxm
    from .ghmaxmr import Ghmaxmr as Ghmaxmr
    from .ghmaxr import Ghmaxr as Ghmaxr
    from .ghmaxrsin import Ghmaxrsin as Ghmaxrsin
    from .ghmaxsin import Ghmaxsin as Ghmaxsin
    from .ghtot import Ghtot as Ghtot
    from .ghtotm import Ghtotm as Ghtotm
    from .ghtotsin import Ghtotsin as Ghtotsin
    from .gtert import Gtert as Gtert
    from .gttot import Gttot as Gttot
    from .gttotsin import Gttotsin as Gttotsin
    from .hjus import Hjus as Hjus
    from .hliq import Hliq as Hliq
    from .hmont import Hmont as Hmont
    from .intercambio import Intercambio as Intercambio
    from .invade import Invade as Invade
    from .invadem import Invadem as Invadem
    from .mediasmerc import Mediasmerc as Mediasmerc
    from .mediasree import Mediasree as Mediasree
    from .mediasrep import Mediasrep as Mediasrep
    from .mediasrhq import Mediasrhq as Mediasrhq
    from .mediasrhv import Mediasrhv as Mediasrhv
    from .mediassin import Mediassin as Mediassin
    from .mediasusie import Mediasusie as Mediasusie
    from .mediasusih import Mediasusih as Mediasusih
    from .mediasusit import Mediasusit as Mediasusit
    from .mercl import Mercl as Mercl
    from .merclsin import Merclsin as Merclsin
    from .mevmin import Mevmin as Mevmin
    from .mevminm import Mevminm as Mevminm
    from .mevminsin import Mevminsin as Mevminsin
    from .nwlistopdat import Nwlistopdat as Nwlistopdat
    from .perdf import Perdf as Perdf
    from .perdfm import Perdfm as Perdfm
    from .perdfsin import Perdfsin as Perdfsin
    from .pivarm import Pivarm as Pivarm
    from .pivarmincr import Pivarmincr as Pivarmincr
    from .qafluh import Qafluh as Qafluh
    from .qbomb import Qbomb as Qbomb
    from .qdesviouh import Qdesviouh as Qdesviouh
    from .qincruh import Qincruh as Qincruh
    from .qturuh import Qturuh as Qturuh
    from .qvertuh import Qvertuh as Qvertuh
    from .rhslppdf import Rhslppdf as Rhslppdf
    from .rhslpptb import Rhslpptb as Rhslpptb
    from .vagua import Vagua as Vagua
    from .valor_agua import ValorAgua as ValorAgua
    from .varmpuh import Varmpuh as Varmpuh
    from .varmuh import Varmuh as Varmuh
    from .vbomb import Vbomb as Vbomb
    from .vdesviouh import Vdesviouh as Vdesviouh
    from .vento import Vento as Vento
    from .vertuh import Vertuh as Vertuh
    from .verturb import Verturb as Verturb
    from .verturbm import Verturbm as Verturbm
    from .verturbsin import Verturbsin as Verturbsin
    from .vevapuh import Vevapuh as Vevapuh
    from .vevmin import Vevmin as Vevmin
    from .vevminm import Vevminm as Vevminm
    from .vevminsin import Vevminsin as Vevminsin
    from .vghmin import Vghmin as Vghmin
    from .vghminm import Vghminm as Vghminm
    from .vghminsin import Vghminsin as Vghminsin
    from .vghminuh import Vghminuh as Vghminuh
    from .viol_eletrica import ViolEletrica as ViolEletrica
    from .viol_eletricasin import ViolEletricasin as ViolEletricasin
    from .viol_evmin import ViolEvmin as ViolEvmin
    from .viol_evminm import ViolEvminm as ViolEvminm
    from .viol_evminsin import ViolEvminsin as ViolEvminsin
    from .viol_fpha import ViolFpha as ViolFpha
    from .viol_ghmin import ViolGhmin as ViolGhmin
    from .viol_ghminm import ViolGhminm as ViolGhminm
    from .viol_ghminsin import ViolGhminsin as ViolGhminsin
    from .viol_ghminuh import ViolGhminuh as ViolGhminuh
    from .viol_lpp_dfmax import ViolLppDfmax as ViolLppDfmax
    from .viol_lpp_dfmaxm import ViolLppDfmaxm as ViolLppDfmaxm
    from .viol_lpp_dfmaxsin import ViolLppDfmaxsin as ViolLppDfmaxsin
    from .viol_lpp_tbmax import ViolLppTbmax as ViolLppTbmax
    from .viol_lpp_tbmaxm import ViolLppTbmaxm as ViolLppTbmaxm
    from .viol_lpp_tbmaxsin import ViolLppTbmaxsin as ViolLppTbmaxsin
    from .viol_neg_evap import ViolNegEvap as ViolNegEvap
    from .viol_neg_vretiruh import ViolNegVretiruh as ViolNegVretiruh
    from .viol_pos_evap import ViolPosEvap as ViolPosEvap
    from .viol_pos_vretiruh import ViolPosVretiruh as ViolPosVretiruh
    from .viol_rhq import ViolRHQ as ViolRHQ
    from .viol_rhv import ViolRHV as ViolRHV
    from .viol_turbmax import ViolTurbmax as ViolTurbmax
    from .viol_turbmin import ViolTurbmin as ViolTurbmin
    from .viol_vazmax import ViolVazmax as ViolVazmax
    from .viol_vazmin import ViolVazmin as ViolVazmin
    from .vmort import Vmort as Vmort
    from .vmortm import Vmortm as Vmortm
    from .vmortsin import Vmortsin as Vmortsin
    from .vretiradauh import Vretiradauh as Vretiradauh
    from .vturuh import Vturuh as Vturuh

_LAZY_IMPORTS: dict[str, str] = {
    # Deprecated
    "CVRHQs": "c_v_rhq_s",
    "CVRHQ": "c_v_rhq",
    "CVRHVs": "c_v_rhv_s",
    "CVRHV": "c_v_rhv",
    "Celetricas": "celetricas",
    "Vdesviouh": "vdesviouh",
    "Vturuh": "vturuh",
    "Vertuh": "vertuh",
    "Vagua": "vagua",
    "Deletricas": "deletricas",
    "Vevmin": "vevmin",
    "Vevminm": "vevminm",
    "Vevminsin": "vevminsin",
    "Dfphauh": "dfphauh",
    "Vghmin": "vghmin",
    "Vghminm": "vghminm",
    "Vghminsin": "vghminsin",
    "Vghminuh": "vghminuh",
    "Dlppdfmax": "dlppdfmax",
    "Dlppdfmaxm": "dlppdfmaxm",
    "Dlppdfmaxs": "dlppdfmaxs",
    "Dlpptbmax": "dlpptbmax",
    "Dlpptbmaxm": "dlpptbmaxm",
    "Dlpptbmaxs": "dlpptbmaxs",
    "Dtbmax": "dtbmax",
    "Dtbmin": "dtbmin",
    "Dvazmax": "dvazmax",
    "Depminuh": "depminuh",
    "Desvuh": "desvuh",
    "Dposevap": "dposevap",
    "Dnegevap": "dnegevap",
    "Vbomb": "vbomb",
    "Nwlistopdat": "nwlistopdat",
    "CviolRhqsin": "cviol_rhq_sin",
    "CviolRhq": "cviol_rhq",
    "CviolRhvsin": "cviol_rhv_sin",
    "CviolRhv": "cviol_rhv",
    "Cbomb": "cbomb",
    "Cbombsin": "cbombsin",
    "Cdef": "cdef",
    "Cdefsin": "cdefsin",
    "CviolEletrica": "cviol_eletrica",
    "CviolEletricasin": "cviol_eletricasin",
    "Cmarg": "cmarg",
    "Cmargmed": "cmargmed",
    "Coper": "coper",
    "CustoFuturo": "custo_futuro",
    "Corteolm": "corteolm",
    "Cterm": "cterm",
    "Ctermsin": "ctermsin",
    "Def": "deficit",
    "Defsin": "defsin",
    "Edesvc": "edesvc",
    "Edesvcm": "edesvcm",
    "Edesvcsin": "edesvcsin",
    "Evapo": "evapo",
    "Evapom": "evapom",
    "Evaporsin": "evaporsin",
    "Evert": "evert",
    "Evertm": "evertm",
    "Evertsin": "evertsin",
    "Exces": "exces",
    "Excessin": "excessin",
    "FormRHQ": "form_rhq",
    "FormRHV": "form_rhv",
    "Fteolm": "fteolm",
    "Fteolsin": "fteolsin",
    "Eaf": "eaf",
    "Eafb": "eafb",
    "Eafbm": "eafbm",
    "Eafbsin": "eafbsin",
    "Eafm": "eafm",
    "Earmf": "earmf",
    "Earmfm": "earmfm",
    "Earmfp": "earmfp",
    "Earmfpm": "earmfpm",
    "Earmfsin": "earmfsin",
    "Earmfpsin": "earmfpsin",
    "Geol": "geol",
    "Geolm": "geolm",
    "Geolsin": "geolsin",
    "GhFphexat": "gh_fphexat",
    "Ghiduh": "ghiduh",
    "GhmaxFpha": "ghmax_fpha",
    "GhmaxFphc": "ghmax_fphc",
    "Ghmax": "ghmax",
    "Ghmaxm": "ghmaxm",
    "Ghmaxmr": "ghmaxmr",
    "Ghmaxr": "ghmaxr",
    "Ghmaxrsin": "ghmaxrsin",
    "Ghmaxsin": "ghmaxsin",
    "Ghidr": "ghidr",
    "Ghidrm": "ghidrm",
    "Ghidrsin": "ghidrsin",
    "Ghtot": "ghtot",
    "Ghtotm": "ghtotm",
    "Ghtotsin": "ghtotsin",
    "Gtert": "gtert",
    "Gttot": "gttot",
    "Gttotsin": "gttotsin",
    "Hjus": "hjus",
    "Hliq": "hliq",
    "Hmont": "hmont",
    "Intercambio": "intercambio",
    "Invade": "invade",
    "Invadem": "invadem",
    "Mediassin": "mediassin",
    "Mediasmerc": "mediasmerc",
    "Mediasree": "mediasree",
    "Mediasusih": "mediasusih",
    "Mediasusit": "mediasusit",
    "Mediasusie": "mediasusie",
    "Mediasrep": "mediasrep",
    "Mediasrhq": "mediasrhq",
    "Mediasrhv": "mediasrhv",
    "Mercl": "mercl",
    "Merclsin": "merclsin",
    "Mevmin": "mevmin",
    "Mevminm": "mevminm",
    "Mevminsin": "mevminsin",
    "Perdf": "perdf",
    "Perdfm": "perdfm",
    "Perdfsin": "perdfsin",
    "Pivarm": "pivarm",
    "Pivarmincr": "pivarmincr",
    "Qafluh": "qafluh",
    "Qincruh": "qincruh",
    "Rhslppdf": "rhslppdf",
    "Rhslpptb": "rhslpptb",
    "ValorAgua": "valor_agua",
    "Varmpuh": "varmpuh",
    "Varmuh": "varmuh",
    "Qbomb": "qbomb",
    "Vento": "vento",
    "Qvertuh": "qvertuh",
    "Verturb": "verturb",
    "Verturbm": "verturbm",
    "Verturbsin": "verturbsin",
    "Qturuh": "qturuh",
    "Qdesviouh": "qdesviouh",
    "Vmort": "vmort",
    "Vmortm": "vmortm",
    "Vmortsin": "vmortsin",
    "Vevapuh": "vevapuh",
    "ViolEletricasin": "viol_eletricasin",
    "Vretiradauh": "vretiradauh",
    "ViolFpha": "viol_fpha",
    "ViolLppDfmax": "viol_lpp_dfmax",
    "ViolLppDfmaxm": "viol_lpp_dfmaxm",
    "ViolLppDfmaxsin": "viol_lpp_dfmaxsin",
    "ViolLppTbmax": "viol_lpp_tbmax",
    "ViolLppTbmaxm": "viol_lpp_tbmaxm",
    "ViolLppTbmaxsin": "viol_lpp_tbmaxsin",
    "ViolTurbmax": "viol_turbmax",
    "ViolTurbmin": "viol_turbmin",
    "ViolVazmax": "viol_vazmax",
    "ViolVazmin": "viol_vazmin",
    "ViolEvmin": "viol_evmin",
    "ViolEvminm": "viol_evminm",
    "ViolEvminsin": "viol_evminsin",
    "ViolGhmin": "viol_ghmin",
    "ViolGhminm": "viol_ghminm",
    "ViolGhminsin": "viol_ghminsin",
    "ViolGhminuh": "viol_ghminuh",
    "ViolRHQ": "viol_rhq",
    "ViolRHV": "viol_rhv",
    "ViolEletrica": "viol_eletrica",
    "ViolPosEvap": "viol_pos_evap",
    "ViolNegEvap": "viol_neg_evap",
    "ViolNegVretiruh": "viol_neg_vretiruh",
    "ViolPosVretiruh": "viol_pos_vretiruh",
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
