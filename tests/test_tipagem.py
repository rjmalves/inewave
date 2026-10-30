# Testes da tipagem estática exposta pelo pacote
import ast
import importlib
import inspect
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    get_args,
    get_overloads,
)

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
import pytest

from inewave.libs import Eolica, Indices, Restricoes, UsinasHidreletricas
from inewave.newave import Modif

CLASSES_COM_ACESSORES_DF = [
    Eolica,
    Indices,
    Modif,
    Restricoes,
    UsinasHidreletricas,
]


def _acessores_df(classe: Type[Any]) -> List[Callable[..., Any]]:
    return [
        f
        for nome, f in inspect.getmembers(classe, inspect.isfunction)
        if not nome.startswith("_") and "df" in inspect.signature(f).parameters
    ]


def _parametros_sem_df(f: Callable[..., Any]) -> List[Any]:
    return [
        (p.name, p.default, p.annotation)
        for p in inspect.signature(f).parameters.values()
        if p.name != "df"
    ]


def _contem_dataframe(anotacao: Any) -> bool:
    if anotacao is pd.DataFrame:
        return True
    return any(_contem_dataframe(a) for a in get_args(anotacao))


@pytest.mark.parametrize(
    "classe", CLASSES_COM_ACESSORES_DF, ids=lambda c: c.__name__
)
def test_acessores_df_tem_overloads(classe: Type[Any]) -> None:
    acessores = _acessores_df(classe)
    assert acessores
    for f in acessores:
        stubs = get_overloads(f)
        assert len(stubs) == 3, f.__qualname__
        verdadeiro, falso, booleano = (
            inspect.signature(s).parameters["df"] for s in stubs
        )
        # df=True só pode ser passado por nome e retorna sempre um DataFrame
        assert verdadeiro.annotation == Literal[True], f.__qualname__
        assert verdadeiro.kind is inspect.Parameter.KEYWORD_ONLY
        assert inspect.signature(stubs[0]).return_annotation is pd.DataFrame
        assert falso.annotation == Literal[False], f.__qualname__
        assert not _contem_dataframe(
            inspect.signature(stubs[1]).return_annotation
        ), f.__qualname__
        assert booleano.annotation is bool, f.__qualname__
        assert (
            inspect.signature(stubs[2]).return_annotation
            == inspect.signature(f).return_annotation
        ), f.__qualname__
        for s in stubs:
            assert _parametros_sem_df(s) == _parametros_sem_df(f), (
                f.__qualname__
            )


PACOTES_LAZY = ["inewave.newave", "inewave.nwlistop"]


@pytest.mark.parametrize("pacote", PACOTES_LAZY)
def test_imports_de_tipagem_iguais_a_tabela_lazy(pacote: str) -> None:
    # Os verificadores de tipo leem o bloco TYPE_CHECKING, e o tempo de
    # execução lê _LAZY_IMPORTS: os dois precisam listar os mesmos nomes
    modulo = importlib.import_module(pacote)
    arvore = ast.parse(inspect.getsource(modulo))
    blocos = [
        n
        for n in arvore.body
        if isinstance(n, ast.If) and ast.unparse(n.test) == "TYPE_CHECKING"
    ]
    assert len(blocos) == 1
    importados: Dict[str, Optional[str]] = {}
    for n in blocos[0].body:
        assert isinstance(n, ast.ImportFrom) and n.level == 1
        for alias in n.names:
            # "import X as X" marca a reexportação explícita
            assert alias.asname == alias.name
            importados[alias.name] = n.module
    assert importados == modulo._LAZY_IMPORTS


@pytest.mark.parametrize("pacote", PACOTES_LAZY)
def test_tabela_lazy_cobre_todos_os_modulos(pacote: str) -> None:
    modulo = importlib.import_module(pacote)
    pasta = Path(inspect.getfile(modulo)).parent
    modulos = {p.stem for p in pasta.glob("*.py") if p.stem != "__init__"}
    assert modulos == set(modulo._LAZY_IMPORTS.values())


@pytest.mark.parametrize("pacote", PACOTES_LAZY)
def test_nomes_lazy_resolvem_para_as_classes(pacote: str) -> None:
    modulo = importlib.import_module(pacote)
    for nome, submodulo in modulo._LAZY_IMPORTS.items():
        classe = getattr(modulo, nome)
        assert inspect.isclass(classe), nome
        assert classe.__module__ == f"{pacote}.{submodulo}", nome


def test_arquivos_nwlistop_satisfazem_arquivo_com_valores() -> None:
    import inewave.nwlistop as nwlistop

    esperado = inspect.signature(
        nwlistop.ArquivoComValores.valores.fget
    ).return_annotation
    assert not hasattr(nwlistop.Nwlistopdat, "valores")
    for nome in nwlistop.__all__:
        if nome in ("ArquivoComValores", "Nwlistopdat"):
            continue
        propriedade = inspect.getattr_static(
            getattr(nwlistop, nome), "valores", None
        )
        assert isinstance(propriedade, property), nome
        assert (
            inspect.signature(propriedade.fget).return_annotation == esperado
        ), nome
