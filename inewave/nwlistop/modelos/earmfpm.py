from inewave.config import MESES_DF

from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.tabular import ColumnDef
from inewave.nwlistop.modelos.blocos.tabela_serie_anual import (
    TabelaSerieAnual,
)


class EarmsAnos(TabelaSerieAnual):
    """
    Bloco com as informações das tabelas de energias armazenada final
    por série e por mês/ano de estudo.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 1)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(8, 7 + 10 * i, 1))
        for i in range(len(MESES_DF))
    ]
