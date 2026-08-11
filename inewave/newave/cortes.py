from cfinterface.files.sectionfile import SectionFile
from cfinterface.storage import StorageType
from inewave.newave.modelos.cortes import SecaoDadosCortes
from inewave.newave.cortesh import Cortesh

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from typing import TypeVar, Optional, Union, List, Any


class Cortes(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes aos
    cortes de Benders.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosCortes]
    STORAGE = StorageType.BINARY

    @classmethod
    def read(
        cls,
        content: Union[str, bytes],
        tamanho_registro: int = 1664,
        indice_ultimo_corte: int = 0,
        numero_total_cortes: int = 10000,
        codigos_rees: List[int] = [],
        codigos_uhes: List[int] = [],
        codigos_submercados: List[int] = [],
        ordem_maxima_parp: int = 12,
        numero_patamares: int = 3,
        lag_maximo_gnl: int = 2,
        por_estagio: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> "Cortes":
        """
        Lê um arquivo de cortes de Benders.

        Para o arquivo consolidado (`cortes.dat`) informe o índice GLOBAL do
        estágio (`cortesh.ultimo_registro_cortes_estagio`) em
        ``indice_ultimo_corte``. Para uma partição por estágio
        (`cortes-<estagio>.dat`) passe ``por_estagio=True`` — os índices locais
        e o número de cortes são derivados do próprio arquivo, ignorando o
        índice global do cabeçalho.

        Considere usar :meth:`from_cortesh`, que deriva automaticamente as
        dimensões (códigos de UHEs, ordem do PAR(p), patamares, lag GNL) a
        partir de um :class:`Cortesh`.
        """
        return super().read(  # type: ignore[return-value]
            content,
            tamanho_registro=tamanho_registro,
            indice_ultimo_corte=indice_ultimo_corte,
            numero_total_cortes=numero_total_cortes,
            codigos_rees=codigos_rees,
            codigos_uhes=codigos_uhes,
            codigos_submercados=codigos_submercados,
            ordem_maxima_parp=ordem_maxima_parp,
            numero_patamares_carga=numero_patamares,
            lag_maximo_gnl=lag_maximo_gnl,
            por_estagio=por_estagio,
            *args,
            **kwargs,
        )

    @classmethod
    def from_cortesh(
        cls,
        content: Union[str, bytes],
        cortesh: Cortesh,
        indice_ultimo_corte: int = 0,
        numero_total_cortes: int = 10000,
        por_estagio: bool = False,
    ) -> "Cortes":
        """
        Lê um arquivo de cortes INDIVIDUALIZADO derivando todas as dimensões
        de um :class:`Cortesh`:

        - ``codigos_uhes`` na ordem de ``cortesh.dados_uhes`` (por
          ``indice_usina``), considerando APENAS as UHEs não-fictícias
          (``ficticia == 0``): o registro individualizado carrega apenas essas,
          de forma que ``n_coef == 2 + G + U*(2+P)`` com ``U`` = número de UHEs
          não-fictícias. Contar as fictícias produziria um ``ValueError`` de
          layout inconsistente;
        - ``ordem_maxima_parp`` a partir das ordens do PAR(p) do cabeçalho;
        - ``numero_patamares`` e ``lag_maximo_gnl`` do cabeçalho;
        - ``tamanho_registro`` = ``cortesh.tamanho_registro_individualizado``.

        Para uma partição passe ``por_estagio=True`` (índices locais derivados
        do arquivo). Para o consolidado informe ``indice_ultimo_corte`` global
        (`cortesh.ultimo_registro_cortes_estagio`).

        Estágios agregados em REE ainda não são cobertos por este atalho — use
        :meth:`read` diretamente informando ``codigos_rees``.
        """
        submercados = list(range(1, cortesh.numero_submercados + 1))
        ordem_maxima_parp = cortesh.ordem_maxima_parp()
        dados_uhes = cortesh.dados_uhes
        codigos_uhes = dados_uhes.loc[
            dados_uhes["ficticia"] == 0, "codigo_usina"
        ].tolist()
        return cls.read(
            content,
            tamanho_registro=cortesh.tamanho_registro_individualizado,
            indice_ultimo_corte=indice_ultimo_corte,
            numero_total_cortes=numero_total_cortes,
            codigos_rees=[],
            codigos_uhes=codigos_uhes,
            codigos_submercados=submercados,
            ordem_maxima_parp=ordem_maxima_parp,
            numero_patamares=cortesh.numero_patamares,
            lag_maximo_gnl=cortesh.lag_maximo_gnl,
            por_estagio=por_estagio,
        )

    @property
    def cortes(self) -> Optional[pd.DataFrame]:
        """
        Retorna o conjunto dos cortes de Benders construídos
        durante o cálculo da política.

        - indice_corte (`int`)
        - iteracao_construcao (`str`)
        - indice_forward (`int`)
        - iteracao_inativacao (`int`)
        - rhs (`float`)

        Se o estágio em questão for agregado em REE:

        - pi_earm_ree1 (`float`)
        - pi_ena_ree1_lag1 (`float`)
        - ...
        - pi_ena_ree1_lagN (`float`)
        - pi_earm_ree2 (`float`)
        - ...
        - pi_ena_reeR_lagN (`float`)
        - ... (pi_gnl, veja abaixo) ...
        - pi_mx_sar_ree1 (`float`)
        - ...
        - pi_mx_sar_reeR (`float`)

        Se o estágio em questão for individualizado:

        - pi_varm_uhe1 (`float`)
        - pi_qafl_uhe1_lag1 (`float`)
        - ...
        - pi_qafl_uhe1_lagN (`float`)
        - pi_varm_uhe2 (`float`)
        - ...
        - pi_qafl_uheU_lagN (`float`)
        - ... (pi_gnl, veja abaixo) ...
        - pi_mx_sar_uhe1 (`float`)
        - ...
        - pi_mx_sar_uheU (`float`)

        Para todos os estágios:

        - pi_gnl_sbm1_pat1_lag1 (`float`)
        - ...
        - pi_gnl_sbm1_pat1_lagL (`float`)
        - pi_gnl_sbm1_pat2_lag1 (`float`)
        - ...
        - pi_gnl_sbm1_patP_lagL (`float`)
        - pi_gnl_sbm2_pat1_lag1 (`float`)
        - ...
        - pi_gnl_sbmS_patP_lagL (`float`)

        Os coeficientes ``pi_mx_sar_*`` (multiplicadores da restrição de aversão
        a risco / SAR) formam sempre o último bloco do registro — por UHE no caso
        individualizado, por REE no agregado. Em alguns casos híbridos o registro
        pode conter coeficientes extras entre ``pi_qafl`` e ``pi_mx_sar`` que o
        NEWAVE não expõe no `nwlistcf.rel`; esses são descartados sem
        desalinhar os blocos nomeados (veja o CHANGELOG da versão 1.15.1).

        R é o número de REEs.

        U é o número de UHEs.

        S é o número de submercados.

        N é a máxima ordem do modelo PAR(p) ajustado.

        P é o número de patamares de carga.

        L é o lag máximo de despacho GNL antecipado.

        :return: Os coeficientes dos cortes em uma tabela.
        :rtype: pd.DataFrame | None
        """
        dados = [r for r in self.data.of_type(SecaoDadosCortes)]
        if len(dados) == 1:
            return dados[0].data
        else:
            return None
