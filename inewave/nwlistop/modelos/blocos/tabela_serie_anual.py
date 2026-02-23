from typing import IO, List, Optional

import pandas as pd  # type: ignore
from cfinterface.components.block import Block
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line
from cfinterface.components.tabular import ColumnDef, TabularParser

from inewave._utils.formatacao import formata_df_meses_para_datas_nwlistop
from inewave.config import MESES_DF


class TabelaSerieAnual(Block):
    """
    Base class for nwlistop blocks with year-grouped tabular data
    indexed by synthetic series and month.

    Subclasses must override ``COLUMNS`` with a list of
    :class:`~cfinterface.components.tabular.ColumnDef` instances:

    - The first entry must have ``name="serie"`` and use an
      :class:`~cfinterface.components.integerfield.IntegerField`.
    - The remaining 12 entries must have ``name=MESES_DF[i]`` and use
      :class:`~cfinterface.components.floatfield.FloatField` instances.

    The output :class:`pandas.DataFrame` stored in ``self.data`` is
    identical in column names, dtypes, and values to what the legacy
    :class:`~inewave.nwlistop.modelos.blocos.valoresserie.ValoresSerie`
    produces.
    """

    __slots__ = ["_parser", "_ano", "_separador"]

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = "MEDIA "

    YEAR_LINE: Line = Line([IntegerField(4, 10)])
    COLUMNS: List[ColumnDef] = []

    def __init__(
        self,
        previous=None,
        next=None,
        data=None,
    ) -> None:
        super().__init__(previous, next, data)
        self._parser = TabularParser(self.__class__.COLUMNS)
        self._ano: Optional[int] = None
        self._separador: str = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        if not isinstance(self.data, pd.DataFrame):
            return not isinstance(o.data, pd.DataFrame)
        if not isinstance(o.data, pd.DataFrame):
            return False
        return self.data.equals(o.data)

    def read(self, file: IO, *args, **kwargs) -> bool:
        self._ano = self.__class__.YEAR_LINE.read(file.readline())[0]
        self._separador = file.readline()

        raw_lines: List[str] = []
        while True:
            linha = file.readline()
            if self.ends(linha) or len(linha) <= 1:
                break
            raw_lines.append(linha)

        self.data = self._build_dataframe(self._parser.parse_lines(raw_lines))
        return True

    def write(self, file: IO, *args, **kwargs) -> bool:
        """
        Does NOT write the MEDIA terminator — the block framework handles
        the boundary between blocks.
        """
        if self.data is None or self._ano is None:
            return False

        file.write(f"     ANO: {str(int(self._ano)).rjust(4)}\n")
        if self._separador:
            file.write(self._separador)
        for row_line in self._parser.format_rows(self._tidy_to_wide()):
            file.write(row_line)

        return True

    def _build_dataframe(self, parsed: dict) -> pd.DataFrame:
        df = pd.DataFrame(parsed)
        if df.empty:
            return pd.DataFrame(columns=["data", "serie", "valor"])

        df["ano"] = int(self._ano)  # type: ignore[arg-type]
        # NaN series values are replaced with 1 (single-series files).
        df.loc[df["serie"].isna(), "serie"] = 1
        df = df[["ano", "serie"] + MESES_DF]
        df = df.astype({"serie": "int64", "ano": "int64"})
        return formata_df_meses_para_datas_nwlistop(df)

    def _tidy_to_wide(self) -> dict:
        df: pd.DataFrame = self.data
        year = int(df["data"].iloc[0].year)
        df_wide = (
            df[df["data"].dt.year == year]
            .pivot(index="serie", columns="data", values="valor")
            .reset_index()
        )
        result: dict = {"serie": df_wide["serie"].tolist()}
        for col in df_wide.columns[1:]:
            result[MESES_DF[col.month - 1]] = df_wide[col].tolist()
        return result
