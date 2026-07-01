from pathlib import Path
from typing import IO, Any, TypeVar
from warnings import warn

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from cfinterface.files.registerfile import RegisterFile
from cfinterface.storage import StorageType

from inewave.config import MESES_ABREV
from inewave.newave.modelos.hidr import RegistroUHEHidr, RegistroUHEHidrF64


class Hidr(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao cadastro das
    usinas hidroelétricas.

    Suporta os dois formatos do arquivo binário: o formato com
    registros de 792 bytes (coeficientes dos polinômios volume-cota e
    cota-área em 32 bits) e o formato com registros de 832 bytes
    (coeficientes em 64 bits). Na leitura, o formato é detectado
    automaticamente pelo tamanho do arquivo, que corresponde a 320 ou
    600 registros em um dos dois tamanhos, podendo ser forçado com
    `version="f32"` ou `version="f64"`. A escrita é feita sempre no
    mesmo formato lido, a menos que seja feita uma conversão explícita
    com :meth:`converte_tamanho_registro`.
    """

    T = TypeVar("T")

    REGISTERS = [RegistroUHEHidr]
    VERSIONS = {
        "f32": [RegistroUHEHidr],
        "f64": [RegistroUHEHidrF64],
    }
    STORAGE = StorageType.BINARY

    __REGISTROS_POR_TAMANHO: dict[int, type[RegistroUHEHidr]] = {
        RegistroUHEHidr.TAMANHO_REGISTRO: RegistroUHEHidr,
        RegistroUHEHidrF64.TAMANHO_REGISTRO: RegistroUHEHidrF64,
    }

    # Quantidades de registros (usinas) que o cadastro do hidr pode
    # conter. O arquivo é um vetor de tamanho fixo, idêntico nos dois
    # formatos de precisão.
    __NUMEROS_REGISTROS_SUPORTADOS = (320, 600)

    # Tamanhos de arquivo (em bytes) reconhecidos, mapeando cada tamanho
    # válido para a respectiva versão. Derivado das combinações de
    # número de registros e tamanho de registro; as quatro combinações
    # geram tamanhos distintos, sem ambiguidade entre os formatos.
    __TAMANHOS_VALIDOS: dict[int, str] = {
        num * tamanho: versao
        for num in __NUMEROS_REGISTROS_SUPORTADOS
        for versao, tamanho in (
            ("f32", RegistroUHEHidr.TAMANHO_REGISTRO),
            ("f64", RegistroUHEHidrF64.TAMANHO_REGISTRO),
        )
    }

    def __init__(self, data: Any = ...) -> None:
        super().__init__(data)
        self.__df: pd.DataFrame | None = None

    @classmethod
    def __detecta_versao(cls, content: str | bytes) -> str | None:
        """
        Detecta o formato do arquivo a partir do tamanho do seu
        conteúdo. Um arquivo hidr válido contém 320 ou 600 registros,
        de 792 bytes (coeficientes em 32 bits) ou de 832 bytes
        (coeficientes em 64 bits), resultando em um dos tamanhos
        reconhecidos. Tamanhos diferentes geram um aviso e a leitura
        assume o formato de 792 bytes.
        """
        if isinstance(content, bytes):
            num_bytes = len(content)
        elif isinstance(content, str) and Path(content).is_file():
            num_bytes = Path(content).stat().st_size
        else:
            return None
        versao = cls.__TAMANHOS_VALIDOS.get(num_bytes)
        if versao is not None:
            return versao
        warn(
            f"O tamanho do arquivo hidr ({num_bytes} bytes) não"
            + " corresponde a nenhum formato conhecido (320 ou 600"
            + " registros de 792 ou 832 bytes). Assumindo registros de"
            + f" {RegistroUHEHidr.TAMANHO_REGISTRO} bytes. Use o"
            + ' argumento version="f32" ou version="f64" para forçar o'
            + " formato.",
            stacklevel=3,
        )
        return None

    @classmethod
    def read(
        cls,
        content: str | bytes,
        *args: Any,
        version: str | None = None,
        **kwargs: Any,
    ) -> "Hidr":
        if version is None:
            version = cls.__detecta_versao(content)
        h = super().read(content, *args, version=version, **kwargs)
        assert isinstance(h, Hidr)
        return h

    @property
    def tamanho_registro(self) -> int:
        """
        O tamanho em bytes dos registros do arquivo: 792 para o
        formato com coeficientes dos polinômios em 32 bits ou 832
        para o formato em 64 bits.

        :return: O tamanho do registro em bytes
        :rtype: int
        """
        for r in self.data.of_type(RegistroUHEHidr):
            return type(r).TAMANHO_REGISTRO
        return RegistroUHEHidr.TAMANHO_REGISTRO

    def converte_tamanho_registro(self, precisao: str) -> None:
        """
        Converte os registros do arquivo para o formato com o tamanho
        de registro dado, de modo que a próxima escrita seja feita
        neste formato. A conversão de 832 para 792 bytes implica em
        perda de precisão nos coeficientes dos polinômios volume-cota
        e cota-área.

        :param precisao: A precisão dos coeficients dos polinômios
            ('f32' ou 'f64')
        """

        mapa_tamanhos = {"f32": 792, "f64": 832}

        tamanho_registro = mapa_tamanhos.get(precisao)
        if tamanho_registro is None:
            raise ValueError(
                f"Precisão inválida: '{precisao}'. Os valores"
                + " suportados são 'f32' e 'f64'."
            )
        classe_registro = self.__class__.__REGISTROS_POR_TAMANHO[
            tamanho_registro
        ]
        for r in list(self.data.of_type(RegistroUHEHidr)):
            if type(r) is classe_registro:
                continue
            novo = classe_registro(data=list(r.data))
            self.data.add_after(r, novo)
            self.data.remove(r)

    def write(self, to: str | IO[Any], *args: Any, **kwargs: Any) -> None:
        self.__atualiza_registros()
        super().write(to, *args, **kwargs)

    def __monta_df_de_registros(self) -> pd.DataFrame | None:
        registros: list[RegistroUHEHidr] = [
            r for r in self.data.of_type(RegistroUHEHidr)
        ]
        if len(registros) == 0:
            return None
        colunas = [
            "nome_usina",
            "posto",
            "submercado",
            "empresa",
            "codigo_usina_jusante",
            "desvio",
            "volume_minimo",
            "volume_maximo",
            "volume_vertedouro",
            "volume_desvio",
            "cota_minima",
            "cota_maxima",
            *[f"a{i}_volume_cota" for i in range(5)],
            *[f"a{i}_cota_area" for i in range(5)],
            *[f"evaporacao_{m}" for m in MESES_ABREV],
            "numero_conjuntos_maquinas",
            *[f"maquinas_conjunto_{i}" for i in range(1, 6)],
            *[f"potencia_nominal_conjunto_{i}" for i in range(1, 6)],
            *[f"queda_nominal_conjunto_{i}" for i in range(1, 6)],
            *[f"vazao_nominal_conjunto_{i}" for i in range(1, 6)],
            "produtibilidade_especifica",
            "perdas",
            "numero_polinomios_jusante",
            *[f"a{i}_jusante_1" for i in range(5)],
            *[f"a{i}_jusante_2" for i in range(5)],
            *[f"a{i}_jusante_3" for i in range(5)],
            *[f"a{i}_jusante_4" for i in range(5)],
            *[f"a{i}_jusante_5" for i in range(5)],
            *[f"a{i}_jusante_6" for i in range(5)],
            *[f"referencia_jusante_{i}" for i in range(1, 7)],
            "canal_fuga_medio",
            "influencia_vertimento_canal_fuga",
            "fator_carga_maximo",
            "fator_carga_minimo",
            "vazao_minima_historica",
            "numero_unidades_base",
            "tipo_turbina",
            "representacao_conjunto",
            "teif",
            "ip",
            "tipo_perda",
            "data",
            "observacao",
            "volume_referencia",
            "tipo_regulacao",
        ]

        dados = [
            [
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
            for r in registros
        ]

        df = pd.DataFrame(
            data=dados,
            index=range(1, len(registros) + 1),
            columns=colunas,
        )
        df.index.name = "codigo_usina"

        df = df.astype(
            {
                "nome_usina": str,
                "posto": "Int64",
                "submercado": "Int64",
                "empresa": "Int64",
                "codigo_usina_jusante": "Int64",
                "desvio": "Int64",
                "volume_minimo": float,
                "volume_maximo": float,
                "volume_vertedouro": float,
                "volume_desvio": float,
                "cota_minima": float,
                "cota_maxima": float,
                "produtibilidade_especifica": float,
                "perdas": float,
                "canal_fuga_medio": float,
                "influencia_vertimento_canal_fuga": "Int64",
                "fator_carga_maximo": float,
                "fator_carga_minimo": float,
                "vazao_minima_historica": "Int64",
                "numero_unidades_base": "Int64",
                "tipo_turbina": "Int64",
                "representacao_conjunto": "Int64",
                "teif": float,
                "ip": float,
                "tipo_perda": "Int64",
                "data": str,
                "observacao": str,
                "volume_referencia": float,
                "tipo_regulacao": str,
            },
        )
        return df

    def __atualiza_registros(self) -> None:
        registros: list[RegistroUHEHidr] = [r for r in self.data][1:]  # type: ignore[assignment]
        for (_, linha), r in zip(self.cadastro.iterrows(), registros):
            r.nome = linha["nome_usina"]
            r.posto = linha["posto"]
            r.subsistema = linha["submercado"]
            r.empresa = linha["empresa"]
            r.jusante = linha["codigo_usina_jusante"]
            r.desvio = linha["desvio"]
            r.volume_minimo = linha["volume_minimo"]
            r.volume_maximo = linha["volume_maximo"]
            r.volume_vertedouro = linha["volume_vertedouro"]
            r.volume_desvio = linha["volume_desvio"]
            r.cota_minima = linha["cota_minima"]
            r.cota_maxima = linha["cota_maxima"]
            r.polinomio_volume_cota = linha[
                [f"a{i}_volume_cota" for i in range(5)]
            ].tolist()
            r.polinomio_cota_area = linha[
                [f"a{i}_cota_area" for i in range(5)]
            ].tolist()
            r.evaporacao = linha[
                [f"evaporacao_{m}" for m in MESES_ABREV]
            ].tolist()
            r.numero_conjuntos_maquinas = linha["numero_conjuntos_maquinas"]
            r.potef_conjunto = linha[
                [f"potencia_nominal_conjunto_{i}" for i in range(1, 6)]
            ].tolist()
            r.hef_conjunto = linha[
                [f"queda_nominal_conjunto_{i}" for i in range(1, 6)]
            ].tolist()
            r.qef_conjunto = linha[
                [f"vazao_nominal_conjunto_{i}" for i in range(1, 6)]
            ].tolist()
            r.produtibilidade_especifica = linha["produtibilidade_especifica"]
            r.perdas = linha["perdas"]
            r.numero_polinomios_jusante = linha["numero_polinomios_jusante"]
            r.polinomios_jusante = linha[
                [f"a{i}_jusante_1" for i in range(5)]
                + [f"a{i}_jusante_2" for i in range(5)]
                + [f"a{i}_jusante_3" for i in range(5)]
                + [f"a{i}_jusante_4" for i in range(5)]
                + [f"a{i}_jusante_5" for i in range(5)]
                + [f"a{i}_jusante_6" for i in range(5)]
                + [f"referencia_jusante_{i}" for i in range(1, 7)]
            ].tolist()
            r.canal_fuga_medio = linha["canal_fuga_medio"]
            r.influencia_vertimento_canal_fuga = linha[
                "influencia_vertimento_canal_fuga"
            ]
            r.fator_carga_maximo = linha["fator_carga_maximo"]
            r.fator_carga_minimo = linha["fator_carga_minimo"]
            r.vazao_minima_historica = linha["vazao_minima_historica"]
            r.numero_unidades_base = linha["numero_unidades_base"]
            r.tipo_turbina = linha["tipo_turbina"]
            r.representacao_conjunto = linha["representacao_conjunto"]
            r.teif = linha["teif"]
            r.ip = linha["ip"]
            r.tipo_perda = linha["tipo_perda"]
            r.data_referencia = linha["data"]
            r.observacao = linha["observacao"]
            r.volume_referencia = linha["volume_referencia"]
            r.tipo_regulacao = linha["tipo_regulacao"]

    @property
    def cadastro(self) -> pd.DataFrame:
        """
        Obtém a tabela com os dados cadastrais existentes no arquivo
        binário.

        - nome_usina (`str`): nome da usina (12 caracteres)
        - posto (`int`): posto de vazão natural da usina
        - submercado (`int`): submercado da usina
        - empresa (`int`): agente responsável pela usina
        - codigo_usina_jusante (`int`): posto à jusante da usina
        - desvio (`float`): TODO
        - volume_minimo (`float`): volume mínimo da usina (hm3)
        - volume_maximo (`float`): volume máximo da usina (hm3)
        - volume_vertedouro (`float`): volume do vertedouro da usina (hm3)
        - volume_desvio (`float`): TODO
        - cota_minima (`float`): cota mínima da usina (m)
        - cota_maxima (`float`): cota máxima da usina (m)
        - a[0-4]_volume_cota (`float`): coeficientes do polinômio volume-cota
        - a[0-4]_cota_area (`float`): coeficientes do polinômio cota-área
        - evaporacao_[JAN..DEZ] (`float`): coeficientes de evaporação (mm)
        - numero_conjuntos_maquinas (`int`): número de conjuntos de máquinas
        - maquinas_conjunto_[1-5] (`int`): máquinas por conjunto
        - potencia_nominal_conjunto_[1-5] (`float`): potência das máquinas (MWmed)
        - queda_nominal_conjunto_[1-5]: alturas nominais de queda por conjunto (m)
        - vazao_nominal_conjunto_[1-5]: vazões nominais por conjunto (m3/s)
        - produtibilidade_especifica (`float`): produtibilidade específica
        - perdas (`float`): perdas da usina
        - numero_polinomios_jusante (`int`): número de polinômios de jusante
        - a[0-4]_jusante_[1-6] (`float`): coeficientes de cada polinjus
        - referencia_jusante_[1-6] (`float`): coeficientes do polinjus de referência
        - canal_fuga_medio (`float`): cota média do canal de fuga (m)
        - influencia_vertimento_canal_fuga (`int`): TODO (0 ou 1)
        - fator_carga_maximo (`float`): TODO (%)
        - fator_carga_minimo (`float`): TODO (%)
        - vazao_minima_historica (`float`): vazão mínima da usina (m3/s)
        - numero_unidades_base (`int`): TODO
        - tipo_turbina (`int`): TODO
        - representacao_conjunto (`int`): TODO
        - teif (`float`): TODO (%)
        - ip (`float`): TODO (%)
        - tipo_perda (`int`): TODO
        - data (`str`): DD-MM-AA
        - observacao (`str`): observação qualquer sobre a usina
        - volume_referencia (`float`): TODO (hm3)
        - tipo_regulacao (`str`): D, S ou M

        :return: A tabela com os dados cadastrais
        :rtype: pd.DataFrame | None
        """
        if self.__df is None:
            self.__df = self.__monta_df_de_registros()
        return self.__df

    @cadastro.setter
    def cadastro(self, df: pd.DataFrame) -> None:
        self.__df = df
