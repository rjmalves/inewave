# Imports de módulos externos
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField


from inewave.newave.modelos.blocos.tabelacsv import TabelaCSV


class TabelaEcoEvap(TabelaCSV):
    """
    Bloco com o eco dos dados para representação linear
    da evaporação.
    """

    BEGIN_PATTERN = "-----;-----;"
    LINE_MODEL = Line(
        [
            IntegerField(size=5),
            IntegerField(size=5),
            LiteralField(size=14),
            FloatField(size=11, decimal_digits=2),
            FloatField(size=11, decimal_digits=2),
            IntegerField(size=8),
            IntegerField(size=11),
            IntegerField(size=11),
            IntegerField(size=15),
        ],
        delimiter=";",
    )
    COLUMN_NAMES = [
        "periodo",
        "codigo_usina",
        "nome_usina",
        "volume_referencia_hm3",
        "evaporacao_referencia_hm3",
        "coeficiente_evaporacao_mm_mes",
        "flag_evaporacao",
        "evaporacao_linear",
        "tipo_volume_referencia",
    ]
    END_PATTERN = ""
