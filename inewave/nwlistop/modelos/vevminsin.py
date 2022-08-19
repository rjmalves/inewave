from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class VevminAnos(ValoresSerie):
    """
    Bloco com as informações das tabelas de violação da meta
    de energia de vazão mínima em MWmes.
    """

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(9, 7 + 9 * i, 0) for i in range(len(MESES_DF) + 1)]  # type: ignore
    )
