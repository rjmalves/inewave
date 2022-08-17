from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.hidr import RegistroUHEHidr
from inewave.config import MESES_ABREV
import pandas as pd  # type: ignore


from typing import TypeVar, List, Optional


class Hidr(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao cadastro das
    usinas hidroelétricas.
    """

    T = TypeVar("T")

    REGISTERS = [RegistroUHEHidr]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__df: Optional[pd.DataFrame] = None

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="hidr.dat") -> "Hidr":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="hidr.dat"):
        self.__atualiza_registros()
        self.write(diretorio, nome_arquivo)

    def __monta_df_de_registros(self) -> Optional[pd.DataFrame]:
        registros: List[RegistroUHEHidr] = [
            r for r in self.data.of_type(RegistroUHEHidr)
        ]
        if len(registros) == 0:
            return None
        df = pd.DataFrame(
            columns=[
                "Nome",
                "Posto",
                "Subsistema",
                "Empresa",
                "Jusante",
                "Desvio",
                "Volume Mínimo",
                "Volume Máximo",
                "Volume Vertedouro",
                "Volume Desvio",
                "Cota Mínima",
                "Cota Máxima",
                *[f"A{i} VC" for i in range(5)],
                *[f"A{i} CA" for i in range(5)],
                *[f"Evaporação {m}" for m in MESES_ABREV],
                "Num. Conjuntos Máquinas",
                *[f"Num. Máquinas Conjunto {i}" for i in range(1, 6)],
                *[f"PotEf Conjunto {i}" for i in range(1, 6)],
                *[f"HEf Conjunto {i}" for i in range(1, 6)],
                *[f"QEf Conjunto {i}" for i in range(1, 6)],
                "Produtibilidade Específica",
                "Perdas",
                "Número PJUS",
                *[f"A{i} PJUS1" for i in range(5)],
                *[f"A{i} PJUS2" for i in range(5)],
                *[f"A{i} PJUS3" for i in range(5)],
                *[f"A{i} PJUS4" for i in range(5)],
                *[f"A{i} PJUS5" for i in range(5)],
                *[f"A{i} PJUS6" for i in range(5)],
                *[f"REF PJUS {i}" for i in range(1, 7)],
                "Canal de Fuga Médio",
                "Influencia Vert. Cfuga",
                "Fator Carga Max.",
                "Fator Carga Min.",
                "Vazão Mínima Histórica",
                "Num. Unidades Base",
                "Tipo Turbina",
                "Representação Conjunto",
                "TEIF",
                "IP",
                "Tipo de Perda",
                "Data",
                "Observação",
                "Volume de Referência",
                "Tipo de Regulação",
            ]
        )
        for i, r in enumerate(registros):
            df.loc[i + 1] = [
                r.nome,
                r.posto,
                r.subsistema,
                r.empresa,
                r.jusante,
                r.desvio,
                r.volume_minimo,
                r.volume_maximo,
                r.volume_vertedouro,
                r.volume_desvio,
                r.cota_minima,
                r.cota_maxima,
                *(r.polinomio_volume_cota),
                *(r.polinomio_cota_area),
                *(r.evaporacao),
                r.numero_conjuntos_maquinas,
                *(r.numero_maquinas_conjunto),
                *(r.potef_conjunto),
                *(r.hef_conjunto),
                *(r.qef_conjunto),
                r.produtibilidade_especifica,
                r.perdas,
                r.numero_polinomios_jusante,
                *(r.polinomios_jusante),
                r.canal_fuga_medio,
                r.influencia_vertimento_canal_fuga,
                r.fator_carga_maximo,
                r.fator_carga_minimo,
                r.vazao_minima_historica,
                r.numero_unidades_base,
                r.tipo_turbina,
                r.representacao_conjunto,
                r.teif,
                r.ip,
                r.tipo_perda,
                r.data_referencia,
                r.observacao,
                r.volume_referencia,
                r.tipo_regulacao,
            ]
        df.index.name = "Código"

        df = df.astype(
            {
                "Nome": str,
                "Posto": int,
                "Subsistema": int,
                "Empresa": int,
                "Jusante": int,
                "Desvio": int,
                "Volume Mínimo": float,
                "Volume Máximo": float,
                "Volume Vertedouro": float,
                "Volume Desvio": float,
                "Cota Mínima": float,
                "Cota Máxima": float,
                "Produtibilidade Específica": float,
                "Perdas": float,
                "Canal de Fuga Médio": float,
                "Influencia Vert. Cfuga": int,
                "Fator Carga Max.": float,
                "Fator Carga Min.": float,
                "Vazão Mínima Histórica": int,
                "Num. Unidades Base": int,
                "Tipo Turbina": int,
                "Representação Conjunto": int,
                "TEIF": float,
                "IP": float,
                "Tipo de Perda": int,
                "Data": str,
                "Observação": str,
                "Volume de Referência": float,
                "Tipo de Regulação": str,
            },
        )
        return df

    def __atualiza_registros(self):
        registros: List[RegistroUHEHidr] = [r for r in self.data][1:]
        for (_, linha), r in zip(self.cadastro.iterrows(), registros):
            r.nome = linha["Nome"]
            r.posto = linha["Posto"]
            r.subsistema = linha["Subsistema"]
            r.empresa = linha["Empresa"]
            r.jusante = linha["Jusante"]
            r.desvio = linha["Desvio"]
            r.volume_minimo = linha["Volume Mínimo"]
            r.volume_maximo = linha["Volume Máximo"]
            r.volume_vertedouro = linha["Volume Vertedouro"]
            r.volume_desvio = linha["Volume Desvio"]
            r.cota_minima = linha["Cota Mínima"]
            r.cota_maxima = linha["Cota Máxima"]
            r.polinomio_volume_cota = linha[
                [f"A{i} VC" for i in range(5)]
            ].tolist()
            r.polinomio_cota_area = linha[
                [f"A{i} CA" for i in range(5)]
            ].tolist()
            r.evaporacao = linha[
                [f"Evaporação {m}" for m in MESES_ABREV]
            ].tolist()
            r.numero_conjuntos_maquinas = linha["Num. Conjuntos Máquinas"]
            r.potef_conjunto = linha[
                [f"PotEf Conjunto {i}" for i in range(1, 6)]
            ].tolist()
            r.hef_conjunto = linha[
                [f"HEf Conjunto {i}" for i in range(1, 6)]
            ].tolist()
            r.qef_conjunto = linha[
                [f"QEf Conjunto {i}" for i in range(1, 6)]
            ].tolist()
            r.produtibilidade_especifica = linha["Produtibilidade Específica"]
            r.perdas = linha["Perdas"]
            r.numero_polinomios_jusante = linha["Número PJUS"]
            r.polinomios_jusante = linha[
                [f"A{i} PJUS1" for i in range(5)]
                + [f"A{i} PJUS2" for i in range(5)]
                + [f"A{i} PJUS3" for i in range(5)]
                + [f"A{i} PJUS4" for i in range(5)]
                + [f"A{i} PJUS5" for i in range(5)]
                + [f"A{i} PJUS6" for i in range(5)]
                + [f"REF PJUS {i}" for i in range(1, 7)]
            ].tolist()
            r.canal_fuga_medio = linha["Canal de Fuga Médio"]
            r.influencia_vertimento_canal_fuga = linha[
                "Influencia Vert. Cfuga"
            ]
            r.fator_carga_maximo = linha["Fator Carga Max."]
            r.fator_carga_minimo = linha["Fator Carga Min."]
            r.vazao_minima_historica = linha["Vazão Mínima Histórica"]
            r.numero_unidades_base = linha["Num. Unidades Base"]
            r.tipo_turbina = linha["Tipo Turbina"]
            r.representacao_conjunto = linha["Representação Conjunto"]
            r.teif = linha["TEIF"]
            r.ip = linha["IP"]
            r.tipo_perda = linha["Tipo de Perda"]
            r.data_referencia = linha["Data"]
            r.observacao = linha["Observação"]
            r.volume_referencia = linha["Volume de Referência"]
            r.tipo_regulacao = linha["Tipo de Regulação"]

    @property
    def cadastro(self) -> pd.DataFrame:
        """
        Obtém a tabela com os dados cadastrais existentes no arquivo
        binário.

        - Nome (`str`): nome da usina (12 caracteres)
        - Posto (`int`): posto de vazão natural da usina
        - Subsistema (`int`): subsistema da usina
        - Empresa (`int`): agente responsável pela usina
        - Jusante (`int`): posto à jusante da usina
        - Desvio (`float`): TODO
        - Volume Mínimo (`float`): volume mínimo da usina (hm3)
        - Volume Máximo (`float`): volume máximo da usina (hm3)
        - Volume Vertedouro (`float`): volume do vertedouro da usina (hm3)
        - Volume Desvio (`float`): TODO
        - Cota Mínima (`float`): cota mínima da usina (m)
        - Cota Máxima (`float`): cota máxima da usina (m)
        - A[0-4] VC (`float`): coeficientes do polinômio volume-cota
        - A[0-4] CA (`float`): coeficientes do polinômio cota-área
        - Evaporação [JAN..DEZ] (`float`): coeficientes de evaporação (mm)
        - Num Conjunto Máquinas (`int`): número de conjuntos de máquinas
        - Num Máquinas Conjunto [1-5] (`int`): máquinas por conjunto
        - PotEf. Conjunto [1-5] (`float`): potência das máquinas (MWmed)
        - HEf Conjunto [1-5]: alturas nominais de queda por conjunto (m)
        - QEf Conjunto [1-5]: vazões nominais por conjunto (m3/s)
        - Produtibilidade Específica (`float`): produtibilidade específica
        - Perdas (`float`): perdas da usina
        - Número PJUS (`int`): número de polinômios de jusante
        - C[0-4] PJUS[1-6] (`float`): coeficientes de cada polinjus
        - REF PJUS [1-6] (`float`): coeficientes do polinjus de referência
        - Canal de Fuga Médio (`float`): cota média do canal de fuga (m)
        - Influencia Vert. Cfuga (`int`): TODO (0 ou 1)
        - Fator Carga Max. (`float`): TODO (%)
        - Fator Carga Min. (`float`): TODO (%)
        - Vazão Mínima Histórica (`float`): vazão mínima da usina (m3/s)
        - Num. Unidades Base (`int`): TODO
        - Tipo Turbina (`int`): TODO
        - Representação Conjunto (`int`): TODO
        - TEIF (`float`): TODO (%)
        - IP (`float`): TODO (%)
        - Tipo de Perda (`int`): TODO
        - Data (`str`): DD-MM-AA
        - Observação (`str`): observação qualquer sobre a usina
        - Volume de Referência (`float`): TODO (hm3)
        - Tipo de Regulação (`str`): D, S ou M

        :return: A tabela com os dados cadastrais
        :rtype: List[pd.DataFrame]
        """
        if self.__df is None:
            self.__df = self.__monta_df_de_registros()
        return self.__df

    @cadastro.setter
    def cadastro(self, df: pd.DataFrame):
        self.__df = df
