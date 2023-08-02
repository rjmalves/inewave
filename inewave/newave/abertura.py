from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class Abertura(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao número de
    aberturas utilizadas por período.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
