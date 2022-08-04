from inewave.nwlistop.modelos.geolsin import GEAnos

from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)


class GeolSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração eólica total
    para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `geolsin.out`.
    """

    BLOCKS = [
        GEAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="geolsin.out"
    ) -> "GeolSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="geolsin.out"):
        self.write(diretorio, nome_arquivo)
