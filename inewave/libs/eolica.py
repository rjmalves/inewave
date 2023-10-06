from typing import TypeVar, List, Optional, Union, Type
from datetime import datetime
import pandas as pd  # type: ignore
from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.libs.modelos.eolica import (
    RegistroEolicaCadastro,
    RegistroEolicaCadastroConjuntoAerogeradores,
    RegistroEolicaCadastroAerogerador,
    RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo,
    RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
    RegistroPEECadastro,
    RegistroPEEPotenciaInstaladaPeriodo,
    RegistroEolicaConfiguracao,
    RegistroPEEConfiguracaoPeriodo,
    RegistroEolicaFTE,
    RegistroPEEFTE,
    RegistroEolicaGeracaoPeriodo,
    RegistroEolicaGeracaoPatamar,
    RegistroPEEGeracaoPatamar,
    RegistroEolicaHistoricoVentoHorizonte,
    RegistroEolicaHistoricoVento,
    RegistroHistoricoVentoHorizonte,
    RegistroHistoricoVento,
    RegistroPEEPostoVento,
    RegistroPostoVentoCadastro,
    RegistroEolicaSubmercado,
    RegistroPEESubmercado,
)


class Eolica(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao dados
    das usinas eólicas do sistema.
    """

    T = TypeVar("T", bound=Register)

    REGISTERS = [
        RegistroEolicaCadastroAerogerador,
        RegistroEolicaCadastroConjuntoAerogeradores,
        RegistroEolicaCadastro,
        RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo,
        RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
        RegistroPEECadastro,
        RegistroPEEPotenciaInstaladaPeriodo,
        RegistroEolicaConfiguracao,
        RegistroPEEConfiguracaoPeriodo,
        RegistroEolicaFTE,
        RegistroPEEFTE,
        RegistroEolicaGeracaoPeriodo,
        RegistroEolicaGeracaoPatamar,
        RegistroPEEGeracaoPatamar,
        RegistroEolicaHistoricoVentoHorizonte,
        RegistroEolicaHistoricoVento,
        RegistroHistoricoVentoHorizonte,
        RegistroHistoricoVento,
        RegistroPEEPostoVento,
        RegistroPostoVentoCadastro,
        RegistroEolicaSubmercado,
        RegistroPEESubmercado,
    ]

    def __registros_ou_df(
        self, t: Type[T], **kwargs
    ) -> Optional[Union[T, List[T], pd.DataFrame]]:
        if kwargs.get("df"):
            return self._as_df(t)
        else:
            kwargs_sem_df = {k: v for k, v in kwargs.items() if k != "df"}
            return self.data.get_registers_of_type(t, **kwargs_sem_df)

    def eolica_cadastro(
        self,
        codigo_eolica: Optional[int] = None,
        nome_eolica: Optional[str] = None,
        quantidade_conjuntos: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaCadastro, List[RegistroEolicaCadastro], pd.DataFrame
        ]
    ]:
        """
        Obtém um registro que cadastra uma usina eólica.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param nome_eolica: nome da usina
        :type nome_eolica: str | None
        :param quantidade_conjuntos: quantidade de conjuntos de geradores
        :type quantidade_conjuntos: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaCadastro` |
            list[:class:`RegistroEolicaCadastro`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaCadastro,
            codigo_eolica=codigo_eolica,
            nome_eolica=nome_eolica,
            quantidade_conjuntos=quantidade_conjuntos,
            df=df,
        )

    def eolica_cadastro_conjunto_aerogeradores(
        self,
        codigo_eolica: Optional[int] = None,
        indice_conjunto: Optional[int] = None,
        nome_conjunto: Optional[str] = None,
        quantidade_aerogeradores: Optional[int] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaCadastroConjuntoAerogeradores,
            List[RegistroEolicaCadastroConjuntoAerogeradores],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que cadastra um conjunto de aerogeradores
        de uma usina.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param indice_conjunto: código do conjunto de geradores da usina
        :type indice_conjunto: int | None
        :param nome_conjunto: nome do conjunto
        :type nome_conjunto: str | None
        :param quantidade_aerogeradores: quantidade de geradores no conjunto
        :type quantidade_aerogeradores: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaCadastroConjuntoAerogeradores` |
            list[:class:`RegistroEolicaCadastroConjuntoAerogeradores`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaCadastroConjuntoAerogeradores,
            codigo_eolica=codigo_eolica,
            indice_conjunto=indice_conjunto,
            nome_conjunto=nome_conjunto,
            quantidade_aerogeradores=quantidade_aerogeradores,
            df=df,
        )

    def eolica_cadastro_aerogerador(
        self,
        codigo_eolica: Optional[int] = None,
        indice_conjunto: Optional[int] = None,
        velocidade_cutin: Optional[float] = None,
        velocidade_nominal: Optional[float] = None,
        velocidade_cutout: Optional[float] = None,
        potencia_velocidade_cutin: Optional[float] = None,
        potencia_velocidade_nominal: Optional[float] = None,
        potencia_velocidade_cutout: Optional[float] = None,
        altura_torre: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaCadastroAerogerador,
            List[RegistroEolicaCadastroAerogerador],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que o cadastro de um conjunto de aerogeradores
        de uma usina.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: float | None
        :param indice_conjunto: código do conjunto de geradores da usina
        :type indice_conjunto: float | None
        :param velocidade_cutin: velocidade de cutin do gerador
        :type velocidade_cutin: float | None
        :param velocidade_nominal: velocidade nominal do gerador
        :type velocidade_nominal: float | None
        :param velocidade_cutout: velocidade de cutout do gerador
        :type velocidade_cutout: float | None
        :param potencia_velocidade_cutin: potência na velocidade de cutin
        :type potencia_velocidade_cutin: float | None
        :param potencia_velocidade_nominal: potência na velocidade nominal
        :type potencia_velocidade_nominal: float | None
        :param potencia_velocidade_cutout: potência na velocidade cutout
        :type potencia_velocidade_cutout: float | None
        :param altura_torre: altura da torre do gerador
        :type altura_torre: float | None

        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaCadastroAerogerador` |
            list[:class:`RegistroEolicaCadastroAerogerador`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaCadastroAerogerador,
            codigo_eolica=codigo_eolica,
            indice_conjunto=indice_conjunto,
            velocidade_cutin=velocidade_cutin,
            velocidade_nominal=velocidade_nominal,
            velocidade_cutout=velocidade_cutout,
            potencia_velocidade_cutin=potencia_velocidade_cutin,
            potencia_velocidade_nominal=potencia_velocidade_nominal,
            potencia_velocidade_cutout=potencia_velocidade_cutout,
            altura_torre=altura_torre,
            df=df,
        )

    def eolica_conjunto_aerogeradores_quantidade_operando_periodo(
        self,
        codigo_eolica: Optional[int] = None,
        indice_conjunto: Optional[int] = None,
        periodo_inicial: Optional[datetime] = None,
        periodo_final: Optional[datetime] = None,
        numero_aerogeradores: Optional[int] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo,
            List[RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que o cadastro de um conjunto de aerogeradores
        de uma usina.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param indice_conjunto: código do conjunto de geradores da usina
        :type indice_conjunto: int | None
        :param periodo_inicial: período de início de operação
        :type periodo_inicial: datetime | None
        :param periodo_final: período de fim de operação
        :type periodo_final: datetime | None
        :param numero_aerogeradores: número de geradores operando
        :type numero_aerogeradores: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo` |
            list[:class:`RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo,
            codigo_eolica=codigo_eolica,
            indice_conjunto=indice_conjunto,
            periodo_inicial=periodo_inicial,
            periodo_final=periodo_final,
            numero_aerogeradores=numero_aerogeradores,
            df=df,
        )

    def eolica_conjunto_aerogeradores_potencia_efetiva_periodo(
        self,
        codigo_eolica: Optional[int] = None,
        indice_conjunto: Optional[int] = None,
        periodo_inicial: Optional[datetime] = None,
        periodo_final: Optional[datetime] = None,
        potencia_efetiva: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
            List[RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a potência efetiva por período
        para um conjunto de aerogeradores.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param indice_conjunto: código do conjunto de geradores da usina
        :type indice_conjunto: int | None
        :param periodo_inicial: período de início de operação
        :type periodo_inicial: datetime | None
        :param periodo_final: período de fim de operação
        :type periodo_final: datetime | None
        :param potencia_efetiva: potência efetiva do conjunto de aerogeradores
        :type potencia_efetiva: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva` |
            list[:class:`RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
            codigo_eolica=codigo_eolica,
            indice_conjunto=indice_conjunto,
            periodo_inicial=periodo_inicial,
            periodo_final=periodo_final,
            potencia_efetiva=potencia_efetiva,
            df=df,
        )

    def pee_cad(
        self,
        codigo_pee: Optional[int] = None,
        nome_pee: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroPEECadastro, List[RegistroPEECadastro], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra um PEE.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param nome_pee: nome do PEE
        :type nome_pee: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEECadastro` |
            list[:class:`RegistroPEECadastro`] | None
        """
        return self.__registros_ou_df(
            RegistroPEECadastro,
            codigo_pee=codigo_pee,
            nome_pee=nome_pee,
            df=df,
        )

    def pee_pot_inst_per(
        self,
        codigo_pee: Optional[int] = None,
        periodo_inicial: Optional[datetime] = None,
        periodo_final: Optional[datetime] = None,
        potencia_instalada: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroPEEPotenciaInstaladaPeriodo,
            List[RegistroPEEPotenciaInstaladaPeriodo],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a potência instalada por período
        para um PEE.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param periodo_inicial: período de início de operação
        :type periodo_inicial: datetime | None
        :param periodo_final: período de fim de operação
        :type periodo_final: datetime | None
        :param potencia_instalada: potência efetiva do PEE
        :type potencia_instalada: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEPotenciaInstaladaPeriodo` |
            list[:class:`RegistroPEEPotenciaInstaladaPeriodo`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEPotenciaInstaladaPeriodo,
            codigo_pee=codigo_pee,
            periodo_inicial=periodo_inicial,
            periodo_final=periodo_final,
            potencia_instalada=potencia_instalada,
            df=df,
        )

    def eolica_configuracao(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        estado_operacao: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaConfiguracao,
            List[RegistroEolicaConfiguracao],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a configuração de operação para
        uma usina eólica em um período.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param data_inicial: período de início da configuração
        :type data_inicial: datetime | None
        :param data_final: período de fim da configuração
        :type data_final: datetime | None
        :param estado_operacao: tipo de operação
        :type estado_operacao: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaConfiguracao` |
            list[:class:`RegistroEolicaConfiguracao`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaConfiguracao,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            estado_operacao=estado_operacao,
            df=df,
        )

    def pee_config_per(
        self,
        codigo_pee: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        estado_operacao: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroPEEConfiguracaoPeriodo,
            List[RegistroPEEConfiguracaoPeriodo],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a configuração de operação para
        um PEE em um período.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param data_inicial: período de início da configuração
        :type data_inicial: datetime | None
        :param data_final: período de fim da configuração
        :type data_final: datetime | None
        :param estado_operacao: tipo de operação
        :type estado_operacao: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEConfiguracaoPeriodo` |
            list[:class:`RegistroPEEConfiguracaoPeriodo`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEConfiguracaoPeriodo,
            codigo_pee=codigo_pee,
            data_inicial=data_inicial,
            data_final=data_final,
            estado_operacao=estado_operacao,
            df=df,
        )

    def eolica_funcao_producao(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        coeficiente_linear: Optional[float] = None,
        coeficiente_angular: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroEolicaFTE, List[RegistroEolicaFTE], pd.DataFrame]
    ]:
        """
        Obtém um registro que contém a função de produção vento-geração
        para um período de tempo.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param data_inicial: a data inicial de validade para a função
        :type data_inicial: datetime | None
        :param data_final: a data final de validade para a função
        :type data_final: datetime | None
        :param coeficiente_linear: o coeficiente linear
        :type coeficiente_linear: float | None
        :param coeficiente_angular: o coeficiente angular
        :type coeficiente_angular: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaFTE` |
            list[:class:`RegistroEolicaFTE`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaFTE,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            coeficiente_linear=coeficiente_linear,
            coeficiente_angular=coeficiente_angular,
            df=df,
        )

    def pee_fpvp_lin_pu_per(
        self,
        codigo_pee: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        coeficiente_linear: Optional[float] = None,
        coeficiente_angular: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[RegistroPEEFTE, List[RegistroPEEFTE], pd.DataFrame]]:
        """
        Obtém um registro que contém a função de produção vento-geração
        para um período de tempo para um PEE, em p.u.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param data_inicial: a data inicial de validade para a função
        :type data_inicial: datetime | None
        :param data_final: a data final de validade para a função
        :type data_final: datetime | None
        :param coeficiente_linear: o coeficiente linear
        :type coeficiente_linear: float | None
        :param coeficiente_angular: o coeficiente angular
        :type coeficiente_angular: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEFTE` |
            list[:class:`RegistroPEEFTE`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEFTE,
            codigo_pee=codigo_pee,
            data_inicial=data_inicial,
            data_final=data_final,
            coeficiente_linear=coeficiente_linear,
            coeficiente_angular=coeficiente_angular,
            df=df,
        )

    def eolica_geracao_periodo(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        geracao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaGeracaoPeriodo,
            List[RegistroEolicaGeracaoPeriodo],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém o valor de geração para uma usina
        eólica durante um período.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicial: data de início do histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do histórico
        :type data_final: datetime | None
        :param geracao: valor de geração
        :type geracao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaGeracaoPeriodo` |
            list[:class:`RegistroEolicaGeracaoPeriodo`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaGeracaoPeriodo,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            geracao=geracao,
            df=df,
        )

    def eolica_geracao_profundidade_periodo_patamar(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        indice_patamar: Optional[int] = None,
        profundidade: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaGeracaoPatamar,
            List[RegistroEolicaGeracaoPatamar],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a profundidade de um patamar
        de geração para um período.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicial: data de início do registro histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do registro histórico
        :type data_final: datetime | None
        :param indice_patamar: patamar de geração eólica
        :type indice_patamar: int | None
        :param profundidade: profundidade do patamar de geração
        :type profundidade: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaGeracaoPatamar` |
            list[:class:`RegistroEolicaGeracaoPatamar`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaGeracaoPatamar,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            indice_patamar=indice_patamar,
            profundidade=profundidade,
            df=df,
        )

    def pee_ger_prof_per_pat(
        self,
        codigo_pee: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        indice_patamar: Optional[int] = None,
        profundidade: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroPEEGeracaoPatamar,
            List[RegistroPEEGeracaoPatamar],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a profundidade de um patamar
        de geração para um período, para um PEE.

        :param codigo_pee: código do PEE
        :type codigo_pee: int | None
        :param data_inicial: data de início do registro histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do registro histórico
        :type data_final: datetime | None
        :param indice_patamar: patamar de geração eólica
        :type indice_patamar: int | None
        :param profundidade: profundidade do patamar de geração
        :type profundidade: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEGeracaoPatamar` |
            list[:class:`RegistroPEEGeracaoPatamar`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEGeracaoPatamar,
            codigo_pee=codigo_pee,
            data_inicial=data_inicial,
            data_final=data_final,
            indice_patamar=indice_patamar,
            profundidade=profundidade,
            df=df,
        )

    def eolica_historico_vento_horizonte(
        self,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaHistoricoVentoHorizonte,
            List[RegistroEolicaHistoricoVentoHorizonte],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém o horizonte de um histórico.

        :param data_inicial: data de início do histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do histórico
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaHistoricoVentoHorizonte` |
            list[:class:`RegistroEolicaHistoricoVentoHorizonte`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaHistoricoVentoHorizonte,
            data_inicial=data_inicial,
            data_final=data_final,
            df=df,
        )

    def eolica_historico_vento(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        velocidade: Optional[float] = None,
        direcao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaHistoricoVento,
            List[RegistroEolicaHistoricoVento],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a o valor de vento para um
        intervalo do histórico.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicial: data de início do registro histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do registro histórico
        :type data_final: datetime | None
        :param velocidade: velocidade do vento
        :type velocidade: float | None
        :param direcao: direção do vento
        :type direcao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaHistoricoVento` |
            list[:class:`RegistroEolicaHistoricoVento`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaHistoricoVento,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            velocidade=velocidade,
            direcao=direcao,
            df=df,
        )

    def vento_hist_horiz(
        self,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroHistoricoVentoHorizonte,
            List[RegistroHistoricoVentoHorizonte],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém o horizonte de um histórico.

        :param data_inicial: data de início do histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do histórico
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroHistoricoVentoHorizonte` |
            list[:class:`RegistroHistoricoVentoHorizonte`] | None
        """
        return self.__registros_ou_df(
            RegistroHistoricoVentoHorizonte,
            data_inicial=data_inicial,
            data_final=data_final,
            df=df,
        )

    def vento_hist(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        velocidade: Optional[float] = None,
        direcao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroHistoricoVento, List[RegistroHistoricoVento], pd.DataFrame
        ]
    ]:
        """
        Obtém um registro que contém a o valor de vento para um
        intervalo do histórico.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicial: data de início do registro histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do registro histórico
        :type data_final: datetime | None
        :param velocidade: velocidade do vento
        :type velocidade: float | None
        :param direcao: direção do vento
        :type direcao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroHistoricoVento` |
            list[:class:`RegistroHistoricoVento`] | None
        """
        return self.__registros_ou_df(
            RegistroHistoricoVento,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            velocidade=velocidade,
            direcao=direcao,
            df=df,
        )

    def posto_vento_cad(
        self,
        codigo_posto: Optional[int] = None,
        nome_posto: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroPostoVentoCadastro,
            List[RegistroPostoVentoCadastro],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém o cadastro de um posto
            de vento.

        :param codigo_posto: código que identifica o posto
        :type codigo_posto: int | None
        :param nome_posto: nome do posto de vento
        :type nome_posto: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPostoVentoCadastro` |
            list[:class:`RegistroPostoVentoCadastro`] | None
        """
        return self.__registros_ou_df(
            RegistroPostoVentoCadastro,
            codigo_posto=codigo_posto,
            nome_posto=nome_posto,
            df=df,
        )

    def pee_posto(
        self,
        codigo_pee: Optional[datetime] = None,
        codigo_posto: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroPEEPostoVento, List[RegistroPEEPostoVento], pd.DataFrame]
    ]:
        """
        Obtém um registro que contém o mapeamento entre um posto
            e um PEE.

        :param codigo_pee: código que identifica o PEE
        :type codigo_pee: int | None
        :param codigo_posto: código que identifica o posto
        :type codigo_posto: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEPostoVento` |
            list[:class:`RegistroPEEPostoVento`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEPostoVento,
            codigo_pee=codigo_pee,
            codigo_posto=codigo_posto,
            df=df,
        )

    def eolica_submercado(
        self,
        codigo_eolica: Optional[int] = None,
        codigo_submercado: Optional[int] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroEolicaSubmercado,
            List[RegistroEolicaSubmercado],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém o mapeamento usina-submercado.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param codigo_submercado: código que especifica o submercado
        :type codigo_submercado: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaSubmercado` |
            list[:class:`RegistroEolicaSubmercado`] | None
        """
        return self.__registros_ou_df(
            RegistroEolicaSubmercado,
            codigo_eolica=codigo_eolica,
            codigo_submercado=codigo_submercado,
            df=df,
        )

    def pee_subm(
        self,
        codigo_pee: Optional[int] = None,
        codigo_submercado: Optional[int] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroPEESubmercado, List[RegistroPEESubmercado], pd.DataFrame]
    ]:
        """
        Obtém um registro que contém o mapeamento PEE-submercado.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param codigo_submercado: código que especifica o submercado
        :type codigo_submercado: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEESubmercado` |
            list[:class:`RegistroPEESubmercado`] | None
        """
        return self.__registros_ou_df(
            RegistroPEESubmercado,
            codigo_pee=codigo_pee,
            codigo_submercado=codigo_submercado,
            df=df,
        )
