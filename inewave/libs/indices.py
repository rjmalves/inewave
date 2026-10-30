from typing import Any, List, Literal, Optional, Type, TypeVar, Union, overload

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile

from inewave.libs.modelos.indices import RegistroIndice


class Indices(RegisterFile):
    """
    Armazena os dados do arquivo de índices das LIBS (``indices.csv``,
    manual do NEWAVE, seção 3.4), que associa cada identificador de card
    das LIBS ao arquivo que contém os seus registros.

    Regras de leitura e escrita:

    - toda linha que contém ``;`` e não começa com ``&`` (após os
      espaços iniciais) é um registro :class:`RegistroIndice`, no
      formato ``IDENTIFICADOR;DESCRICAO;ARQUIVO``;
    - as linhas iniciadas por ``&`` são comentários, mesmo quando
      contêm ``;``, e são reescritas sem alterações;
    - os espaços em torno dos valores são removidos e os identificadores
      não são convertidos para maiúsculas;
    - um campo vazio é lido como ``""``, e não como ``None``;
    - identificadores repetidos são mantidos como registros separados,
      na ordem do arquivo, sem gerar erro;
    - na escrita, os registros são reescritos como
      ``IDENTIFICADOR;DESCRICAO;ARQUIVO``.
    """

    T = TypeVar("T", bound=Register)

    REGISTERS = [RegistroIndice]

    def __init__(self, data: Any = ...) -> None:
        super().__init__(data)

    def __registros_ou_df(
        self, t: Type[T], **kwargs: Any
    ) -> Optional[Union[T, List[T], pd.DataFrame]]:
        if kwargs.get("df"):
            return self._as_df(t)
        else:
            kwargs_sem_df = {k: v for k, v in kwargs.items() if k != "df"}
            return self.data.get_registers_of_type(t, **kwargs_sem_df)

    @overload
    def indices(
        self,
        identificador: Optional[str] = None,
        arquivo: Optional[str] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def indices(
        self,
        identificador: Optional[str] = None,
        arquivo: Optional[str] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[RegistroIndice, List[RegistroIndice]]]: ...
    @overload
    def indices(
        self,
        identificador: Optional[str] = None,
        arquivo: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroIndice, List[RegistroIndice], pd.DataFrame]
    ]: ...
    def indices(
        self,
        identificador: Optional[str] = None,
        arquivo: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[RegistroIndice, List[RegistroIndice], pd.DataFrame]]:
        """
        Obtém registros que associam os identificadores dos cards das
        LIBS aos arquivos que contêm os seus registros.
        Opcionalmente, o retorno pode ser transformado em um `DataFrame`,
        com as colunas ``arquivo``, ``descricao`` e ``identificador``.

        :param identificador: o identificador do card das LIBS
        :type identificador: str | None
        :param arquivo: o arquivo que contém os registros do card
        :type arquivo: str | None
        :param df: ignorar os filtros e retornar
            todos os dados de registros como um DataFrame
        :type df: bool
        :return: Os registros, se existirem.
        :rtype: :class:`RegistroIndice` | list[:class:`RegistroIndice`] |
            :class:`pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroIndice,
            identificador=identificador,
            arquivo=arquivo,
            df=df,
        )
