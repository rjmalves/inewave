from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from typing import List, Dict, IO, Any


class BlocoDadosNwlistop(Section):
    """
    Bloco do arquivo nwlistop.dat que armazena as informações de mês de
    início e fim para a impressão.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_opcao = Line([IntegerField(1, 1)])
        self.__linha_arquivo = Line(
            [LiteralField(29, 0), LiteralField(40, 30)]
        )
        self.__linha_series_op1 = Line(
            [IntegerField(4, 1), IntegerField(4, 6)]
        )
        self.__linha_periodos = Line([IntegerField(3, 1), IntegerField(3, 5)])
        self.__linha_variaveis_op2 = Line(
            [IntegerField(2, 1 + 3 * i) for i in range(21)]
        )
        self.__linha_uhes_op2 = Line(
            [IntegerField(3, 1 + 4 * i) for i in range(16)]
        )
        self.data: Dict[str, Any] = {}
        self.__comentarios: List[List[str]] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDadosNwlistop):
            return False
        bloco: BlocoDadosNwlistop = o
        if not all(
            [
                isinstance(self.data, dict),
                isinstance(o.data, dict),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def __read_op1(self, file: IO):
        # Le os nomes dos arquivos
        self.data["arquivos"] = []
        for _ in range(3):
            self.data["arquivos"].append(
                self.__linha_arquivo.read(file.readline())
            )

        self.__comentarios.append([])
        for _ in range(2):
            self.__comentarios[-1].append(file.readline())
        # Le o periodo inicial e final
        self.data["periodos"] = self.__linha_periodos.read(file.readline())

        self.__comentarios.append([])
        self.__comentarios[-1].append(file.readline())
        # Le a serie inicial e final
        self.data["series"] = self.__linha_series_op1.read(file.readline())

    def __read_op2(self, file: IO):
        # Le os nomes dos arquivos
        self.data["arquivos"] = []
        for _ in range(3):
            self.data["arquivos"].append(
                self.__linha_arquivo.read(file.readline())
            )

        self.__comentarios.append([])
        for _ in range(2):
            self.__comentarios[-1].append(file.readline())
        # Le o periodo inicial e final
        self.data["periodos"] = self.__linha_periodos.read(file.readline())

        self.__comentarios.append([])
        for _ in range(6):
            self.__comentarios[-1].append(file.readline())
        # Le as variáveis para os estágios agregados
        self.data["variaveis_ree"] = self.__linha_variaveis_op2.read(
            file.readline()
        )

        self.__comentarios.append([])
        for _ in range(4):
            self.__comentarios[-1].append(file.readline())

        # Le as variáveis para os estágios individualizados
        self.data["variaveis_uhe"] = self.__linha_variaveis_op2.read(
            file.readline()
        )

        self.__comentarios.append([])
        self.__comentarios[-1].append(file.readline())

        # Le as usinas para os estágios individualizados
        self.data["uhes"] = self.__linha_uhes_op2.read(file.readline())

    def __read_op4(self, file: IO):
        # Le os nomes dos arquivos
        self.data["arquivos"] = []
        for _ in range(3):
            self.data["arquivos"].append(
                self.__linha_arquivo.read(file.readline())
            )

        self.__comentarios = []
        while True:
            linha = file.readline()
            if len(linha) < 3:
                break
            self.__comentarios.append(linha)

    # Override
    def read(self, file: IO, *args, **kwargs):
        opcao = self.__linha_opcao.read(file.readline())[0]
        self.data["opcao"] = opcao
        if opcao == 1:
            self.__read_op1(file)
        elif opcao == 2:
            self.__read_op2(file)
        elif opcao == 4:
            self.__read_op4(file)

    # Override
    def write(self, file: IO, *args, **kwargs):
        opcao = self.data["opcao"]
        file.write(self.__linha_opcao.write([opcao]))
        if opcao == 1:
            self.__write_op1(file)
        elif opcao == 2:
            self.__write_op2(file)
        elif opcao == 4:
            self.__write_op4(file)

    # Override
    def __write_op1(self, file: IO, *args, **kwargs):
        # Escreve os nomes de arquivos
        for c in self.data["arquivos"]:
            file.write(self.__linha_arquivo.write(c))
        # Escreve as linhas de cabeçalho para períodos
        for c in self.__comentarios[0]:
            file.write(c)
        # Escreve os períodos
        file.write(self.__linha_periodos.write(self.data["periodos"]))
        # Escreve as linhas de cabeçalho para séries
        for c in self.__comentarios[1]:
            file.write(c)
        # Escreve as séries
        file.write(self.__linha_periodos.write(self.data["series"]))

    # Override
    def __write_op2(self, file: IO, *args, **kwargs):
        # Escreve os nomes de arquivos
        for c in self.data["arquivos"]:
            file.write(self.__linha_arquivo.write(c))
        # Escreve as linhas de cabeçalho para períodos
        for c in self.__comentarios[0]:
            file.write(c)
        # Escreve os períodos
        file.write(self.__linha_periodos.write(self.data["periodos"]))
        # Escreve as linhas de cabeçalho para variáveis agregadas
        for c in self.__comentarios[1]:
            file.write(c)
        # Escreve as séries
        file.write(self.__linha_periodos.write(self.data["variaveis_ree"]))
        # Escreve as linhas de cabeçalho para variáveis individualizadas
        for c in self.__comentarios[2]:
            file.write(c)
        # Escreve as séries
        file.write(self.__linha_periodos.write(self.data["variaveis_uhe"]))
        # Escreve as linhas de cabeçalho para usinas
        for c in self.__comentarios[3]:
            file.write(c)
        # Escreve as séries
        file.write(self.__linha_periodos.write(self.data["uhes"]))

    # Override
    def __write_op4(self, file: IO, *args, **kwargs):
        # Escreve os nomes de arquivos
        for c in self.data["arquivos"]:
            file.write(self.__linha_arquivo.write(c))
        # Escreve as linhas de comentários
        for c in self.__comentarios:
            file.write(c)
