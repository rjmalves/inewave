# Imports de módulos externos
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField

from inewave.newave.modelos.blocos.tabelacsv import TabelaCSV


class TabelaAvlCortesFpha(TabelaCSV):
    """
    Bloco com as informações dos cortes da função de produção para as
    UHEs do modelo NEWAVE.
    """

    BEGIN_PATTERN = "-----;-----;--------------;"
    LINE_MODEL = Line(
        [
            IntegerField(size=5),
            IntegerField(size=5),
            LiteralField(size=14),
            IntegerField(size=7),
            FloatField(size=10, decimal_digits=6),
            FloatField(size=16, decimal_digits=8),
            FloatField(size=16, decimal_digits=8),
            FloatField(size=16, decimal_digits=8),
            FloatField(size=16, decimal_digits=8),
            FloatField(size=16, decimal_digits=8),
        ],
        delimiter=";",
    )
    COLUMN_NAMES = [
        "codigo_usina",
        "periodo",
        "nome_usina",
        "indice_corte",
        "fator_correcao",
        "rhs_energia",
        "coeficiente_volume_util_MW_hm3",
        "coeficiente_vazao_turbinada_MW_m3s",
        "coeficiente_vazao_vertida_MW_m3s",
        "coeficiente_vazao_lateral_MW_m3s",
    ]
    END_PATTERN = ""
