from inewave._utils.arquivo import ArquivoRegistros
from inewave._utils.dadosarquivo import DadosArquivoRegistros
from inewave._utils.escritaregistros import EscritaRegistros
from inewave._utils.registronewave import RegistroNEWAVE

from inewave.newave.modelos.modif import LeituraModif
from inewave.newave.modelos.modif import USINA, VOLMIN, VOLMAX, NUMCNJ, NUMMAQ
from inewave.newave.modelos.modif import VAZMIN, CFUGA, CMONT
from inewave.newave.modelos.modif import VMAXT, VMINT, VMINP, VAZMINT


from typing import Type, TypeVar, List


class Modif(ArquivoRegistros):
    """
    Armazena os dados de entrada do NEWAVE referentes às alterações nas
    configurações das usinas hidroelétricas.

    **Parâmetros**

    """

    T = TypeVar("T")

    def __init__(self, dados: DadosArquivoRegistros) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="modif.dat") -> "Modif":
        """ """
        leitor = LeituraModif(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="modif.dat"):
        """ """
        escritor = EscritaRegistros(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    def __obtem_registros(self, tipo: Type[T]) -> List[T]:
        registros = []
        for b in self._registros:
            if isinstance(b, tipo):
                registros.append(b)
        return registros

    @property
    def usina(self) -> List[USINA]:
        regs: List[USINA] = self.__obtem_registros(USINA)
        return regs

    @property
    def volmin(self) -> List[VOLMIN]:
        regs: List[VOLMIN] = self.__obtem_registros(VOLMIN)
        return regs

    @property
    def volmax(self) -> List[VOLMAX]:
        regs: List[VOLMAX] = self.__obtem_registros(VOLMAX)
        return regs

    @property
    def numcnj(self) -> List[NUMCNJ]:
        regs: List[NUMCNJ] = self.__obtem_registros(NUMCNJ)
        return regs

    @property
    def nummaq(self) -> List[NUMMAQ]:
        regs: List[NUMMAQ] = self.__obtem_registros(NUMMAQ)
        return regs

    @property
    def vazmin(self) -> List[VAZMIN]:
        regs: List[VAZMIN] = self.__obtem_registros(VAZMIN)
        return regs

    @property
    def cfuga(self) -> List[CFUGA]:
        regs: List[CFUGA] = self.__obtem_registros(CFUGA)
        return regs

    @property
    def cmont(self) -> List[CMONT]:
        regs: List[CMONT] = self.__obtem_registros(CMONT)
        return regs

    @property
    def vmaxt(self) -> List[VMAXT]:
        regs: List[VMAXT] = self.__obtem_registros(VMAXT)
        return regs

    @property
    def vmint(self) -> List[VMINT]:
        regs: List[VMINT] = self.__obtem_registros(VMINT)
        return regs

    @property
    def vminp(self) -> List[VMINP]:
        regs: List[VMINP] = self.__obtem_registros(VMINP)
        return regs

    @property
    def vazmint(self) -> List[VAZMINT]:
        regs: List[VAZMINT] = self.__obtem_registros(VAZMINT)
        return regs

    def modificacoes_usina(self, codigo: int) -> List[RegistroNEWAVE]:
        regs: List[USINA] = self.__obtem_registros(USINA)
        indice = -1.0
        indice_proximo = -1.0
        for r in regs:
            if indice != -1.0:
                indice_proximo = r._ordem
                break
            if r.codigo == codigo:
                indice = r._ordem
        if indice_proximo != -1.0:
            regs_usina = self._dados.registros[
                int(indice) : int(indice_proximo)
            ]
        else:
            regs_usina = self._dados.registros[int(indice) :]
        return regs_usina
