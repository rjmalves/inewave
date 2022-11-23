from typing import Type, TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicahistorico import (
    RegistroEolicaHistoricoVentoHorizonte,
    RegistroEolicaHistoricoVento,
    RegistroHistoricoVentoHorizonte,
    RegistroHistoricoVento,
)


class EolicaHistorico(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao histórico
    de ventos das usinas eólicas.
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroEolicaHistoricoVentoHorizonte,
        RegistroEolicaHistoricoVento,
        RegistroHistoricoVentoHorizonte,
        RegistroHistoricoVento,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="hist-ventos.csv"
    ) -> "EolicaHistorico":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="hist-ventos.csv"):
        self.write(diretorio, nome_arquivo)

    def __registros_por_tipo(self, registro: Type[T]) -> List[T]:
        """
        Obtém os registro de um tipo, se houver algum no arquivo.

        :param registro: Um tipo de registro para ser lido
        :type registro: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int

        """
        return [b for b in self.data.of_type(registro)]

    def __obtem_registros(self, tipo: Type[T]) -> List[T]:
        return self.__registros_por_tipo(tipo)

    def __obtem_registros_com_filtros(
        self, tipo_registro: Type[T], **kwargs
    ) -> Optional[Union[T, List[T]]]:
        def __atende(r) -> bool:
            condicoes: List[bool] = []
            for k, v in kwargs.items():
                if v is not None:
                    condicoes.append(getattr(r, k) == v)
            return all(condicoes)

        regs_filtro = [
            r for r in self.__obtem_registros(tipo_registro) if __atende(r)
        ]
        if len(regs_filtro) == 0:
            return None
        elif len(regs_filtro) == 1:
            return regs_filtro[0]
        else:
            return regs_filtro

    def cria_registro(self, anterior: Register, registro: Register):
        """
        Adiciona um registro ao arquivo após um outro registro previamente
        existente.

        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.add_after(anterior, registro)

    def deleta_registro(self, registro: Register):
        """
        Remove um registro existente no arquivo.

        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.remove(registro)

    def append_registro(self, registro: Register):
        """
        Adiciona um registro ao arquivo na última posição.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.append(registro)

    def preppend_registro(self, registro: Register):
        """
        Adiciona um registro ao arquivo na primeira posição.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.preppend(registro)

    def eolica_historico_vento_horizonte(
        self,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Optional[
        Union[
            RegistroEolicaHistoricoVentoHorizonte,
            List[RegistroEolicaHistoricoVentoHorizonte],
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
        return self.__obtem_registros_com_filtros(
            RegistroEolicaHistoricoVentoHorizonte,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def eolica_historico_vento(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        velocidade: Optional[float] = None,
        direcao: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroEolicaHistoricoVento,
            List[RegistroEolicaHistoricoVento],
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
        return self.__obtem_registros_com_filtros(
            RegistroEolicaHistoricoVento,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            velocidade=velocidade,
            direcao=direcao,
        )

    def vento_hist_horiz(
        self,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Optional[
        Union[
            RegistroHistoricoVentoHorizonte,
            List[RegistroHistoricoVentoHorizonte],
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
        return self.__obtem_registros_com_filtros(
            RegistroHistoricoVentoHorizonte,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def vento_hist(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        velocidade: Optional[float] = None,
        direcao: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroHistoricoVento,
            List[RegistroHistoricoVento],
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
        return self.__obtem_registros_com_filtros(
            RegistroHistoricoVento,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            velocidade=velocidade,
            direcao=direcao,
        )
