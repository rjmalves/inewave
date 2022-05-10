from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.modif import USINA, VOLMIN, VOLMAX, NUMCNJ, NUMMAQ
from inewave.newave.modelos.modif import VAZMIN, CFUGA, CMONT
from inewave.newave.modelos.modif import VMAXT, VMINT, VMINP, VAZMINT


from typing import Type, TypeVar, List


class Modif(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às alterações nas
    configurações das usinas hidroelétricas.
    """

    T = TypeVar("T")

    REGISTERS = [
        USINA,
        VOLMIN,
        VOLMAX,
        NUMCNJ,
        NUMMAQ,
        VAZMIN,
        CFUGA,
        CMONT,
        VMAXT,
        VMINT,
        VMINP,
        VAZMINT,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="modif.dat") -> "Modif":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="modif.dat"):
        self.write(diretorio, nome_arquivo)

    def __registros_por_tipo(self, registro: Type[T]) -> List[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int

        """
        return [b for b in self.data.of_type(registro)]

    @property
    def usina(self) -> List[USINA]:
        regs: List[USINA] = self.__registros_por_tipo(USINA)
        return regs

    @property
    def volmin(self) -> List[VOLMIN]:
        regs: List[VOLMIN] = self.__registros_por_tipo(VOLMIN)
        return regs

    @property
    def volmax(self) -> List[VOLMAX]:
        regs: List[VOLMAX] = self.__registros_por_tipo(VOLMAX)
        return regs

    @property
    def numcnj(self) -> List[NUMCNJ]:
        regs: List[NUMCNJ] = self.__registros_por_tipo(NUMCNJ)
        return regs

    @property
    def nummaq(self) -> List[NUMMAQ]:
        regs: List[NUMMAQ] = self.__registros_por_tipo(NUMMAQ)
        return regs

    @property
    def vazmin(self) -> List[VAZMIN]:
        regs: List[VAZMIN] = self.__registros_por_tipo(VAZMIN)
        return regs

    @property
    def cfuga(self) -> List[CFUGA]:
        regs: List[CFUGA] = self.__registros_por_tipo(CFUGA)
        return regs

    @property
    def cmont(self) -> List[CMONT]:
        regs: List[CMONT] = self.__registros_por_tipo(CMONT)
        return regs

    @property
    def vmaxt(self) -> List[VMAXT]:
        regs: List[VMAXT] = self.__registros_por_tipo(VMAXT)
        return regs

    @property
    def vmint(self) -> List[VMINT]:
        regs: List[VMINT] = self.__registros_por_tipo(VMINT)
        return regs

    @property
    def vminp(self) -> List[VMINP]:
        regs: List[VMINP] = self.__registros_por_tipo(VMINP)
        return regs

    @property
    def vazmint(self) -> List[VAZMINT]:
        regs: List[VAZMINT] = self.__registros_por_tipo(VAZMINT)
        return regs

    def modificacoes_usina(self, codigo: int) -> List[Register]:
        """
        Filtra os registros que são associados a uma usina específica.

        :param codigo: O código da usina
        :type codigo: int
        :return: Os registros que modificam a usina
        :rtype: List[Register]
        """
        usinas = self.usina
        reg_usina: List[USINA] = list(
            filter(lambda r: r.codigo == codigo, usinas)
        )
        modificacoes_usina: List[Register] = []
        if len(reg_usina) > 0:
            r = reg_usina[0].next
            while not isinstance(r, USINA) or r.is_last:
                modificacoes_usina.append(r)
                r = r.next

        return modificacoes_usina
