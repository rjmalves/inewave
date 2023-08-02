from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class ENSOAux(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao arquivo ENSO 2.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
