from cfinterface.components.section import Section
from typing import IO, List
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class SecaoDadosCortes(Section):
    """
    Registro com os cortes da FCF.
    """

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosCortes):
            return False
        bloco: SecaoDadosCortes = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(bloco.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    def __le_e_atribui_int(
        self, file: IO, destino: np.ndarray, tamanho: int, indice: int
    ):
        destino[indice, :] = np.frombuffer(
            file.read(tamanho * 4),
            dtype=np.int32,
            count=tamanho,
        )

    def __le_e_atribui_float(
        self, file: IO, destino: np.ndarray, tamanho: int, indice: int
    ):
        destino[indice, :] = np.frombuffer(
            file.read(tamanho * 8),
            dtype=np.float64,
            count=tamanho,
        )

    def __inicializa_variaveis(self):
        self.__tabela_int = np.zeros(
            (self.__numero_total_cortes, 4), dtype=np.int32
        )
        bytes_nao_coeficientes = 4 * 4
        self.__numero_coeficientes = int(
            (self.__tamanho_registro - bytes_nao_coeficientes) / 8
        )
        self.__tabela_float = np.zeros(
            (self.__numero_total_cortes, self.__numero_coeficientes),
            dtype=np.float64,
        )

    def __le_registro(
        self,
        file: IO,
        offset: int,
        indice: int,
    ) -> int:
        file.seek(offset)
        self.__le_e_atribui_int(file, self.__tabela_int, 4, indice)
        self.__le_e_atribui_float(
            file, self.__tabela_float, self.__numero_coeficientes, indice
        )
        indice_proximo_corte = self.__tabela_int[indice, 0]
        self.__tabela_int[indice, 0] = indice
        return indice_proximo_corte

    def __converte_array_ree(self, cortes_lidos: int) -> pd.DataFrame:
        self.__tabela_int = self.__tabela_int[:cortes_lidos, :]
        df_int = pd.DataFrame(
            self.__tabela_int,
            columns=[
                "indice_corte",
                "iteracao_construcao",
                "indice_forward",
                "iteracao_desativacao",
            ],
        )
        # O índice guardado é o índice do corte anterior.
        # Para transformar no índice do corte em si, soma 1
        df_int["indice_corte"] += 1
        self.__tabela_float = self.__tabela_float[:cortes_lidos, :]

        cols_earm = [f"pi_earm_ree{i}" for i in self.__codigos_rees]
        cols_ena = [
            f"pi_ena_ree{i}_lag{j}"
            for i in self.__codigos_rees
            for j in range(1, self.__ordem_maxima_parp + 1)
        ]
        cols_gnl = [
            f"pi_gnl_sbm{i}_pat{j}_lag{k}"
            for i in self.__codigos_submercados
            for j in range(1, self.__numero_patamares_carga + 1)
            for k in range(1, self.__lag_maximo_gnl + 1)
        ]

        num_cols = 1 + len(cols_earm) + len(cols_ena) + len(cols_gnl)
        df_float = pd.DataFrame(
            self.__tabela_float[:, :num_cols],
            columns=["rhs"] + cols_earm + cols_ena + cols_gnl,
        )
        return pd.concat([df_int, df_float], axis=1)

    def __converte_array_indiv(self, cortes_lidos: int) -> pd.DataFrame:
        self.__tabela_int = self.__tabela_int[:cortes_lidos, :]
        df_int = pd.DataFrame(
            self.__tabela_int,
            columns=[
                "indice_corte",
                "iteracao_construcao",
                "indice_forward",
                "iteracao_desativacao",
            ],
        )
        # O índice guardado é o índice do corte anterior.
        # Para transformar no índice do corte em si, soma 1
        df_int["indice_corte"] += 1
        self.__tabela_float = self.__tabela_float[:cortes_lidos, :]

        cols_varm = [f"pi_varm_uhe{i}" for i in self.__codigos_uhes]
        cols_qafl = [
            f"pi_qafl_uhe{i}_lag{j}"
            for i in self.__codigos_uhes
            for j in range(1, self.__ordem_maxima_parp + 1)
        ]
        cols_gnl = [
            f"pi_gnl_sbm{i}_pat{j}_lag{k}"
            for i in self.__codigos_submercados
            for j in range(1, self.__numero_patamares_carga + 1)
            for k in range(1, self.__lag_maximo_gnl + 1)
        ]

        num_cols_gnl = len(cols_gnl)
        num_cols_varm_qafl = len(self.__codigos_uhes) * (
            self.__ordem_maxima_parp + 1
        )
        offset_inicio_cols_varm = num_cols_gnl + 2
        indices_cols_df_float = (
            [0]
            + list(range(1, num_cols_gnl + 1))
            + list(
                range(
                    offset_inicio_cols_varm,
                    offset_inicio_cols_varm + num_cols_varm_qafl,
                )
            )
        )

        df_float = pd.DataFrame(
            self.__tabela_float[:, indices_cols_df_float],
            columns=["rhs"] + cols_gnl + cols_varm + cols_qafl,
        )
        return pd.concat([df_int, df_float], axis=1)

    def __converte_array_em_dataframe(self, cortes_lidos: int):
        if len(self.__codigos_rees) > 0:
            df = self.__converte_array_ree(cortes_lidos)
        elif len(self.__codigos_uhes) > 0:
            df = self.__converte_array_indiv(cortes_lidos)
        else:
            df = pd.DataFrame(
                columns=[
                    "indice_corte",
                    "iteracao_construcao",
                    "indice_forward",
                    "iteracao_desativacao",
                ],
            )
        # Inverte a indexação
        df["indice_corte"] = df["indice_corte"].to_numpy()[::-1]
        self.data = df

    def read(
        self,
        file: IO,
        tamanho_registro: int = 1664,
        indice_ultimo_corte: int = 1,
        numero_total_cortes: int = 10000,
        codigos_rees: List[str] = [],
        codigos_uhes: List[str] = [],
        codigos_submercados: List[str] = [],
        ordem_maxima_parp: int = 12,
        numero_patamares_carga: int = 3,
        lag_maximo_gnl: int = 2,
        *args,
        **kwargs,
    ):
        # Atribui variáveis locais
        self.__tamanho_registro = tamanho_registro
        self.__numero_total_cortes = numero_total_cortes
        self.__codigos_rees = codigos_rees
        self.__codigos_uhes = codigos_uhes
        self.__codigos_submercados = codigos_submercados
        self.__ordem_maxima_parp = ordem_maxima_parp
        self.__numero_patamares_carga = numero_patamares_carga
        self.__lag_maximo_gnl = lag_maximo_gnl
        # Realiza leitura
        self.__inicializa_variaveis()
        indice_proximo_corte = self.__le_registro(
            file, (indice_ultimo_corte - 1) * tamanho_registro, 0
        )
        cortes_lidos = 1
        while (indice_proximo_corte != 0) and (
            cortes_lidos < numero_total_cortes
        ):
            indice_proximo_corte = self.__le_registro(
                file,
                tamanho_registro * (indice_proximo_corte - 1),
                cortes_lidos,
            )
            cortes_lidos += 1
        self.__converte_array_em_dataframe(cortes_lidos)
