from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.qafluh import QaflAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class QaflUH(ArquivoUsina):
    """
    Armazena os dados das saídas referentes às vazões afluentes por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `qafluh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        QaflAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="qafluh001.out"
    ) -> "QaflUH":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
