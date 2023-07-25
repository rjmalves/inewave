from cfinterface.components.section import Section
import numpy as np  # type: ignore
from typing import List
from typing import IO


class SecaoDadosForwarh(Section):
    """
    Registro com os dados da execução do caso existente no
    arquivo forwarh.dat
    """

    ZVAZ = 100

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosForwarh):
            return False
        bloco: SecaoDadosForwarh = o
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
        _ = np.frombuffer(
            file.read(1 * 4),
            dtype=np.int32,
            count=1,
        )
        nome_caso = file.read(80).decode("utf-8").strip()
        dados_primeiro_bloco = np.frombuffer(
            file.read(7 * 4),
            dtype=np.int32,
            count=7,
        )
        self.data = [nome_caso] + list(dados_primeiro_bloco)
        dados_segundo_bloco = np.frombuffer(
            file.read((self.numero_submercados + 12) * 4),
            dtype=np.int32,
            count=self.numero_submercados + 12,
        )
        self.data += list(dados_segundo_bloco)
        dados_terceiro_bloco = np.frombuffer(
            file.read((self.__class__.ZVAZ + 4) * 4),
            dtype=np.int32,
            count=self.__class__.ZVAZ + 4,
        )
        self.data += list(dados_terceiro_bloco)

    def __offset_primeiro_bloco(self):
        return 7 + self.numero_submercados

    def __offset_segundo_bloco(self):
        return self.__offset_primeiro_bloco() + 13 + self.__class__.ZVAZ

    @property
    def nome_caso(self) -> str:
        return self.data[0]

    @nome_caso.setter
    def nome_caso(self, v: str):
        self.data[0] = v

    @property
    def numero_rees(self) -> int:
        return self.data[1]

    @numero_rees.setter
    def numero_rees(self, v: int):
        self.data[1] = v

    @property
    def numero_submercados(self) -> int:
        return self.data[2]

    @numero_submercados.setter
    def numero_submercados(self, v: int):
        self.data[2] = v

    @property
    def numero_series_gravadas(self) -> int:
        return self.data[3]

    @numero_series_gravadas.setter
    def numero_series_gravadas(self, v: int):
        self.data[3] = v

    @property
    def numero_aberturas(self) -> int:
        return self.data[4]

    @numero_aberturas.setter
    def numero_aberturas(self, v: int):
        self.data[4] = v

    @property
    def numero_estagios_estudo(self) -> int:
        return self.data[5]

    @numero_estagios_estudo.setter
    def numero_estagios_estudo(self, v: int):
        self.data[5] = v

    @property
    def intervalo_series_gravadas(self) -> int:
        return self.data[6]

    @intervalo_series_gravadas.setter
    def intervalo_series_gravadas(self, v: int):
        self.data[6] = v

    @property
    def numero_classes_termicas_submercados(self) -> List[int]:
        return self.data[7 : self.__offset_primeiro_bloco()]

    @numero_classes_termicas_submercados.setter
    def numero_classes_termicas_submercados(self, v: List[int]):
        self.data = (
            self.data[:7] + v + self.data[: self.__offset_primeiro_bloco()]
        )

    @property
    def numero_patamares_deficit(self) -> int:
        return self.data[self.__offset_primeiro_bloco()]

    @numero_patamares_deficit.setter
    def numero_patamares_deficit(self, v: int):
        self.data[self.__offset_primeiro_bloco()] = v

    @property
    def tamanho_registro_arquivo_forward(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 1]

    @tamanho_registro_arquivo_forward.setter
    def tamanho_registro_arquivo_forward(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 1] = v

    @property
    def numero_registros_arquivo_forward(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 2]

    @numero_registros_arquivo_forward.setter
    def numero_registros_arquivo_forward(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 2] = v

    @property
    def numero_registros_necessarios_estagio(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 3]

    @numero_registros_necessarios_estagio.setter
    def numero_registros_necessarios_estagio(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 3] = v

    @property
    def ano_inicio_estudo(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 4]

    @ano_inicio_estudo.setter
    def ano_inicio_estudo(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 4] = v

    @property
    def ano_inicio_historico_vazoes(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 5]

    @ano_inicio_historico_vazoes.setter
    def ano_inicio_historico_vazoes(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 5] = v

    @property
    def numero_anos_descontar_historico_vazoes(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 6]

    @numero_anos_descontar_historico_vazoes.setter
    def numero_anos_descontar_historico_vazoes(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 6] = v

    @property
    def numero_estagios_ano(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 7]

    @numero_estagios_ano.setter
    def numero_estagios_ano(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 7] = v

    @property
    def mes_inicio_estudo(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 8]

    @mes_inicio_estudo.setter
    def mes_inicio_estudo(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 8] = v

    @property
    def mes_inicio_pre_estudo(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 9]

    @mes_inicio_pre_estudo.setter
    def mes_inicio_pre_estudo(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 9] = v

    @property
    def numero_estagios_pre_estudo(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 10]

    @numero_estagios_pre_estudo.setter
    def numero_estagios_pre_estudo(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 10] = v

    @property
    def numero_patamares_carga(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 11]

    @numero_patamares_carga.setter
    def numero_patamares_carga(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 11] = v

    @property
    def ordem_maxima_parp(self) -> int:
        return self.data[self.__offset_primeiro_bloco() + 12]

    @ordem_maxima_parp.setter
    def ordem_maxima_parp(self, v: int):
        self.data[self.__offset_primeiro_bloco() + 12] = v

    @property
    def ano_inicio_series_historicas_simuladas(self) -> List[int]:
        return self.data[
            self.__offset_primeiro_bloco() + 13 : self.__offset_segundo_bloco()
        ]

    @ano_inicio_series_historicas_simuladas.setter
    def ano_inicio_series_historicas_simuladas(self, v: List[int]):
        self.data = (
            self.data[self.__offset_primeiro_bloco() + 13 :]
            + v
            + self.data[self.__offset_segundo_bloco() :]
        )

    @property
    def numero_anos_historico_vazoes(self) -> int:
        return self.data[self.__offset_segundo_bloco()]

    @numero_anos_historico_vazoes.setter
    def numero_anos_historico_vazoes(self, v: int):
        self.data[self.__offset_segundo_bloco()] = v

    @property
    def numero_total_submercados(self) -> int:
        return self.data[self.__offset_segundo_bloco() + 1]

    @numero_total_submercados.setter
    def numero_total_submercados(self, v: int):
        self.data[self.__offset_segundo_bloco() + 1] = v

    @property
    def simulacao_final_individualizada(self) -> int:
        return self.data[self.__offset_segundo_bloco() + 2]

    @simulacao_final_individualizada.setter
    def simulacao_final_individualizada(self, v: int):
        self.data[self.__offset_segundo_bloco() + 2] = v
