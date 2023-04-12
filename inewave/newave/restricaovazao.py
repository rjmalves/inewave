from typing import Type, TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.restricaovazao import (
    RegistroRHQ,
    RegistroRHQHorizPer,
    RegistroRHQLsLPPVoli,
)


class RestricaoVazao(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao cadastro
    das restrições lineares por partes no domínio de vazão (RHQ).
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroRHQLsLPPVoli,
        RegistroRHQHorizPer,
        RegistroRHQ,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="restricao-vazao.csv"
    ) -> "RestricaoVazao":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(
        self, diretorio: str, nome_arquivo="restricao-vazao.csv"
    ):
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

    def rhq(
        self,
        codigo_restricao: Optional[int] = None,
        formula: Optional[str] = None,
    ) -> Optional[Union[RegistroRHQ, List[RegistroRHQ]]]:
        """
        Obtém um registro que cadastra uma usina restrição linear por
        partes de vazão (UHE).

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param formula: equação da restrição
        :type formula: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQ` |
            list[:class:`RegistroRHQ`] | None
        """
        return self.__obtem_registros_com_filtros(
            RegistroRHQ,
            codigo_restricao=codigo_restricao,
            formula=formula,
        )

    def rhq_horiz_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Optional[Union[RegistroRHQHorizPer, List[RegistroRHQHorizPer]]]:
        """
        Obtém um registro que cadastra o horizonte de validade de uma
        restrição linear por partes de vazão.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data inicial de validade da restrição
        :type data_inicial: datetime | None
        :param data_final: data final de validade da restrição
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQHorizPer` |
            list[:class:`RegistroRHQHorizPer`] | None
        """
        return self.__obtem_registros_com_filtros(
            RegistroRHQHorizPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def rhq_ls_lpp_voli(
        self,
        codigo_restricao: Optional[int] = None,
        indice_reta: Optional[int] = None,
        coeficiente_angular: Optional[float] = None,
        coeficiente_linear: Optional[float] = None,
    ) -> Optional[Union[RegistroRHQLsLPPVoli, List[RegistroRHQLsLPPVoli]]]:
        """
        Obtém um registro que cadastra as retas da restrição linear
        por partes de vazão.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param indice_reta: índice da reta definida
        :type indice_reta: int | None
        :param coeficiente_angular: coeficiente angular da reta
        :type coeficiente_angular: float | None
        :param coeficiente_linear: coeficiente linear da reta
        :type coeficiente_linear: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQLsLPPVoli` |
            list[:class:`RegistroRHQLsLPPVoli`] | None
        """
        return self.__obtem_registros_com_filtros(
            RegistroRHQLsLPPVoli,
            codigo_restricao=codigo_restricao,
            indice_reta=indice_reta,
            coeficiente_angular=coeficiente_angular,
            coeficiente_linear=coeficiente_linear,
        )
