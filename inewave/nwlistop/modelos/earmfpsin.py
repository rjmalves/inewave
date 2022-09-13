from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField


from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class EarmsAnos(ValoresSerie):
    """
    Bloco com as informações das tabelas de energias armazenada final
    por série e por mês/ano de estudo.
    """

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [IntegerField(4, 1)]  # type: ignore
        + [
            FloatField(8, 7 + 10 * i, 1) for i in range(len(MESES_DF) + 1)  # type: ignore
        ]
    )
