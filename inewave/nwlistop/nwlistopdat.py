from inewave.nwlistop.modelos.nwlistopdat import (
    BlocoDadosNwlistop,
)

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional, Type, List

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Nwlistopdat(SectionFile):
    """
    Armazena os dados de entrada para a execução do programa auxiliar
    NWLISTOP, existentes no arquivo `nwlistop.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoDadosNwlistop]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="nwlistop.dat"
    ) -> "Nwlistopdat":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

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

    @property
    def opcao(self) -> Optional[int]:
        """
        A opção de execução do programa nwlistop.

        :return: O flag de opção
        :rtype: Optional[int] | None
        """
        b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
        if b is not None:
            return b.data.get("opcao")
        return None

    @opcao.setter
    def opcao(self, v: int):
        b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
        if b is not None:
            b.data["opcao"] = v

    @property
    def periodo_inicial_impressao(self) -> Optional[int]:
        """
        O período inicial para impressão dos dados de saída.

        :return: O índice do período
        :rtype: Optional[int] | None
        """
        if self.opcao in [1, 2, 4]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                return b.data["periodos"][0]
            return None
        else:
            raise ValueError("Períodos só são suportados nas opções [1, 2, 4]")

    @periodo_inicial_impressao.setter
    def periodo_inicial_impressao(self, v: int):
        if self.opcao in [1, 2, 4]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                b.data["periodos"][0] = v
        else:
            raise ValueError("Períodos só são suportados nas opções [1, 2, 4]")

    @property
    def periodo_final_impressao(self) -> Optional[int]:
        """
        O período final para impressão dos dados de saída.

        :return: O índice do período
        :rtype: Optional[int] | None
        """
        if self.opcao in [1, 2, 4]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                return b.data["periodos"][1]
            return None
        else:
            raise ValueError("Períodos só são suportados nas opções [1, 2, 4]")

    @periodo_final_impressao.setter
    def periodo_final_impressao(self, v: int):
        if self.opcao in [1, 2, 4]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                b.data["periodos"][1] = v
        else:
            raise ValueError("Períodos só são suportados nas opções [1, 2, 4]")

    @property
    def serie_inicial_impressao(self) -> Optional[int]:
        """
        A série inicial para impressão dos dados de saída.

        :return: O índice da série
        :rtype: Optional[int] | None
        """
        if self.opcao in [1]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                return b.data["series"][0]
            return None
        else:
            raise ValueError("Séries só são suportadas na opção [1]")

    @serie_inicial_impressao.setter
    def serie_inicial_impressao(self, v: int):
        if self.opcao in [1]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                b.data["series"][0] = v
        else:
            raise ValueError("Séries só são suportadas na opção [1]")

    @property
    def serie_final_impressao(self) -> Optional[int]:
        """
        A série final para impressão dos dados de saída.

        :return: O índice da série
        :rtype: Optional[int] | None
        """
        if self.opcao in [1]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                return b.data["series"][1]
            return None
        else:
            raise ValueError("Séries só são suportadas na opção [1]")

    @serie_final_impressao.setter
    def serie_final_impressao(self, v: int):
        if self.opcao in [1]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                b.data["series"][1] = v
        else:
            raise ValueError("Séries só são suportadas na opção [1]")

    @property
    def variaveis_impressao_estagios_agregados(self) -> Optional[List[int]]:
        """
        As variáveis dos períodos agregados a serem impressas na
        opção 2.

        :return: A lista dos códigos das variáveis.
        :rtype: Optional[List[int]] | None
        """
        if self.opcao in [2]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                return b.data["variaveis_ree"]
            return None
        else:
            raise ValueError("Variáveis só são suportadas na opção [2]")

    @variaveis_impressao_estagios_agregados.setter
    def variaveis_impressao_estagios_agregados(self, v: List[int]):
        if self.opcao in [2]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                b.data["variaveis_ree"] = v
        else:
            raise ValueError("Variáveis só são suportadas na opção [2]")

    @property
    def variaveis_impressao_estagios_individualizados(
        self,
    ) -> Optional[List[int]]:
        """
        As variáveis dos períodos individualizados a serem impressas na
        opção 2.

        :return: A lista dos códigos das variáveis.
        :rtype: Optional[List[int]] | None
        """
        if self.opcao in [2]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                return b.data["variaveis_uhe"]
            return None
        else:
            raise ValueError("Variáveis só são suportadas na opção [2]")

    @variaveis_impressao_estagios_individualizados.setter
    def variaveis_impressao_estagios_individualizados(self, v: List[int]):
        if self.opcao in [2]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                b.data["variaveis_uhe"] = v
        else:
            raise ValueError("Variáveis só são suportadas na opção [2]")

    @property
    def uhes_impressao_estagios_individualizados(
        self,
    ) -> Optional[List[int]]:
        """
        As UHEs que terão as variáveis impressas na opção 2.

        :return: A lista dos códigos das UHEs.
        :rtype: Optional[List[int]] | None
        """
        if self.opcao in [2]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                return b.data["uhes"]
            return None
        else:
            raise ValueError("UHEs só são suportadas na opção [2]")

    @uhes_impressao_estagios_individualizados.setter
    def uhes_impressao_estagios_individualizados(self, v: List[int]):
        if self.opcao in [2]:
            b = self.__bloco_por_tipo(BlocoDadosNwlistop, 0)
            if b is not None:
                b.data["uhes"] = v
        else:
            raise ValueError("UHEs só são suportadas na opção [2]")
