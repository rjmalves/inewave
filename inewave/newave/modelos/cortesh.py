from cfinterface.components.section import Section
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import List
from typing import IO


class SecaoDadosCortesh(Section):
    """
    Registro com os dados da execução do caso existente no
    arquivo cortesh.dat
    """

    REGISTER_SIZE = 46080

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__df_ultimo_corte_por_estagio = pd.DataFrame()
        self.__df_dados_submercado = pd.DataFrame()
        self.__df_dados_uhes = pd.DataFrame()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosCortesh):
            return False
        bloco: SecaoDadosCortesh = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO, *args, **kwargs):
        # Leitura do primeiro registro (dados gerais)
        self.__le_primeiro_registro(file)
        # Segundo registro (ultimo registro de cortes por estagio)
        self.__le_segundo_registro(file)
        # Terceiro registro (ordens dos modelos PARP)
        self.__le_terceiro_registro(file)
        # Quarto registro (configuracoes)
        self.__le_quarto_registro(file)
        # Quinto registro (duracoes dos patamares)
        self.__le_quinto_registro(file)
        # Sexto registro (iteracao atual)
        self.__le_sexto_registro(file)
        # Setimo registro (dados da curva de aversao)
        self.__le_setimo_registro(file)
        # Oitavo registro (dados da SAR)
        self.__le_oitavo_registro(file)
        # Nono registro (dados do CVaR)
        self.__le_nono_registro(file)
        # Decimo registro (usinas hidreletricas)
        self.__le_decimo_registro(file)
        # Decimo primeiro registro (rees e submercados)
        self.__le_decimo_primeiro_registro(file)
        # Decimo segundo registro (dados diversos REEs)
        self.__le_decimo_segundo_registro(file)
        # Decimo terceiro registro (numero UHEs estagios individualizados)
        self.__le_decimo_terceiro_registro(file)
        # Decimo quarto registro (dados UHEs)
        self.__le_decimo_quarto_registro(file)

    def __le_primeiro_registro(self, file: IO):
        dados_primeiro_bloco = np.frombuffer(
            file.read(24 * 4),
            dtype=np.int32,
            count=24,
        )
        versao_nao_ofic = file.read(20).decode("utf-8").strip()
        dados_segundo_bloco = np.frombuffer(
            file.read(10 * 4),
            dtype=np.int32,
            count=10,
        )
        self.data = (
            list(dados_primeiro_bloco)
            + [versao_nao_ofic]
            + list(dados_segundo_bloco)
        )

    def __le_segundo_registro(self, file: IO):
        file.seek(1 * self.__class__.REGISTER_SIZE)
        n_estagios = (
            self.numero_estagios_pre
            + self.numero_estagios_estudo
            + self.numero_estagios_pos
        )
        self.__tamanho_segundo_registro = n_estagios
        dados_segundo_registro = np.frombuffer(
            file.read(self.__tamanho_segundo_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_segundo_registro,
        )
        self.data += list(dados_segundo_registro)

    def __le_terceiro_registro(self, file: IO):
        file.seek(2 * self.__class__.REGISTER_SIZE)
        n_estagios = (
            self.numero_estagios_pre
            + self.numero_estagios_estudo
            + self.numero_estagios_pos
        )
        self.__tamanho_terceiro_registro = n_estagios * self.numero_rees
        dados_terceiro_registro = np.frombuffer(
            file.read(self.__tamanho_terceiro_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_terceiro_registro,
        )
        self.data += list(dados_terceiro_registro)

    def __le_quarto_registro(self, file: IO):
        file.seek(3 * self.__class__.REGISTER_SIZE)
        n_estagios = (
            self.numero_estagios_pre
            + self.numero_estagios_estudo
            + self.numero_estagios_pos
        )
        self.__tamanho_quarto_registro = n_estagios
        dados_quarto_registro = np.frombuffer(
            file.read(self.__tamanho_quarto_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_quarto_registro,
        )
        self.data += list(dados_quarto_registro)

    def __le_quinto_registro(self, file: IO):
        file.seek(4 * self.__class__.REGISTER_SIZE)
        self.__tamanho_quinto_registro = (
            self.numero_estagios_estudo * self.numero_patamares
        )
        dados_quinto_registro = np.frombuffer(
            file.read(self.__tamanho_quinto_registro * 8),
            dtype=np.float64,
            count=self.__tamanho_quinto_registro,
        )
        self.data += list(dados_quinto_registro)

    def __le_sexto_registro(self, file: IO):
        file.seek(5 * self.__class__.REGISTER_SIZE)
        self.__tamanho_sexto_registro = 1
        dados_sexto_registro = np.frombuffer(
            file.read(self.__tamanho_sexto_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_sexto_registro,
        )
        self.data += list(dados_sexto_registro)

    def __le_setimo_registro(self, file: IO):
        file.seek(6 * self.__class__.REGISTER_SIZE)
        self.__tamanho_setimo_registro = (
            self.numero_rees * (self.numero_estagios_estudo + 1)
            if self.usa_curva_aversao
            else 0
        )
        dados_setimo_registro = (
            np.frombuffer(
                file.read(self.__tamanho_setimo_registro * 8),
                dtype=np.float64,
                count=self.__tamanho_setimo_registro,
            )
            if self.usa_curva_aversao
            else np.array([], dtype=np.float64)
        )
        self.data += list(dados_setimo_registro)

    def __le_oitavo_registro(self, file: IO):
        file.seek(7 * self.__class__.REGISTER_SIZE)
        self.__tamanho_oitavo_registro = (
            (2 + self.numero_estagios_estudo + 2 * self.numero_estagios_ano)
            if self.usa_sar
            else 0
        )
        dados_oitavo_registro = (
            list(
                np.frombuffer(
                    file.read(1 * 8),
                    dtype=np.float64,
                    count=1,
                )
            )
            + list(
                np.frombuffer(
                    file.read((self.__tamanho_oitavo_registro - 1) * 4),
                    dtype=np.int32,
                    count=self.__tamanho_oitavo_registro - 1,
                )
            )
            if self.usa_sar
            else []
        )
        self.data += list(dados_oitavo_registro)

    def __le_nono_registro(self, file: IO):
        file.seek(8 * self.__class__.REGISTER_SIZE)
        self.__tamanho_nono_registro = (
            (
                1
                + 2
                * (self.numero_estagios_estudo + 2 * self.numero_estagios_ano)
            )
            if self.usa_cvar
            else 0
        )
        dados_nono_registro = (
            list(
                np.frombuffer(
                    file.read(1 * 4),
                    dtype=np.int32,
                    count=1,
                )
            )
            + list(
                np.frombuffer(
                    file.read((self.__tamanho_nono_registro - 1) * 8),
                    dtype=np.float64,
                    count=self.__tamanho_nono_registro - 1,
                )
            )
            if self.usa_cvar
            else []
        )
        self.data += list(dados_nono_registro)

    def __le_decimo_registro(self, file: IO):
        file.seek(9 * self.__class__.REGISTER_SIZE)
        self.__tamanho_decimo_registro = 1 + 2 * self.numero_maximo_uhes
        dados_decimo_registro = np.frombuffer(
            file.read(self.__tamanho_decimo_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_decimo_registro,
        )
        self.data += list(dados_decimo_registro)

    def __le_decimo_primeiro_registro(self, file: IO):
        file.seek(10 * self.__class__.REGISTER_SIZE)
        tamanho_decimo_primeiro_registro_bloco_1 = (
            self.numero_submercados + self.numero_rees
        )
        dados_decimo_primeiro_registro_bloco_1 = np.frombuffer(
            file.read(tamanho_decimo_primeiro_registro_bloco_1 * 4),
            dtype=np.int32,
            count=tamanho_decimo_primeiro_registro_bloco_1,
        )
        tamanho_decimo_primeiro_registro_bloco_2 = (
            self.numero_total_submercados + self.numero_rees
        )
        dados_decimo_primeiro_registro_bloco_2: List[str] = []
        for i in range(tamanho_decimo_primeiro_registro_bloco_2):
            dados_decimo_primeiro_registro_bloco_2.append(
                file.read(10).decode("utf-8").strip()
            )
        tamanho_decimo_primeiro_registro_bloco_3 = (
            self.numero_total_submercados + self.numero_rees
        )
        dados_decimo_primeiro_registro_bloco_3 = np.frombuffer(
            file.read(tamanho_decimo_primeiro_registro_bloco_3 * 4),
            dtype=np.int32,
            count=tamanho_decimo_primeiro_registro_bloco_3,
        )
        self.data += list(dados_decimo_primeiro_registro_bloco_1)
        self.data += dados_decimo_primeiro_registro_bloco_2
        self.data += list(dados_decimo_primeiro_registro_bloco_3)
        self.__tamanho_decimo_primeiro_registro = (
            tamanho_decimo_primeiro_registro_bloco_1
            + tamanho_decimo_primeiro_registro_bloco_2
            + tamanho_decimo_primeiro_registro_bloco_3
        )

    def __le_decimo_segundo_registro(self, file: IO):
        file.seek(11 * self.__class__.REGISTER_SIZE)
        self.__tamanho_decimo_segundo_registro = 8
        dados_decimo_segundo_registro = np.frombuffer(
            file.read(self.__tamanho_decimo_segundo_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_decimo_segundo_registro,
        )
        self.data += list(dados_decimo_segundo_registro)

    def __le_decimo_terceiro_registro(self, file: IO):
        file.seek(12 * self.__class__.REGISTER_SIZE)
        self.__tamanho_decimo_terceiro_registro = self.mes_agregacao
        dados_decimo_terceiro_registro = np.frombuffer(
            file.read(self.__tamanho_decimo_terceiro_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_decimo_terceiro_registro,
        )
        self.data += list(dados_decimo_terceiro_registro)

    def __le_decimo_quarto_registro(self, file: IO):
        tamanho_bloco_decimo_quarto_registro = (
            6
            + self.numero_estagios_pre
            + self.numero_estagios_estudo
            + self.numero_estagios_pos
        )
        self.__tamanho_decimo_quarto_registro = (
            self.numero_maximo_uhes * tamanho_bloco_decimo_quarto_registro
        )
        for i in range(self.numero_maximo_uhes):
            file.seek((13 + i) * self.__class__.REGISTER_SIZE)
            dados_decimo_quarto_registro = np.frombuffer(
                file.read(tamanho_bloco_decimo_quarto_registro * 4),
                dtype=np.int32,
                count=tamanho_bloco_decimo_quarto_registro,
            )
            self.data += list(dados_decimo_quarto_registro)

    def __offset_primeiro_registro(self) -> int:
        return 35

    def __offset_segundo_registro(self) -> int:
        return (
            self.__offset_primeiro_registro() + self.__tamanho_segundo_registro
        )

    def __offset_terceiro_registro(self) -> int:
        return (
            self.__offset_segundo_registro() + self.__tamanho_terceiro_registro
        )

    def __offset_quarto_registro(self) -> int:
        return (
            self.__offset_terceiro_registro() + self.__tamanho_quarto_registro
        )

    def __offset_quinto_registro(self) -> int:
        return self.__offset_quarto_registro() + self.__tamanho_quinto_registro

    def __offset_sexto_registro(self) -> int:
        return self.__offset_quinto_registro() + self.__tamanho_sexto_registro

    def __offset_setimo_registro(self) -> int:
        return self.__offset_sexto_registro() + self.__tamanho_setimo_registro

    def __offset_oitavo_registro(self) -> int:
        return self.__offset_setimo_registro() + self.__tamanho_oitavo_registro

    def __offset_nono_registro(self) -> int:
        return self.__offset_oitavo_registro() + self.__tamanho_nono_registro

    def __offset_decimo_registro(self) -> int:
        return self.__offset_nono_registro() + self.__tamanho_decimo_registro

    def __offset_decimo_primeiro_registro(self) -> int:
        return (
            self.__offset_decimo_registro()
            + self.__tamanho_decimo_primeiro_registro
        )

    def __offset_decimo_segundo_registro(self) -> int:
        return (
            self.__offset_decimo_primeiro_registro()
            + self.__tamanho_decimo_segundo_registro
        )

    def __offset_decimo_terceiro_registro(self) -> int:
        return (
            self.__offset_decimo_segundo_registro()
            + self.__tamanho_decimo_terceiro_registro
        )

    @property
    def versao_newave(self) -> int:
        return self.data[0]

    @versao_newave.setter
    def versao_newave(self, v: int):
        self.data[0] = v

    @property
    def tamanho_corte(self) -> int:
        return self.data[1]

    @tamanho_corte.setter
    def tamanho_corte(self, v: int):
        self.data[1] = v

    @property
    def tamanho_estado(self) -> int:
        return self.data[2]

    @tamanho_estado.setter
    def tamanho_estado(self, v: int):
        self.data[2] = v

    @property
    def numero_rees(self) -> int:
        return self.data[3]

    @numero_rees.setter
    def numero_rees(self, v: int):
        self.data[3] = v

    @property
    def numero_estagios_pre(self) -> int:
        return self.data[4]

    @numero_estagios_pre.setter
    def numero_estagios_pre(self, v: int):
        self.data[4] = v

    @property
    def numero_estagios_estudo(self) -> int:
        return self.data[5]

    @numero_estagios_estudo.setter
    def numero_estagios_estudo(self, v: int):
        self.data[5] = v

    @property
    def numero_estagios_pos(self) -> int:
        return self.data[6]

    @numero_estagios_pos.setter
    def numero_estagios_pos(self, v: int):
        self.data[6] = v

    @property
    def numero_estagios_ano(self) -> int:
        return self.data[7]

    @numero_estagios_ano.setter
    def numero_estagios_ano(self, v: int):
        self.data[7] = v

    @property
    def numero_configuracoes(self) -> int:
        return self.data[8]

    @numero_configuracoes.setter
    def numero_configuracoes(self, v: int):
        self.data[8] = v

    @property
    def numero_forwards(self) -> int:
        return self.data[9]

    @numero_forwards.setter
    def numero_forwards(self, v: int):
        self.data[9] = v

    @property
    def numero_patamares(self) -> int:
        return self.data[10]

    @numero_patamares.setter
    def numero_patamares(self, v: int):
        self.data[10] = v

    @property
    def ano_inicio_estudo(self) -> int:
        return self.data[11]

    @ano_inicio_estudo.setter
    def ano_inicio_estudo(self, v: int):
        self.data[11] = v

    @property
    def mes_inicio_estudo(self) -> int:
        return self.data[12]

    @mes_inicio_estudo.setter
    def mes_inicio_estudo(self, v: int):
        self.data[12] = v

    @property
    def lag_maximo_gnl(self) -> int:
        return self.data[13]

    @lag_maximo_gnl.setter
    def lag_maximo_gnl(self, v: int):
        self.data[13] = v

    @property
    def mecanismo_aversao(self) -> int:
        return self.data[14]

    @mecanismo_aversao.setter
    def mecanismo_aversao(self, v: int):
        self.data[14] = v

    @property
    def numero_submercados(self) -> int:
        return self.data[15]

    @numero_submercados.setter
    def numero_submercados(self, v: int):
        self.data[15] = v

    @property
    def numero_total_submercados(self) -> int:
        return self.data[16]

    @numero_total_submercados.setter
    def numero_total_submercados(self, v: int):
        self.data[16] = v

    @property
    def usa_curva_aversao(self) -> int:
        return self.data[17]

    @usa_curva_aversao.setter
    def usa_curva_aversao(self, v: int):
        self.data[17] = v

    @property
    def usa_sar(self) -> int:
        return self.data[18]

    @usa_sar.setter
    def usa_sar(self, v: int):
        self.data[18] = v

    @property
    def usa_cvar(self) -> int:
        return self.data[19]

    @usa_cvar.setter
    def usa_cvar(self, v: int):
        self.data[19] = v

    @property
    def considera_no_zero_calculo_zinf(self) -> int:
        return self.data[20]

    @considera_no_zero_calculo_zinf.setter
    def considera_no_zero_calculo_zinf(self, v: int):
        self.data[20] = v

    @property
    def mes_agregacao(self) -> int:
        return self.data[21]

    @mes_agregacao.setter
    def mes_agregacao(self, v: int):
        self.data[21] = v

    @property
    def numero_maximo_uhes(self) -> int:
        return self.data[22]

    @numero_maximo_uhes.setter
    def numero_maximo_uhes(self, v: int):
        self.data[22] = v

    @property
    def considera_afluencia_anual(self) -> int:
        return self.data[23]

    @considera_afluencia_anual.setter
    def considera_afluencia_anual(self, v: int):
        self.data[23] = v

    @property
    def versao_nao_oficial(self) -> str:
        return self.data[24]

    @versao_nao_oficial.setter
    def versao_nao_oficial(self, v: str):
        self.data[24] = v

    @property
    def tipo_penalizacao_curva(self) -> int:
        return self.data[25]

    @tipo_penalizacao_curva.setter
    def tipo_penalizacao_curva(self, v: int):
        self.data[25] = v

    @property
    def mes_penalizacao_curva(self) -> int:
        return self.data[26]

    @mes_penalizacao_curva.setter
    def mes_penalizacao_curva(self, v: int):
        self.data[26] = v

    @property
    def opcao_parpa(self) -> int:
        return self.data[27]

    @opcao_parpa.setter
    def opcao_parpa(self, v: int):
        self.data[27] = v

    @property
    def tipo_agregacao_caso(self) -> int:
        return self.data[28]

    @tipo_agregacao_caso.setter
    def tipo_agregacao_caso(self, v: int):
        self.data[28] = v

    @property
    def estagio_individualizado_inicial(self) -> int:
        return self.data[29]

    @estagio_individualizado_inicial.setter
    def estagio_individualizado_inicial(self, v: int):
        self.data[29] = v

    @property
    def estagio_individualizado_final(self) -> int:
        return self.data[30]

    @estagio_individualizado_final.setter
    def estagio_individualizado_final(self, v: int):
        self.data[30] = v

    @property
    def tamanho_registro_individualizado(self) -> int:
        return self.data[31]

    @tamanho_registro_individualizado.setter
    def tamanho_registro_individualizado(self, v: int):
        self.data[31] = v

    @property
    def estagio_agregado_inicial(self) -> int:
        return self.data[32]

    @estagio_agregado_inicial.setter
    def estagio_agregado_inicial(self, v: int):
        self.data[32] = v

    @property
    def estagio_agregado_final(self) -> int:
        return self.data[33]

    @estagio_agregado_final.setter
    def estagio_agregado_final(self, v: int):
        self.data[33] = v

    @property
    def tamanho_registro_agregado(self) -> int:
        return self.data[34]

    @tamanho_registro_agregado.setter
    def tamanho_registro_agregado(self, v: int):
        self.data[34] = v

    @property
    def ultimo_registro_cortes_estagio(self) -> pd.DataFrame:
        if self.__df_ultimo_corte_por_estagio.empty:
            offset = self.__offset_primeiro_registro()
            indices = self.data[
                offset : offset + self.__tamanho_segundo_registro
            ]
            self.__df_ultimo_corte_por_estagio = pd.DataFrame(
                data={
                    "tipo_estagio": ["pre"] * self.numero_estagios_pre
                    + ["estudo"] * self.numero_estagios_estudo
                    + ["pos"] * self.numero_estagios_pos,
                    "estagio": list(range(1, self.numero_estagios_pre + 1))
                    + list(range(1, self.numero_estagios_estudo + 1))
                    + list(range(1, self.numero_estagios_pos + 1)),
                    "indice_ultimo_corte": indices,
                }
            )
        return self.__df_ultimo_corte_por_estagio

    @property
    def ordens_modelos_parp(self) -> List[int]:
        offset = self.__offset_segundo_registro()
        return self.data[offset : offset + self.__tamanho_terceiro_registro]

    @property
    def configuracoes(self) -> List[int]:
        offset = self.__offset_terceiro_registro()
        return self.data[offset : offset + self.__tamanho_quarto_registro]

    @property
    def duracoes_patamares(self) -> List[float]:
        offset = self.__offset_quarto_registro()
        return self.data[offset : offset + self.__tamanho_quinto_registro]

    @property
    def iteracao_atual(self) -> int:
        offset = self.__offset_quinto_registro()
        return self.data[offset]

    @property
    def penalidade_violacao_curva(self) -> List[float]:
        if self.usa_curva_aversao == 0:
            return []
        offset = self.__offset_sexto_registro()
        return self.data[offset : offset + self.numero_rees]

    @property
    def curva_aversao(self) -> List[float]:
        if self.usa_curva_aversao == 0:
            return []
        offset = self.__offset_sexto_registro() + self.numero_rees
        return self.data[
            offset : offset + self.numero_rees * self.numero_estagios_estudo
        ]

    @property
    def penalidade_violacao_sar(self) -> float:
        if self.usa_sar == 0:
            return 0.0
        offset = self.__offset_setimo_registro()
        return self.data[offset]

    @property
    def uso_series_condicionadas_sar(self) -> int:
        if self.usa_sar == 0:
            return 0
        offset = self.__offset_setimo_registro() + 1
        return self.data[offset]

    @property
    def flag_aplicacao_sar(self) -> List[int]:
        if self.usa_sar == 0:
            return []
        offset = self.__offset_setimo_registro() + 2
        return self.data[
            offset : offset
            + self.numero_estagios_estudo
            + 2 * self.numero_estagios_ano
        ]

    @property
    def flag_cvar(self) -> int:
        if self.usa_cvar == 0:
            return 0
        offset = self.__offset_oitavo_registro()
        return self.data[offset]

    @property
    def alfa_cvar(self) -> List[float]:
        if self.usa_cvar == 0:
            return []
        offset = self.__offset_oitavo_registro() + 1
        return self.data[
            offset : offset
            + self.numero_estagios_estudo
            + 2 * self.numero_estagios_ano
        ]

    @property
    def lambda_cvar(self) -> List[float]:
        if self.usa_cvar == 0:
            return []
        offset = (
            self.__offset_oitavo_registro()
            + 1
            + self.numero_estagios_estudo
            + 2 * self.numero_estagios_ano
        )
        return self.data[
            offset : offset
            + self.numero_estagios_estudo
            + 2 * self.numero_estagios_ano
        ]

    @property
    def numero_uhes(self) -> int:
        offset = self.__offset_nono_registro()
        return self.data[offset]

    @property
    def codigos_uhes(self) -> List[int]:
        offset = self.__offset_nono_registro() + 1
        return self.data[offset : offset + self.numero_uhes]

    @property
    def codigo_interno_ree_uhes(self) -> List[int]:
        offset = self.__offset_nono_registro() + 1 + self.numero_uhes
        return self.data[offset : offset + self.numero_uhes]

    @property
    def rees_por_submercado(self) -> List[int]:
        offset = self.__offset_decimo_registro()
        return self.data[offset : offset + self.numero_submercados]

    @property
    def codigos_internos_rees_por_submercado(self) -> List[int]:
        offset = self.__offset_decimo_registro() + self.numero_submercados
        return self.data[offset : offset + self.numero_rees]

    @property
    def nomes_rees_submercados(self) -> List[str]:
        offset = (
            self.__offset_decimo_registro()
            + self.numero_submercados
            + self.numero_rees
        )
        return self.data[
            offset : offset + self.numero_rees + self.numero_submercados
        ]

    @property
    def codigos_rees_submercados(self) -> List[int]:
        offset = (
            self.__offset_decimo_registro()
            + self.numero_submercados
            + self.numero_total_submercados
            + 2 * self.numero_rees
        )
        return self.data[
            offset : offset + self.numero_rees + self.numero_submercados
        ]

    @property
    def dados_submercados(self) -> pd.DataFrame:
        if self.__df_dados_submercado.empty:
            offset_codigos = (
                self.__offset_decimo_registro()
                + self.numero_submercados
                + self.numero_total_submercados
                + 3 * self.numero_rees
            )
            offset_nomes = (
                self.__offset_decimo_registro()
                + self.numero_submercados
                + 2 * self.numero_rees
            )
            offset_numero_rees = self.__offset_decimo_registro()
            codigos = self.data[
                offset_codigos : offset_codigos + self.numero_total_submercados
            ]
            nomes = self.data[
                offset_nomes : offset_nomes + self.numero_total_submercados
            ]
            numeros = self.data[
                offset_numero_rees : offset_numero_rees
                + self.numero_submercados
            ]
            self.__df_dados_submercado = pd.DataFrame(
                data={
                    "codigo_submercado": codigos,
                    "nome_submercado": nomes,
                    "numero_rees_submercado": numeros
                    + [0] * (len(codigos) - len(numeros)),
                }
            )
        return self.__df_dados_submercado

    @property
    def numero_coeficientes_derivacao_inexata_parpa(self) -> int:
        offset = self.__offset_decimo_primeiro_registro()
        return self.data[offset]

    @property
    def constante_numero_rees(self) -> int:
        offset = self.__offset_decimo_primeiro_registro()
        return self.data[offset + 2]

    @property
    def constante_numero_rees_ordem_maxima_parp(self) -> int:
        offset = self.__offset_decimo_primeiro_registro()
        return self.data[offset + 3]

    @property
    def constante_numero_submercados_patamares_carga_lag_maximo_gnl(
        self,
    ) -> int:
        offset = self.__offset_decimo_primeiro_registro()
        return self.data[offset + 4]

    @property
    def constante_numero_maximo_uhes(self) -> int:
        offset = self.__offset_decimo_primeiro_registro()
        return self.data[offset + 6]

    @property
    def constante_numero_maximo_uhes_ordem_maxima_parp(self) -> int:
        offset = self.__offset_decimo_primeiro_registro()
        return self.data[offset + 7]

    @property
    def numero_uhes_estagios_individualizados(self) -> List[int]:
        offset = self.__offset_decimo_segundo_registro()
        return self.data[offset : offset + self.mes_agregacao]

    @property
    def dados_uhes(self) -> pd.DataFrame:
        if self.__df_dados_uhes.empty:
            offset = self.__offset_decimo_terceiro_registro()
            tamanho_bloco_dados_uhes = int(
                self.__tamanho_decimo_quarto_registro / self.numero_maximo_uhes
            )
            dados = np.array(
                self.data[
                    offset : offset + self.__tamanho_decimo_quarto_registro
                ]
            ).reshape((-1, tamanho_bloco_dados_uhes))
            cols_dados = [
                "codigo_usina",
                "indice_usina",
                "posto",
                "ficticia",
                "codigo_submercado",
                "mes_agregacao",
            ]
            df = pd.DataFrame(
                dados[:, :6],
                columns=cols_dados,
            )
            rees_submercado = np.array(self.rees_por_submercado).cumsum()
            codigos_internos = self.codigos_internos_rees_por_submercado
            codigos_externos = self.codigos_rees_submercados[
                : self.numero_rees
            ]
            nomes = self.nomes_rees_submercados[: self.numero_rees]
            codigos_submercados = self.codigos_rees_submercados[
                self.numero_rees :
            ]
            nomes_submercados = self.nomes_rees_submercados[self.numero_rees :]
            df["codigo_interno_ree"] = df.apply(
                lambda linha: self.codigo_interno_ree_uhes[
                    self.codigos_uhes.index(linha["codigo_usina"])
                ],
                axis=1,
            )
            df["codigo_ree"] = df.apply(
                lambda linha: codigos_externos[
                    codigos_internos.index(linha["codigo_interno_ree"])
                ],
                axis=1,
            )
            df["nome_ree"] = df.apply(
                lambda linha: nomes[
                    codigos_internos.index(linha["codigo_interno_ree"])
                ],
                axis=1,
            )
            df["codigo_submercado"] = df.apply(
                lambda linha: codigos_submercados[
                    np.where(rees_submercado >= linha["codigo_interno_ree"])[
                        0
                    ][0]
                ],
                axis=1,
            )
            df["nome_submercado"] = df.apply(
                lambda linha: nomes_submercados[
                    codigos_submercados.index(linha["codigo_submercado"])
                ],
                axis=1,
            )
            self.__df_dados_uhes = df
        return self.__df_dados_uhes
