from typing import Type, TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicageracao import (
    RegistroEolicaGeracaoPeriodo,
    RegistroEolicaGeracaoPatamar,
)


class EolicaGeracao(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao histórico
    de geração das usinas eólicas.
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroEolicaGeracaoPeriodo,
        RegistroEolicaGeracaoPatamar,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eolica-geracao.csv"
    ) -> "EolicaGeracao":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(
        self, diretorio: str, nome_arquivo="eolica-geracao.csv"
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

    def eolica_geracao_periodo(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        geracao: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroEolicaGeracaoPeriodo,
            List[RegistroEolicaGeracaoPeriodo],
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
        return self.__obtem_registros_com_filtros(
            RegistroEolicaGeracaoPeriodo,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            geracao=geracao,
        )

    def eolica_geracao_profundidade_periodo_patamar(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        indice_patamar: Optional[int] = None,
        profundidade: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroEolicaGeracaoPatamar,
            List[RegistroEolicaGeracaoPatamar],
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
        return self.__obtem_registros_com_filtros(
            RegistroEolicaGeracaoPatamar,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            indice_patamar=indice_patamar,
            profundidade=profundidade,
        )
