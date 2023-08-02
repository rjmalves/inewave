from inewave.newave.modelos.selcor import (
    BlocoDadosSelcor,
)

from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional


class Selcor(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à metodologia
    de seleção de cortes.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [
        BlocoDadosSelcor,
    ]

    @property
    def iteracao_inicial(self) -> Optional[int]:
        """
        O número da iteração inicial em que é aplicada a seleção
        de cortes.

        :return: O número da iteração
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            return b.data[0][0]
        return None

    @iteracao_inicial.setter
    def iteracao_inicial(self, valor: int):
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            b.data[0][0] = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def tamanho_janela(self) -> Optional[int]:
        """
        O tamanho da janela de cortes ativos.

        :return: A janela
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            return b.data[1][0]
        return None

    @tamanho_janela.setter
    def tamanho_janela(self, valor: int):
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            b.data[1][0] = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def numero_cortes_adicionados_por_iteracao(self) -> Optional[int]:
        """
        O número de cortes que são adicionados a cada iteração
        do processo de seleção de cortes.

        :return: O número de cortes adicionados.
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            return b.data[2][0]
        return None

    @numero_cortes_adicionados_por_iteracao.setter
    def numero_cortes_adicionados_por_iteracao(self, valor: int):
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            b.data[2][0] = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def considera_cortes_da_propria_iteracao(self) -> Optional[int]:
        """
        O flag para considerar ou não os cortes construídos na própria
        iteração durante a backward.

        :return: O valor do flag
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            return b.data[3][0]
        return None

    @considera_cortes_da_propria_iteracao.setter
    def considera_cortes_da_propria_iteracao(self, valor: int):
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            b.data[3][0] = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def imprime_relatorio(self) -> Optional[int]:
        """
        O flag para realizar ou não a impressão do relatório de
        saída do processo de seleção de cortes.

        :return: O valor do flag
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            return b.data[4][0]
        return None

    @imprime_relatorio.setter
    def imprime_relatorio(self, valor: int):
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            b.data[4][0] = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def iteracoes_impressao(self) -> Optional[List[int]]:
        """
        O intervalo de iterações para as quais será realizada
        a impressão dos valores de saída.

        :return: As iterações inicial e final
        :rtype: list[int] | None
        """
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            return b.data[5]
        return None

    @iteracoes_impressao.setter
    def iteracoes_impressao(self, valor: List[int]):
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            b.data[5] = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def series_impressao(self) -> Optional[List[int]]:
        """
        O intervalo de séries para as quais será realizada
        a impressão dos valores de saída.

        :return: As séries inicial e final
        :rtype: list[int] | None
        """
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            return b.data[6]
        return None

    @series_impressao.setter
    def series_impressao(self, valor: List[int]):
        b = self.data.get_sections_of_type(BlocoDadosSelcor)
        if isinstance(b, BlocoDadosSelcor):
            b.data[6] = valor
        else:
            raise ValueError("Campo não lido")
