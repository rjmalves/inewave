from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from typing import IO, Any, List, Optional


class PeriodoImpressaoCortesEstados(Section):
    """
    Bloco do arquivo nwlistcf.dat que armazena as informações de mês de
    início e fim para a impressão.
    """

    __slots__ = ["__linha", "__cabecalhos"]

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [IntegerField(3, 1), IntegerField(3, 5), IntegerField(1, 9)]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, PeriodoImpressaoCortesEstados):
            return False
        bloco: PeriodoImpressaoCortesEstados = o
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
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        # Lê as linhas de cabeçalho
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        self.data = self.__linha.read(file.readline())

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        # Escreve as linhas de cabeçalho
        for c in self.__cabecalhos:
            file.write(c)

        file.write(self.__linha.write(self.data))


class OpcoesImpressao(Section):
    """
    Bloco do arquivo nwlistcf.dat que armazena as informações das opções
    de impressão selecionadas.
    """

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [IntegerField(2, 1), IntegerField(2, 4), IntegerField(2, 7)]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, OpcoesImpressao):
            return False
        bloco: OpcoesImpressao = o
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
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        # Lê as linhas de cabeçalho
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        self.data = self.__linha.read(file.readline())

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        # Escreve as linhas de cabeçalho
        for c in self.__cabecalhos:
            file.write(c)

        file.write(self.__linha.write(self.data))
