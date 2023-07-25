from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from typing import List, IO


class BlocoVarreduraShist(Section):
    """
    Bloco de informações de varredura existente no arquivo `shist.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__line = Line(
            [
                IntegerField(3, 0),
                IntegerField(4, 4),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoVarreduraShist):
            return False
        bloco: BlocoVarreduraShist = o
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

        self.data = self.__line.read(file.readline())

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, list):
            raise ValueError("Dados do shist.dat não foram lidos com sucesso")

        file.write(self.__line.write(self.data))


class BlocoSeriesSimulacaoShist(Section):
    """
    Bloco de informações das séries para a simulação
    existente no arquivo `shist.dat`.
    """

    END_PATTERN = "9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__line = Line(
            [
                IntegerField(4, 0),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSeriesSimulacaoShist):
            return False
        bloco: BlocoSeriesSimulacaoShist = o
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

        self.data: List[int] = []
        while True:
            linha = file.readline()
            if (
                BlocoSeriesSimulacaoShist.END_PATTERN in linha[:4]
                or len(linha) < 2
            ):
                break

            self.data.append(self.__line.read(linha)[0])

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, list):
            raise ValueError("Dados do shist.dat não foram lidos com sucesso")

        for s in self.data:
            file.write(self.__line.write([s]))

        file.write(BlocoSeriesSimulacaoShist.END_PATTERN + "\n")
