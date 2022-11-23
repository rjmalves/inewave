from typing import Type, TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicafte import RegistroEolicaFTE, RegistroPEEFTE


class EolicaFTE(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às funções de
    transferência vento-potência.
    """

    T = TypeVar("T")

    REGISTERS = [RegistroEolicaFTE, RegistroPEEFTE]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eolica-fte.csv"
    ) -> "EolicaFTE":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="eolica-fte.csv"):
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

    def eolica_funcao_producao(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        coeficiente_linear: Optional[float] = None,
        coeficiente_angular: Optional[float] = None,
    ) -> Optional[Union[RegistroEolicaFTE, List[RegistroEolicaFTE]]]:
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
        return self.__obtem_registros_com_filtros(
            RegistroEolicaFTE,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            coeficiente_linear=coeficiente_linear,
            coeficiente_angular=coeficiente_angular,
        )

    def pee_fpvp_lin_pu_per(
        self,
        codigo_pee: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        coeficiente_linear: Optional[float] = None,
        coeficiente_angular: Optional[float] = None,
    ) -> Optional[Union[RegistroPEEFTE, List[RegistroPEEFTE]]]:
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
        return self.__obtem_registros_com_filtros(
            RegistroPEEFTE,
            codigo_pee=codigo_pee,
            data_inicial=data_inicial,
            data_final=data_final,
            coeficiente_linear=coeficiente_linear,
            coeficiente_angular=coeficiente_angular,
        )
