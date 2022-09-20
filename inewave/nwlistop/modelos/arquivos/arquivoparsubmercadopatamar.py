from inewave.nwlistop.modelos.blocos.parsubmercados import ParSubmercados
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import Type, TypeVar, Optional


class ArquivoParSubmercadoPatamar(BlockFile):
    """
    Armazena os dados das saídas por patamar, por par de submercados.
    """

    T = TypeVar("T")

    BLOCKS = [ParSubmercados, ValoresSeriePatamar]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__valores = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="arq.out"
    ) -> "ArquivoParSubmercadoPatamar":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="arq.out"):
        self.write(diretorio, nome_arquivo)

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(ValoresSeriePatamar):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
        return df

    @property
    def valores(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores por patamar, por série e
        por mês/ano de estudo.

        - Ano (`int`)
        - Série (`int`)
        - Patamar (`str`)
        - Janeiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela dos valores por patamar.
        :rtype: pd.DataFrame | None
        """
        if self.__valores is None:
            self.__valores = self.__monta_tabela()
        return self.__valores

    @property
    def submercado_de(self) -> Optional[str]:
        """
        O submercado de origem associado ao arquivo lido.

        :return: Os nome do submercado
        :rtype: str
        """
        b = self.__bloco_por_tipo(ParSubmercados, 0)
        if b is not None:
            return b.data[0]
        return None

    @property
    def submercado_para(self) -> Optional[str]:
        """
        O submercado de destino associado ao arquivo lido.

        :return: Os nome do submercado
        :rtype: str
        """
        b = self.__bloco_por_tipo(ParSubmercados, 0)
        if b is not None:
            return b.data[1]
        return None
