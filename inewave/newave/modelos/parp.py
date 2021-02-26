from inewave.config import REES
from typing import Dict, List
import numpy as np  # type: ignore


class PARp:
    """
    Armazena os dados de saída do NEWAVE referentes aos modelos e às
    séries sintéticas de energia geradas pelo PAR(p) e PAR(p)-A.


    Esta classe lida com informações de saída do NEWAVE e
    cujas saídas devem ser compatíveis com as observadas através
    do NWLISTOP.

    **Parâmetros**

    - ordens_orig: `Dict[int, np.ndarray]`
    - ordens_finais: `Dict[int, np.ndarray]`
    - coeficientes: `Dict[int, np.ndarray]`
    - series_energia: `Dict[int, np.ndarray]`
    - correl_energia: `Dict[int, np.ndarray]`
    - series_medias: `Dict[int, np.ndarray]`
    - correl_media: `Dict[int, np.ndarray]`

    """
    def __init__(self,
                 ordens_orig: Dict[int, np.ndarray],
                 ordens_finais: Dict[int, np.ndarray],
                 coeficientes: Dict[int, np.ndarray],
                 series_energia: Dict[int, np.ndarray],
                 correl_energia: Dict[int, np.ndarray],
                 series_medias: Dict[int, np.ndarray],
                 correl_media: Dict[int, np.ndarray],
                 correl_e_anual: Dict[int, np.ndarray],
                 correl_e_mensal: Dict[int, np.ndarray]):
        self.ordens_orig = ordens_orig
        self.ordens_finais = ordens_finais
        self.coeficientes = coeficientes
        self.series_energia = series_energia
        self.correl_energia = correl_energia
        self.series_medias = series_medias
        self.correl_media = correl_media
        self.correl_e_anual = correl_e_anual
        self.correl_e_mensal = correl_e_mensal

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre PARp avalia todos os campos.
        """
        if not isinstance(o, PARp):
            return False
        parp: PARp = o
        eq_ordens_o = all([np.array_equal(o1, o2)
                           for (o1, o2) in zip(self.ordens_orig.values(),
                                               parp.ordens_orig.values())])
        eq_ordens_f = all([np.array_equal(o1, o2)
                           for (o1, o2) in zip(self.ordens_finais.values(),
                                               parp.ordens_finais.values())])
        eq_coefs = all([np.array_equal(c1, c2)
                        for (c1, c2) in zip(self.coeficientes.values(),
                                            parp.coeficientes.values())])
        eq_series_e = all([np.array_equal(s1, s2)
                           for (s1, s2) in zip(self.series_energia.values(),
                                               parp.series_energia.values())])
        eq_correl_e = all([np.array_equal(s1, s2)
                           for (s1, s2) in zip(self.correl_energia.values(),
                                               parp.correl_energia.values())])
        eq_medias_e = all([np.array_equal(s1, s2)
                           for (s1, s2) in zip(self.series_medias.values(),
                                               parp.series_medias.values())])
        eq_correl_med = all([np.array_equal(s1, s2)
                             for (s1, s2) in zip(self.correl_media.values(),
                                                 parp.correl_media.values())])
        eq_correl_a = all([np.array_equal(s1, s2)
                           for (s1, s2) in zip(self.correl_e_anual.values(),
                                               parp.correl_e_anual.values())])
        eq_correl_m = all([np.array_equal(s1, s2)
                           for (s1, s2) in zip(self.correl_e_mensal.values(),
                                               parp.correl_e_mensal.values())])
        return all([eq_ordens_o,
                    eq_ordens_f,
                    eq_coefs,
                    eq_series_e,
                    eq_correl_e,
                    eq_medias_e,
                    eq_correl_med,
                    eq_correl_a,
                    eq_correl_m])

    def series_energia_ree(self,
                           ree: int) -> Dict[int, np.ndarray]:
        """
        A tabela de séries de energia para todas as configurações
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`,
        excluindo a coluna dos anos.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [configuracao] e retorna um np.ndarray.
        """
        dict_series: Dict[int, np.ndarray] = {}
        n_configs = self.series_energia[ree].shape[2]
        for c in range(n_configs):
            dict_series[c + 1] = self.series_energia[ree][:, :, c][:, 1:]

        return dict_series

    def series_medias_ree(self,
                          ree: int) -> Dict[int, np.ndarray]:
        """
        A tabela de séries das médias anuais de energia para todos os anos
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [ano] e retorna um np.ndarray.
        """
        dict_series: Dict[int, np.ndarray] = {}
        n_anos = self.series_medias[ree].shape[2]
        anos = self.anos_estudo
        for c in range(n_anos):
            dict_series[anos[c]] = self.series_medias[ree][:, :, c]

        return dict_series

    def correlograma_energia_ree(self,
                                 ree: int) -> Dict[int,
                                                   np.ndarray]:
        """
        A tabela de autocorrelações parciais da série de energia
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`,
        excluindo a coluna dos meses.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [mes] e retorna um np.ndarray.
        """
        dict_correl: Dict[int, np.ndarray] = {}
        n_meses = self.correl_energia[ree].shape[0]
        for m in range(n_meses):
            dict_correl[m + 1] = self.correl_energia[ree][m, 1:]

        return dict_correl

    def correlograma_media_ree(self,
                               ree: int) -> Dict[int,
                                                 np.ndarray]:
        """
        A tabela de correlações cruzadas da série de médias anuais de
        energia com as séries de energia de uma determinada REE, no mesmo
        formato do arquivo `parp.dat`, excluindo a coluna dos meses.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [mes] e retorna um np.ndarray.
        """
        dict_correl: Dict[int, np.ndarray] = {}
        n_meses = self.correl_media[ree].shape[0]
        for m in range(n_meses):
            dict_correl[m + 1] = self.correl_media[ree][m, 1:]

        return dict_correl

    def ordens_originais_ree(self,
                             ree: int) -> Dict[int, np.ndarray]:
        """
        A tabela de ordens originais do modelo PAR ou PAR-A
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`,
        organizada por ano de estudo.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [ano] e retorna um np.ndarray.
        """
        anos = self.anos_estudo
        ordens = [self.ordens_orig[ree][i, 1:]
                  for i in range(self.ordens_orig[ree].shape[0])]
        return {a: o for a, o in zip(anos, ordens)}

    def ordens_finais_ree(self,
                          ree: int) -> Dict[int, np.ndarray]:
        """
        A tabela de ordens finais do modelo PAR ou PAR-A
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`,
        organizada por ano de estudo.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [ano] e retorna um np.ndarray.
        """
        anos = self.anos_estudo
        ordens = [self.ordens_finais[ree][i, 1:]
                  for i in range(self.ordens_finais[ree].shape[0])]
        return {a: o for a, o in zip(anos, ordens)}

    def coeficientes_ree(self,
                         ree: int) -> List[np.ndarray]:
        """
        Lista de coeficientes dos modelos PAR ou PAR-A.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `List[np.ndarray]`

        **Sobre**

        No caso de um modelo PAR-A de ordem p, a lista possui
        p + 1 coeficientes, e a última posição contém o
        coeficiente da componente anual.
        """
        # Extrai os coeficientes regressivos
        todos_coefs = self.coeficientes[ree][:, :, 0]
        coefs: List[List[float]] = []
        for i, c in enumerate(todos_coefs):
            coefs.append([])
            for co in c:
                if co == 0.:
                    break
                coefs[i].append(co)
        # Extrai os coeficientes da componente anual
        coefs_anual = self.coeficientes[ree][:, :, 2]
        for i, c in enumerate(coefs_anual):
            coefs[i].append(c[0])

        return [np.array(c) for c in coefs]

    @property
    def correlacoes_espaciais_anuais(self) -> Dict[int,
                                                   Dict[int,
                                                        Dict[int,
                                                             float]]]:
        """
        Correlações espaciais anuais para cada combinação de
        REEs em cada configuração do sistema, da mesma maneira
        encontrada no arquivo `parp.dat`.

        **Retorna**

        `Dict[int, Dict[int, Dict[int, float]]]`

        **Sobre**

        O acesso é feito com `[configuracao][ree1][ree2]`, onde `ree1`
        e `ree2` são inteiros de 1 ao número de REEs, indexados da mesma
        maneira do NEWAVE (1 = SUDESTE, 2 = SUL...).
        """
        corrs = self.correl_e_anual
        rees = range(1, len(REES) + 1)
        corrs_anuais: Dict[int, Dict[int, Dict[int, float]]] = {}
        for c in corrs.keys():
            if c not in corrs_anuais.keys():
                corrs_anuais[c] = {}
            for ree1 in rees:
                if ree1 not in corrs_anuais[c].keys():
                    corrs_anuais[c][ree1] = {}
                for ree2 in rees:
                    corrs_anuais[c][ree1][ree2] = corrs[c][ree1-1,
                                                           ree2-1]
        return corrs_anuais

    @property
    def correlacoes_espaciais_mensais(self) -> Dict[int,
                                                    Dict[int,
                                                         Dict[int,
                                                              np.ndarray]]]:
        """
        Correlações espaciais mensais para cada combinação de
        REEs em cada configuração do sistema, da mesma maneira
        encontrada no arquivo `parp.dat`.

        **Retorna**

        `Dict[int, Dict[int, Dict[int, np.ndarray]]]`

        **Sobre**

        O acesso é feito com `[configuracao][ree1][ree2]`, onde `ree1`
        e `ree2` são inteiros de 1 ao número de REEs, indexados da mesma
        maneira do NEWAVE (1 = SUDESTE, 2 = SUL...). É retornada a lista
        com as correlações para todos os meses, ordenadas por mês.
        """
        corrs = self.correl_e_mensal
        rees = range(1, len(REES) + 1)
        corrs_mensais: Dict[int, Dict[int, Dict[int, np.ndarray]]] = {}
        for c in corrs.keys():
            if c not in corrs_mensais.keys():
                corrs_mensais[c] = {}
            for ree1 in rees:
                if ree1 not in corrs_mensais[c].keys():
                    corrs_mensais[c][ree1] = {}
                for ree2 in rees:
                    corrs_mensais[c][ree1][ree2] = corrs[c][ree1-1,
                                                            :,
                                                            ree2-1]
        return corrs_mensais

    @property
    def anos_historico(self) -> List[int]:
        """
        A lista de anos do histórico associados às séries de
        energia.

        **Retorna**

        `List[int]`
        """
        a = np.array(self.series_energia[1][:, :, 0][:, 0],
                     dtype=np.int64)
        return list(a)

    @property
    def anos_estudo(self) -> List[int]:
        """
        A lista de anos do estudo associados às tabelas de
        coeficientes e ordens dos modelos.

        **Retorna**

        `List[int]`
        """
        a = np.array(self.ordens_finais[1][:, 0], dtype=np.int64)
        return list(a)
