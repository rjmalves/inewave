from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List


class RegistroUHEHidr(Register):
    """
    Registro com os dados associados a uma UHE, existentes no
    arquivo HIDR.
    """

    LINE = Line(
        [
            LiteralField(size=12, starting_position=0),  # Nome
            IntegerField(size=4, starting_position=12),  # Posto
            IntegerField(size=8, starting_position=16),  # Posto BDH
            IntegerField(size=4, starting_position=24),  # Subsistema
            IntegerField(size=4, starting_position=28),  # Empresa
            IntegerField(size=4, starting_position=32),  # Jusante
            IntegerField(size=4, starting_position=36),  # Desvio
            FloatField(size=4, starting_position=40),  # Volume Mínimo
            FloatField(size=4, starting_position=44),  # Volume Máximo
            FloatField(size=4, starting_position=48),  # Volume Vertedouro
            FloatField(size=4, starting_position=52),  # Volume Desvio
            FloatField(size=4, starting_position=56),  # Cota Mínima
            FloatField(size=4, starting_position=60),  # Cota Máxima
            FloatField(size=4, starting_position=64),  # Pol VC 0
            FloatField(size=4, starting_position=68),  # Pol VC 1
            FloatField(size=4, starting_position=72),  # Pol VC 2
            FloatField(size=4, starting_position=76),  # Pol VC 3
            FloatField(size=4, starting_position=80),  # Pol VC 4
            FloatField(size=4, starting_position=84),  # Pol CA 0
            FloatField(size=4, starting_position=88),  # Pol CA 1
            FloatField(size=4, starting_position=92),  # Pol CA 2
            FloatField(size=4, starting_position=96),  # Pol CA 3
            FloatField(size=4, starting_position=100),  # Pol CA 4
            IntegerField(size=4, starting_position=104),  # Evap JAN
            IntegerField(size=4, starting_position=108),  # Evap FEV
            IntegerField(size=4, starting_position=112),  # Evap MAR
            IntegerField(size=4, starting_position=116),  # Evap ABR
            IntegerField(size=4, starting_position=120),  # Evap MAI
            IntegerField(size=4, starting_position=124),  # Evap JUN
            IntegerField(size=4, starting_position=128),  # Evap JUL
            IntegerField(size=4, starting_position=132),  # Evap AGO
            IntegerField(size=4, starting_position=136),  # Evap SET
            IntegerField(size=4, starting_position=140),  # Evap OUT
            IntegerField(size=4, starting_position=144),  # Evap NOV
            IntegerField(size=4, starting_position=148),  # Evap DEZ
            IntegerField(size=4, starting_position=152),  # Num. Conj. Máquinas
            IntegerField(
                size=4, starting_position=156
            ),  # Num. Máquinas Conj. 1
            IntegerField(
                size=4, starting_position=160
            ),  # Num. Máquinas Conj. 2
            IntegerField(
                size=4, starting_position=164
            ),  # Num. Máquinas Conj. 3
            IntegerField(
                size=4, starting_position=168
            ),  # Num. Máquinas Conj. 4
            IntegerField(
                size=4, starting_position=172
            ),  # Num. Máquinas Conj. 5
            FloatField(size=4, starting_position=176),  # Potência Conj. 1
            FloatField(size=4, starting_position=180),  # Potência Conj. 2
            FloatField(size=4, starting_position=184),  # Potência Conj. 3
            FloatField(size=4, starting_position=188),  # Potência Conj. 4
            FloatField(size=4, starting_position=192),  # Potência Conj. 5
            LiteralField(size=300, starting_position=196),  # Campos ignorados
            FloatField(size=4, starting_position=496),  # H Nominal 1
            FloatField(size=4, starting_position=500),  # H Nominal 2
            FloatField(size=4, starting_position=504),  # H Nominal 3
            FloatField(size=4, starting_position=508),  # H Nominal 4
            FloatField(size=4, starting_position=512),  # H Nominal 5
            IntegerField(size=4, starting_position=516),  # Q Nominal 1
            IntegerField(size=4, starting_position=520),  # Q Nominal 2
            IntegerField(size=4, starting_position=524),  # Q Nominal 3
            IntegerField(size=4, starting_position=528),  # Q Nominal 4
            IntegerField(size=4, starting_position=532),  # Q Nominal 5
            FloatField(size=4, starting_position=536),  # Produtibilidade
            FloatField(size=4, starting_position=540),  # Perdas
            IntegerField(size=4, starting_position=544),  # Núm. Pol. Jus.
            FloatField(size=4, starting_position=548),  # Pol. Jus. 1 - 0
            FloatField(size=4, starting_position=552),  # Pol. Jus. 1 - 1
            FloatField(size=4, starting_position=556),  # Pol. Jus. 1 - 2
            FloatField(size=4, starting_position=560),  # Pol. Jus. 1 - 3
            FloatField(size=4, starting_position=564),  # Pol. Jus. 1 - 4
            FloatField(size=4, starting_position=568),  # Pol. Jus. 2 - 0
            FloatField(size=4, starting_position=572),  # Pol. Jus. 2 - 1
            FloatField(size=4, starting_position=576),  # Pol. Jus. 2 - 2
            FloatField(size=4, starting_position=580),  # Pol. Jus. 2 - 3
            FloatField(size=4, starting_position=584),  # Pol. Jus. 2 - 4
            FloatField(size=4, starting_position=588),  # Pol. Jus. 3 - 0
            FloatField(size=4, starting_position=592),  # Pol. Jus. 3 - 1
            FloatField(size=4, starting_position=596),  # Pol. Jus. 3 - 2
            FloatField(size=4, starting_position=600),  # Pol. Jus. 3 - 3
            FloatField(size=4, starting_position=604),  # Pol. Jus. 3 - 4
            FloatField(size=4, starting_position=608),  # Pol. Jus. 4 - 0
            FloatField(size=4, starting_position=612),  # Pol. Jus. 4 - 1
            FloatField(size=4, starting_position=616),  # Pol. Jus. 4 - 2
            FloatField(size=4, starting_position=620),  # Pol. Jus. 4 - 3
            FloatField(size=4, starting_position=624),  # Pol. Jus. 4 - 4
            FloatField(size=4, starting_position=628),  # Pol. Jus. 5 - 0
            FloatField(size=4, starting_position=632),  # Pol. Jus. 5 - 1
            FloatField(size=4, starting_position=636),  # Pol. Jus. 5 - 2
            FloatField(size=4, starting_position=640),  # Pol. Jus. 5 - 3
            FloatField(size=4, starting_position=644),  # Pol. Jus. 5 - 4
            FloatField(size=4, starting_position=648),  # Pol. Jus. 6 - 0
            FloatField(size=4, starting_position=652),  # Pol. Jus. 6 - 1
            FloatField(size=4, starting_position=656),  # Pol. Jus. 6 - 2
            FloatField(size=4, starting_position=660),  # Pol. Jus. 6 - 3
            FloatField(size=4, starting_position=664),  # Pol. Jus. 6 - 4
            FloatField(size=4, starting_position=668),  # Pol. Jus. REF - 1
            FloatField(size=4, starting_position=672),  # Pol. Jus. REF - 2
            FloatField(size=4, starting_position=676),  # Pol. Jus. REF - 3
            FloatField(size=4, starting_position=680),  # Pol. Jus. REF - 4
            FloatField(size=4, starting_position=684),  # Pol. Jus. REF - 5
            FloatField(size=4, starting_position=688),  # Pol. Jus. REF - 6
            FloatField(size=4, starting_position=692),  # Canal Fuga Médio
            IntegerField(size=4, starting_position=696),  # Influência no vert
            FloatField(size=4, starting_position=700),  # Fator de Carga Máximo
            FloatField(size=4, starting_position=704),  # Fator de Carga Mínimo
            IntegerField(size=4, starting_position=708),  # Vazão Mínima Hist.
            IntegerField(size=4, starting_position=712),  # Núm. de Unid. Base
            IntegerField(size=4, starting_position=716),  # Tipo de Turbina
            IntegerField(size=4, starting_position=720),  # Repr. Conjunto
            FloatField(size=4, starting_position=724),  # TEIF
            FloatField(size=4, starting_position=728),  # IP
            IntegerField(size=4, starting_position=732),  # Tipo Perda
            LiteralField(size=12, starting_position=736),  # Data
            LiteralField(size=39, starting_position=748),  # Observação
            FloatField(size=4, starting_position=787),  # Volume de Referência
            LiteralField(size=1, starting_position=791),  # Tipo de Regular.
        ],
        storage="BINARY",
    )

    @property
    def nome(self) -> str:
        return self.data[0]

    @nome.setter
    def nome(self, v: str):
        self.data[0] = v

    @property
    def posto(self) -> int:
        return self.data[1]

    @posto.setter
    def posto(self, v: int):
        self.data[1] = v

    @property
    def subsistema(self) -> int:
        return self.data[3]

    @subsistema.setter
    def subsistema(self, v: int):
        self.data[3] = v

    @property
    def empresa(self) -> int:
        return self.data[4]

    @empresa.setter
    def empresa(self, v: int):
        self.data[4] = v

    @property
    def jusante(self) -> int:
        return self.data[5]

    @jusante.setter
    def jusante(self, v: int):
        self.data[5] = v

    @property
    def desvio(self) -> int:
        return self.data[6]

    @desvio.setter
    def desvio(self, v: int):
        self.data[6] = v

    @property
    def volume_minimo(self) -> float:
        return self.data[7]

    @volume_minimo.setter
    def volume_minimo(self, v: float):
        self.data[7] = v

    @property
    def volume_maximo(self) -> float:
        return self.data[8]

    @volume_maximo.setter
    def volume_maximo(self, v: float):
        self.data[8] = v

    @property
    def volume_vertedouro(self) -> float:
        return self.data[9]

    @volume_vertedouro.setter
    def volume_vertedouro(self, v: float):
        self.data[9] = v

    @property
    def volume_desvio(self) -> float:
        return self.data[10]

    @volume_desvio.setter
    def volume_desvio(self, v: float):
        self.data[10] = v

    @property
    def cota_minima(self) -> float:
        return self.data[11]

    @cota_minima.setter
    def cota_minima(self, v: float):
        self.data[11] = v

    @property
    def cota_maxima(self) -> float:
        return self.data[12]

    @cota_maxima.setter
    def cota_maxima(self, v: float):
        self.data[12] = v

    @property
    def polinomio_volume_cota(self) -> List[float]:
        return self.data[13:18]

    @polinomio_volume_cota.setter
    def polinomio_volume_cota(self, v: List[float]):
        self.data[13:18] = v

    @property
    def polinomio_cota_area(self) -> List[float]:
        return self.data[18:23]

    @polinomio_cota_area.setter
    def polinomio_cota_area(self, v: List[float]):
        self.data[18:23] = v

    @property
    def evaporacao(self) -> List[float]:
        return self.data[23:35]

    @evaporacao.setter
    def evaporacao(self, v: List[float]):
        self.data[23:35] = v

    @property
    def numero_conjuntos_maquinas(self) -> int:
        return self.data[35]

    @numero_conjuntos_maquinas.setter
    def numero_conjuntos_maquinas(self, v: int):
        self.data[35] = v

    @property
    def numero_maquinas_conjunto(self) -> List[int]:
        return self.data[36:41]

    @numero_maquinas_conjunto.setter
    def numero_maquinas_conjunto(self, v: List[int]):
        self.data[36:41] = v

    @property
    def potef_conjunto(self) -> List[float]:
        return self.data[41:46]

    @potef_conjunto.setter
    def potef_conjunto(self, v: List[float]):
        self.data[41:46] = v

    @property
    def hef_conjunto(self) -> List[float]:
        return self.data[47:52]

    @hef_conjunto.setter
    def hef_conjunto(self, v: List[float]):
        self.data[47:52] = v

    @property
    def qef_conjunto(self) -> List[float]:
        return self.data[52:57]

    @qef_conjunto.setter
    def qef_conjunto(self, v: List[float]):
        self.data[52:57] = v

    @property
    def produtibilidade_especifica(self) -> float:
        return self.data[57]

    @produtibilidade_especifica.setter
    def produtibilidade_especifica(self, v: float):
        self.data[57] = v

    @property
    def perdas(self) -> float:
        return self.data[58]

    @perdas.setter
    def perdas(self, v: float):
        self.data[58] = v

    @property
    def numero_polinomios_jusante(self) -> int:
        return self.data[59]

    @numero_polinomios_jusante.setter
    def numero_polinomios_jusante(self, v: int):
        self.data[59] = v

    @property
    def polinomios_jusante(self) -> List[float]:
        return self.data[60:96]

    @polinomios_jusante.setter
    def polinomios_jusante(self, v: List[float]):
        self.data[60:96] = v

    @property
    def canal_fuga_medio(self) -> float:
        return self.data[96]

    @canal_fuga_medio.setter
    def canal_fuga_medio(self, v: float):
        self.data[96] = v

    @property
    def influencia_vertimento_canal_fuga(self) -> int:
        return self.data[97]

    @influencia_vertimento_canal_fuga.setter
    def influencia_vertimento_canal_fuga(self, v: int):
        self.data[97] = v

    @property
    def fator_carga_maximo(self) -> float:
        return self.data[98]

    @fator_carga_maximo.setter
    def fator_carga_maximo(self, v: float):
        self.data[98] = v

    @property
    def fator_carga_minimo(self) -> float:
        return self.data[99]

    @fator_carga_minimo.setter
    def fator_carga_minimo(self, v: float):
        self.data[99] = v

    @property
    def vazao_minima_historica(self) -> int:
        return self.data[100]

    @vazao_minima_historica.setter
    def vazao_minima_historica(self, v: int):
        self.data[100] = v

    @property
    def numero_unidades_base(self) -> int:
        return self.data[101]

    @numero_unidades_base.setter
    def numero_unidades_base(self, v: int):
        self.data[101] = v

    @property
    def tipo_turbina(self) -> int:
        return self.data[102]

    @tipo_turbina.setter
    def tipo_turbina(self, v: int):
        self.data[102] = v

    @property
    def representacao_conjunto(self) -> int:
        return self.data[103]

    @representacao_conjunto.setter
    def representacao_conjunto(self, v: int):
        self.data[103] = v

    @property
    def teif(self) -> float:
        return self.data[104]

    @teif.setter
    def teif(self, v: float):
        self.data[104] = v

    @property
    def ip(self) -> float:
        return self.data[105]

    @ip.setter
    def ip(self, v: float):
        self.data[105] = v

    @property
    def tipo_perda(self) -> int:
        return self.data[106]

    @tipo_perda.setter
    def tipo_perda(self, v: int):
        self.data[106] = v

    @property
    def data_referencia(self) -> str:
        return self.data[107]

    @data_referencia.setter
    def data_referencia(self, v: str):
        self.data[107] = v

    @property
    def observacao(self) -> str:
        return self.data[108]

    @observacao.setter
    def observacao(self, v: str):
        self.data[108] = v

    @property
    def volume_referencia(self) -> float:
        return self.data[109]

    @volume_referencia.setter
    def volume_referencia(self, v: float):
        self.data[109] = v

    @property
    def tipo_regulacao(self) -> str:
        return self.data[110]

    @tipo_regulacao.setter
    def tipo_regulacao(self, v: str):
        self.data[110] = v
