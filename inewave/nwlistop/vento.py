from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.vento import VentoAnos


class Vento(ArquivoUsina):
    """
    Armazena os dados das saídas referentes às velocidades do
    vento por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vento00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        VentoAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vento001.out"
    ) -> "Vento":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vento001.out"):
        self.write(diretorio, nome_arquivo)
