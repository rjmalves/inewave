from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField


from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class VghminAnos(ValoresSeriePatamar):
    """
    Bloco com as informações das tabelas de violação da meta de
    geração hidráulica mínima.
    """

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 1),
            LiteralField(5, 6),
        ]
        + [FloatField(8, 12 + 9 * i, 1) for i in range(len(MESES_DF) + 1)]  # type: ignore
    )
