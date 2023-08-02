from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class Sar(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à superfície de
    aversão à risco (SAR).

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
