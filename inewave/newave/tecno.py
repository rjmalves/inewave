from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class Tecno(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às tecnologias
    disponíveis para geração de energia.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
