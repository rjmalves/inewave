# Imports de módulos externos
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField

from inewave.newave.modelos.blocos.tabelacsv import TabelaCSV


class TabelaEcoFpha(TabelaCSV):
    """
    Bloco com as informações da função de produção para as
    UHEs do modelo NEWAVE.
    """

    BEGIN_PATTERN = "----;----;-------------;----;"
    LINE_MODEL = Line(
        [
            IntegerField(size=4),
            IntegerField(size=4),
            LiteralField(size=13),
            IntegerField(size=4),
            IntegerField(size=4),
            IntegerField(size=4),
            IntegerField(size=4),
            IntegerField(size=5),
            FloatField(size=8, decimal_digits=1),
            FloatField(size=8, decimal_digits=1),
            IntegerField(size=5),
            FloatField(size=8, decimal_digits=1),
            FloatField(size=8, decimal_digits=1),
            FloatField(size=8, decimal_digits=1),
            FloatField(size=8, decimal_digits=1),
        ],
        delimiter=";",
    )
    COLUMN_NAMES = [
        "codigo_usina",
        "periodo",
        "nome_usina",
        "tipo",
        "conv",
        "alfa",
        "rems",
        "numero_pontos_vazao_turbinada",
        "vazao_turbinada_minima",
        "vazao_turbinada_maxima",
        "numero_pontos_volume_armazenado",
        "volume_armazenado_minimo",
        "volume_armazenado_maximo",
        "geracao_minima",
        "geracao_maxima",
    ]
    END_PATTERN = ""
