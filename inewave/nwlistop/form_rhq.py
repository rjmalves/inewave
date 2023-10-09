from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricaopatamar import (
    ArquivoRestricaoPatamar,
)
from inewave.nwlistop.modelos.form_rhq import FormRHQAnos


class FormRHQ(ArquivoRestricaoPatamar):
    """
    Armazena os dados das saídas referentes aos valores das restrições
    RHQ por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `form_rhqXXX.out`.

    """

    BLOCKS = [
        Restricao,
        FormRHQAnos,
    ]
