from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.qincruh import QincrAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Qincruh(ArquivoUsina):
    """
    Armazena os dados das saídas referentes às vazões incrementais por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `qincruh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        QincrAnos,
    ]
