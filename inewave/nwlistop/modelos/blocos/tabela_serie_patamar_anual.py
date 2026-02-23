from typing import IO, List, Optional

import pandas as pd  # type: ignore
from cfinterface.components.block import Block
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line
from cfinterface.components.tabular import ColumnDef, TabularParser

from inewave._utils.formatacao import formata_df_meses_para_datas_nwlistop
from inewave.config import MESES_DF


class TabelaSeriePatamarAnual(Block):
    """
    Base class for nwlistop blocks with year-grouped tabular data
    indexed by synthetic series, load level (patamar), and month.

    Subclasses must override ``COLUMNS`` with a list of
    :class:`~cfinterface.components.tabular.ColumnDef` instances:

    - The first entry must have ``name="serie"`` and use an
      :class:`~cfinterface.components.integerfield.IntegerField`.
    - The second entry must have ``name="patamar"`` and use an
      :class:`~cfinterface.components.integerfield.IntegerField`.
    - The remaining 12 entries must have ``name=MESES_DF[i]`` and use
      :class:`~cfinterface.components.floatfield.FloatField` instances.

    Series carry-forward: when the ``serie`` field reads as ``None``
    (blank in the source file), the previous series value is reused,
    grouping multiple patamar rows under the same synthetic series.

    The output :class:`pandas.DataFrame` stored in ``self.data`` is
    identical in column names, dtypes, and values to what the legacy
    :class:`~inewave.nwlistop.modelos.blocos.valoresseriepatamar\
.ValoresSeriePatamar` produces.
    """

    __slots__ = ["_parser", "_ano", "_separador"]

    BEGIN_PATTERN = "     ANO: "
    # Note: leading space distinguishes " MEDIA" from column-header
    # lines that contain "MEDIA " (trailing space) as a label.
    END_PATTERN = " MEDIA"

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

        parsed = self._parser.parse_lines(raw_lines)
        self._apply_series_carry_forward(parsed)
        self.data = self._build_dataframe(parsed)
        return True

    def write(self, file: IO, *args, **kwargs) -> bool:
        """
        The serie field is written only on the first patamar row of each
        series group (subsequent rows left blank), matching the source
        file format. Does NOT write the MEDIA terminator — the block
        framework handles the boundary between blocks.
        """
        if self.data is None or self._ano is None:
            return False

        file.write(f"     ANO: {str(int(self._ano)).rjust(4)}\n")
        if self._separador:
            file.write(self._separador)

        wide = self._tidy_to_wide()
        serie_values = wide.get("serie", [])
        patamar_values = wide.get("patamar", [])
        for i, row_line in enumerate(self._parser.format_rows(wide)):
            if (
                i > 0
                and serie_values[i] == serie_values[i - 1]
                and patamar_values[i] != patamar_values[i - 1]
            ):
                row_line = self._blank_serie_field(row_line)
            file.write(row_line)

        return True

    @staticmethod
    def _apply_series_carry_forward(parsed: dict) -> None:
        """
        Fill None values in the ``serie`` list with the last seen value,
        defaulting to 1. Mutates *parsed* in-place.
        """
        series_list: List = parsed.get("serie", [])
        current: int = 1
        for idx, val in enumerate(series_list):
            if val is not None:
                current = int(val)
            else:
                series_list[idx] = current

    def _build_dataframe(self, parsed: dict) -> pd.DataFrame:
        df = pd.DataFrame(parsed)
        if df.empty:
            return pd.DataFrame(columns=["data", "patamar", "serie", "valor"])

        df["ano"] = int(self._ano)  # type: ignore[arg-type]
        df = df[["ano", "serie", "patamar"] + MESES_DF]
        df = df.astype({"serie": "int64", "ano": "int64"})
        return formata_df_meses_para_datas_nwlistop(df)

    def _tidy_to_wide(self) -> dict:
        df: pd.DataFrame = self.data
        year = int(df["data"].iloc[0].year)
        df_wide = (
            df[df["data"].dt.year == year]
            .pivot(index=["serie", "patamar"], columns="data", values="valor")
            .reset_index()
        )
        result: dict = {
            "serie": df_wide["serie"].tolist(),
            "patamar": df_wide["patamar"].tolist(),
        }
        for col in df_wide.columns[2:]:
            result[MESES_DF[col.month - 1]] = df_wide[col].tolist()
        return result

    def _blank_serie_field(self, row_line: str) -> str:
        field = self.__class__.COLUMNS[0].field
        start: int = field.starting_position
        width: int = field.size
        return row_line[:start] + " " * width + row_line[start + width :]
