from typing import Type, TypeVar, List, Optional, Union

from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicasubmercado import (
    RegistroEolicaSubmercado,
)


class EolicaSubmercado(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao mapeamento
    de usinas eólicas e submercados.
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroEolicaSubmercado,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eolica-submercado.csv"
    ) -> "EolicaSubmercado":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(
        self, diretorio: str, nome_arquivo="eolica-submercado.csv"
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

    def eolica_submercado(
        self,
        codigo_eolica: Optional[int] = None,
        codigo_submercado: Optional[int] = None,
    ) -> Optional[
        Union[
            RegistroEolicaSubmercado,
            List[RegistroEolicaSubmercado],
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
        return self.__obtem_registros_com_filtros(
            RegistroEolicaSubmercado,
            codigo_eolica=codigo_eolica,
            codigo_submercado=codigo_submercado,
        )
