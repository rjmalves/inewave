from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField

from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class ViolFphaAnos(ValoresSeriePatamar):
    """
    Bloco com as informações das tabelas de corte de geração eólica
    da usina por mês/ano de estudo.
    """

    __slots__ = []

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
            LiteralField(5, 6),
        ]
        + [
            FloatField(13, 16 + 15 * i, 7, format="E")
            for i in range(len(MESES_DF))
        ]  # type: ignore
    )
