# Imports de módulos externos
from cfinterface.components.section import Section
from typing import IO, Any, Optional
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package


class TabelaMediasusih(Section):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-USIH.CSV`.
    """

    __slots__ = ["data"]

    def __init__(self, previous: Optional[Any] = None, next: Optional[Any] = None, data: Optional[Any] = None) -> None:
        super().__init__(previous, next, data)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TabelaMediasusih):
            return False
        bloco: TabelaMediasusih = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return bool(self.data.equals(bloco.data))

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        tabela = pd.read_csv(file, skipinitialspace=True)
        col_usi = "USIH_ext"
        tabela = tabela.rename(columns={col_usi: "codigo_usina"})
        tabela = tabela.loc[tabela["codigo_usina"] > 0]
        cols = tabela.columns.tolist()
        df = tabela.drop(columns=[cols[-1]])
        cols_id = ["VAR", "codigo_usina"]
        cols_estagios = [c for c in df.columns.tolist() if c not in cols_id]
        df = df.melt(
            id_vars=cols_id,
            value_vars=cols_estagios,
            var_name="estagio",
            value_name="valor",
        )
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df["estagio"] = df["estagio"].astype(int)
        df["estagio"] -= df["estagio"].min() - 1
        df = df.pivot_table(
            index=["estagio", "codigo_usina"],
            columns="VAR",
            values="valor",
        ).reset_index()
        self.data = df
