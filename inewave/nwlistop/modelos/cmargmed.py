from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line

from inewave.config import MESES_DF
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class CmargsAnos28(ValoresSerie):
    """
    Bloco com a informaçao do submercado associado aos valores de Custo
    Marginal de Operação.
    """

    __slots__ = []

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(8, 9 + 10 * i, 2) for i in range(len(MESES_DF))]  # type: ignore
    )


class CmargsAnos(ValoresSerie):
    """
    Bloco com a informaçao do submercado associado aos valores de Custo
    Marginal de Operação.
    """

    __slots__ = []

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(11, 9 + 11 * i, 2) for i in range(len(MESES_DF))]  # type: ignore
    )
