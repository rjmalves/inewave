from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField


from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie  # type: ignore


class EafsAnos(ValoresSerie):
    """
    Bloco com as informações das tabelas de energias afluente bruta
    por série e por mês/ano de estudo.
    """

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [IntegerField(4, 2)]  # type: ignore
        + [
            FloatField(8, 6 + 9 * i, 0) for i in range(len(MESES_DF) + 1)  # type: ignore
        ]
    )
