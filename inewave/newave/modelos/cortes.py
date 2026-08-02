from cfinterface.components.section import Section
from typing import Any, IO, List, Tuple
import numpy as np
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package


class SecaoDadosCortes(Section):
    """
    Registro com os cortes da FCF.

    Suporta tanto o arquivo consolidado (`cortes.dat`, todos os estágios com
    índices GLOBAIS) quanto os arquivos particionados por estágio
    (`cortes-<estagio>.dat`, um estágio por arquivo com índices LOCAIS).

    Layout de um registro (``tamanho_registro`` bytes)::

        int32[4]   = [indice_proximo, iteracao_construcao,
                      indice_forward, iteracao_desativacao]
        float64[n] = [rhs, coeficientes...]  com n = (tamanho_registro - 16) / 8

    Onde ``indice_proximo`` é um ponteiro 1-based para o corte ANTERIOR na
    lista ligada (0 termina a cadeia) e ``n`` é o número de coeficientes.

    Para um estágio individualizado o bloco de coeficientes é::

        rhs · PIGTAD(G) · reservado(1, sempre 0.0) · PIVARM(U) · PIAFL(U·P) · PIMX_SAR(U)

    com ``G = n_submercados · n_patamares · lag_maximo_gnl``, ``U = n_uhes`` e
    ``P = ordem_maxima_parp``, de forma que ``n == 2 + G + U · (2 + P)``.

    Para um estágio agregado em REE o bloco é::

        rhs · PIEARM(R) · PIH(R·P) · PIGTAD(G) · [PIMX_SAR, PIMX_VMN ...]

    Sobre os arquivos particionados: o cabeçalho (`cortesh.dat`) descreve o
    estudo COMPLETO em índices globais; uma partição carrega seus próprios
    índices LOCAIS. O número de cortes é derivado do próprio arquivo
    (``file_size // tamanho_registro``), descontando o registro sentinela
    final (``rhs == 0``) que a partição sempre carrega.
    """

    __slots__ = [
        "__tabela_int",
        "__numero_coeficientes",
        "__tabela_float",
        "__tamanho_registro",
        "__numero_total_cortes",
        "__codigos_rees",
        "__codigos_uhes",
        "__codigos_submercados",
        "__ordem_maxima_parp",
        "__numero_patamares_carga",
        "__lag_maximo_gnl",
    ]

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
        self, file: IO[Any], destino: np.ndarray, tamanho: int, indice: int
    ) -> None:
        destino[indice, :] = np.frombuffer(
            file.read(tamanho * 4),
            dtype=np.int32,
            count=tamanho,
        )

    def __le_e_atribui_float(
        self, file: IO[Any], destino: np.ndarray, tamanho: int, indice: int
    ) -> None:
        destino[indice, :] = np.frombuffer(
            file.read(tamanho * 8),
            dtype=np.float64,
            count=tamanho,
        )

    def __inicializa_variaveis(self) -> None:
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

    @staticmethod
    def __tamanho_arquivo(file: IO[Any]) -> int:
        posicao_atual = file.tell()
        file.seek(0, 2)
        tamanho = file.tell()
        file.seek(posicao_atual)
        return tamanho

    def __parametros_particao(
        self, file: IO[Any], tamanho_arquivo: int
    ) -> Tuple[int, int]:
        """
        Deriva ``(indice_ultimo_corte, numero_total_cortes)`` locais a partir
        de um arquivo particionado por estágio.

        O arquivo contém ``file_size // tamanho_registro`` posições, sendo a
        ÚLTIMA um registro sentinela (``rhs == 0``, sem corte válido). Os cortes
        reais ocupam as posições ``1 .. N-1``, com a entrada da lista ligada no
        último corte real.
        """
        if tamanho_arquivo % self.__tamanho_registro != 0:
            raise ValueError(
                "Arquivo de cortes particionado inconsistente: tamanho "
                f"{tamanho_arquivo} não é múltiplo de tamanho_registro "
                f"{self.__tamanho_registro}."
            )
        numero_posicoes = tamanho_arquivo // self.__tamanho_registro
        if numero_posicoes <= 0:
            raise ValueError(
                "Arquivo de cortes particionado vazio "
                f"(tamanho {tamanho_arquivo})."
            )
        numero_total_cortes = numero_posicoes
        if self.__possui_sentinela(file, numero_posicoes):
            numero_total_cortes = numero_posicoes - 1
        if numero_total_cortes <= 0:
            raise ValueError(
                "Arquivo de cortes particionado sem cortes válidos "
                f"(posições {numero_posicoes})."
            )
        return numero_total_cortes, numero_total_cortes

    def __possui_sentinela(self, file: IO[Any], numero_posicoes: int) -> bool:
        """
        Verifica se a última posição é o registro sentinela que a partição
        carrega (``rhs == 0.0``). Um corte real tem sempre RHS não-nulo.
        """
        offset = (numero_posicoes - 1) * self.__tamanho_registro
        file.seek(offset + 4 * 4)
        rhs = np.frombuffer(file.read(8), dtype=np.float64, count=1)[0]
        return bool(rhs == 0.0)

    def __valida_indice_entrada(
        self, indice: int, tamanho_arquivo: int
    ) -> None:
        if indice <= 0:
            raise ValueError(
                "Índice de entrada dos cortes deve ser positivo, recebido "
                f"{indice}. Para uma partição use por_estagio=True; para o "
                "arquivo consolidado use o índice global do estágio "
                "(cortesh.ultimo_registro_cortes_estagio)."
            )
        self.__valida_offset(indice, tamanho_arquivo)

    def __valida_offset(self, indice: int, tamanho_arquivo: int) -> None:
        offset = (indice - 1) * self.__tamanho_registro
        if offset < 0 or offset + self.__tamanho_registro > tamanho_arquivo:
            raise ValueError(
                f"Corte de índice {indice} aponta para offset {offset} fora "
                f"do arquivo (tamanho {tamanho_arquivo}, tamanho_registro "
                f"{self.__tamanho_registro}). Índices globais do consolidado "
                "não podem ser usados em uma partição — use por_estagio=True."
            )

    def __valida_layout_coeficientes(self) -> None:
        """
        Confere que o número de coeficientes nomeados (derivado das dimensões)
        casa com ``(tamanho_registro - 16) / 8``. Uma divergência indica
        ``ordem_maxima_parp`` / ``lag_maximo_gnl`` / códigos incorretos e
        produziria desalinhamento silencioso dos coeficientes.
        """
        gnl = (
            len(self.__codigos_submercados)
            * self.__numero_patamares_carga
            * self.__lag_maximo_gnl
        )
        if len(self.__codigos_rees) > 0:
            # rhs · PIEARM(R) · PIH(R·P) · PIGTAD(G) · [tail PIMX_SAR/VMN]
            esperado = (
                1
                + len(self.__codigos_rees) * (1 + self.__ordem_maxima_parp)
                + gnl
            )
            if esperado > self.__numero_coeficientes:
                raise ValueError(self.__mensagem_layout(esperado, gnl))
        elif len(self.__codigos_uhes) > 0:
            # rhs · PIGTAD(G) · reservado(1) · PIVARM(U) · PIAFL(U·P) · PIMX_SAR(U)
            esperado = (
                2
                + gnl
                + len(self.__codigos_uhes) * (2 + self.__ordem_maxima_parp)
            )
            if esperado > self.__numero_coeficientes:
                raise ValueError(self.__mensagem_layout(esperado, gnl))

    def __mensagem_layout(self, esperado: int, gnl: int) -> str:
        return (
            "Layout de coeficientes inconsistente: esperados "
            f"{esperado} coeficientes nomeados (gnl={gnl}, "
            f"ordem_maxima_parp={self.__ordem_maxima_parp}, "
            f"lag_maximo_gnl={self.__lag_maximo_gnl}, "
            f"n_uhes={len(self.__codigos_uhes)}, "
            f"n_rees={len(self.__codigos_rees)}), mas o registro comporta "
            f"{self.__numero_coeficientes} = (tamanho_registro - 16) / 8. "
            "Verifique ordem_maxima_parp / lag_maximo_gnl e os códigos "
            "informados para a versão do NEWAVE."
        )

    def __le_registro(
        self,
        file: IO[Any],
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
        cols_mx_sar = [f"pi_mx_sar_uhe{i}" for i in self.__codigos_uhes]

        num_uhes = len(self.__codigos_uhes)
        num_cols_gnl = len(cols_gnl)
        num_cols_varm_qafl = num_uhes * (self.__ordem_maxima_parp + 1)
        # Layout físico: rhs[0] · gnl[1..G] · reservado[G+1] ·
        #                varm+qafl[G+2 ..] · mx_sar[...]
        offset_inicio_cols_varm = num_cols_gnl + 2
        offset_inicio_cols_mx_sar = offset_inicio_cols_varm + num_cols_varm_qafl
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
        colunas = ["rhs"] + cols_gnl + cols_varm + cols_qafl
        # O bloco PIMX_SAR só é mapeado quando cabe no registro (evita ler
        # além do fim em registros com layout de outra versão do NEWAVE).
        if offset_inicio_cols_mx_sar + num_uhes <= self.__numero_coeficientes:
            indices_cols_df_float += list(
                range(
                    offset_inicio_cols_mx_sar,
                    offset_inicio_cols_mx_sar + num_uhes,
                )
            )
            colunas += cols_mx_sar

        df_float = pd.DataFrame(
            self.__tabela_float[:, indices_cols_df_float],
            columns=colunas,
        )
        return pd.concat([df_int, df_float], axis=1)

    def __converte_array_em_dataframe(self, cortes_lidos: int) -> Any:
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

    def read(  # type: ignore[override]  # signature extends base class
        self,
        file: IO[Any],
        tamanho_registro: int = 1664,
        indice_ultimo_corte: int = 1,
        numero_total_cortes: int = 10000,
        codigos_rees: List[str] = [],
        codigos_uhes: List[str] = [],
        codigos_submercados: List[str] = [],
        ordem_maxima_parp: int = 12,
        numero_patamares_carga: int = 3,
        lag_maximo_gnl: int = 2,
        por_estagio: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Atribui variáveis locais
        self.__tamanho_registro = tamanho_registro
        self.__codigos_rees = codigos_rees
        self.__codigos_uhes = codigos_uhes
        self.__codigos_submercados = codigos_submercados
        self.__ordem_maxima_parp = ordem_maxima_parp
        self.__numero_patamares_carga = numero_patamares_carga
        self.__lag_maximo_gnl = lag_maximo_gnl

        tamanho_arquivo = self.__tamanho_arquivo(file)
        # Numa partição por estágio os índices locais são derivados do arquivo,
        # ignorando o índice global (do estudo completo) do cabeçalho.
        if por_estagio:
            indice_ultimo_corte, numero_total_cortes = (
                self.__parametros_particao(file, tamanho_arquivo)
            )
        self.__numero_total_cortes = numero_total_cortes

        # Realiza leitura
        self.__inicializa_variaveis()
        self.__valida_layout_coeficientes()
        self.__valida_indice_entrada(indice_ultimo_corte, tamanho_arquivo)

        indice_proximo_corte = self.__le_registro(
            file, (indice_ultimo_corte - 1) * tamanho_registro, 0
        )
        cortes_lidos = 1
        while (indice_proximo_corte != 0) and (
            cortes_lidos < numero_total_cortes
        ):
            self.__valida_offset(indice_proximo_corte, tamanho_arquivo)
            indice_proximo_corte = self.__le_registro(
                file,
                tamanho_registro * (indice_proximo_corte - 1),
                cortes_lidos,
            )
            cortes_lidos += 1
        self.__converte_array_em_dataframe(cortes_lidos)
