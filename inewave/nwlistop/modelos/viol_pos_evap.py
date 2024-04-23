from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField

from inewave.nwlistop.modelos.blocos.valoresserie import (
    ValoresSerie,
)


class ViolPosEvapAnos(ValoresSerie):
    """
    Bloco com as informações das tabelas de desvio positivo
    da evaporação por usina por mês/ano de estudo.
    """

    __slots__ = []

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(14, 15 + 15 * i, 2, format="E") for i in range(len(MESES_DF))]  # type: ignore
    )
