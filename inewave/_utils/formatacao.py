import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from datetime import datetime
from inewave.config import MESES_DF
from typing import List

__COLS_IDENTIFICACAO = ["data", "ano", "serie", "patamar", "classe"]


def __formata_df_meses_para_datas_serie(df: pd.DataFrame) -> pd.DataFrame:
    anos = np.array(df["ano"].unique().tolist())
    series = np.array(df["serie"].unique().tolist())
    n_series = len(series)
    datas_df = []
    series_df = []
    for a in anos:
        datas_df.append(
            np.tile(
                pd.date_range(
                    datetime(year=a, month=1, day=1),
                    datetime(year=a, month=12, day=1),
                    freq="MS",
                ).to_numpy(),
                n_series,
            ),
        )
        series_df.append(np.repeat(series, 12))
    valores = []
    for a in anos:
        valores.append(
            df.loc[
                (df["ano"] == a),
                MESES_DF,
            ]
            .to_numpy()
            .flatten()
        )
    df_formatado = pd.DataFrame(
        data={
            "data": np.concatenate(datas_df),
            "serie": np.concatenate(series_df),
            "valor": np.concatenate(valores),
        }
    )
    return df_formatado


def __formata_df_meses_para_datas_serie_patamar(
    df: pd.DataFrame,
) -> pd.DataFrame:
    anos = np.array(df["ano"].unique().tolist())
    series = np.array(df["serie"].unique().tolist())
    patamares = np.array(df["patamar"].unique().tolist())
    n_series = len(series)
    n_patamares = len(patamares)
    datas_df = []
    patamares_df = []
    series_df = []
    for a in anos:
        datas_df.append(
            np.tile(
                pd.date_range(
                    datetime(year=a, month=1, day=1),
                    datetime(year=a, month=12, day=1),
                    freq="MS",
                ).to_numpy(),
                n_series * n_patamares,
            ),
        )
        patamares_df.append(np.tile(np.repeat(patamares, 12), n_series))
        series_df.append(np.repeat(series, 12 * n_patamares))

    valores = []
    for a in anos:
        valores.append(
            df.loc[
                (df["ano"] == a),
                MESES_DF,
            ]
            .to_numpy()
            .flatten()
        )
    df_formatado = pd.DataFrame(
        data={
            "data": np.concatenate(datas_df),
            "patamar": np.concatenate(patamares_df),
            "serie": np.concatenate(series_df),
            "valor": np.concatenate(valores),
        }
    )
    return df_formatado


def __formata_df_meses_para_datas_classetermica_serie_patamar(
    df: pd.DataFrame,
) -> pd.DataFrame:
    anos = np.array(df["ano"].unique().tolist())
    classes = np.array(df["classe"].unique().tolist())
    series = np.array(df["serie"].unique().tolist())
    patamares = np.array(df["patamar"].unique().tolist())
    n_classes = len(classes)
    n_series = len(series)
    n_patamares = len(patamares)
    datas_df = []
    classes_df = []
    series_df = []
    patamares_df = []
    for a in anos:
        datas_df.append(
            np.tile(
                pd.date_range(
                    datetime(year=a, month=1, day=1),
                    datetime(year=a, month=12, day=1),
                    freq="MS",
                ).to_numpy(),
                n_classes * n_series * n_patamares,
            ),
        )
        classes_df.append(np.repeat(classes, 12 * n_series * n_patamares))
        patamares_df.append(
            np.tile(np.repeat(patamares, 12), n_classes * n_series)
        )
        series_df.append(
            np.tile(np.repeat(series, 12 * n_patamares), n_classes)
        )
    valores = []
    for a in anos:
        valores.append(
            df.loc[
                (df["ano"] == a),
                MESES_DF,
            ]
            .to_numpy()
            .flatten()
        )
    df_formatado = pd.DataFrame(
        data={
            "classe": np.concatenate(classes_df),
            "data": np.concatenate(datas_df),
            "patamar": np.concatenate(patamares_df),
            "serie": np.concatenate(series_df),
            "valor": np.concatenate(valores),
        }
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


def prepara_vetor_anos_tabela(anos: List[str]) -> List[datetime]:
    # Se tem pré, substitui por 0001
    # Se tem pós, substitui por 9999
    # Repete os valores existentes 12 vezes
    anos_convertidos: List[int] = []
    for a in anos:
        if a == "PRE":
            a_convertido = 1
        elif a == "POS":
            a_convertido = 9999
        else:
            a_convertido = int(a)
        anos_convertidos.append(a_convertido)

    anos_array = np.array(anos_convertidos).repeat(len(MESES_DF))
    meses = np.tile(np.arange(1, 13), len(anos))
    return [
        datetime(year=a, month=m, day=1) for a, m in zip(anos_array, meses)
    ]


def repete_vetor(
    valores: list, n_repeticoes: int = len(MESES_DF)
) -> np.ndarray:
    return np.array(valores).repeat(n_repeticoes)


def prepara_valor_ano(ano: int) -> str:
    if ano == 1:
        return "PRE"
    elif ano == 9999:
        return "POS"
    else:
        return str(ano)
