from inewave.nwlistcf.modelos.nwlistcfdat import (
    PeriodoImpressaoCortesEstados,
    OpcoesImpressao,
)

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional, List


class Nwlistcfdat(SectionFile):
    """
    Armazena os dados de entrada para a execução do programa auxiliar
    NWLISTCF, existentes no arquivo `nwlistcf.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [PeriodoImpressaoCortesEstados, OpcoesImpressao]

    @property
    def mes_inicio(self) -> Optional[int]:
        """
        O mês (calendário) de início para impressão dos cortes

        :return: O mês calendário de início
        :rtype: Optional[int] | None
        """
        b = self.data.get_sections_of_type(PeriodoImpressaoCortesEstados)
        if isinstance(b, PeriodoImpressaoCortesEstados):
            return b.data[0]
        return None

    @mes_inicio.setter
    def mes_inicio(self, v: int):
        b = self.data.get_sections_of_type(PeriodoImpressaoCortesEstados)
        if isinstance(b, PeriodoImpressaoCortesEstados):
            b.data[0] = v

    @property
    def mes_fim(self) -> Optional[int]:
        """
        O mês de fim para impressão dos cortes

        :return: O mês calendário de fim
        :rtype: Optional[int] | None
        """
        b = self.data.get_sections_of_type(PeriodoImpressaoCortesEstados)
        if isinstance(b, PeriodoImpressaoCortesEstados):
            return b.data[1]
        return None

    @mes_fim.setter
    def mes_fim(self, v: int):
        b = self.data.get_sections_of_type(PeriodoImpressaoCortesEstados)
        if isinstance(b, PeriodoImpressaoCortesEstados):
            b.data[1] = v

    @property
    def imprime_cortes_ativos(self) -> Optional[int]:
        """
        O flag para impressão somente dos cortes ativos.

        :return: O valor do flag
        :rtype: Optional[int] | None
        """
        b = self.data.get_sections_of_type(PeriodoImpressaoCortesEstados)
        if isinstance(b, PeriodoImpressaoCortesEstados):
            return b.data[2]
        return None

    @imprime_cortes_ativos.setter
    def imprime_cortes_ativos(self, v: int):
        b = self.data.get_sections_of_type(PeriodoImpressaoCortesEstados)
        if isinstance(b, PeriodoImpressaoCortesEstados):
            b.data[2] = v

    @property
    def opcoes_impressao(self) -> Optional[List[int]]:
        """
        As opções de impressão selecionadas.

        :return: As opções de impressão
        :rtype: Optional[List[int]] | None
        """
        b = self.data.get_sections_of_type(OpcoesImpressao)
        if isinstance(b, OpcoesImpressao):
            return b.data
        return None

    @opcoes_impressao.setter
    def opcoes_impressao(self, v: List[int]):
        b = self.data.get_sections_of_type(OpcoesImpressao)
        if isinstance(b, OpcoesImpressao):
            b.data = v
