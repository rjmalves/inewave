from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class Perda(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos fatores de perda
    das usinas e das interligações.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
