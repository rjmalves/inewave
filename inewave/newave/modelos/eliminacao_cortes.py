from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import IO, List


class BlocoParametrosEliminacaoCortes(Section):
    """
    Bloco com os parâmetros para eliminação de cortes de Benders
    utilizados pelo NEWAVE, extraído do arquivo `eliminacao_cortes.dat`.
    """

    __slots__ = ["__linha", "__cabecalhos", "__comentarios", "data"]

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(60, 0),     # Descrição do parâmetro
                FloatField(6, 61, 2),     # Valor PARAL (coluna 1)
                IntegerField(6, 68),     # Valor A.P.P (coluna 2)  
                IntegerField(6, 75),     # Valor S.M. (coluna 3)
            ]
        )
        self.__cabecalhos: List[str] = []
        self.__comentarios: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoParametrosEliminacaoCortes):
            return False
        bloco: BlocoParametrosEliminacaoCortes = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO, *args, **kwargs):
        # Salta as linhas de cabeçalhos
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Lê as linhas de parâmetros
        self.data: List[List] = []
        
        for _ in range(4):  
            linha = file.readline()
            if not linha:
                break
            dados = self.__linha.read(linha)

            self.__comentarios.append(dados[0].strip())
            self.data.append(dados[1:])

        for _ in range(3):  
            linha = file.readline()
            if not linha:
                break
            dados = self.__linha.read(linha)

            self.__comentarios.append(dados[0].strip())
            self.data.append([dados[1]])

    # Override  
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, list):
            raise ValueError("Dados do eliminacao_cortes.dat não foram lidos com sucesso")

        for c, s in zip(self.__comentarios, self.data):
            file.write(self.__linha.write([c] + s))
