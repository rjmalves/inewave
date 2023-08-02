from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class Clasgas(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às classes
    de gás.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
