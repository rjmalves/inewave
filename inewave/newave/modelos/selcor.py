from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from typing import List, IO


class BlocoDadosSelcor(Section):
    """
    Bloco de informações da parametrização do processo de seleção
    de cortes existentes no arquivo `selcor.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__line = Line(
            [
                LiteralField(60, 0),
                IntegerField(4, 63),
                IntegerField(4, 69),
            ]
        )
        self.__cabecalhos: List[str] = []
        self.__comentarios: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDadosSelcor):
            return False
        bloco: BlocoDadosSelcor = o
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
        self.data: List[List[int]] = []
        for _ in range(7):
            dados_linha = self.__line.read(file.readline())
            self.__comentarios.append(dados_linha[0])
            self.data.append(dados_linha[1:])

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, list):
            raise ValueError("Dados do selcor.dat não foram lidos com sucesso")

        for c, s in zip(self.__comentarios, self.data):
            file.write(self.__line.write([c] + s))
