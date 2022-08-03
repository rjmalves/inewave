from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class CoperAnos(ValoresSerie):
    """
    Bloco com as informações das tabelas de custos de operação.
    """

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(10, 7 + 10 * i, 2) for i in range(len(MESES_DF) + 1)]  # type: ignore
    )
