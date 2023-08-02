from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class BID(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à demanda
    sem bidding.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []
