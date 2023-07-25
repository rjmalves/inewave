# Imports de módulos externos
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField


from inewave.newave.modelos.blocos.tabelacsv import TabelaCSV


class TabelaAvlEvap(TabelaCSV):
    """
    Bloco com as informações de avaliação da representação linear
    para a evaporação.
    """

    BEGIN_PATTERN = "-----;-----;"
    LINE_MODEL = Line(
        [
            IntegerField(size=5),
            IntegerField(size=5),
            LiteralField(size=14),
            FloatField(size=10, decimal_digits=2),
            FloatField(size=10, decimal_digits=2),
            FloatField(size=10, decimal_digits=2),
            FloatField(size=10, decimal_digits=3),
            FloatField(size=10, decimal_digits=2),
        ],
        delimiter=";",
    )
    COLUMN_NAMES = [
        "periodo",
        "codigo_usina",
        "nome_usina",
        "volume_armazenado_hm3",
        "evaporacao_calculada_hm3",
        "evaporacao_modelo_hm3",
        "desvio_absoluto_hm3",
        "desvio_percentual",
    ]
    END_PATTERN = ""
