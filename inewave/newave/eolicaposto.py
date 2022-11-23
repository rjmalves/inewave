from typing import Type, TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicaposto import (
    RegistroPEEPostoVento,
    RegistroPostoVentoCadastro,
)


class EolicaPosto(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos postos
    de vento e sua associação com os PEE.
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroPEEPostoVento,
        RegistroPostoVentoCadastro,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eolica-posto.csv"
    ) -> "EolicaPosto":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="eolica-posto.csv"):
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

    def posto_vento_cad(
        self,
        codigo_posto: Optional[int] = None,
        nome_posto: Optional[str] = None,
    ) -> Optional[
        Union[
            RegistroPostoVentoCadastro,
            List[RegistroPostoVentoCadastro],
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
        return self.__obtem_registros_com_filtros(
            RegistroPostoVentoCadastro,
            codigo_posto=codigo_posto,
            nome_posto=nome_posto,
        )

    def pee_posto(
        self,
        codigo_pee: Optional[datetime] = None,
        codigo_posto: Optional[datetime] = None,
    ) -> Optional[Union[RegistroPEEPostoVento, List[RegistroPEEPostoVento]]]:
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
        return self.__obtem_registros_com_filtros(
            RegistroPEEPostoVento,
            codigo_pee=codigo_pee,
            codigo_posto=codigo_posto,
        )
