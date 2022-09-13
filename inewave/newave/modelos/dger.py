from typing import IO, List, Optional
from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField


class BlocoNomeCaso(Section):
    """
    Bloco com o nome do caso, existente
    no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(80, 0)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNomeCaso):
            return False
        bloco: BlocoNomeCaso = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[str]:
        """
        O valor da opção configurada

        :return: O nome do caso
        :rtype: Optional[str]
        """
        return self.data[0]

    @valor.setter
    def valor(self, v: str):
        self.data[0] = v


class BlocoTipoExecucao(Section):
    """
    Bloco com o tipo de execução do caso,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(43, 25)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTipoExecucao):
            return False
        bloco: BlocoTipoExecucao = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O tipo de execução
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoDuracaoPeriodo(Section):
    """
    Bloco com a duração do período de execução,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(2, 23)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDuracaoPeriodo):
            return False
        bloco: BlocoDuracaoPeriodo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A duração do período
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumAnosEstudo(Section):
    """
    Bloco com o número de anos no período de estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(2, 23)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumAnosEstudo):
            return False
        bloco: BlocoNumAnosEstudo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de anos de estudo
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoMesInicioPreEstudo(Section):
    """
    Bloco com o mês de início do pré-estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(2, 23)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMesInicioPreEstudo):
            return False
        bloco: BlocoMesInicioPreEstudo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O mês de início do período pré estudo
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoMesInicioEstudo(Section):
    """
    Bloco com o mês de início do período de estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(2, 23)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMesInicioEstudo):
            return False
        bloco: BlocoMesInicioEstudo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O mês de início do estudo
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoAnoInicioEstudo(Section):
    """
    Bloco com o ano do início do período de estudo
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoAnoInicioEstudo):
            return False
        bloco: BlocoAnoInicioEstudo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(4, 21)])

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O ano de início do estudo
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumAnosPreEstudo(Section):
    """
    Bloco com o número de anos do período pré-estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(2, 23)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumAnosPreEstudo):
            return False
        bloco: BlocoNumAnosPreEstudo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de anos de pré estudo
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumAnosPosEstudo(Section):
    """
    Bloco com o número de anos do período pós-estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(2, 23)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumAnosPosEstudo):
            return False
        bloco: BlocoNumAnosPosEstudo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de anos de pós estudo
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumAnosPosEstudoSimFinal(Section):
    """
    Bloco com o número de anos do período pós-estudo na simulação final,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(2, 23)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumAnosPosEstudoSimFinal):
            return False
        bloco: BlocoNumAnosPosEstudoSimFinal = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de anos de pós estudo na simulação final.
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImprimeDados(Section):
    """
    Bloco com a opção de imprimir dados das usinas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(1, 24)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImprimeDados):
            return False
        bloco: BlocoImprimeDados = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não das informações
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImprimeMercados(Section):
    """
    Bloco com a opção de imprimir dados de mercados,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(1, 24)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImprimeMercados):
            return False
        bloco: BlocoImprimeMercados = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não das informações
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImprimeEnergias(Section):
    """
    Bloco com a opção de imprimir dados das energias,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(1, 24)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImprimeEnergias):
            return False
        bloco: BlocoImprimeEnergias = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não das informações
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImprimeModeloEstocastico(Section):
    """
    Bloco com a opção de imprimir dados do modelo estocástico,
    de geração de cenários existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(1, 24)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImprimeModeloEstocastico):
            return False
        bloco: BlocoImprimeModeloEstocastico = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não das informações
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImprimeSubsistema(Section):
    """
    Bloco com a opção de imprimir dados dos subsistemas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(1, 24)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImprimeSubsistema):
            return False
        bloco: BlocoImprimeSubsistema = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não das informações
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumMaxIteracoes(Section):
    """
    Bloco com o número máximo de iterações,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(4, 21)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumMaxIteracoes):
            return False
        bloco: BlocoNumMaxIteracoes = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número máximo de iterações
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumForwards(Section):
    """
    Bloco com o número de simulações forward,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(4, 21)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumForwards):
            return False
        bloco: BlocoNumForwards = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de séries forward.
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumAberturas(Section):
    """
    Bloco com o número aberturas e se são consideradas
    aberturas variáveis, existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(4, 21)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumAberturas):
            return False
        bloco: BlocoNumAberturas = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de aberturas
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumSeriesSinteticas(Section):
    """
    Bloco com o número de séries sintéticas utilizadas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(4, 21)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumSeriesSinteticas):
            return False
        bloco: BlocoNumSeriesSinteticas = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de séries sintéticas.
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoOrdemMaximaPARp(Section):
    """
    Bloco com a ordem máxima do modelo PAR(p),
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(2, 23)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoOrdemMaximaPARp):
            return False
        bloco: BlocoOrdemMaximaPARp = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A ordem máxima do modelo PAR(p)
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoAnoInicialHistorico(Section):
    """
    Bloco com o ano inicial do histórico,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(4, 21), IntegerField(1, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoAnoInicialHistorico):
            return False
        bloco: BlocoAnoInicialHistorico = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def ano_inicial(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A ordem máxima do modelo PAR(p)
        :rtype: int
        """
        return self.data[1]

    @ano_inicial.setter
    def ano_inicial(self, v: int):
        self.data[1] = v

    @property
    def tamanho_registro_arquivo(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A opção de tamanho do registro no arquivo
            de vazões históricas.
        :rtype: int
        """
        return self.data[2]

    @tamanho_registro_arquivo.setter
    def tamanho_registro_arquivo(self, v: int):
        self.data[2] = v


class BlocoCalculaVolInicial(Section):
    """
    Bloco com a configuração para calcular ou não
    o volume armazenado inicial para o caso,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(43, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCalculaVolInicial):
            return False
        bloco: BlocoCalculaVolInicial = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O cálculo ou não do EARM inicial
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoVolInicialSubsistema(Section):
    """
    Bloco com o ano inicial do histórico,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_nome: List[Field] = [LiteralField(21, 0)]
        campos_volumes: List[Field] = [
            FloatField(5, 21 + i * 7, 1) for i in range(5)
        ]
        self.__linha = Line(campo_nome + campos_volumes)
        self.__cabecalho: str = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoVolInicialSubsistema):
            return False
        bloco: BlocoVolInicialSubsistema = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.__cabecalho = file.readline()
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__cabecalho)
        file.write(self.__linha.write(self.data))

    @property
    def valores(self) -> List[Optional[float]]:
        """
        Os valores da opção configurada

        :return: Os EARM iniciais
        :rtype: List[float]
        """
        return self.data[1:]

    @valores.setter
    def valores(self, v: List[float]):
        self.data = [self.data[0]] + v


class BlocoTolerancia(Section):
    """
    Bloco com a tolerância de convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(21, 0), FloatField(5, 21, 1)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTolerancia):
            return False
        bloco: BlocoTolerancia = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[float]:
        """
        O valor da opção configurada

        :return: A tolerância
        :rtype: float
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: float):
        self.data[1] = v


class BlocoTaxaDesconto(Section):
    """
    Bloco com a taxa de desconto,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(21, 0), FloatField(5, 21, 1)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTaxaDesconto):
            return False
        bloco: BlocoTaxaDesconto = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[float]:
        """
        O valor da opção configurada

        :return: A taxa de desconto
        :rtype: float
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: float):
        self.data[1] = v


class BlocoTipoSimFinal(Section):
    """
    Bloco com a opção do tipo de simulação final,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(24, 0),
                IntegerField(1, 24),
                IntegerField(1, 28),
                LiteralField(76, 31),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTipoSimFinal):
            return False
        bloco: BlocoTipoSimFinal = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> List[int]:
        """
        O valor da opção configurada

        :return: O tipo de simulação final
        :rtype: list[int | None]
        """
        return self.data[1:3]

    @valor.setter
    def valor(self, v: List[int]):
        self.data[1:3] = v


