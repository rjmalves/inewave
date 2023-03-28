from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from typing import IO


class SecaoDadosCortesH(Section):
    """
    Registro com os dados da execução do caso existente no
    arquivo cortesh.dat
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_cabecalho = Line(
            [
                IntegerField(size=4, starting_position=0),  # Versão NEWAVE
                IntegerField(size=4, starting_position=4),  # Tamanho Cortes
                IntegerField(size=4, starting_position=8),  # Tamanho Estados
                IntegerField(size=4, starting_position=12),  # Num REEs
                IntegerField(size=4, starting_position=16),  # Num Períodos PRE
                IntegerField(size=4, starting_position=20),  # Num Períodos EST
                IntegerField(size=4, starting_position=24),  # Num Períodos POS
                IntegerField(
                    size=4, starting_position=28
                ),  # Num Configurações
                IntegerField(size=4, starting_position=32),  # NPEA - ??
                IntegerField(size=4, starting_position=36),  # Num Forwards
                IntegerField(size=4, starting_position=40),  # Num Pat. Carga
                IntegerField(size=4, starting_position=44),  # Ano Inic. EST
                IntegerField(size=4, starting_position=48),  # Mes Inic. EST
                IntegerField(size=4, starting_position=52),  # Lag Máximo GNL
                IntegerField(size=4, starting_position=56),  # Mec. Aversão
                IntegerField(size=4, starting_position=60),  # Num Submercados
                IntegerField(size=4, starting_position=64),  # Num Subm + Fict
            ],
            storage="BINARY",
        )

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
        dados_cabecalho = self.__linha_cabecalho.read(
            file.read(self.__linha_cabecalho.size)
        )
        self.__numero_estagios = sum(dados_cabecalho[4:7])
        indices_ultimos_cortes_periodo = Line(
            [
                IntegerField(size=1, starting_position=0 + 1 * i)
                for i in range(self.__numero_estagios)
            ],
            storage="BINARY",
        )
        dados_ultimos_cortes = indices_ultimos_cortes_periodo.read(
            file.read(indices_ultimos_cortes_periodo.size)
        )
        self.data = dados_cabecalho + dados_ultimos_cortes

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
    def numero_configuracoes(self) -> int:
        return self.data[7]

    @numero_configuracoes.setter
    def numero_configuracoes(self, v: int):
        self.data[7] = v

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
