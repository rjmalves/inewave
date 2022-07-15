from inewave.newave.modelos.curva import (
    BlocoConfiguracoesPenalizacaoCurva,
    BlocoPenalidadesViolacaoREECurva,
    BlocoCurvaSegurancaSubsistema,
    BlocoMaximoIteracoesProcessoIterativoEtapa2,
    BlocoIteracaoAPartirProcessoIterativoEtapa2,
    BlocoToleranciaProcessoIterativoEtapa2,
    BlocoImpressaoRelatorioProcessoIterativoEtapa2,
)

from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore


class Curva(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à curva para
    penalização por volume mínimo dos reservatórios.
    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoConfiguracoesPenalizacaoCurva,
        BlocoPenalidadesViolacaoREECurva,
        BlocoCurvaSegurancaSubsistema,
        BlocoMaximoIteracoesProcessoIterativoEtapa2,
        BlocoIteracaoAPartirProcessoIterativoEtapa2,
        BlocoToleranciaProcessoIterativoEtapa2,
        BlocoImpressaoRelatorioProcessoIterativoEtapa2,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="curva.dat") -> "Curva":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="curva.dat"):
        self.write(diretorio, nome_arquivo)

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
    def configuracoes_penalizacao(self) -> Optional[list]:
        """
        Linha de configuração das opções de penalização do
        arquivo curva.dat.

        :return: Os valores dos campos da linha como uma lista.
        :rtype: Optional[list]
        """
        b = self.__bloco_por_tipo(BlocoConfiguracoesPenalizacaoCurva, 0)
        if b is not None:
            return b.data
        return None

    @configuracoes_penalizacao.setter
    def configuracoes_penalizacao(self, valor: list):
        b = self.__bloco_por_tipo(BlocoConfiguracoesPenalizacaoCurva, 0)
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def custos_penalidades(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os custos para penalização em cada REE.

        - Subsistema (`int`)
        - Custo (`float`)

        :return: Os custos por REE em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoPenalidadesViolacaoREECurva, 0)
        if b is not None:
            return b.data
        return None

    @custos_penalidades.setter
    def custos_penalidades(self, valor: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoPenalidadesViolacaoREECurva, 0)
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def curva_seguranca(self) -> Optional[pd.DataFrame]:
        """
        Tabela da curva de segurança por REE.

        - REE (`int`)
        - Ano (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: Os valores dos campos da linha como uma lista.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoCurvaSegurancaSubsistema, 0)
        if b is not None:
            return b.data
        return None

    @curva_seguranca.setter
    def curva_seguranca(self, valor: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoCurvaSegurancaSubsistema, 0)
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def maximo_iteracoes_etapa2(self) -> Optional[int]:
        """
        Número máximo de iterações no processo iterativo de 2ª
        etapa.

        :return: O valor como um int
        :rtype: Optional[int]
        """
        b = self.__bloco_por_tipo(
            BlocoMaximoIteracoesProcessoIterativoEtapa2, 0
        )
        if b is not None:
            return b.data
        return None

    @maximo_iteracoes_etapa2.setter
    def maximo_iteracoes_etapa2(self, valor: int):
        b = self.__bloco_por_tipo(
            BlocoMaximoIteracoesProcessoIterativoEtapa2, 0
        )
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def iteracao_a_partir_etapa2(self) -> Optional[int]:
        """
        Iteração a partir da qual ocorre o processo iterativo de 2ª
        etapa.

        :return: O valor como um int
        :rtype: Optional[int]
        """
        b = self.__bloco_por_tipo(
            BlocoIteracaoAPartirProcessoIterativoEtapa2, 0
        )
        if b is not None:
            return b.data
        return None

    @iteracao_a_partir_etapa2.setter
    def iteracao_a_partir_etapa2(self, valor: int):
        b = self.__bloco_por_tipo(
            BlocoIteracaoAPartirProcessoIterativoEtapa2, 0
        )
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def tolerancia_processo_etapa2(self) -> Optional[float]:
        """
        Tolerância para a execução do processo iterativo de etapa 2.

        :return: O valor como um float
        :rtype: Optional[float]
        """
        b = self.__bloco_por_tipo(BlocoToleranciaProcessoIterativoEtapa2, 0)
        if b is not None:
            return b.data
        return None

    @tolerancia_processo_etapa2.setter
    def tolerancia_processo_etapa2(self, valor: int):
        b = self.__bloco_por_tipo(BlocoToleranciaProcessoIterativoEtapa2, 0)
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def impressao_relatorio_etapa2(self) -> Optional[int]:
        """
        Opção de impressão ou não do relatório do
        processo iterativo de 2ª etapa.

        :return: O valor como um int
        :rtype: Optional[int]
        """
        b = self.__bloco_por_tipo(
            BlocoImpressaoRelatorioProcessoIterativoEtapa2, 0
        )
        if b is not None:
            return b.data
        return None

    @impressao_relatorio_etapa2.setter
    def impressao_relatorio_etapa2(self, valor: int):
        b = self.__bloco_por_tipo(
            BlocoImpressaoRelatorioProcessoIterativoEtapa2, 0
        )
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")
