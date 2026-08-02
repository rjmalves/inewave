from cfinterface.files.sectionfile import SectionFile
from cfinterface.storage import StorageType
from inewave.newave.modelos.cortese import SecaoDadosCortese
from inewave.newave.cortesh import Cortesh

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from typing import TypeVar, Optional, Union, List, Any


class Cortese(SectionFile):
    """
    Armazena os estados visitados que geraram os cortes de Benders da FCF,
    presentes nos arquivos `cortese.dat` (consolidado, todos os estágios) e
    `cortese-<estagio>.dat` (particionado por estágio). É o par binário do
    relatório textual `estados.rel`.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosCortese]
    STORAGE = StorageType.BINARY

    @classmethod
    def read(
        cls,
        content: Union[str, bytes],
        tamanho_estado: int = 0,
        numero_rees: int = 0,
        codigos_uhes: List[int] = [],
        numero_total_submercados: int = 0,
        numero_patamares: int = 3,
        lag_maximo_gnl: int = 0,
        estados_termicos_gnl: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> "Cortese":
        """
        Lê um arquivo de estados dos cortes.

        Tanto o consolidado (`cortese.dat`) quanto uma partição
        (`cortese-<estagio>.dat`) são lidos por completo (todos os registros do
        arquivo); a partição não possui registro sentinela. Considere usar
        :meth:`from_cortesh`, que deriva as dimensões de um :class:`Cortesh`.
        """
        return super().read(  # type: ignore[return-value]
            content,
            tamanho_estado=tamanho_estado,
            numero_rees=numero_rees,
            codigos_uhes=codigos_uhes,
            numero_total_submercados=numero_total_submercados,
            numero_patamares=numero_patamares,
            lag_maximo_gnl=lag_maximo_gnl,
            estados_termicos_gnl=estados_termicos_gnl,
            *args,
            **kwargs,
        )

    @classmethod
    def from_cortesh(
        cls,
        content: Union[str, bytes],
        cortesh: Cortesh,
    ) -> "Cortese":
        """
        Lê um arquivo de estados derivando as dimensões de um
        :class:`Cortesh` (número de REEs, ordem das UHEs de
        ``cortesh.dados_uhes``, submercados totais, patamares e lag GNL).
        """
        return cls.read(
            content,
            tamanho_estado=cortesh.tamanho_estado,
            numero_rees=cortesh.numero_rees,
            codigos_uhes=cortesh.dados_uhes["codigo_usina"].tolist(),
            numero_total_submercados=cortesh.numero_total_submercados,
            numero_patamares=cortesh.numero_patamares,
            lag_maximo_gnl=cortesh.lag_maximo_gnl,
        )

    @property
    def estados(self) -> Optional[pd.DataFrame]:
        """
        Retorna os estados visitados que geraram os cortes.

        - iteracao_construcao (`int`)
        - indice_forward (`int`)
        - iteracao_desativacao (`int`)
        - funcao_objetivo (`float`)
        - earm_ree1 ... earm_reeR (`float`)
        - varm_uhe1 ... varm_uheU (`float`)
        - sgt_sbm1_pat1_est1 ... (`float`, quando há despacho GNL antecipado)
        - reservado_0 ... (`float`, estados de máxima violação e preenchimento)

        :return: Os estados em uma tabela.
        :rtype: pd.DataFrame | None
        """
        dados = [r for r in self.data.of_type(SecaoDadosCortese)]
        if len(dados) == 1:
            return dados[0].data
        else:
            return None
