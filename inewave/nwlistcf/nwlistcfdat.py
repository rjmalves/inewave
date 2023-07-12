from inewave.nwlistcf.modelos.nwlistcfdat import (
    PeriodoImpressaoCortesEstados,
    OpcoesImpressao,
)

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional, Type, List

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Nwlistcfdat(SectionFile):
    """
    Armazena os dados de entrada para a execução do programa auxiliar
    NWLISTCF, existentes no arquivo `nwlistcf.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [PeriodoImpressaoCortesEstados, OpcoesImpressao]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="nwlistcf.dat"
    ) -> "Nwlistcfdat":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

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
    def mes_inicio(self) -> Optional[int]:
        """
        O mês (calendário) de início para impressão dos cortes

        :return: O mês calendário de início
        :rtype: Optional[int] | None
        """
        b = self.__bloco_por_tipo(PeriodoImpressaoCortesEstados, 0)
        if b is not None:
            return b.data[0]
        return None

    @mes_inicio.setter
    def mes_inicio(self, v: int):
        b = self.__bloco_por_tipo(PeriodoImpressaoCortesEstados, 0)
        if b is not None:
            b.data[0] = v

    @property
    def mes_fim(self) -> Optional[int]:
        """
        O mês de fim para impressão dos cortes

        :return: O mês calendário de fim
        :rtype: Optional[int] | None
        """
        b = self.__bloco_por_tipo(PeriodoImpressaoCortesEstados, 0)
        if b is not None:
            return b.data[1]
        return None

    @mes_fim.setter
    def mes_fim(self, v: int):
        b = self.__bloco_por_tipo(PeriodoImpressaoCortesEstados, 0)
        if b is not None:
            b.data[1] = v

    @property
    def imprime_cortes_ativos(self) -> Optional[int]:
        """
        O flag para impressão somente dos cortes ativos.

        :return: O valor do flag
        :rtype: Optional[int] | None
        """
        b = self.__bloco_por_tipo(PeriodoImpressaoCortesEstados, 0)
        if b is not None:
            return b.data[2]
        return None

    @imprime_cortes_ativos.setter
    def imprime_cortes_ativos(self, v: int):
        b = self.__bloco_por_tipo(PeriodoImpressaoCortesEstados, 0)
        if b is not None:
            b.data[2] = v

    @property
    def opcoes_impressao(self) -> Optional[List[int]]:
        """
        As opções de impressão selecionadas.

        :return: As opções de impressão
        :rtype: Optional[List[int]] | None
        """
        b = self.__bloco_por_tipo(OpcoesImpressao, 0)
        if b is not None:
            return b.data
        return None

    @opcoes_impressao.setter
    def opcoes_impressao(self, v: List[int]):
        b = self.__bloco_por_tipo(OpcoesImpressao, 0)
        if b is not None:
            b.data = v
