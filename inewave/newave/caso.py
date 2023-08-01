from inewave.newave.modelos.caso import NomeCaso, CaminhoGerenciadorProcessos

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Caso(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao caso de estudo.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que podem ser modificadas através do arquivo `caso.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [NomeCaso, CaminhoGerenciadorProcessos]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="caso.dat") -> "Caso":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="caso.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def arquivos(self) -> Optional[str]:
        """
        Caminho para o arquivo `arquivos.dat` de entrada do NEWAVE.

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

    @property
    def gerenciador_processos(self) -> Optional[str]:
        """
        Caminho para o gerenciador de processos do NEWAVE.

        :return: O caminho para o arquivo
        :rtype: str | None
        """
        b = self.data.get_sections_of_type(CaminhoGerenciadorProcessos)
        if isinstance(b, CaminhoGerenciadorProcessos):
            return b.data
        return None

    @gerenciador_processos.setter
    def gerenciador_processos(self, a: str):
        b = self.data.get_sections_of_type(CaminhoGerenciadorProcessos)
        if isinstance(b, CaminhoGerenciadorProcessos):
            b.data = a
