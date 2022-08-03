from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField

from inewave.nwlistop.modelos.blocos.valoresree import ValoresREE


class EafsAnos(ValoresREE):
    """
    Bloco com as informações das tabelas de energias afluente bruta
    por série e por mês/ano de estudo.
    """

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = " MEDIA"
    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(8, 7 + 9 * i, 1) for i in range(len(MESES_DF) + 1)]  # type: ignore
    )
