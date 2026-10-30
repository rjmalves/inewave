# Testes da tipagem estática exposta pelo pacote
import inspect
from typing import Any, Callable, List, Literal, Type, get_args, get_overloads

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