class BlocoImpressaoOperacao(Section):
    """
    Bloco com a opção para impressão da operação detalhada,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(30, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImpressaoOperacao):
            return False
        bloco: BlocoImpressaoOperacao = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não da operação
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImpressaoConvergencia(Section):
    """
    Bloco com a opção para impressão da convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(40, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImpressaoConvergencia):
            return False
        bloco: BlocoImpressaoConvergencia = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não da convergência
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoIntervaloGravar(Section):
    """
    Bloco com a opção para impressão do intervalo para gravar,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(40, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoIntervaloGravar):
            return False
        bloco: BlocoIntervaloGravar = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O intervalo para gravar
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoMinIteracoes(Section):
    """
    Bloco com o número mínimo de iterações,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(3, 22)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMinIteracoes):
            return False
        bloco: BlocoMinIteracoes = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número mínimo de iterações
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRacionamentoPreventivo(Section):
    """
    Bloco com o uso de racionamento preventivo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(50, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRacionamentoPreventivo):
            return False
        bloco: BlocoRacionamentoPreventivo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso ou não de racionamento preventivo
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoNumAnosManutUTE(Section):
    """
    Bloco com o número de anos considerados de manutenção de UTEs,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(35, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumAnosManutUTE):
            return False
        bloco: BlocoNumAnosManutUTE = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de anos de manutenção das UTEs
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoTendenciaHidrologica(Section):
    """
    Bloco com o uso e a forma de uso da tendência hidrológica,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(24, 0),
                IntegerField(1, 24),
                IntegerField(1, 29),
                LiteralField(62, 33),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTendenciaHidrologica):
            return False
        bloco: BlocoTendenciaHidrologica = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def considera_tendencia_hidrologica_calculo_politica(
        self,
    ) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da tendência hidrológica no
            cálculo da política
        :rtype: int
        """
        return self.data[1]

    @considera_tendencia_hidrologica_calculo_politica.setter
    def considera_tendencia_hidrologica_calculo_politica(self, v: int):
        self.data[1] = v

    @property
    def considera_tendencia_hidrologica_sim_final(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da tendência hidrológica no
            cálculo da política
        :rtype: int
        """
        return self.data[2]

    @considera_tendencia_hidrologica_sim_final.setter
    def considera_tendencia_hidrologica_sim_final(self, v: int):
        self.data[2] = v


class BlocoRestricaoItaipu(Section):
    """
    Bloco com a consideração das restrições de Itaipu,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(32, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRestricaoItaipu):
            return False
        bloco: BlocoRestricaoItaipu = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso ou não da restrição de Itaipu
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoBid(Section):
    """
    Bloco com a consideração das restrições de BID,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(32, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoBid):
            return False
        bloco: BlocoBid = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso ou não de BID
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoPerdasTransmissao(Section):
    """
    Bloco com a consideração das perdas na transmissão,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(32, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoPerdasTransmissao):
            return False
        bloco: BlocoPerdasTransmissao = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso ou não de perdas na transmissão
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoElNino(Section):
    """
    Bloco com a consideração do El Nino,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(32, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoElNino):
            return False
        bloco: BlocoElNino = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso ou não de ElNino
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoEnso(Section):
    """
    Bloco com a consideração de ENSO,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(25, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEnso):
            return False
        bloco: BlocoEnso = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso ou não de ENSO
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoDuracaoPorPatamar(Section):
    """
    Bloco com a consideração da duração por patamar,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDuracaoPorPatamar):
            return False
        bloco: BlocoDuracaoPorPatamar = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A configuração da duração por patamar
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoOutrosUsosAgua(Section):
    """
    Bloco com a consideração dos outros usos da água,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoOutrosUsosAgua):
            return False
        bloco: BlocoOutrosUsosAgua = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A configuração dos outros usos da água
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoCorrecaoDesvio(Section):
    """
    Bloco com a consideração da correção do desvio,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(47, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCorrecaoDesvio):
            return False
        bloco: BlocoCorrecaoDesvio = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A configuração da correção dos desvios
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoCurvaAversao(Section):
    """
    Bloco com a consideração da curva de penalização por VminP,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(40, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCurvaAversao):
            return False
        bloco: BlocoCurvaAversao = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A configuração da curva de aversão
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoTipoGeracaoENA(Section):
    """
    Bloco com a consideração do tipo de geração de ENA,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(95, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTipoGeracaoENA):
            return False
        bloco: BlocoTipoGeracaoENA = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A configuração da geração das ENAs
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRiscoDeficit(Section):
    """
    Bloco com o uso e a forma de consideração do risco de déficit,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), FloatField(4, 21, 1), FloatField(4, 27, 1)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRiscoDeficit):
            return False
        bloco: BlocoRiscoDeficit = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def primeira_profundidade_risco_deficit(self) -> Optional[float]:
        """
        O valor da opção configurada

        :return: A primeira profundidade para o cálculo do
            risco de déficit
        :rtype: float
        """
        return self.data[1]

    @primeira_profundidade_risco_deficit.setter
    def primeira_profundidade_risco_deficit(self, v: float):
        self.data[1] = v

    @property
    def segunda_profundidade_risco_deficit(self) -> Optional[float]:
        """
        O valor da opção configurada

        :return: A segunda profundidade para o cálculo do
            risco de déficit
        :rtype: float
        """
        return self.data[2]

    @segunda_profundidade_risco_deficit.setter
    def segunda_profundidade_risco_deficit(self, v: float):
        self.data[2] = v


