from inewave.nwlistop.modelos.arquivos._base_serie import _ArquivoSerieBase
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class ArquivoSIN(_ArquivoSerieBase):
    """
    Armazena os dados das saídas por submercado.
    """

    __slots__: list[str] = []

    BLOCKS = [ValoresSerie]
