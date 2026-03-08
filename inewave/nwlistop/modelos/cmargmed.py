from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.tabular import ColumnDef

from inewave.config import MESES_DF
from inewave.nwlistop.modelos.blocos.tabela_serie_anual import (
    TabelaSerieAnual,
)


class CmargsAnos28(TabelaSerieAnual):
    """
    Bloco com a informaçao do submercado associado aos valores de Custo
    Marginal de Operação.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(8, 9 + 10 * i, 2))
        for i in range(len(MESES_DF))
    ]


class CmargsAnos(TabelaSerieAnual):
    """
    Bloco com a informaçao do submercado associado aos valores de Custo
    Marginal de Operação.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(11, 9 + 11 * i, 2))
        for i in range(len(MESES_DF))
    ]
