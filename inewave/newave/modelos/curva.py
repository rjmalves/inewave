from inewave.config import MAX_ANOS_ESTUDO, MAX_SUBMERCADOS, MESES_DF

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.literalfield import LiteralField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class BlocoConfiguracoesPenalizacaoCurva(Section):
    """
    Bloco de informações das usinas cadastradas
    no arquivo do NEWAVE `conft.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
                IntegerField(3, 5),
                IntegerField(3, 9),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConfiguracoesPenalizacaoCurva):
            return False
        bloco: BlocoConfiguracoesPenalizacaoCurva = o
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
    def read(self, file: IO):
        self.__cabecalhos.append(file.readline())

        self.data = self.__linha.read(file.readline())

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, list):
            raise ValueError("Dados do curva.dat não foram lidos com sucesso")
        file.write(self.__linha.write(self.data))


class BlocoPenalidadesViolacaoREECurva(Section):
    """
    Bloco com informações das penalidades por violação para cada
    REE.
    """

    FIM_BLOCO = " 999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
                FloatField(7, 11, 2),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoPenalidadesViolacaoREECurva):
            return False
        bloco: BlocoPenalidadesViolacaoREECurva = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=["Sistema", "Custo"])
            df = df.astype({"Sistema": "int64"})
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_SUBMERCADOS, 2))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if (
                len(linha) < 3
                or BlocoPenalidadesViolacaoREECurva.FIM_BLOCO in linha
            ):
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            tabela[i, :] = self.__linha.read(linha)
            i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do curva.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            file.write(
                self.__linha.write([int(lin["Sistema"])] + [lin["Custo"]])
            )
        file.write(BlocoPenalidadesViolacaoREECurva.FIM_BLOCO + "\n")


class BlocoCurvaSegurancaSubsistema(Section):
    """
    Bloco com informações da curva de segurança de operação por mês/ano
    e por subsistema.
    """

    FIM_BLOCO = "9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line([IntegerField(3, 1)])
        campo_ano: List[Field] = [IntegerField(4, 0)]
        campos_curva: List[Field] = [
            FloatField(5, i * 6 + 6, 1) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_curva)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCurvaSegurancaSubsistema):
            return False
        bloco: BlocoCurvaSegurancaSubsistema = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=["REE", "Ano"] + MESES_DF)
            df = df.astype({"REE": "int64", "Ano": "int64"})
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        tabela = np.zeros(
            (MAX_SUBMERCADOS * MAX_ANOS_ESTUDO, len(MESES_DF) + 2)
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if (
                len(linha) < 3
                or BlocoCurvaSegurancaSubsistema.FIM_BLOCO in linha
            ):
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            if len(linha) < 10:
                subsis_atual = self.__linha_subsis.read(linha)[0]
            else:
                tabela[i, 0] = subsis_atual
                tabela[i, 1:] = self.__linha.read(linha)
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do curva.dat não foram lidos com sucesso")

        ultimo_ree = 0
        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if linha_lida["REE"] != ultimo_ree:
                ultimo_ree = linha_lida["REE"]
                file.write(self.__linha_subsis.write([int(ultimo_ree)]))
            file.write(
                self.__linha.write(
                    [int(linha_lida["Ano"])] + linha_lida[MESES_DF].tolist()
                )
            )

        file.write(BlocoCurvaSegurancaSubsistema.FIM_BLOCO + "\n")


class BlocoMaximoIteracoesProcessoIterativoEtapa2(Section):
    """
    Bloco com informações do número máximo de iterações da
    segunda etapa do processo iterativo no cálculo da curva de aversão.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(26, 0), IntegerField(6, 28), LiteralField(46, 39)]
        )
        self.__cabecalhos: List[str] = []
        self.__campo: str = ""
        self.__comentario: str = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMaximoIteracoesProcessoIterativoEtapa2):
            return False
        bloco: BlocoMaximoIteracoesProcessoIterativoEtapa2 = o
        if not all(
            [
                isinstance(self.data, int),
                isinstance(o.data, int),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO):

        # Salta as linhas adicionais
        self.__cabecalhos.append(file.readline())

        self.__campo, self.data, self.__comentario = self.__linha.read(
            file.readline()
        )

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, int):
            raise ValueError("Dados do curva.dat não foram lidos com sucesso")

        file.write(
            self.__linha.write([self.__campo, self.data, self.__comentario])
        )


class BlocoIteracaoAPartirProcessoIterativoEtapa2(Section):
    """
    Bloco com informações da iteração a partir da qual ocorre a
    segunda etapa do processo iterativo no cálculo da curva de aversão.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(26, 0), IntegerField(6, 28), LiteralField(46, 39)]
        )
        self.__campo: str = ""
        self.__comentario: str = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoIteracaoAPartirProcessoIterativoEtapa2):
            return False
        bloco: BlocoIteracaoAPartirProcessoIterativoEtapa2 = o
        if not all(
            [
                isinstance(self.data, int),
                isinstance(o.data, int),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO):

        self.__campo, self.data, self.__comentario = self.__linha.read(
            file.readline()
        )

    # Override
    def write(self, file: IO):
        if not isinstance(self.data, int):
            raise ValueError("Dados do curva.dat não foram lidos com sucesso")

        file.write(
            self.__linha.write([self.__campo, self.data, self.__comentario])
        )


class BlocoToleranciaProcessoIterativoEtapa2(Section):
    """
    Bloco com informações da tolerância para a
    segunda etapa do processo iterativo no cálculo da curva de aversão.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(26, 0), FloatField(6, 28, 3), LiteralField(46, 39)]
        )
        self.__campo: str = ""
        self.__comentario: str = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoToleranciaProcessoIterativoEtapa2):
            return False
        bloco: BlocoToleranciaProcessoIterativoEtapa2 = o
        if not all(
            [
                isinstance(self.data, float),
                isinstance(o.data, float),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO):

        self.__campo, self.data, self.__comentario = self.__linha.read(
            file.readline()
        )

    # Override
    def write(self, file: IO):
        if not isinstance(self.data, float):
            raise ValueError("Dados do curva.dat não foram lidos com sucesso")

        file.write(
            self.__linha.write([self.__campo, self.data, self.__comentario])
        )


class BlocoImpressaoRelatorioProcessoIterativoEtapa2(Section):
    """
    Bloco com informações da impressão de relatório na
    segunda etapa do processo iterativo no cálculo da curva de aversão.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [LiteralField(26, 0), IntegerField(6, 28), LiteralField(46, 39)]
        )
        self.__campo: str = ""
        self.__comentario: str = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoImpressaoRelatorioProcessoIterativoEtapa2):
            return False
        bloco: BlocoImpressaoRelatorioProcessoIterativoEtapa2 = o
        if not all(
            [
                isinstance(self.data, int),
                isinstance(o.data, int),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO):
        self.__campo, self.data, self.__comentario = self.__linha.read(
            file.readline()
        )

    # Override
    def write(self, file: IO):
        if not isinstance(self.data, int):
            raise ValueError("Dados do curva.dat não foram lidos com sucesso")

        file.write(
            self.__linha.write([self.__campo, self.data, self.__comentario])
        )
