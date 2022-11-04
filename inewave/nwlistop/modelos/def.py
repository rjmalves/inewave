from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField


from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class DefAnos(ValoresSeriePatamar):
    """
    Bloco com as informações das tabelas de déficit.
    """

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [
            IntegerField(4, 1),
            LiteralField(5, 6),
        ]  # type: ignore
        + [
            FloatField(8, 12 + 9 * i, 1) for i in range(len(MESES_DF) + 1)  # type: ignore
        ]
    )
