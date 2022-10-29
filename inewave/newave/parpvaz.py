from inewave.newave.modelos.parpvaz import BlocoSerieVazoesUHE
from inewave.newave.modelos.parpvaz import BlocoCorrelVazoesUHE
from inewave.newave.modelos.parpvaz import BlocoCorrelParcialVazoesUHE
from inewave.newave.modelos.parpvaz import BlocoOrdemModeloUHE
from inewave.newave.modelos.parpvaz import BlocoCoeficientesModeloUHE
from inewave.newave.modelos.parpvaz import BlocoSerieRuidosUHE
from inewave.newave.modelos.parpvaz import BlocoCorrelRuidosUHE
from inewave.newave.modelos.parpvaz import BlocoCorrelEspacialAnualMensalUHE

from cfinterface.components.block import Block
from cfinterface.files.blockfile import BlockFile
from typing import Type, TypeVar, Optional, Any, List
import pandas as pd  # type: ignore


class PARpvaz(BlockFile):
    """
    Armazena os dados de saída do NEWAVE referentes aos modelos e às
    séries sintéticas de vazões geradas pelo PAR(p).


    Esta classe lida com informações de saída do NEWAVE e
    cujas saídas devem ser compatíveis com as observadas através
    do NWLISTOP.

    """

    T = TypeVar("T")

    BLOCKS = [
        BlocoSerieVazoesUHE,
        BlocoCorrelVazoesUHE,
        BlocoCorrelParcialVazoesUHE,
        BlocoOrdemModeloUHE,
        BlocoCoeficientesModeloUHE,
        BlocoSerieRuidosUHE,
        BlocoCorrelRuidosUHE,
        BlocoCorrelEspacialAnualMensalUHE,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__series_vazoes = None
        self.__correl_series_vazoes = None
        self.__correl_parcial_series_vazoes = None
        self.__series_ruido = None
        self.__correl_series_ruido = None
        self.__ordem_original_modelo = None
        self.__ordem_final_modelo = None
        self.__coeficientes = None
        self.__correl_espacial_anual_mensal = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="parpvaz.dat"
    ) -> "PARpvaz":
        return cls.read(diretorio, nome_arquivo)

    def __uhes(self) -> Optional[List[str]]:
        """
        Retorna a lista das UHEs lidos do arquivo.

        :return: Os nomes das UHEs
        :rtype: List[str]
        """
        if self.series_vazoes_uhe is None:
            return None
        else:
            return self.series_vazoes_uhe["UHE"].unique().tolist()

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

    def __adiciona_coluna_uhe(
        self, df: Optional[pd.DataFrame]
    ) -> Optional[pd.DataFrame]:
        """
        Adiciona uma coluna com as UHEs de cada amostra, assumindo
        a mesma ordem das séries de vazões.

        :param df: O DataFrame que irá receber as UHEs
        :type df: pd.DataFrame
        :return: O DataFrame com as UHEs
        :rtype: pd.DataFrame
        """
        if df is None:
            return None
        uhes = self.__uhes()
        if uhes is None:
            return None
        linhas_por_uhe = df.shape[0] / len(uhes)
        if int(linhas_por_uhe) != linhas_por_uhe:
            raise ValueError(
                f"{df.shape[0]} linhas não podem ser "
                + f"divididas em {len(uhes)} grupos"
            )
        cols = list(df.columns)
        col_uhe: List[str] = []
        for uhe in uhes:
            col_uhe += [uhe] * int(linhas_por_uhe)
        df["UHE"] = col_uhe
        return df[["UHE"] + cols]

    def __adiciona_coluna_uhe_com_estagios(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Adiciona uma coluna com as UHEs de cada amostra e outra
        com o estágio de cada uma, assumindo
        a mesma ordem das séries de vazões.

        :param df: O DataFrame que irá receber as UHEs
        :type df: pd.DataFrame
        :return: O DataFrame com as UHEs
        :rtype: pd.DataFrame
        """
        uhes = self.__uhes()
        if uhes is None:
            return None
        linhas_por_uhe = df.shape[0] / len(uhes)
        if int(linhas_por_uhe) != linhas_por_uhe:
            raise ValueError(
                f"{df.shape[0]} linhas não podem ser "
                + f"divididas em {len(uhes)} grupos"
            )
        cols = list(df.columns)
        col_uhe: List[str] = []
        col_estagio: List[int] = []
        for uhe in uhes:
            col_uhe += [uhe] * int(linhas_por_uhe)
            col_estagio += list(range(1, int(linhas_por_uhe) + 1))
        df["UHE"] = col_uhe
        df["Estágio"] = col_estagio
        return df[["UHE", "Estágio"] + cols]

    def __adiciona_coluna_uhe_corrigindo_pre_pos(
        self, df: Optional[pd.DataFrame]
    ) -> Optional[pd.DataFrame]:
        """
        Adiciona uma coluna com as UHEs de cada amostra e outra
        com o estágio de cada uma, assumindo
        a mesma ordem das séries de vazões, e corrigindo os valores
        dos anos se houve períodos PRE e POS.

        :param df: O DataFrame que irá receber as UHEs
        :type df: pd.DataFrame
        :return: O DataFrame com as UHEs
        :rtype: pd.DataFrame
        """

        def converte_vetor_anos(anos: List[str], n: int) -> List[int]:
            # Descobre os anos pré e pós estudo
            numero_anos_pre = len([p for p in anos if p == "PRE"]) // n
            numero_anos_pos = len([p for p in anos if p == "POS"]) // n
            anos_estudo = [int(p) for p in anos if p not in ["PRE", "POS"]]
            # TODO - remover fallback de 1970 quando estiver o ano correto.
            # Descobre o primeiro ano de estudo
            primeiro_ano_estudo = (
                sorted(anos_estudo)[0] if len(anos_estudo) > 0 else 1970
            )
            # Descobre o último ano de estudo
            ultimo_ano_estudo = (
                sorted(anos_estudo)[-1] if len(anos_estudo) > 0 else 1970
            )
            indice_inicio_pos = anos.index("POS")
            # Substitui os anos pré e pós pelos valores específicos
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
        uhes = self.__uhes()
        if uhes is None:
            return None
        linhas_por_uhe = df.shape[0] / len(uhes)
        if int(linhas_por_uhe) != linhas_por_uhe:
            raise ValueError(
                f"{df.shape[0]} linhas não podem ser "
                + f"divididas em {len(uhes)} grupos"
            )
        cols = list(df.columns)
        col_uhe: List[str] = []
        for uhe in uhes:
            col_uhe += [uhe] * int(linhas_por_uhe)
        df["UHE"] = col_uhe
        uhe0 = uhes[0]
        ano0 = df["Ano"].unique().tolist()[0]
        filtro = (df["Ano"] == ano0) & (df["UHE"] == uhe0)
        n_series = df.loc[filtro].shape[0]
        for i, uhe in enumerate(uhes):
            i_i = i * int(linhas_por_uhe)
            i_f = i_i + int(linhas_por_uhe) - 1
            df.loc[i_i:i_f, "Ano"] = converte_vetor_anos(
                df.loc[i_i:i_f, "Ano"].tolist(), n_series
            )
        return df[["UHE"] + cols]

    @property
    def series_vazoes_uhe(self) -> Optional[pd.DataFrame]:
        """
        A tabela de séries de vazões para todas as configurações
        e UHEs, no mesmo formato do arquivo `parpvaz.dat`.

        - UHE (`str`)
        - Configuração (`int`)
        - Ano (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        if self.__series_vazoes is None:
            self.__series_vazoes = self.__concatena_dados(BlocoSerieVazoesUHE)
        return self.__series_vazoes

    @property
    def series_ruido_uhe(self) -> Optional[pd.DataFrame]:
        """
        A tabela de séries de ruído para todas as UHEs,
        no mesmo formato do arquivo `parpvaz.dat`.

        - UHE (`str`)
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
            self.__series_ruido = self.__concatena_dados(BlocoSerieRuidosUHE)
            self.__series_ruido = (
                self.__adiciona_coluna_uhe_corrigindo_pre_pos(
                    self.__series_ruido
                )
            )
        return self.__series_ruido

    @property
    def correlacao_series_vazoes_uhe(self) -> Optional[pd.DataFrame]:
        """
        A tabela de correlação das séries de vazões para
        todas as configurações vigentes e UHEs,
        no mesmo formato do arquivo `parpvaz.dat`.

        - UHE (`str`)
        - Data (`date`)
        - Lag 1 (`float`)
        - Lag 2 (`float`)
        - ...
        - Lag 11 (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        if self.__correl_series_vazoes is None:
            self.__correl_series_vazoes = self.__concatena_dados(
                BlocoCorrelVazoesUHE
            )
            self.__correl_series_vazoes = self.__adiciona_coluna_uhe(
                self.__correl_series_vazoes
            )
        return self.__correl_series_vazoes

    @property
    def correlacao_parcial_series_vazoes_uhe(self) -> Optional[pd.DataFrame]:
        """
        A tabela de correlação das séries de vazões para
        todas as configurações vigentes e UHEs,
        no mesmo formato do arquivo `parpvaz.dat`.

        - UHE (`str`)
        - Data (`date`)
        - Lag 1 (`float`)
        - Lag 2 (`float`)
        - ...
        - Lag 11 (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        if self.__correl_parcial_series_vazoes is None:
            self.__correl_parcial_series_vazoes = self.__concatena_dados(
                BlocoCorrelParcialVazoesUHE
            )
            self.__correl_parcial_series_vazoes = self.__adiciona_coluna_uhe(
                self.__correl_parcial_series_vazoes
            )
        return self.__correl_parcial_series_vazoes

    @property
    def correlacao_series_ruidos_uhe(self) -> Optional[pd.DataFrame]:
        """
        A tabela de correlação das séries de ruídos para
        todas as configurações vigentes e UHEs,
        no mesmo formato do arquivo `parpvaz.dat`.

        - UHE (`str`)
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
                BlocoCorrelRuidosUHE
            )
            self.__correl_series_ruido = self.__adiciona_coluna_uhe(
                self.__correl_series_ruido
            )
        return self.__correl_series_ruido

    @property
    def ordem_original_modelo(self) -> Optional[pd.DataFrame]:
        """
        A tabela de ordens originais do modelo PAR ou PAR-A
        de cada UHE, no mesmo formato do arquivo `parpvaz.dat`,
        organizada por ano de estudo.

        - UHE (`str`)
        - Ano (`int`)
        - Janeiro (`int`)
        - Fevereiro (`int`)
        - ...
        - Dezembro (`int`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """

        if self.__ordem_original_modelo is None:
            dados = self.__concatena_dados(BlocoOrdemModeloUHE)
            if dados is not None:
                dados = (
                    dados.loc[dados["Tipo"] == "ORIGINAL", :]
                    .drop(columns=["Tipo"])
                    .copy()
                )
                dados = self.__adiciona_coluna_uhe(dados)
                self.__ordem_original_modelo = dados

        return self.__ordem_original_modelo

    @property
    def ordem_final_modelo(self) -> Optional[pd.DataFrame]:
        """
        A tabela de ordens finais do modelo PAR ou PAR-A
        de cada UHE, no mesmo formato do arquivo `parpvaz.dat`,
        organizada por ano de estudo.

        - UHE (`str`)
        - Ano (`int`)
        - Janeiro (`int`)
        - Fevereiro (`int`)
        - ...
        - Dezembro (`int`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        if self.__ordem_final_modelo is None:
            dados = self.__concatena_dados(BlocoOrdemModeloUHE)
            if dados is not None:
                dados = (
                    dados.loc[dados["Tipo"] == "FINAL", :]
                    .drop(columns=["Tipo"])
                    .copy()
                )
                dados = self.__adiciona_coluna_uhe(dados)
                self.__ordem_final_modelo = dados

        return self.__ordem_final_modelo

    @property
    def coeficientes(self) -> Optional[pd.DataFrame]:
        """
        Lista de coeficientes dos modelos PAR ou PAR-A
        de cada UHE, no mesmo formato do arquivo `parpvaz.dat`,
        organizada por período de estudo.

        - UHE (`str`)
        - Estágio (`int`)
        - Psi 1 (`int`)
        - Psi 2 (`int`)
        - ...
        - Psi 11 (`int`)
        - Psi A (`int`)
        - Psi Norm 1 (`int`)
        - Psi Norm 2 (`int`)
        - ...
        - Psi Norm 11 (`int`)
        - Psi Norm A (`int`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        if self.__coeficientes is None:
            dados = self.__concatena_dados(BlocoCoeficientesModeloUHE)
            if dados is not None:
                dados = self.__adiciona_coluna_uhe_com_estagios(dados)
                self.__coeficientes = dados

        return self.__coeficientes

    @property
    def correlacao_espacial_anual_mensal(self) -> Optional[pd.DataFrame]:
        """
        A tabela de correlação para todas as UHEs,
        no mesmo formato do arquivo `parpvaz.dat`.

        - UHE 1 (`str`)
        - UHE 2 (`str`)
        - Janeiro (`str`)
        - Fevereiro (`str`)
        - ...
        - Dezembro (`str`)
        - Anual (`str`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        if self.__correl_espacial_anual_mensal is None:
            self.__correl_espacial_anual_mensal = self.__concatena_dados(
                BlocoCorrelEspacialAnualMensalUHE
            )
        return self.__correl_espacial_anual_mensal
