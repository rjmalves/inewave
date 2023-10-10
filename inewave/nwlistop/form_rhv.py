from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricao import (
    ArquivoRestricao,
)
from inewave.nwlistop.modelos.form_rhv import FormRHVAnos


class FormRHV(ArquivoRestricao):
    """
    Armazena os dados das saídas referentes aos valores das restrições
    RHV por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `form_rhvXXX.out`.

    """

    BLOCKS = [
        Restricao,
        FormRHVAnos,
    ]
