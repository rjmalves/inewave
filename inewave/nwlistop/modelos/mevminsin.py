from inewave.config import MESES_DF

from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField


from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class MevminAnos(ValoresSerie):
    """
    Bloco com as informações das tabelas de metas de energia de vazão
    mínima por série e por mês/ano de estudo.
    """

    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [  # type: ignore
            IntegerField(4, 2),
        ]
        + [FloatField(8, 8 + 9 * i, 1) for i in range(len(MESES_DF))]  # type: ignore
    )
