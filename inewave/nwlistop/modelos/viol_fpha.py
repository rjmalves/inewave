from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.tabular import ColumnDef

from inewave.config import MESES_DF
from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
    TabelaSeriePatamarAnual,
)


class ViolFphaAnos(TabelaSeriePatamarAnual):
    """
    Bloco com as informações das tabelas de corte de geração eólica
    da usina por mês/ano de estudo.
    """

    __slots__ = []

    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
        ColumnDef("patamar", LiteralField(5, 6)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(13, 16 + 15 * i, 7, format="E"))
        for i in range(len(MESES_DF))
    ]
