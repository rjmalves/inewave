from inewave.config import MESES_DF

from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.tabular import ColumnDef
from inewave.nwlistop.modelos.blocos.tabela_serie_anual import (
    TabelaSerieAnual,
)


class DposEvapAnos(TabelaSerieAnual):
    """
    Bloco com as informações das tabelas de desvio positivo
    da evaporação por usina por mês/ano de estudo.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(14, 15 + 15 * i, 2, format="E"))
        for i in range(len(MESES_DF))
    ]
