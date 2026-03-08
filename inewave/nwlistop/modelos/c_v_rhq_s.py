from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.tabular import ColumnDef

from inewave.config import MESES_DF
from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
    TabelaSeriePatamarAnual,
)


class CVRHQAnos(TabelaSeriePatamarAnual):
    """
    Bloco com as informações das tabelas de custo de violação de
    restrições RHQ para o SIN por mês/ano de estudo.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
        ColumnDef("patamar", LiteralField(5, 6)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(9, 11 + 9 * i, 1))
        for i in range(len(MESES_DF))
    ]
