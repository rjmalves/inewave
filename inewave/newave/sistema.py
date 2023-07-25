from inewave.newave.modelos.sistema import (
    BlocoCustosDeficit,
    BlocoGeracaoUsinasNaoSimuladas,
    BlocoIntercambioSubsistema,
    BlocoMercadoEnergiaSistema,
    BlocoNumeroPatamaresDeficit,
)


from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Sistema(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações
    dos subsistemas (submercados).

    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoNumeroPatamaresDeficit,
        BlocoCustosDeficit,
        BlocoIntercambioSubsistema,
        BlocoMercadoEnergiaSistema,
        BlocoGeracaoUsinasNaoSimuladas,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="sistema.dat"
    ) -> "Sistema":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="sistema.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    @property
    def numero_patamares_deficit(self) -> Optional[int]:
        """
        O número de patamares de déficit utilizados no estudo.

        :return: O número de patamares como um inteiro
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoNumeroPatamaresDeficit, 0)
        if b is not None:
            return b.data
        return None

    @numero_patamares_deficit.setter
    def numero_patamares_deficit(self, n: int):
        b = self.__bloco_por_tipo(BlocoNumeroPatamaresDeficit, 0)
        if b is not None:
            b.data = n

    @property
    def custo_deficit(self) -> Optional[pd.DataFrame]:
        """
        Tabela com o custo de cada patamar de déficit, por
        subsistema.

        - codigo_submercado (`int`)
        - nome_submercado (`str`)
        - ficticio (`int`)
        - custo_deficit_patamar_1 (`float`)
        - ...
        - custo_deficit_patamar_5 (`float`)
        - corte_patamar_1 (`float`)
        - ...
        - corte_patamar_5 (`float`)

        :return: A duração por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoCustosDeficit, 0)
        if b is not None:
            return b.data
        return None

    @custo_deficit.setter
    def custo_deficit(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoCustosDeficit, 0)
        if b is not None:
            b.data = df

    @property
    def limites_intercambio(self) -> Optional[pd.DataFrame]:
        """
        Tabela com o limite de intercâmbio por par de
        subsistemas.

        - submercado_de (`int`)
        - submercado_para (`int`)
        - sentido (`int`)
        - ano (`int`)
        - janeiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A duração por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoIntercambioSubsistema, 0)
        if b is not None:
            return b.data
        return None

    @limites_intercambio.setter
    def limites_intercambio(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoIntercambioSubsistema, 0)
        if b is not None:
            b.data = df

    @property
    def mercado_energia(self) -> Optional[pd.DataFrame]:
        """
        Tabela com o mercado total de energia por período de estudo.

        - submercado (`int`)
        - ano (`int`)
        - janeiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A carga por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoMercadoEnergiaSistema, 0)
        if b is not None:
            return b.data
        return None

    @mercado_energia.setter
    def mercado_energia(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoMercadoEnergiaSistema, 0)
        if b is not None:
            b.data = df

    @property
    def geracao_usinas_nao_simuladas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a geração das usinas não simuladas por fonte
        de geração.

        - submercado (`int`)
        - bloco (`int`)
        - fonte (`str`)
        - ano (`int`)
        - janeiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A carga por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoGeracaoUsinasNaoSimuladas, 0)
        if b is not None:
            return b.data
        return None

    @geracao_usinas_nao_simuladas.setter
    def geracao_usinas_nao_simuladas(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoGeracaoUsinasNaoSimuladas, 0)
        if b is not None:
            b.data = df
