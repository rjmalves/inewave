from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Clasgas(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às classes
    de gás.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