class BlocoIteracaoParaSimFinal(Section):
    """
    Bloco com a consideração da iteração para simulação final,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoIteracaoParaSimFinal):
            return False
        bloco: BlocoIteracaoParaSimFinal = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A iteração a partir para simulação final
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoAgrupamentoLivre(Section):
    """
    Bloco com a consideração do agrupamento de intercâmbios,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoAgrupamentoLivre):
            return False
        bloco: BlocoAgrupamentoLivre = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não do agrupamento
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoEqualizacaoPenalInt(Section):
    """
    Bloco com a consideração da equalização da penalização de intercâmbios,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(19, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEqualizacaoPenalInt):
            return False
        bloco: BlocoEqualizacaoPenalInt = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A equalização da penalização do intercâmbio
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRepresentacaoSubmot(Section):
    """
    Bloco com a consideração da representação de submotorização,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(64, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRepresentacaoSubmot):
            return False
        bloco: BlocoRepresentacaoSubmot = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A representação da submotorização
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoOrdenacaoAutomatica(Section):
    """
    Bloco com a consideração da ordenação automática,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(32, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoOrdenacaoAutomatica):
            return False
        bloco: BlocoOrdenacaoAutomatica = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da ordenação automática
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoConsideraCargaAdicional(Section):
    """
    Bloco com a consideração de cargas adicionais,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(32, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConsideraCargaAdicional):
            return False
        bloco: BlocoConsideraCargaAdicional = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da carga adicional
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoDeltaZSUP(Section):
    """
    Bloco com a tolerância de variação do Zsup,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), FloatField(4, 21, 0), LiteralField(21, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDeltaZSUP):
            return False
        bloco: BlocoDeltaZSUP = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[float]:
        """
        O valor da opção configurada

        :return: O fator de correção aplicado ao Zsup
        :rtype: float
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: float):
        self.data[1] = v


