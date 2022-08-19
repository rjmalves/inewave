from inewave.newave.modelos.parpeol import BlocoSerieVentosUEE
from inewave.newave.modelos.parpeol import BlocoCorrelVentosUEE
from inewave.newave.modelos.parpeol import BlocoSerieRuidosUEE
from inewave.newave.modelos.parpeol import BlocoCorrelRuidosUEE
from inewave.newave.modelos.parpeol import BlocoCorrelEspacialAnualConfig
from inewave.newave.modelos.parpeol import BlocoCorrelEspacialMensalConfig

from cfinterface.components.block import Block
from cfinterface.files.blockfile import BlockFile
from typing import Type, TypeVar, Optional, Any, List
import pandas as pd  # type: ignore


class PARpeol(BlockFile):
    """
    Armazena os dados de saída do NEWAVE referentes às
    séries sintéticas de ventos geradas pelo PAR(p).

    Esta classe lida com informações de saída do NEWAVE e
    cujas saídas devem ser compatíveis com as observadas através
    do NWLISTOP.

    """

    T = TypeVar("T")

    BLOCKS = [
        BlocoSerieVentosUEE,
        BlocoCorrelVentosUEE,
        BlocoSerieRuidosUEE,
        BlocoCorrelRuidosUEE,
        BlocoCorrelEspacialAnualConfig,
        BlocoCorrelEspacialMensalConfig,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__series_ventos = None
        self.__correl_series_ventos = None
        self.__series_ruido = None
        self.__correl_series_ruido = None
        self.__correl_espacial_anual = None
        self.__correl_espacial_mensal = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="parpeol.dat"
    ) -> "PARpeol":
        return cls.read(diretorio, nome_arquivo)

    def __uees(self) -> Optional[List[str]]:
        """
        Retorna a lista das UEEs lidos do arquivo.

        :return: Os nomes das UEEs
        :rtype: List[str]
        """
        if self.series_ventos_uee is None:
            return None
        else:
            return self.series_ventos_uee["UEE"].unique().tolist()

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    def __concatena_dados(self, bloco: Type[Block]) -> Optional[Any]:
        """
        Obtém os dados de um bloco se este existir dentre os blocos do arquivo.

        :param bloco: O tipo do bloco cujos dados serão extraídos
        :type bloco: Type[T]
        :param indice: Qual dos blocos do tipo será acessado
        :type indice: int, optional
        :return: Os dados do bloco, se existirem
        :rtype: Any
        """
        dados = pd.DataFrame()
        for b in self.data.of_type(bloco):
            if dados.empty:
                dados = b.data
            else:
                dados = pd.concat([dados, b.data], ignore_index=True)
        if not dados.empty:
            return dados
        else:
            return None

    def __adiciona_coluna_uee(
        self, df: Optional[pd.DataFrame]
    ) -> Optional[pd.DataFrame]:
        """
        Adiciona uma coluna com as UEEs de cada amostra, assumindo
        a mesma ordem das séries de ventos.

        :param df: O DataFrame que irá receber as UEEs
        :type df: pd.DataFrame
        :return: O DataFrame com as UEEs
        :rtype: pd.DataFrame
        """
        if df is None:
            return None
        uees = self.__uees()
        if uees is None:
            return None
        linhas_por_uee = df.shape[0] / len(uees)
        if int(linhas_por_uee) != linhas_por_uee:
            raise ValueError(
                f"{df.shape[0]} linhas não podem ser "
                + f"divididas em {len(uees)} grupos"
            )
        cols = list(df.columns)
        col_uee: List[str] = []
        for uee in uees:
            col_uee += [uee] * int(linhas_por_uee)
        df["UEE"] = col_uee
        return df[["UEE"] + cols]

    def __adiciona_coluna_uee_com_estagios(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Adiciona uma coluna com as UEEs de cada amostra e outra
        com o estágio de cada uma, assumindo
        a mesma ordem das séries de ventos.

        :param df: O DataFrame que irá receber as UEEs
        :type df: pd.DataFrame
        :return: O DataFrame com as UEEs
        :rtype: pd.DataFrame
        """
        uees = self.__uees()
        if uees is None:
            return None
        linhas_por_uee = df.shape[0] / len(uees)
        if int(linhas_por_uee) != linhas_por_uee:
            raise ValueError(
                f"{df.shape[0]} linhas não podem ser "
                + f"divididas em {len(uees)} grupos"
            )
        cols = list(df.columns)
        col_uee: List[str] = []
        col_estagio: List[int] = []
        for uee in uees:
            col_uee += [uee] * int(linhas_por_uee)
            col_estagio += list(range(1, int(linhas_por_uee) + 1))
        df["UEE"] = col_uee
        df["Estágio"] = col_estagio
        return df[["UEE", "Estágio"] + cols]

    def __adiciona_coluna_uee_corrigindo_pre_pos(
        self, df: Optional[pd.DataFrame]
    ) -> Optional[pd.DataFrame]:
        """
        Adiciona uma coluna com as UEEs de cada amostra e outra
        com o estágio de cada uma, assumindo
        a mesma ordem das séries de ventos, e corrigindo os valores
        dos anos se houve períodos PRE e POS.

        :param df: O DataFrame que irá receber as UEEs
        :type df: pd.DataFrame
        :return: O DataFrame com as UEEs
        :rtype: pd.DataFrame
        """

        def converte_vetor_anos(anos: List[str], n: int) -> List[int]:
            # Descobre os anos pré e pós estudo
            numero_anos_pre = len([p for p in anos if p == "PRE"]) // n
            numero_anos_pos = len([p for p in anos if p == "POS"]) // n
            anos_estudo = [int(p) for p in anos if p not in ["PRE", "POS"]]
            # Descobre o primeiro ano de estudo
            primeiro_ano_estudo = sorted(anos_estudo)[0]
            # Descobre o último ano de estudo
            ultimo_ano_estudo = sorted(anos_estudo)[-1]
            # Substitui os anos pré e pós pelos valores específicos
            indice_inicio_pos = anos.index("POS") if "POS" in anos else -1
            for a in range(numero_anos_pre):
                idx_i = n * a
                idx_f = idx_i + n
                ano = primeiro_ano_estudo - (numero_anos_pre - a)
                anos[idx_i:idx_f] = [str(ano)] * n
            for a in range(numero_anos_pos):
                idx_i = indice_inicio_pos + n * a
                idx_f = idx_i + n
                ano = ultimo_ano_estudo + a + 1
                anos[idx_i:idx_f] = [str(ano)] * n
            return [int(a) for a in anos]

        if df is None:
            return None
        uees = self.__uees()
        if uees is None:
            return None
        linhas_por_uee = df.shape[0] / len(uees)
        if int(linhas_por_uee) != linhas_por_uee:
            raise ValueError(
                f"{df.shape[0]} linhas não podem ser "
                + f"divididas em {len(uees)} grupos"
            )
        cols = list(df.columns)
        col_uee: List[str] = []
        for uee in uees:
            col_uee += [uee] * int(linhas_por_uee)
        df["UEE"] = col_uee
        uee0 = uees[0]
        ano0 = df["Ano"].unique().tolist()[0]
        filtro = (df["Ano"] == ano0) & (df["UEE"] == uee0)
        n_series = df.loc[filtro].shape[0]
        for i, uee in enumerate(uees):
            i_i = i * int(linhas_por_uee)
            i_f = i_i + int(linhas_por_uee) - 1
            df.loc[i_i:i_f, "Ano"] = converte_vetor_anos(
                df.loc[i_i:i_f, "Ano"].tolist(), n_series
            )
        return df[["UEE"] + cols]

    @property
    def series_ventos_uee(self) -> Optional[pd.DataFrame]:
        """
        A tabela de séries de ventos para todas as configurações
        e UEEs, no mesmo formato do arquivo `parpeol.dat`.

        - UEE (`str`)
        - Configuração (`int`)
        - Ano (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        if self.__series_ventos is None:
            self.__series_ventos = self.__concatena_dados(BlocoSerieVentosUEE)
        return self.__series_ventos

    @property
    def series_ruido_uee(self) -> Optional[pd.DataFrame]:
        """
        A tabela de séries de ruído para todos os UEEs,
        no mesmo formato do arquivo `parpeol.dat`.

        - UEE (`str`)
        - Ano (`int`)
        - Série (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        if self.__series_ruido is None:
            self.__series_ruido = self.__concatena_dados(BlocoSerieRuidosUEE)
            self.__series_ruido = (
                self.__adiciona_coluna_uee_corrigindo_pre_pos(
                    self.__series_ruido
                )
            )
        return self.__series_ruido

    @property
    def correlacao_series_ventos_uee(self) -> Optional[pd.DataFrame]:
        """
        A tabela de correlação das séries de ventos para
        todas as configurações vigentes e UEEs,
        no mesmo formato do arquivo `parpeol.dat`.

        - UEE (`str`)
        - Data (`date`)
        - Lag 1 (`float`)
        - Lag 2 (`float`)
        - ...
        - Lag 11 (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        if self.__correl_series_ventos is None:
            self.__correl_series_ventos = self.__concatena_dados(
                BlocoCorrelVentosUEE
            )
            self.__correl_series_ventos = self.__adiciona_coluna_uee(
                self.__correl_series_ventos
            )
        return self.__correl_series_ventos

    @property
    def correlacao_series_ruidos_uee(self) -> Optional[pd.DataFrame]:
        """
        A tabela de correlação das séries de ruídos para
        todas as configurações vigentes e UEEs,
        no mesmo formato do arquivo `parpeol.dat`.

        - UEE (`str`)
        - Data (`date`)
        - Lag 1 (`float`)
        - Lag 2 (`float`)
        - ...
        - Lag 11 (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        if self.__correl_series_ruido is None:
            self.__correl_series_ruido = self.__concatena_dados(
                BlocoCorrelRuidosUEE
            )
            self.__correl_series_ruido = self.__adiciona_coluna_uee(
                self.__correl_series_ruido
            )
        return self.__correl_series_ruido

    @property
    def correlacao_espacial_anual(self) -> Optional[pd.DataFrame]:
        """
        A tabela de correlação para todas as configurações
        e REEs / UEEs, no mesmo formato do arquivo `parpeol.dat`.

        - Configuração (`int`)
        - UEE (`str`)
        - <Nome do REE 1> (`str`)
        - <Nome do REE 2> (`str`)
        - ...
        - <Nome do REE N> (`str`)
        - <Nome da UEE 1> (`str`)
        - ...
        - <Nome da UEE M> (`str`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        if self.__correl_espacial_anual is None:
            self.__correl_espacial_anual = self.__concatena_dados(
                BlocoCorrelEspacialAnualConfig
            )
        return self.__correl_espacial_anual

    @property
    def correlacao_espacial_mensal(self) -> Optional[pd.DataFrame]:
        """
        A tabela de correlação para todas as configurações
        e REEs / UEEs, no mesmo formato do arquivo `parpeol.dat`.

        - Configuração (`int`)
        - REE (`str`)
        - MES (`int`)
        - <Nome do REE 1> (`str`)
        - <Nome do REE 2> (`str`)
        - ...
        - <Nome do REE N> (`str`)
        - <Nome da UEE 1> (`str`)
        - ...
        - <Nome da UEE M> (`str`)

        :return: A tabela como um DataFrame.
        :rtype: Optional[pd.DataFrame]
        """
        if self.__correl_espacial_mensal is None:
            self.__correl_espacial_mensal = self.__concatena_dados(
                BlocoCorrelEspacialMensalConfig
            )
        return self.__correl_espacial_mensal
