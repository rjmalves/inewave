from typing import Dict
import numpy as np  # type: ignore
from inewave.config import SUBMERCADOS, NUM_VARIAVEIS_MEDIAS


class MediasMerc:
    """
    Armazena os dados das saídas referentes às médias de diversas variáveis
    agrupadas por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-MERC.CSV`.

    **Parâmetros**

    - mes_pmo: `int`
    - tabela: `np.ndarray`

    """
    def __init__(self,
                 mes_pmo: int,
                 tabela: np.ndarray):
        self.mes_pmo = mes_pmo
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre MediasMerc avalia todos os valores da tabela.
        """
        if not isinstance(o, MediasMerc):
            return False
        medias: MediasMerc = o
        eq_mes_pmo = self.mes_pmo == medias.mes_pmo
        return eq_mes_pmo and np.array_equal(self.tabela, medias.tabela)

    def _extrai_variavel_tabela(self,
                                indice_variavel: int) -> Dict[str,
                                                              np.ndarray]:
        """
        Lógica para extrair uma variável qualquer da tabela de médias,
        partindo do índice dela (num. da linha) dentro do seu submercado.
        """
        valores: Dict[str, np.ndarray] = {sub: np.array([])
                                          for sub in SUBMERCADOS}
        for i, sub in enumerate(SUBMERCADOS):
            lin = NUM_VARIAVEIS_MEDIAS * i + indice_variavel
            valores[sub] = self.tabela[lin, :]
        return valores

    @property
    def energias_armazenadas_absolutas(self) -> Dict[str,
                                                     np.ndarray]:
        """
        Energias armazenadas em valores absolutos (MWmed) para
        cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.

        """
        return self._extrai_variavel_tabela(0)

    @property
    def energias_armazenadas_percentuais(self) -> Dict[str,
                                                       np.ndarray]:
        """
        Energias armazenadas em valores em percentual da EARMax
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.

        """
        return self._extrai_variavel_tabela(1)

    @property
    def percentil_10_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 10% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(2)

    @property
    def percentil_20_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 20% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(3)

    @property
    def percentil_30_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 30% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(4)

    @property
    def percentil_40_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 40% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(5)

    @property
    def percentil_50_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 50% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(6)

    @property
    def percentil_60_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 60% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(7)

    @property
    def percentil_70_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 70% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(8)

    @property
    def percentil_80_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 80% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(9)

    @property
    def percentil_90_energias_armazenadas(self) -> Dict[str,
                                                        np.ndarray]:
        """
        Valores para o percentil 90% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(10)

    @property
    def percentil_100_energias_armazenadas(self) -> Dict[str,
                                                         np.ndarray]:
        """
        Valores para o percentil 100% da energia armazenada
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(11)

    @property
    def energia_natural_afluente(self) -> Dict[str,
                                               np.ndarray]:
        """
        Energias naturais afluentes em valores absolutos (MWmed)
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(12)

    @property
    def energia_controlavel_corrigida(self) -> Dict[str,
                                                    np.ndarray]:
        """
        Energias controláveis corrigidas em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(13)

    @property
    def energia_fio_dagua_bruta(self) -> Dict[str,
                                              np.ndarray]:
        """
        Energias fio d'água brutas em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(14)

    @property
    def energia_fio_dagua_liquida(self) -> Dict[str,
                                                np.ndarray]:
        """
        Energias fio d'água líquidas em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(15)

    @property
    def geracao_hidraulica_maxima(self) -> Dict[str,
                                                np.ndarray]:
        """
        Gerações hidráulicas máximas em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(16)

    @property
    def geracao_hidraulica_total(self) -> Dict[str,
                                               np.ndarray]:
        """
        Gerações hidráulicas totais em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(18)

    @property
    def geracao_hidraulica_controlavel(self) -> Dict[str,
                                                     np.ndarray]:
        """
        Gerações hidráulicas controláveis em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(19)

    @property
    def geracao_hidraulica_fio_dagua_liquida(self) -> Dict[str,
                                                           np.ndarray]:
        """
        Gerações hidráulicas fio d'água líquidas em valores
        absolutos (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(20)

    @property
    def geracao_eolica(self) -> Dict[str,
                                     np.ndarray]:
        """
        Gerações eólicas em valores absolutos (MWmed) para cada um
        dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(21)

    @property
    def geracao_solar(self) -> Dict[str,
                                    np.ndarray]:
        """
        Gerações solares em valores absolutos (MWmed) para cada um
        dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(22)

    @property
    def vertimento_total(self) -> Dict[str,
                                       np.ndarray]:
        """
        Perdas por vertimento totais em valores absolutos (MWmed)
        para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(23)

    @property
    def vertimento_controlavel(self) -> Dict[str,
                                             np.ndarray]:
        """
        Perdas por vertimento controlável em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(24)

    @property
    def vertimento_fio_dagua(self) -> Dict[str,
                                           np.ndarray]:
        """
        Perdas por vertimento fio d'água em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(25)

    @property
    def vertimento_turbinavel(self) -> Dict[str,
                                            np.ndarray]:
        """
        Vertimentos turbináveis em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(26)

    @property
    def energia_evaporada(self) -> Dict[str,
                                        np.ndarray]:
        """
        Perdas por energia evaporada em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(40)

    @property
    def geracao_termica(self) -> Dict[str,
                                      np.ndarray]:
        """
        Gerações de usinas termelétricas em valores absolutos
        (MWmed) para cada um dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(42)

    @property
    def deficit(self) -> Dict[str,
                              np.ndarray]:
        """
        Déficits de carga em valores absolutos (MWmed) para cada um
        dos submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(43)

    @property
    def custo_marginal_operacao(self) -> Dict[str,
                                              np.ndarray]:
        """
        Custos marginais de operação (R$) para cada um dos
        submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(45)

    @property
    def custo_deficit(self) -> Dict[str,
                                    np.ndarray]:
        """
        Custos de déficit (R$) para cada um dos
        submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(46)

    @property
    def custo_termica(self) -> Dict[str,
                                    np.ndarray]:
        """
        Custos de térmicas (R$) para cada um dos
        submercados.

        **Retorna**

        `Dict[str, np.ndarray]`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(47)
