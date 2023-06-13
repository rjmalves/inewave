from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.dtbmin import DtbminAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Dtbmin(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à violação de restrição de
    turbinamento mínimo por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dtbmin00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DtbminAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dtbmin001.out"
    ) -> "Dtbmin":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
