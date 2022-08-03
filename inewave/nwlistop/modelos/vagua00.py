from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField

from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class VAAnos(ValoresSerie):
    """
    Bloco com as informações das tabelas de valor da água por
    REE por mês/ano de estudo.
    """

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(8, 9 + 9 * i, 2) for i in range(len(MESES_DF) + 1)]  # type: ignore
    )
