from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class Itaipu(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às restrições
    de Itaipu.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
