import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from datetime import datetime
from inewave.config import MESES_DF

__COLS_IDENTIFICACAO = ["data", "ano", "serie", "patamar", "classe"]


def __formata_df_meses_para_datas_serie(df: pd.DataFrame) -> pd.DataFrame:
    anos = np.array(df["ano"].unique().tolist())
    datas = pd.date_range(
        datetime(year=anos[0], month=1, day=1),
        datetime(year=anos[-1], month=12, day=1),
        freq="MS",
    )
    df_series = pd.DataFrame()
    for a in anos:
        df_ano = df.loc[df["ano"] == a, MESES_DF].T
        df_ano.columns = [str(s) for s in list(range(1, df_ano.shape[1] + 1))]
        df_series = pd.concat([df_series, df_ano], ignore_index=True)
    df_series["data"] = datas
    cols_not_scenarios = [
        c for c in df_series.columns if c in __COLS_IDENTIFICACAO
    ]
    cols_scenarios = [
        c for c in df_series.columns if c not in __COLS_IDENTIFICACAO
    ]
    df_formatado = pd.melt(
        df_series,
        id_vars=cols_not_scenarios,
        value_vars=cols_scenarios,
        var_name="serie",
        value_name="valor",
    )
    return df_formatado


def __formata_df_meses_para_datas_serie_patamar(
    df: pd.DataFrame,
) -> pd.DataFrame:
    anos = np.array(df["ano"].unique().tolist())
    patamares = np.array(df["patamar"].unique().tolist())
    datas = []
    for a in anos:
        for _ in patamares:
            datas += pd.date_range(
                datetime(year=a, month=1, day=1),
                datetime(year=a, month=12, day=1),
                freq="MS",
            ).tolist()
    df_series = pd.DataFrame()
    for a in anos:
        for p in patamares:
            df_ano_patamar = df.loc[
                (df["ano"] == a) & (df["patamar"] == p),
                MESES_DF,
            ].T
            cols = [
                str(s) for s in list(range(1, df_ano_patamar.shape[1] + 1))
            ]
            df_ano_patamar.columns = cols
            df_ano_patamar["patamar"] = str(p)
            df_ano_patamar = df_ano_patamar[["patamar"] + cols]
            df_series = pd.concat(
                [df_series, df_ano_patamar], ignore_index=True
            )
    df_series["data"] = datas
    cols_not_scenarios = [
        c for c in df_series.columns if c in __COLS_IDENTIFICACAO
    ]
    cols_scenarios = [
        c for c in df_series.columns if c not in __COLS_IDENTIFICACAO
    ]
    df_formatado = pd.melt(
        df_series,
        id_vars=cols_not_scenarios,
        value_vars=cols_scenarios,
        var_name="serie",
        value_name="valor",
    )
    return df_formatado[["data", "patamar", "serie", "valor"]]


def __formata_df_meses_para_datas_classetermica_serie_patamar(
    df: pd.DataFrame,
) -> pd.DataFrame:
    anos = np.array(df["ano"].unique().tolist())
    patamares = np.array(df["patamar"].unique().tolist())
    classes = np.array(df["classe"].unique().tolist())
    datas = []
    for a in anos:
        for _ in patamares:
            for _ in classes:
                datas += pd.date_range(
                    datetime(year=a, month=1, day=1),
                    datetime(year=a, month=12, day=1),
                    freq="MS",
                ).tolist()
    df_series = pd.DataFrame()
    for a in anos:
        for c in classes:
            for p in patamares:
                df_ano_classe_patamar = df.loc[
                    (df["ano"] == a)
                    & (df["classe"] == c)
                    & (df["patamar"] == p),
                    MESES_DF,
                ].T
                cols = [
                    str(s)
                    for s in list(range(1, df_ano_classe_patamar.shape[1] + 1))
                ]
                df_ano_classe_patamar.columns = cols
                df_ano_classe_patamar["classe"] = str(c)
                df_ano_classe_patamar["patamar"] = str(p)
                df_ano_classe_patamar = df_ano_classe_patamar[
                    ["classe", "patamar"] + cols
                ]
                df_series = pd.concat(
                    [df_series, df_ano_classe_patamar], ignore_index=True
                )
    df_series["data"] = datas
    cols_not_scenarios = [
        c for c in df_series.columns if c in __COLS_IDENTIFICACAO
    ]
    cols_scenarios = [
        c for c in df_series.columns if c not in __COLS_IDENTIFICACAO
    ]
    df_formatado = pd.melt(
        df_series,
        id_vars=cols_not_scenarios,
        value_vars=cols_scenarios,
        var_name="serie",
        value_name="valor",
    )
    return df_formatado[["classe", "data", "patamar", "serie", "valor"]]


def formata_df_meses_para_datas_nwlistop(df: pd.DataFrame) -> pd.DataFrame:
    colunas_df = df.columns.tolist()
    colunas_identificacao = tuple(
        [c for c in colunas_df if c in __COLS_IDENTIFICACAO]
    )
    mapa_formatacao = {
        ("ano", "serie"): __formata_df_meses_para_datas_serie,
        (
            "ano",
            "serie",
            "patamar",
        ): __formata_df_meses_para_datas_serie_patamar,
        (
            "ano",
            "classe",
            "serie",
            "patamar",
        ): __formata_df_meses_para_datas_classetermica_serie_patamar,
    }
    return mapa_formatacao[colunas_identificacao](df)