class BlocoDeltaZINF(Section):
    """
    Bloco com a tolerância de variação do Zinf,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), FloatField(4, 21, 1), LiteralField(21, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDeltaZINF):
            return False
        bloco: BlocoDeltaZINF = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[float]:
        """
        O valor da opção configurada

        :return: A tolerância de consideração do Zinf para parada
        :rtype: float
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: float):
        self.data[1] = v


class BlocoDeltasConsecutivos(Section):
    """
    Bloco com o número de deltas consecutivos para covnergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(24, 0), IntegerField(1, 24)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDeltasConsecutivos):
            return False
        bloco: BlocoDeltasConsecutivos = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O número de deltas consecutivos para parada
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoDespachoAntecipadoGNL(Section):
    """
    Bloco com a consideração de despacho antecipado,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDespachoAntecipadoGNL):
            return False
        bloco: BlocoDespachoAntecipadoGNL = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração do despacho antecipado
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoModifAutomaticaAdTerm(Section):
    """
    Bloco com a consideração sobre modificação automática de adiantamento
    de térmicas, existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoModifAutomaticaAdTerm):
            return False
        bloco: BlocoModifAutomaticaAdTerm = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A modificação automática do AdTerm
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoGeracaoHidraulicaMin(Section):
    """
    Bloco com a consideração de geração hidraulica mínima,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoGeracaoHidraulicaMin):
            return False
        bloco: BlocoGeracaoHidraulicaMin = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da geração hidráulica mínima
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoSimFinalComData(Section):
    """
    Bloco com a consideração da data na simulação final,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSimFinalComData):
            return False
        bloco: BlocoSimFinalComData = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso da data na simulação final
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoGerenciamentoPLs(Section):
    """
    Bloco com as configurações do gerenciamento de PLs
    aberturas variáveis, existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(24, 0),
                IntegerField(1, 24),
                IntegerField(1, 29),
                IntegerField(1, 34),
                IntegerField(1, 39),
                IntegerField(1, 44),
                LiteralField(33, 49),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoGerenciamentoPLs):
            return False
        bloco: BlocoGerenciamentoPLs = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def utiliza_gerenciamento_pls(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso ou não do gerenciador externo de PLs.
        :rtype: int
        """
        return self.data[1]

    @utiliza_gerenciamento_pls.setter
    def utiliza_gerenciamento_pls(self, v: int):
        self.data[1] = v

    @property
    def comunicacao_dois_niveis(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O uso da comunicação em dois níveis com o
            gerenciador de PLs.
        :rtype: int
        """
        return self.data[2]

    @comunicacao_dois_niveis.setter
    def comunicacao_dois_niveis(self, v: int):
        self.data[2] = v

    @property
    def armazenamento_local_arquivos_temporarios(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O armazenamento local de arquivos temporários
            na comunicação com o gerenciador de PLs.
        :rtype: int
        """
        return self.data[3]

    @armazenamento_local_arquivos_temporarios.setter
    def armazenamento_local_arquivos_temporarios(self, v: int):
        self.data[3] = v

    @property
    def alocacao_memoria_ena(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A alocação das ENAs em memória
        :rtype: int
        """
        return self.data[4]

    @alocacao_memoria_ena.setter
    def alocacao_memoria_ena(self, v: int):
        self.data[4] = v

    @property
    def alocacao_memoria_cortes(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: OA alocação em memória dos cortes da FCF.
        :rtype: int
        """
        return self.data[5]

    @alocacao_memoria_cortes.setter
    def alocacao_memoria_cortes(self, v: int):
        self.data[5] = v


class BlocoSAR(Section):
    """
    Bloco com a configuração para uso da SAR,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSAR):
            return False
        bloco: BlocoSAR = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da SAR
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoCVAR(Section):
    """
    Bloco com a configuração para uso do CVAR,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(74, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCVAR):
            return False
        bloco: BlocoCVAR = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração do CVAR
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoZSUPMinConvergencia(Section):
    """
    Bloco com a consideração do Zsup mínimo durante a convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoZSUPMinConvergencia):
            return False
        bloco: BlocoZSUPMinConvergencia = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração do Zsup mínimo para convergência
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoDesconsideraVazaoMinima(Section):
    """
    Bloco com a configuração para desconsiderar vazao mínima,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDesconsideraVazaoMinima):
            return False
        bloco: BlocoDesconsideraVazaoMinima = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A desconsideração da VAZMIN
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRestricoesEletricas(Section):
    """
    Bloco com a consideração de restrições elétricas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRestricoesEletricas):
            return False
        bloco: BlocoRestricoesEletricas = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração de restrições elétricas
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoSelecaoCortes(Section):
    """
    Bloco com a consideração da seleção de cortes,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(24, 0),
                IntegerField(1, 24),
                IntegerField(1, 29),
                LiteralField(134, 34),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSelecaoCortes):
            return False
        bloco: BlocoSelecaoCortes = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def considera_na_backward(self) -> Optional[int]:
        """
        A seleção de cortes na etapa backward

        :return: A consideração da seleção de cortes
        :rtype: int
        """
        return self.data[1]

    @considera_na_backward.setter
    def considera_na_backward(self, v: int):
        self.data[1] = v

    @property
    def considera_na_forward(self) -> Optional[int]:
        """
        A seleção de cortes na etapa forward

        :return: A consideração da seleção de cortes
        :rtype: int
        """
        return self.data[2]

    @considera_na_forward.setter
    def considera_na_forward(self, v: int):
        self.data[2] = v


class BlocoJanelaCortes(Section):
    """
    Bloco com a consideração da janela de cortes,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoJanelaCortes):
            return False
        bloco: BlocoJanelaCortes = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da janela de cortes
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoReamostragemCenarios(Section):
    """
    Bloco com as configurações de reamostragem de cenários,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(21, 0),
                IntegerField(4, 21),
                IntegerField(4, 26),
                IntegerField(4, 31),
                LiteralField(87, 37),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoReamostragemCenarios):
            return False
        bloco: BlocoReamostragemCenarios = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def considera_reamostragem_cenarios(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da reamostragem de cenários
        :rtype: int
        """
        return self.data[1]

    @considera_reamostragem_cenarios.setter
    def considera_reamostragem_cenarios(self, v: int):
        self.data[1] = v

    @property
    def tipo_reamostragem_cenarios(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O tipo da reamostragem de cenários
        :rtype: int
        """
        return self.data[2]

    @tipo_reamostragem_cenarios.setter
    def tipo_reamostragem_cenarios(self, v: int):
        self.data[2] = v

    @property
    def passo_reamostragem_cenarios(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O passo para a reamostragem de cenários
        :rtype: int
        """
        return self.data[3]

    @passo_reamostragem_cenarios.setter
    def passo_reamostragem_cenarios(self, v: int):
        self.data[3] = v


class BlocoConvergeNoZero(Section):
    """
    Bloco com a consideração da convergência no 0,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(64, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConvergeNoZero):
            return False
        bloco: BlocoConvergeNoZero = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O cálculo da convergência no zero ou não
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoConsultaFCF(Section):
    """
    Bloco com a consideração da consulta à FCF,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConsultaFCF):
            return False
        bloco: BlocoConsultaFCF = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não da consulta à FCF
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImpressaoENA(Section):
    """
    Bloco com a consideração da impressão da ENA,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(29, 139)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImpressaoENA):
            return False
        bloco: BlocoImpressaoENA = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não da ENA
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImpressaoCortesAtivosSimFinal(Section):
    """
    Bloco com a consideração da impressão dos cortes ativos
    na simulação final, existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(29, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImpressaoCortesAtivosSimFinal):
            return False
        bloco: BlocoImpressaoCortesAtivosSimFinal = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não dos cortes ativos
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRepresentacaoAgregacao(Section):
    """
    Bloco com a representação da agregação,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(31, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRepresentacaoAgregacao):
            return False
        bloco: BlocoRepresentacaoAgregacao = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A forma de representação da agregação
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoMatrizCorrelacaoEspacial(Section):
    """
    Bloco com a representação da correlação espacial,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(21, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMatrizCorrelacaoEspacial):
            return False
        bloco: BlocoMatrizCorrelacaoEspacial = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A forma de matriz de correlação espacial
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoDesconsideraConvEstatistica(Section):
    """
    Bloco com a desconsideração do critério estatístico para convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(16, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDesconsideraConvEstatistica):
            return False
        bloco: BlocoDesconsideraConvEstatistica = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A desconsideração do critério de convergência estatístico
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoMomentoReamostragem(Section):
    """
    Bloco com a escolha do momento de reamostragem,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(25, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMomentoReamostragem):
            return False
        bloco: BlocoMomentoReamostragem = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O momento da reamostragem
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoMantemArquivosEnergias(Section):
    """
    Bloco com a escolha de manter ou não os arquivos de energias,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(35, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMantemArquivosEnergias):
            return False
        bloco: BlocoMantemArquivosEnergias = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A manutenção ou não dos arquivos de ENA
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoInicioTesteConvergencia(Section):
    """
    Bloco com a iteração de início para o teste de convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(42, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoInicioTesteConvergencia):
            return False
        bloco: BlocoInicioTesteConvergencia = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O momento do início do teste de convergência
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoSazonalizarVminT(Section):
    """
    Bloco com a escolha de sazonalizar o VminT nos períodos estáticos,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(50, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSazonalizarVminT):
            return False
        bloco: BlocoSazonalizarVminT = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A sazonalização ou não do VminT
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoSazonalizarVmaxT(Section):
    """
    Bloco com a escolha de sazonalizar o VmaxT nos períodos estáticos,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(50, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSazonalizarVmaxT):
            return False
        bloco: BlocoSazonalizarVmaxT = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A sazonalização ou não do VmaxT
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoSazonalizarVminP(Section):
    """
    Bloco com a escolha de sazonalizar o VminP nos períodos estáticos,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(50, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSazonalizarVminP):
            return False
        bloco: BlocoSazonalizarVminP = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A sazonalização ou não do VminP
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoSazonalizarCfugaCmont(Section):
    """
    Bloco com a escolha de sazonalizar Cfuga e Cmont nos períodos
    estáticos, existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(50, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSazonalizarCfugaCmont):
            return False
        bloco: BlocoSazonalizarCfugaCmont = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A sazonalização ou não dos Cfuga e Cmont
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRestricoesEmissaoGEE(Section):
    """
    Bloco com a escolha de habilitar ou não as retrições de GEE,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRestricoesEmissaoGEE):
            return False
        bloco: BlocoRestricoesEmissaoGEE = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não de restrições de GEE
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoAfluenciaAnualPARp(Section):
    """
    Bloco com a consideração da componente de afluência anual
    para o PAR(p), existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(24, 0),
                IntegerField(1, 24),
                IntegerField(1, 29),
                LiteralField(325, 33),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoAfluenciaAnualPARp):
            return False
        bloco: BlocoAfluenciaAnualPARp = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def consideracao_media_anual_afluencias(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O tipo de consideração da média dos últimos
            12 meses no ajuste do modelo PAR(p).
        :rtype: int
        """
        return self.data[1]

    @consideracao_media_anual_afluencias.setter
    def consideracao_media_anual_afluencias(self, v: int):
        self.data[1] = v

    @property
    def reducao_automatica_ordem(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração da redução automática da ordem
            no ajuste do modelo PAR(p).
        :rtype: int
        """
        return self.data[2]

    @reducao_automatica_ordem.setter
    def reducao_automatica_ordem(self, v: int):
        self.data[2] = v


class BlocoRestricoesFornecGas(Section):
    """
    Bloco com a escolha de habilitar ou não as retrições de fornecimento
    de gás, existente no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRestricoesFornecGas):
            return False
        bloco: BlocoRestricoesFornecGas = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não de restrições de
            fornecimento de gás.
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoMemCalculoCortes(Section):
    """
    Bloco com a escolha de habilitar ou não a impressão da memória de
    cálculo dos cortes de Benders.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(79, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMemCalculoCortes):
            return False
        bloco: BlocoMemCalculoCortes = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não da memória de cálculo de cortes
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoGeracaoEolica(Section):
    """
    Bloco com a escolha de habilitar ou não as incertezas na geração
    eólica na geração de cenários, cálculo da política e simulação final,
    e também a penalidade para corte de eólica.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(24, 0),
                IntegerField(1, 24),
                FloatField(6, 26, 4),
                LiteralField(71, 39),
            ]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoGeracaoEolica):
            return False
        bloco: BlocoGeracaoEolica = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def considera(self) -> int:
        """
        O valor da opção configurada

        :return: A consideração ou não de geração eólica
        :rtype: int
        """
        return self.data[1]

    @considera.setter
    def considera(self, v: int):
        self.data[1] = v

    @property
    def penalidade(self) -> float:
        """
        O valor da opção configurada

        :return: A penalidade de corte da geração eólica
        :rtype: float
        """
        return self.data[2]

    @penalidade.setter
    def penalidade(self, v: float):
        self.data[2] = v


class BlocoCompensacaoCorrelacaoCruzada(Section):
    """
    Bloco com a escolha da forma de compensação da correlação
    cruzada nos cenários do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(62, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCompensacaoCorrelacaoCruzada):
            return False
        bloco: BlocoCompensacaoCorrelacaoCruzada = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não da compensação da
            correlação cruzada.
        :rtype: int
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoConsideracaoTurbinamentoMinimoMaximo(Section):
    """
    Bloco com a escolha da consideração, ou não, das restrições de
    turbinamento mínimo e máximo nos períodos individualizados do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(120, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConsideracaoTurbinamentoMinimoMaximo):
            return False
        bloco: BlocoConsideracaoTurbinamentoMinimoMaximo = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A opção de consideração da restrição
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoConsideracaoDefluenciaMaxima(Section):
    """
    Bloco com a escolha da consideração, ou não, das restrições de
    defluência máxima nos períodos individualizados do NEWAVE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConsideracaoDefluenciaMaxima):
            return False
        bloco: BlocoConsideracaoDefluenciaMaxima = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não da restrição
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoAproveitamentoBasePLsBackward(Section):
    """
    Bloco com a escolha da consideração, ou não, das bases dos PLs
    calculadas na forward para a execução da backward.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(41, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoAproveitamentoBasePLsBackward):
            return False
        bloco: BlocoAproveitamentoBasePLsBackward = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não do aproveitamento
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoImpressaoEstadosGeracaoCortes(Section):
    """
    Bloco com a escolha da consideração, ou não, da impressão dos estados
    nos quais foram construídos os cortes (cortese.dat).
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(1, 24), LiteralField(52, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImpressaoEstadosGeracaoCortes):
            return False
        bloco: BlocoImpressaoEstadosGeracaoCortes = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A impressão ou não do arquivo
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoSementeForward(Section):
    """
    Bloco com a escolha da semente utilizada para geração de
    valores aleatórios durante a simulação forward.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(25, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSementeForward):
            return False
        bloco: BlocoSementeForward = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O valor da semente utilizada
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoSementeBackward(Section):
    """
    Bloco com a escolha da semente utilizada para geração de
    valores aleatórios durante a etapa backward.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(21, 0), IntegerField(4, 21), LiteralField(25, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoSementeBackward):
            return False
        bloco: BlocoSementeBackward = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: O valor da semente utilizada
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRestricaoLPPTurbinamentoMaximoREE(Section):
    """
    Bloco com a escolha da consideração, ou não, das restrições LPP
    de turbinamento máximo por REE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRestricaoLPPTurbinamentoMaximoREE):
            return False
        bloco: BlocoRestricaoLPPTurbinamentoMaximoREE = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não das restrições
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRestricaoLPPDefluenciaMaximaREE(Section):
    """
    Bloco com a escolha da consideração, ou não, das restrições LPP
    de defluência máxima por REE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRestricaoLPPDefluenciaMaximaREE):
            return False
        bloco: BlocoRestricaoLPPDefluenciaMaximaREE = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não das restrições
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRestricaoLPPTurbinamentoMaximoUHE(Section):
    """
    Bloco com a escolha da consideração, ou não, das restrições LPP
    de turbinamento máximo por UHE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRestricaoLPPTurbinamentoMaximoUHE):
            return False
        bloco: BlocoRestricaoLPPTurbinamentoMaximoUHE = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não das restrições
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v


class BlocoRestricaoLPPDefluenciaMaximaUHE(Section):
    """
    Bloco com a escolha da consideração, ou não, das restrições LPP
    de defluência máxima por UHE.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(24, 0), IntegerField(1, 24), LiteralField(33, 28)]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRestricaoLPPDefluenciaMaximaUHE):
            return False
        bloco: BlocoRestricaoLPPDefluenciaMaximaUHE = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())

    def write(self, file: IO):
        file.write(self.__linha.write(self.data))

    @property
    def valor(self) -> Optional[int]:
        """
        O valor da opção configurada

        :return: A consideração ou não das restrições
        :rtype: int | None
        """
        return self.data[1]

    @valor.setter
    def valor(self, v: int):
        self.data[1] = v
