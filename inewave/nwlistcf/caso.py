from inewave.nwlistcf.modelos.caso import NomeCaso

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional


class Caso(SectionFile):
    """
    Armazena os dados de entrada do NWLISTCF referentes ao caso de estudo.

    Esta classe lida com informações de entrada fornecidas ao NWLISTCF e
    que podem ser modificadas através do arquivo `caso.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [NomeCaso]

    @property
    def arquivos(self) -> Optional[str]:
        """
        Caminho para o arquivo `arquivos.dat` de entrada do NWLISTCF.

        :return: O caminho para o arquivo
        :rtype: str | None
        """
        b = self.data.get_sections_of_type(NomeCaso)
        if isinstance(b, NomeCaso):
            return b.data
        return None

    @arquivos.setter
    def arquivos(self, a: str):
        b = self.data.get_sections_of_type(NomeCaso)
        if isinstance(b, NomeCaso):
            b.data = a
