from cfinterface.components.section import Section
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import List
from typing import IO


class SecaoDadosCortesH(Section):
    """
    Registro com os dados da execução do caso existente no
    arquivo cortesh.dat
    """

    REGISTER_SIZE = 46080

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosCortesH):
            return False
        bloco: SecaoDadosCortesH = o
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

        # Segundo registro (ultimo registro de cortes
        # por periodo)
        file.seek(1 * self.__class__.REGISTER_SIZE)
        n_estagios = (
            self.numero_periodos_pre
            + self.numero_periodos_estudo
            + self.numero_periodos_pos
        )
        self.__tamanho_segundo_registro = n_estagios
        dados_segundo_registro = np.frombuffer(
            file.read(self.__tamanho_segundo_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_segundo_registro,
        )
        self.data += list(dados_segundo_registro)
        # Terceiro registro (ordens dos modelos PARP)
        file.seek(2 * self.__class__.REGISTER_SIZE)
        self.__tamanho_terceiro_registro = n_estagios * self.numero_rees
        dados_terceiro_registro = np.frombuffer(
            file.read(self.__tamanho_terceiro_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_terceiro_registro,
        )
        self.data += list(dados_terceiro_registro)
        # Quarto registro (configuracoes)
        file.seek(3 * self.__class__.REGISTER_SIZE)
        self.__tamanho_quarto_registro = n_estagios
        dados_quarto_registro = np.frombuffer(
            file.read(self.__tamanho_quarto_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_quarto_registro,
        )
        self.data += list(dados_quarto_registro)
        # Quinto registro (duracoes dos patamares)
        file.seek(4 * self.__class__.REGISTER_SIZE)
        self.__tamanho_quinto_registro = (
            self.numero_periodos_estudo * self.numero_patamares
        )
        dados_quinto_registro = np.frombuffer(
            file.read(self.__tamanho_quinto_registro * 8),
            dtype=np.float64,
            count=self.__tamanho_quinto_registro,
        )
        self.data += list(dados_quinto_registro)
        # Sexto registro (iteracao atual)
        file.seek(5 * self.__class__.REGISTER_SIZE)
        self.__tamanho_sexto_registro = 1
        dados_sexto_registro = np.frombuffer(
            file.read(self.__tamanho_sexto_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_sexto_registro,
        )
        self.data += list(dados_sexto_registro)
        # Setimo registro (dados da curva de aversao)
        file.seek(6 * self.__class__.REGISTER_SIZE)
        self.__tamanho_setimo_registro = (
            self.numero_rees * (self.numero_periodos_estudo + 1)
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
        # Oitavo registro (dados da SAR)
        file.seek(7 * self.__class__.REGISTER_SIZE)
        self.__tamanho_oitavo_registro = (
            (2 + self.numero_periodos_estudo + 2 * self.npea)
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
        # Nono registro (dados do CVaR)
        file.seek(8 * self.__class__.REGISTER_SIZE)
        self.__tamanho_nono_registro = (
            (1 + 2 * (self.numero_periodos_estudo + 2 * self.npea))
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
        # Decimo registro (usinas hidreletricas)
        file.seek(9 * self.__class__.REGISTER_SIZE)
        self.__tamanho_decimo_registro = 1 + 2 * self.numero_maximo_uhes
        dados_decimo_registro = np.frombuffer(
            file.read(self.__tamanho_decimo_registro * 4),
            dtype=np.int32,
            count=self.__tamanho_decimo_registro,
        )
        self.data += list(dados_decimo_registro)
        # Decimo primeiro registro (rees e submercados)
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
    def numero_periodos_pre(self) -> int:
        return self.data[4]

    @numero_periodos_pre.setter
    def numero_periodos_pre(self, v: int):
        self.data[4] = v

    @property
    def numero_periodos_estudo(self) -> int:
        return self.data[5]

    @numero_periodos_estudo.setter
    def numero_periodos_estudo(self, v: int):
        self.data[5] = v

    @property
    def numero_periodos_pos(self) -> int:
        return self.data[6]

    @numero_periodos_pos.setter
    def numero_periodos_pos(self, v: int):
        self.data[6] = v

    @property
    def npea(self) -> int:
        return self.data[7]

    @npea.setter
    def npea(self, v: int):
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
    def periodo_individualizado_inicial(self) -> int:
        return self.data[29]

    @periodo_individualizado_inicial.setter
    def periodo_individualizado_inicial(self, v: int):
        self.data[29] = v

    @property
    def periodo_individualizado_final(self) -> int:
        return self.data[30]

    @periodo_individualizado_final.setter
    def periodo_individualizado_final(self, v: int):
        self.data[30] = v

    @property
    def tamanho_registro_arquivos_individualizado(self) -> int:
        return self.data[31]

    @tamanho_registro_arquivos_individualizado.setter
    def tamanho_registro_arquivos_individualizado(self, v: int):
        self.data[31] = v

    @property
    def periodo_agregado_inicial(self) -> int:
        return self.data[32]

    @periodo_agregado_inicial.setter
    def periodo_agregado_inicial(self, v: int):
        self.data[32] = v

    @property
    def periodo_agregado_final(self) -> int:
        return self.data[33]

    @periodo_agregado_final.setter
    def periodo_agregado_final(self, v: int):
        self.data[33] = v

    @property
    def tamanho_registro_arquivos_agregado(self) -> int:
        return self.data[34]

    @tamanho_registro_arquivos_agregado.setter
    def tamanho_registro_arquivos_agregado(self, v: int):
        self.data[34] = v

    @property
    def ultimo_registro_cortes_periodos(self) -> List[int]:
        offset = self.__offset_primeiro_registro()
        return self.data[offset : offset + self.__tamanho_segundo_registro]

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
            offset : offset + self.numero_rees * self.numero_periodos_estudo
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
            return 0.0
        offset = self.__offset_setimo_registro() + 1
        return self.data[offset]

    @property
    def flag_aplicacao_sar(self) -> List[int]:
        if self.usa_sar == 0:
            return []
        offset = self.__offset_setimo_registro() + 2
        return self.data[
            offset : offset + self.numero_periodos_estudo + 2 * self.npea
        ]

    @property
    def flag_cvar(self) -> int:
        if self.usa_cvar == 0:
            return []
        offset = self.__offset_oitavo_registro()
        return self.data[offset]

    @property
    def alfa_cvar(self) -> List[float]:
        if self.usa_cvar == 0:
            return []
        offset = self.__offset_oitavo_registro() + 1
        return self.data[
            offset : offset + self.numero_periodos_estudo + 2 * self.npea
        ]

    @property
    def lambda_cvar(self) -> List[float]:
        if self.usa_cvar == 0:
            return []
        offset = (
            self.__offset_oitavo_registro()
            + 1
            + self.numero_periodos_estudo
            + 2 * self.npea
        )
        return self.data[
            offset : offset + self.numero_periodos_estudo + 2 * self.npea
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
            + self.numero_total_submercados
            + self.numero_rees
        )
        return self.data[
            offset : offset + self.numero_rees + self.numero_submercados
        ]

    @property
    def codigos_rees_submercados(self) -> List[int]:
        offset = (
            self.__offset_decimo_registro()
            + 2 * self.numero_total_submercados
            + 2 * self.numero_rees
        )
        return self.data[
            offset : offset + self.numero_rees + self.numero_submercados
        ]
