from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class CustoFuturoAnos(ValoresSerie):
    """
    Bloco com as informações das tabelas de custos futuros.
    """

    __slots__ = []

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(15, 7 + 15 * i, 7, format="E") for i in range(len(MESES_DF))]  # type: ignore
    )
