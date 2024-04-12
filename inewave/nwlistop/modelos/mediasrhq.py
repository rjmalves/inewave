# Imports de módulos externos
from cfinterface.components.section import Section
from typing import IO
import pandas as pd  # type: ignore


class TabelaMediasrhq(Section):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-RHQ.CSV`.
    """

    __slots__ = ["data"]

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TabelaMediasrhq):
            return False
        bloco: TabelaMediasrhq = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO, *args, **kwargs):
        tabela = pd.read_csv(file, skipinitialspace=True)
        col_rhq = "RHQ_ext"
        tabela = tabela.rename(columns={col_rhq: "codigo_restricao"})
        tabela = tabela.loc[tabela["codigo_restricao"] > 0]
        cols = tabela.columns.tolist()
        df = tabela.drop(columns=[cols[-1]])
        cols_id = ["VAR", "codigo_restricao"]
        cols_estagios = [c for c in df.columns.tolist() if c not in cols_id]
        df = df.melt(
            id_vars=cols_id,
            value_vars=cols_estagios,
            var_name="estagio",
            value_name="valor",
        )
        df["estagio"] = df["estagio"].astype(int)
        df["estagio"] -= df["estagio"].min() - 1
        df = df.pivot_table(
            index=["estagio", "codigo_restricao"],
            columns="VAR",
            values="valor",
        ).reset_index()
        self.data = df
