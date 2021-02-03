import numpy as np  # type: ignore


class MediasSIN:
    """
    Armazena os dados das saídas referentes às médias de diversas variáveis
    para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-SIN.CSV`.

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
        A igualdade entre MediasSIN avalia todos os valores da tabela.
        """
        if not isinstance(o, MediasSIN):
            return False
        medias: MediasSIN = o
        eq_mes_pmo = self.mes_pmo == medias.mes_pmo
        return eq_mes_pmo and np.array_equal(self.tabela, medias.tabela)

    def _extrai_variavel_tabela(self,
                                indice_variavel: int) -> np.ndarray:
        """
        Lógica para extrair uma variável qualquer da tabela de médias,
        partindo do índice dela (num. da linha).
        """
        return self.tabela[indice_variavel, :]

    @property
    def energias_armazenadas_absolutas(self) -> np.ndarray:
        """
        Energias armazenadas em valores absolutos (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(0)

    @property
    def energias_armazenadas_percentuais(self) -> np.ndarray:
        """
        Energias armazenadas em valores em percentual da EARMax.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(1)

    @property
    def percentil_10_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 10% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(2)

    @property
    def percentil_20_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 20% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(3)

    @property
    def percentil_30_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 30% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(4)

    @property
    def percentil_40_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 40% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(5)

    @property
    def percentil_50_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 50% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(6)

    @property
    def percentil_60_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 60% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(7)

    @property
    def percentil_70_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 70% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(8)

    @property
    def percentil_80_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 80% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(9)

    @property
    def percentil_90_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 90% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(10)

    @property
    def percentil_100_energias_armazenadas(self) -> np.ndarray:
        """
        Valores para o percentil 100% da energia armazenada.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(11)

    @property
    def energia_natural_afluente(self) -> np.ndarray:
        """
        Energias naturais afluentes em valores absolutos (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(12)

    @property
    def energia_controlavel_corrigida(self) -> np.ndarray:
        """
        Energias controláveis corrigidas em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(13)

    @property
    def energia_fio_dagua_bruta(self) -> np.ndarray:
        """
        Energias fio d'água brutas em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(14)

    @property
    def energia_fio_dagua_liquida(self) -> np.ndarray:
        """
        Energias fio d'água líquidas em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(15)

    @property
    def geracao_hidraulica_maxima(self) -> np.ndarray:
        """
        Gerações hidráulicas máximas em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(16)

    @property
    def geracao_hidraulica_total(self) -> np.ndarray:
        """
        Gerações hidráulicas totais em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(18)

    @property
    def geracao_hidraulica_controlavel(self) -> np.ndarray:
        """
        Gerações hidráulicas controláveis em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(19)

    @property
    def geracao_hidraulica_fio_dagua_liquida(self) -> np.ndarray:
        """
        Gerações hidráulicas fio d'água líquidas em valores
        absolutos (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(20)

    @property
    def geracao_eolica(self) -> np.ndarray:
        """
        Gerações eólicas em valores absolutos (MWmed) para cada um
        dos submercados.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(21)

    @property
    def geracao_solar(self) -> np.ndarray:
        """
        Gerações solares em valores absolutos (MWmed) para cada um
        dos submercados.

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(22)

    @property
    def vertimento_total(self) -> np.ndarray:
        """
        Perdas por vertimento totais em valores absolutos (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(23)

    @property
    def vertimento_controlavel(self) -> np.ndarray:
        """
        Perdas por vertimento controlável em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(24)

    @property
    def vertimento_fio_dagua(self) -> np.ndarray:
        """
        Perdas por vertimento fio d'água em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(25)

    @property
    def vertimento_turbinavel(self) -> np.ndarray:
        """
        Vertimentos turbináveis em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(26)

    @property
    def energia_evaporada(self) -> np.ndarray:
        """
        Perdas por energia evaporada em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(41)

    @property
    def geracao_termica(self) -> np.ndarray:
        """
        Gerações de usinas termelétricas em valores absolutos
        (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(43)

    @property
    def deficit(self) -> np.ndarray:
        """
        Déficits de carga em valores absolutos (MWmed).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(44)

    @property
    def custo_termica(self) -> np.ndarray:
        """
        Custos de térmicas (MMR$).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(45)

    @property
    def custo_deficit(self) -> np.ndarray:
        """
        Custos de déficit (MMR$).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(46)

    @property
    def custo_operacao_total(self) -> np.ndarray:
        """
        Custos de operação totais (MMR$).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(47)

    @property
    def custo_operacao_mx(self) -> np.ndarray:
        """
        Custos de operação MX (MMR$).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(48)

    @property
    def custo_operacao_violacao(self) -> np.ndarray:
        """
        Custos de operação por violação (MMR$).

        **Retorna**

        `np.ndarray`

        **Sobre**

        A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self._extrai_variavel_tabela(49)
