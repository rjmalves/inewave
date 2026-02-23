from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.tabular import ColumnDef

from inewave.config import MESES_DF
from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
    TabelaSeriePatamarAnual,
)


class CmargsAnos27(TabelaSeriePatamarAnual):
    """
    Bloco com a informaçao do submercado associado aos valores de Custo
    Marginal de Operação.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
        ColumnDef("patamar", IntegerField(2, 9)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(8, 15 + 9 * i, 2))
        for i in range(len(MESES_DF))
    ]


class CmargsAnos(TabelaSeriePatamarAnual):
    """
    Bloco com a informaçao do submercado associado aos valores de Custo
    Marginal de Operação.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
        ColumnDef("patamar", IntegerField(2, 9)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(11, 14 + 11 * i, 2))
        for i in range(len(MESES_DF))
    ]
