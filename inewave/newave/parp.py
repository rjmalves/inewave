from typing import List, Type
import numpy as np  # type: ignore

from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.bloco import Bloco
from inewave.newave.modelos.parp import BlocoSerieEnergiaREE
from inewave.newave.modelos.parp import BlocoCorrelParcialREE
from inewave.newave.modelos.parp import BlocoOrdensFinaisCoefsREE
from inewave.newave.modelos.parp import BlocoOrdensOriginaisREE
from inewave.newave.modelos.parp import BlocoSerieMediaREE
from inewave.newave.modelos.parp import BlocoCorrelCruzMediaREE
from inewave.newave.modelos.parp import BlocoCorrelEspAnual
from inewave.newave.modelos.parp import BlocoCorrelEspMensal
from inewave.newave.modelos.parp import LeituraPARp


class PARp(Arquivo):
    """
    Armazena os dados de saída do NEWAVE referentes aos modelos e às
    séries sintéticas de energia geradas pelo PAR(p) e PAR(p)-A.


    Esta classe lida com informações de saída do NEWAVE e
    cujas saídas devem ser compatíveis com as observadas através
    do NWLISTOP.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

        self.__series_energia = self.__por_tipo(BlocoSerieEnergiaREE)
        self.__correl_parcial = self.__por_tipo(BlocoCorrelParcialREE)
        self.__ordens_finais_coefs = self.__por_tipo(BlocoOrdensFinaisCoefsREE)
        self.__ordens_orig = self.__por_tipo(BlocoOrdensOriginaisREE)
        self.__series_medias = self.__por_tipo(BlocoSerieMediaREE)
        self.__correl_cruz = self.__por_tipo(BlocoCorrelCruzMediaREE)
        self.__correl_esp_anual = self.__por_tipo(BlocoCorrelEspAnual)
        self.__correl_esp_mensal = self.__por_tipo(BlocoCorrelEspMensal)

    def __por_tipo(self, tipo: Type[Bloco]) -> List[Bloco]:
        return [b for b in self._blocos if isinstance(b, tipo)]

    def series_energia_ree(self,
                           ree: int,
                           configuracao: int) -> np.ndarray:
        """
        A tabela de séries de energia para todas as configurações
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`,
        excluindo a coluna dos anos.

        **Parâmetros**

        - ree: `int`
        - configuracao: `int`

        **Retorna**

        `np.ndarray`

        **Sobre**

        O acesso é feito com [ano, mes].
        """
        return self.__series_energia[ree - 1].dados[:,
                                                    1:,
                                                    configuracao]

    def series_medias_ree(self,
                          ree: int,
                          ano: int) -> np.ndarray:
        """
        A tabela de séries das médias anuais de energia para todos os anos
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `np.ndarray`

        **Sobre**

        O acesso é feito com [ano] e retorna um np.ndarray.
        """
        return self.__series_medias[ree - 1].dados[:, :, ano]

    def correlograma_energia_ree(self,
                                 ree: int) -> np.ndarray:
        """
        A tabela de autocorrelações parciais da série de energia
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`,
        excluindo a coluna dos meses.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `np.ndarray`

        **Sobre**

        O acesso é feito com [mes, lag].
        """
        return self.__correl_parcial[ree - 1].dados[:, 1:]

    def correlograma_media_ree(self,
                               ree: int) -> np.ndarray:
        """
        A tabela de correlações cruzadas da série de médias anuais de
        energia com as séries de energia de uma determinada REE, no mesmo
        formato do arquivo `parp.dat`, excluindo a coluna dos meses.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `np.ndarray`

        **Sobre**

        O acesso é feito com [mes, lag].
        """
        return self.__correl_cruz[ree - 1].dados[:, 1:]

    def ordens_originais_ree(self,
                             ree: int) -> np.ndarray:
        """
        A tabela de ordens originais do modelo PAR ou PAR-A
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`,
        organizada por ano de estudo.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `np.ndarray`

        **Sobre**

        O acesso é feito com [ano, mes].
        """
        return self.__ordens_orig[ree - 1].dados[:, 1:]

    def ordens_finais_ree(self,
                          ree: int) -> np.ndarray:
        """
        A tabela de ordens finais do modelo PAR ou PAR-A
        de uma determinada REE, no mesmo formato do arquivo `parp.dat`,
        organizada por ano de estudo.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `np.ndarray`

        **Sobre**

        O acesso é feito com [ano, mes].
        """
        return self.__ordens_finais_coefs[ree - 1].dados[0][:, 1:]

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
        todos_coefs = self.__ordens_finais_coefs[ree - 1].dados[1]
        coefs: List[np.ndarray] = []
        meses, _, _ = todos_coefs.shape
        for m in range(meses):
            coefs_parp_ano = todos_coefs[m, :, 0]
            nao_nulos = coefs_parp_ano[coefs_parp_ano != 0]
            coef_parpa_ano = todos_coefs[m, 0, 2]
            if coef_parpa_ano != 0:
                c = np.concatenate([nao_nulos,
                                    np.array([coef_parpa_ano])])
            else:
                c = nao_nulos
            coefs.append(c)

        return coefs

    def coeficientes_desvio_ree(self,
                                ree: int) -> List[np.ndarray]:
        """
        Lista dos coeficientes dos modelos PAR ou PAR-A, multiplicados
        pelos respectivos desvios-padrão de cada mês.

        **Parâmetros**

        - ree: `int`

        **Retorna**

        `List[np.ndarray]`

        **Sobre**

        No caso de um modelo PAR-A de ordem p, a lista possui
        p + 1 coeficientes, e a última posição contém o coeficiente
        da componente anual.
        """
        todos_coefs = self.__ordens_finais_coefs[ree - 1].dados[1]
        coefs: List[np.ndarray] = []
        meses, _, _ = todos_coefs.shape
        for m in range(meses):
            coefs_parp_ano = todos_coefs[m, :, 1]
            nao_nulos = coefs_parp_ano[coefs_parp_ano != 0]
            coef_parpa_ano = todos_coefs[m, 0, 3]
            if coef_parpa_ano != 0:
                c = np.concatenate([nao_nulos,
                                    np.array([coef_parpa_ano])])
            else:
                c = nao_nulos
            coefs.append(c)

        return coefs

    def correlacoes_espaciais_anuais(self, configuracao: int) -> np.ndarray:
        """
        Correlações espaciais anuais para cada combinação de
        REEs em cada configuração do sistema, de maneira ligeiramente
        diferente da encontrada no NEWAVE (ver Sobre abaixo).

        **Parâmetros**

        - configuracao: `int`

        **Retorna**

        `np.ndarray`

        **Sobre**

        O acesso é feito com `[ree1, ree2]`, onde `ree1`
        e `ree2` são inteiros de 0 ao número de REEs - 1, indexados da mesma
        maneira do NEWAVE (0 = SUDESTE, 1 = SUL...).
        """
        return self.__correl_esp_anual[configuracao - 1].dados

    def correlacoes_espaciais_mensais(self,
                                      configuracao: int,
                                      mes: int) -> np.ndarray:
        """
        Correlações espaciais mensais para cada combinação de
        REEs em cada configuração do sistema, da mesma maneira
        encontrada no arquivo `parp.dat`.

        **Parâmetros**

        - mes: `int`

        **Retorna**

        `np.ndarray`

        **Sobre**

        O acesso é feito com `[mes][ree1][ree2]`, onde `ree1`
        e `ree2` são inteiros de 0 ao número de REEs, indexados da mesma
        maneira do NEWAVE (0 = SUDESTE, 1 = SUL...).
        """
        return self.__correl_esp_mensal[configuracao - 1].dados[:, mes, :]

    @property
    def anos_historico(self) -> np.ndarray:
        """
        A lista de anos do histórico associados às séries de
        energia.

        **Retorna**

        `np.ndarray`
        """
        return self.__series_energia[0].dados[:, 0, 0]

    @property
    def anos_estudo(self) -> np.ndarray:
        """
        A lista de anos do estudo associados às tabelas de
        coeficientes e ordens dos modelos.

        **Retorna**

        `np.ndarray`
        """
        return self.__ordens_finais_coefs[0].dados[0][:, 0]

    @anos_estudo.setter
    def anos_estudo(self, anos: np.ndarray):
        self.__ordens_finais_coefs[0].dados[0][:, 0] = anos

    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="parp.dat") -> 'PARp':
        leitor = LeituraPARp(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)
