from inewave.newave.modelos.eliminacao_cortes import BlocoParametrosEliminacaoCortes

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional, List


class EliminacaoCortes(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos parâmetros
    utilizados na eliminação de cortes de Benders.

    Esta classe lida com informações de entrada do NEWAVE que definem
    como o algoritmo de eliminação de cortes deve ser executado,
    incluindo configurações para diferentes algoritmos (Paralelo,
    Análise por Pares, Shapiro Modificado).

    """

    T = TypeVar("T")

    SECTIONS = [BlocoParametrosEliminacaoCortes]

    @property
    def _parametros(self) -> Optional[List[List]]:
        b = self.data.get_sections_of_type(BlocoParametrosEliminacaoCortes)
        if isinstance(b, BlocoParametrosEliminacaoCortes) and isinstance(b.data, list) and len(b.data) > 0:
            return b.data
        return None
    
    def _get_parametro_por_indice(self, indice: int, coluna: int) -> Optional[int]:
        params = self._parametros
        if params and len(params) > indice and len(params[indice]) > coluna:
            return params[indice][coluna]
        return None

    @property
    def algoritmo_avaliacao_paralelo(self) -> Optional[int]:
        """
        Habilita ou não o algoritmo para eliminação de cortes Paralelo.

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(0, 0)    
        return int(valor) if valor is not None else None

    @property
    def algoritmo_avaliacao_pares(self) -> Optional[int]:
        """
        Habilita ou não o algoritmo para eliminação de cortes por Análise por Pares.

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(0, 1)
        return int(valor) if valor is not None else None

    @property
    def algoritmo_avaliacao_shapiro(self) -> Optional[int]:
        """
        Habilita ou não o algoritmo para eliminação de cortes Shapiro Modificado.

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(0, 2)
        return int(valor) if valor is not None else None

    @property
    def iteracao_inicial_paralelo(self) -> Optional[int]:
        """
        Iteração inicial para aplicação da eliminação de cortes (Paralelo).

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(1, 0)
        return int(valor) if valor is not None else None

    @property
    def iteracao_inicial_pares(self) -> Optional[int]:
        """
        Iteração inicial para aplicação da eliminação de cortes (Análise por Pares).

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(1, 1)
        return int(valor) if valor is not None else None

    @property
    def iteracao_inicial_shapiro(self) -> Optional[int]:
        """
        Iteração inicial para aplicação da eliminação de cortes (Shapiro Modificado).

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(1, 2)
        return int(valor) if valor is not None else None

    @property
    def passo_aplicacao_paralelo(self) -> Optional[int]:
        """
        Passo para aplicação da eliminação de cortes (Paralelo).

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(2, 0)
        return int(valor) if valor is not None else None

    @property
    def passo_aplicacao_pares(self) -> Optional[int]:
        """
        Passo para aplicação da eliminação de cortes (Análise por Pares).

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(2, 1)
        return int(valor) if valor is not None else None

    @property
    def passo_aplicacao_shapiro(self) -> Optional[int]:
        """
        Passo para aplicação da eliminação de cortes (Shapiro Modificado).

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(2, 2)
        return int(valor) if valor is not None else None

    @property
    def janela_iteracoes_pares(self) -> Optional[int]:
        """
        Janela de iterações de construção dos cortes a serem avaliados (Análise por Pares).

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(3, 1)
        return int(valor) if valor is not None else None

    @property
    def janela_iteracoes_shapiro(self) -> Optional[int]:
        """
        Janela de iterações de construção dos cortes a serem avaliados (Shapiro Modificado).

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(3, 2)
        return int(valor) if valor is not None else None

    @property
    def fator_limites_afluencias(self) -> Optional[float]:
        """
        Fator aplicado aos limites das afluências passadas (%).

        :return: O valor do parâmetro
        :rtype: float | None
        """
        valor = self._get_parametro_por_indice(4, 0)
        return float(valor) if valor is not None else None

    @property
    def afluencias_sim_final_calculo_limites(self) -> Optional[int]:
        """
        Afluências da simulação final no cálculo dos limites.

        :return: O valor do parâmetro
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(5, 0)
        return int(valor) if valor is not None else None

    @property
    def impressao_relatorios(self) -> Optional[int]:
        """
        Impressão de relatórios da eliminação de cortes.

        :return: O valor do parâmetro (0=NÃO, 1=SIM)
        :rtype: int | None
        """
        valor = self._get_parametro_por_indice(6, 0)
        return int(valor) if valor is not None else None