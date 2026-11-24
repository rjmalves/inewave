from inewave.newave.modelos.newavetim import (
    BlocoBibliotecaPLTim,
    BlocoCasoTim,
    BlocoDataHoraTim,
    BlocoInicioPoliticaTim,
    BlocoIteracoesMinMaxTim,
    BlocoNumeroProcessosTim,
    BlocoTemposEtapasTim,
    BlocoTemposIteracoesTim,
    BlocoTipoExecucaoTim,
    BlocoVersaoModeloTim,
)

from cfinterface.files.blockfile import BlockFile
from datetime import datetime
from typing import TypeVar, Optional
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package


class Newavetim(BlockFile):
    """
    Armazena os dados de saída do NEWAVE referentes aos
    tempos de execução do programa.

    """

    T = TypeVar("T")

    BLOCKS = [
        BlocoVersaoModeloTim,
        BlocoBibliotecaPLTim,
        BlocoCasoTim,
        BlocoDataHoraTim,
        BlocoInicioPoliticaTim,
        BlocoNumeroProcessosTim,
        BlocoTipoExecucaoTim,
        BlocoIteracoesMinMaxTim,
        BlocoTemposEtapasTim,
        BlocoTemposIteracoesTim,
    ]

    @property
    def tempos_etapas(self) -> Optional[pd.DataFrame]:
        """
        Tempos de execução do modelo por etapa do modelo.

        - etapa (`str`)
        - tempo (`timedelta`)

        :return: Os tempos em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoTemposEtapasTim)
        if isinstance(b, BlocoTemposEtapasTim):
            return b.data
        return None

    @property
    def tempos_iteracoes(self) -> Optional[pd.DataFrame]:
        """
        Tempos de cada iteração do cálculo da política.

        - iteracao (`int`)
        - backward (`timedelta`)
        - forward (`timedelta`)
        - total (`timedelta`)

        Os tempos são os escritos pelo NEWAVE, sem correção. Na primeira
        iteração, o NEWAVE às vezes escreve no backward e no forward tempos
        sem sentido, de centenas de horas.

        :return: Os tempos em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoTemposIteracoesTim)
        if isinstance(b, BlocoTemposIteracoesTim):
            return b.data
        return None

    @property
    def versao_modelo(self) -> Optional[str]:
        """
        A versão do modelo utilizada para executar o caso.

        :return: A versão do modelo
        :rtype: str | None
        """
        b = self.data.get_blocks_of_type(BlocoVersaoModeloTim)
        if isinstance(b, BlocoVersaoModeloTim):
            return b.data
        return None

    @property
    def biblioteca_pl(self) -> Optional[str]:
        """
        O texto da biblioteca de PLs utilizada para executar o caso,
        como escrito no arquivo, sem normalização.

        :return: O texto da biblioteca, ou `None` se o arquivo não a
            informa
        :rtype: str | None
        """
        b = self.data.get_blocks_of_type(BlocoBibliotecaPLTim)
        if isinstance(b, BlocoBibliotecaPLTim):
            return b.data
        v = self.data.get_blocks_of_type(BlocoVersaoModeloTim)
        if isinstance(v, BlocoVersaoModeloTim):
            return v.biblioteca_pl
        return None

    @property
    def caso(self) -> Optional[str]:
        """
        O nome do caso, como escrito no arquivo.

        :return: O nome do caso, ou `None` se o arquivo não o informa
        :rtype: str | None
        """
        b = self.data.get_blocks_of_type(BlocoCasoTim)
        if isinstance(b, BlocoCasoTim):
            return b.data
        return None

    @property
    def data_hora_inicio(self) -> Optional[datetime]:
        """
        A data e hora do início da execução, como escritas no arquivo.
        O `datetime` é ingênuo (sem fuso horário), no fuso em que
        o arquivo foi escrito.

        :return: A data e hora, ou `None` se o arquivo não as informa
        :rtype: datetime | None
        """
        for b in self.data.of_type(BlocoDataHoraTim):
            if not isinstance(b.previous, BlocoInicioPoliticaTim):
                return b.data
        return None

    @property
    def data_hora_inicio_politica(self) -> Optional[datetime]:
        """
        A data e hora do início do processo iterativo do cálculo da
        política, como escritas no arquivo. O `datetime` é ingênuo
        (sem fuso horário), no fuso em que o arquivo foi escrito.
        Somente algumas versões do NEWAVE escrevem essa linha.

        :return: A data e hora, ou `None` se o arquivo não as informa
        :rtype: datetime | None
        """
        for b in self.data.of_type(BlocoDataHoraTim):
            if isinstance(b.previous, BlocoInicioPoliticaTim):
                return b.data
        return None

    @property
    def numero_processos(self) -> Optional[int]:
        """
        O número de processos com que o NEWAVE foi executado, como
        escrito no arquivo.

        :return: O número de processos, ou `None` se o arquivo não o
            informa
        :rtype: int | None
        """
        b = self.data.get_blocks_of_type(BlocoNumeroProcessosTim)
        if isinstance(b, BlocoNumeroProcessosTim):
            return b.data[0]
        return None

    @property
    def numero_nos(self) -> Optional[int]:
        """
        O número de nós de processamento com que o NEWAVE foi
        executado, como escrito no arquivo.

        :return: O número de nós, ou `None` se o arquivo não o informa
        :rtype: int | None
        """
        b = self.data.get_blocks_of_type(BlocoNumeroProcessosTim)
        if isinstance(b, BlocoNumeroProcessosTim):
            return b.data[1]
        return None

    @property
    def tipo_execucao(self) -> Optional[str]:
        """
        O tipo de execução do NEWAVE, como escrito no arquivo.

        :return: O tipo de execução, ou `None` se o arquivo não o
            informa
        :rtype: str | None
        """
        b = self.data.get_blocks_of_type(BlocoTipoExecucaoTim)
        if isinstance(b, BlocoTipoExecucaoTim):
            return b.data
        return None

    @property
    def iteracoes_minimo(self) -> Optional[int]:
        """
        O número mínimo de iterações da política, como escrito no
        arquivo.

        :return: O número mínimo de iterações, ou `None` se o arquivo
            não o informa
        :rtype: int | None
        """
        b = self.data.get_blocks_of_type(BlocoIteracoesMinMaxTim)
        if isinstance(b, BlocoIteracoesMinMaxTim):
            return b.data[0]
        return None

    @property
    def iteracoes_maximo(self) -> Optional[int]:
        """
        O número máximo de iterações da política, como escrito no
        arquivo.

        :return: O número máximo de iterações, ou `None` se o arquivo
            não o informa
        :rtype: int | None
        """
        b = self.data.get_blocks_of_type(BlocoIteracoesMinMaxTim)
        if isinstance(b, BlocoIteracoesMinMaxTim):
            return b.data[1]
        return None
