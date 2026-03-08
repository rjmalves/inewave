from inewave.config import MESES_DF

from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.tabular import ColumnDef
from inewave.nwlistop.modelos.blocos.tabela_serie_anual import (
    TabelaSerieAnual,
)


class CdefAnos(TabelaSerieAnual):
    """
    Bloco com as informações das tabelas de custos de déficit.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(10, 7 + 10 * i, 2))
        for i in range(len(MESES_DF))
    ]
