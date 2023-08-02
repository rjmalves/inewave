from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.cortesh import SecaoDadosCortesh

import pandas as pd  # type: ignore
from typing import TypeVar


class Cortesh(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes ao
    cabeçalho dos cortes de Benders.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosCortesh]
    STORAGE = "BINARY"

    def __obtem_dados(self) -> SecaoDadosCortesh:
        dados = [r for r in self.data.of_type(SecaoDadosCortesh)]
        return dados[0]

    @property
    def versao_newave(self) -> int:
        """
        A versão do NEWAVE como um número inteiro (ex. 280000).

        :return: A versão do NEWAVE
        :rtype: int
        """
        return self.__obtem_dados().versao_newave

    @versao_newave.setter
    def versao_newave(self, v: int):
        self.__obtem_dados().versao_newave = v

    @property
    def tamanho_corte(self) -> int:
        """
        O tamanho (em bytes) do registro que contém os coeficientes
        de um corte.

        :return: O tamanho do corte
        :rtype: int
        """
        return self.__obtem_dados().tamanho_corte

    @tamanho_corte.setter
    def tamanho_corte(self, v: int):
        self.__obtem_dados().tamanho_corte = v

    @property
    def tamanho_estado(self) -> int:
        """
        O tamanho (em bytes) do registro que contém um estado
        visitado durante o cálculo da política.

        :return: O tamanho do estado
        :rtype: int
        """
        return self.__obtem_dados().tamanho_estado

    @tamanho_estado.setter
    def tamanho_estado(self, v: int):
        self.__obtem_dados().tamanho_estado = v

    @property
    def numero_rees(self) -> int:
        """
        O número de REEs existentes no caso

        :return: O número de REEs
        :rtype: int
        """
        return self.__obtem_dados().numero_rees

    @numero_rees.setter
    def numero_rees(self, v: int):
        self.__obtem_dados().numero_rees = v

    @property
    def numero_estagios_pre(self) -> int:
        """
        O número de estágios no período pré-estudo.

        :return: O número de estágios do período pré
        :rtype: int
        """
        return self.__obtem_dados().numero_estagios_pre

    @numero_estagios_pre.setter
    def numero_estagios_pre(self, v: int):
        self.__obtem_dados().numero_estagios_pre = v

    @property
    def numero_estagios_estudo(self) -> int:
        """
        O número de estágios no período de estudo.

        :return: O número de estágios do período de estudo.
        :rtype: int
        """
        return self.__obtem_dados().numero_estagios_estudo

    @numero_estagios_estudo.setter
    def numero_estagios_estudo(self, v: int):
        self.__obtem_dados().numero_estagios_estudo = v

    @property
    def numero_estagios_pos(self) -> int:
        """
        O número de estágios no período pós estudo.

        :return: O número de estágios do período pós
        :rtype: int
        """
        return self.__obtem_dados().numero_estagios_pos

    @numero_estagios_pos.setter
    def numero_estagios_pos(self, v: int):
        self.__obtem_dados().numero_estagios_pos = v

    @property
    def numero_estagios_ano(self) -> int:
        """
        O número de estágios existentes ao longo de
        um ano.

        :return: O número de estágios por ano
        :rtype: int
        """
        return self.__obtem_dados().numero_estagios_ano

    @numero_estagios_ano.setter
    def numero_estagios_ano(self, v: int):
        self.__obtem_dados().numero_estagios_ano = v

    @property
    def numero_configuracoes(self) -> int:
        """
        O número de configurações do sistema existentes no caso

        :return: O número de configurações
        :rtype: int
        """
        return self.__obtem_dados().numero_configuracoes

    @numero_configuracoes.setter
    def numero_configuracoes(self, v: int):
        self.__obtem_dados().numero_configuracoes = v

    @property
    def numero_forwards(self) -> int:
        """
        O número de séries forward utilizadas no cálculo
        da política.

        :return: O número de séries
        :rtype: int
        """
        return self.__obtem_dados().numero_forwards

    @numero_forwards.setter
    def numero_forwards(self, v: int):
        self.__obtem_dados().numero_forwards = v

    @property
    def numero_patamares(self) -> int:
        """
        O número de patamares de carga.

        :return: O número de patamares
        :rtype: int
        """
        return self.__obtem_dados().numero_patamares

    @numero_patamares.setter
    def numero_patamares(self, v: int):
        self.__obtem_dados().numero_patamares = v

    @property
    def ano_inicio_estudo(self) -> int:
        """
        O ano de início do período de estudo.

        :return: O ano de início
        :rtype: int
        """
        return self.__obtem_dados().ano_inicio_estudo

    @ano_inicio_estudo.setter
    def ano_inicio_estudo(self, v: int):
        self.__obtem_dados().ano_inicio_estudo = v

    @property
    def mes_inicio_estudo(self) -> int:
        """
        O mês de início do período de estudo. Considera a contagem
        sempre desde o Janeiro do primeiro ano.

        :return: O índice do mês de início.
        :rtype: int
        """
        return self.__obtem_dados().mes_inicio_estudo

    @mes_inicio_estudo.setter
    def mes_inicio_estudo(self, v: int):
        self.__obtem_dados().mes_inicio_estudo = v

    @property
    def lag_maximo_gnl(self) -> int:
        """
        O lag máximo para decisão do despacho antecipado
        das usinas térmicas GNL que é considerado.

        :return: O lag máximo em número de meses
        :rtype: int
        """
        return self.__obtem_dados().lag_maximo_gnl

    @lag_maximo_gnl.setter
    def lag_maximo_gnl(self, v: int):
        self.__obtem_dados().lag_maximo_gnl = v

    @property
    def numero_submercados(self) -> int:
        """
        Número de total de submercados, considerando apenas
        mercados não-fictícios.

        :return: O número de submercados
        :rtype: int
        """
        return self.__obtem_dados().numero_submercados

    @numero_submercados.setter
    def numero_submercados(self, v: int):
        self.__obtem_dados().numero_submercados = v

    @property
    def numero_total_submercados(self) -> int:
        """
        Número de total de submercados, considerando mercados
        fictícios e não-fictícios.

        :return: O número de submercados
        :rtype: int
        """
        return self.__obtem_dados().numero_total_submercados

    @numero_total_submercados.setter
    def numero_total_submercados(self, v: int):
        self.__obtem_dados().numero_total_submercados = v

    @property
    def mes_agregacao(self) -> int:
        """
        O mês em que se inicia a agregação em REEs em casos
        híbridos. Considera a contagem sempre a partir de janeiro
        do primeiro ano, mesmo se o período de estudo
        se iniciar em outro mês.

        :return: O mês
        :rtype: int
        """
        return self.__obtem_dados().mes_agregacao

    @mes_agregacao.setter
    def mes_agregacao(self, v: int):
        self.__obtem_dados().mes_agregacao = v

    @property
    def numero_maximo_uhes(self) -> int:
        """
        Número máximo de UHEs existentes em algum estágio
        do caso.

        :return: O número de UHEs.
        :rtype: int
        """
        return self.__obtem_dados().numero_maximo_uhes

    @numero_maximo_uhes.setter
    def numero_maximo_uhes(self, v: int):
        self.__obtem_dados().numero_maximo_uhes = v

    @property
    def considera_afluencia_anual(self) -> int:
        """
        Flag para indicação se é utilizado o modelo PAR(p)-A
        para geração de cenários.

        :return: O valor do flag
        :rtype: int
        """
        return self.__obtem_dados().considera_afluencia_anual

    @considera_afluencia_anual.setter
    def considera_afluencia_anual(self, v: int):
        self.__obtem_dados().considera_afluencia_anual = v

    @property
    def tipo_agregacao_caso(self) -> int:
        """
        Flag para indicação do tipo de agregação do caso,
        entre agregado, híbrido ou totalmente individualizado.

        :return: O valor do flag
        :rtype: int
        """
        return self.__obtem_dados().tipo_agregacao_caso

    @tipo_agregacao_caso.setter
    def tipo_agregacao_caso(self, v: int):
        self.__obtem_dados().tipo_agregacao_caso = v

    @property
    def estagio_individualizado_inicial(self) -> int:
        """
        O índice do estágio em que se inicia a simulação
        individualizada em UHE.

        :return: O índice do estágio
        :rtype: int
        """
        return self.__obtem_dados().estagio_individualizado_inicial

    @estagio_individualizado_inicial.setter
    def estagio_individualizado_inicial(self, v: int):
        self.__obtem_dados().estagio_individualizado_inicial = v

    @property
    def estagio_individualizado_final(self) -> int:
        """
        O índice do estágio em que termina a simulação
        individualizada em UHE.

        :return: O índice do estágio
        :rtype: int
        """
        return self.__obtem_dados().estagio_individualizado_final

    @estagio_individualizado_final.setter
    def estagio_individualizado_final(self, v: int):
        self.__obtem_dados().estagio_individualizado_final = v

    @property
    def tamanho_registro_individualizado(self) -> int:
        """
        O tamanho (em número de bytes) de um registro de
        corte para estágio individualizado.

        :return: O tamanho (em bytes)
        :rtype: int
        """
        return self.__obtem_dados().tamanho_registro_individualizado

    @tamanho_registro_individualizado.setter
    def tamanho_registro_individualizado(self, v: int):
        self.__obtem_dados().tamanho_registro_individualizado = v

    @property
    def estagio_agregado_inicial(self) -> int:
        """
        O índice do estágio em que se inicia a simulação
        agregada em REE.

        :return: O índice do estágio
        :rtype: int
        """
        return self.__obtem_dados().estagio_agregado_inicial

    @estagio_agregado_inicial.setter
    def estagio_agregado_inicial(self, v: int):
        self.__obtem_dados().estagio_agregado_inicial = v

    @property
    def estagio_agregado_final(self) -> int:
        """
        O índice do estágio em que termina a simulação
        agregada em REE.

        :return: O índice do estágio
        :rtype: int
        """
        return self.__obtem_dados().estagio_agregado_final

    @estagio_agregado_final.setter
    def estagio_agregado_final(self, v: int):
        self.__obtem_dados().estagio_agregado_final = v

    @property
    def tamanho_registro_agregado(self) -> int:
        """
        O tamanho (em número de bytes) de um registro de
        corte para estágio agregado.

        :return: O tamanho (em bytes)
        :rtype: int
        """
        return self.__obtem_dados().tamanho_registro_agregado

    @tamanho_registro_agregado.setter
    def tamanho_registro_agregado(self, v: int):
        self.__obtem_dados().tamanho_registro_agregado = v

    @property
    def ultimo_registro_cortes_estagio(self) -> pd.DataFrame:
        """
        Retorna os dados dos índices do último registro
        de cortes para cada estágio, para leitura do
        arquivo `cortes.dat`.

        - tipo_estagio [pre, estudo, pos] (`str`)
        - estagio (`int`)
        - indice_ultimo_corte (`int`)

        :return: Os dados dos índices dos cortes em uma tabela.
        :rtype: pd.DataFrame
        """
        return self.__obtem_dados().ultimo_registro_cortes_estagio

    @property
    def dados_submercados(self) -> pd.DataFrame:
        """
        Retorna os dados dos submercados e do número
        de REEs por submercados

        - codigo_submercado (`int`)
        - nome_submercado (`str`)
        - numero_rees_submercado (`int`)

        :return: Os dados dos submercados em uma tabela.
        :rtype: pd.DataFrame
        """
        return self.__obtem_dados().dados_submercados

    @property
    def dados_uhes(self) -> pd.DataFrame:
        """
        Retorna os dados das UHEs existentes no
        estudo realizado.

        - codigo_usina (`int`)
        - indice_usina (`int`)
        - posto (`int`)
        - ficticia (`int`)
        - codigo_submercado (`int`)
        - mes_agregacao (`int`)
        - codigo_interno_ree (`int`)
        - nome_ree (`str`)
        - codigo_submercado (`int`)
        - nome_submercado (`str`)

        :return: Os dados das UHEs em uma tabela.
        :rtype: pd.DataFrame
        """
        return self.__obtem_dados().dados_uhes
