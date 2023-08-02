from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class Gtminpat(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à geração térmica
    mínima por patamar.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
