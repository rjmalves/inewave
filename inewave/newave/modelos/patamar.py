from typing import Any, IO, List, Optional

import numpy as np
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from cfinterface.components.field import Field
from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.section import Section

from inewave._utils.formatacao import (
    compara_dataframes_sem_ordem,
    prepara_valor_ano,
    prepara_vetor_anos_tabela,
    repete_vetor,
)
from inewave.config import (
    MAX_ANOS_ESTUDO,
    MAX_PATAMARES,
    MAX_SUBMERCADOS,
    MESES_DF,
)


class BlocoNumeroPatamares(Section):
    """
    Bloco com o número de patamares de carga considerados
    no caso.
    """

    __slots__ = [
        "__linha",
        "__cabecalhos",
    ]

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(2, 1),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumeroPatamares):
            return False
        bloco: BlocoNumeroPatamares = o
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
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        self.data = self.__linha.read(file.readline())[0]

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, int):
            raise ValueError("Dados do patamar.dat não foram lidos com sucesso")
        file.write(self.__linha.write([self.data]))


class BlocoDuracaoPatamar(Section):
    """
    Bloco com a duração de cada patamar por mês
    de estudo, extraído do arquivo `patamar.dat`.
    """

    __slots__ = [
        "__linha",
        "__cabecalhos",
    ]

    FIM_BLOCO = "SUBSISTEMA"

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        campo_ano: List[Field] = [IntegerField(4, 0)]
        campos_duracao: List[Field] = [
            FloatField(6, 6 + i * 8, 4) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_duracao)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoDuracaoPatamar):
            return False
        bloco: BlocoDuracaoPatamar = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return compara_dataframes_sem_ordem(
                self.data, bloco.data, ["patamar", "data"]
            )

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(
                data={
                    "data": prepara_vetor_anos_tabela(anos),  # type: ignore[arg-type]  # numpy array passed where List[str] expected
                    "patamar": repete_vetor(patamares),
                    "valor": tabela.flatten(),
                }
            )
            df = df.fillna(1.0)
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        ano_atual = 0
        patamar_atual = 0
        patamares: List[int] = []
        anos: List[int] = []
        tabela = np.zeros((MAX_SUBMERCADOS * MAX_ANOS_ESTUDO, len(MESES_DF)))
        while True:
            ultima_linha = file.tell()
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoDuracaoPatamar.FIM_BLOCO in linha:
                file.seek(ultima_linha)
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                    patamar_atual = 1
                anos.append(ano_atual)
                patamares.append(patamar_atual)
                tabela[i, :] = dados[1:]
                patamar_atual += 1
                i += 1

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do patamar.dat não foram lidos com sucesso")

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        for ano in sorted(df["ano"].unique()):
            for patamar in sorted(df["patamar"].unique()):
                df_ano_patamar = df.loc[
                    (df["ano"] == ano) & (df["patamar"] == patamar)
                ]
                df_ano_patamar = df_ano_patamar.sort_values(["data"])
                ano_linha = prepara_valor_ano(ano) if patamar == 1 else None
                valores = df_ano_patamar["valor"].tolist()
                file.write(self.__linha.write([ano_linha] + valores))


class BlocoCargaPatamar(Section):
    """
    Bloco com a carga de cada patamar por mês
    de estudo, extraído do arquivo `patamar.dat`.
    """

    __slots__ = [
        "__linha",
        "__linha_subsis",
        "__cabecalhos",
    ]

    FIM_BLOCO = "9999"

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line([IntegerField(4, 0)])
        campo_ano: List[Field] = [IntegerField(4, 3)]
        campo_carga: List[Field] = [
            FloatField(6, 8 + i * 7, 4) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campo_carga)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCargaPatamar):
            return False
        bloco: BlocoCargaPatamar = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return compara_dataframes_sem_ordem(
                self.data,
                bloco.data,
                ["codigo_submercado", "patamar", "data"],
            )

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(
                data={
                    "codigo_submercado": repete_vetor(submercados),
                    "data": prepara_vetor_anos_tabela(anos),  # type: ignore[arg-type]  # numpy array passed where List[str] expected
                    "patamar": repete_vetor(patamares),
                    "valor": tabela.flatten(),
                }
            )
            df = df.fillna(1.0)
            return df

        # Salta as linhas adicionais
        for _ in range(4):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        ano_atual = 0
        patamar_atual = 0
        submercados: List[int] = []
        anos: List[int] = []
        patamares: List[int] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_ANOS_ESTUDO * MAX_PATAMARES,
                len(MESES_DF),
            )
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoCargaPatamar.FIM_BLOCO in linha[:4]:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Distingue cabeçalho de subsistema de linha de tabela pelo
            # conteúdo: a linha de tabela possui valores nas colunas mensais.
            dados = self.__linha.read(linha)
            if all(valor is None for valor in dados[1:]):
                subsis_atual = self.__linha_subsis.read(linha)[0]
                # Um novo subsistema reinicia a contagem de patamares.
                patamar_atual = 1
            else:
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                    patamar_atual = 1
                submercados.append(subsis_atual)
                anos.append(ano_atual)
                patamares.append(patamar_atual)
                tabela[i, :] = dados[1:]
                patamar_atual += 1
                i += 1

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do patamar.dat não foram lidos com sucesso")

        ultimo_subsistema = 0

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        # Ordena pelas chaves de agrupamento para que a escrita do cabeçalho de
        # subsistema (emitido quando a chave muda) independa da ordem das
        # linhas no DataFrame de entrada.
        df = df.sort_values(["codigo_submercado", "ano", "patamar"])
        for _, linha_submercado in (
            df[["codigo_submercado", "ano"]].drop_duplicates().iterrows()
        ):
            for patamar in sorted(df["patamar"].unique()):
                df_merc = df.loc[
                    (
                        df["codigo_submercado"]
                        == linha_submercado["codigo_submercado"]
                    )
                    & (df["ano"] == linha_submercado["ano"])
                    & (df["patamar"] == patamar)
                ]
                df_merc = df_merc.sort_values(["data"])
                if linha_submercado["codigo_submercado"] != ultimo_subsistema:
                    ultimo_subsistema = linha_submercado["codigo_submercado"]
                    file.write(
                        self.__linha_subsis.write(
                            linha_submercado[
                                [
                                    "codigo_submercado",
                                ]
                            ].tolist()
                        )
                    )
                ano_linha = (
                    prepara_valor_ano(linha_submercado["ano"])
                    if patamar == 1
                    else None
                )
                valores = df_merc["valor"].tolist()
                file.write(self.__linha.write([ano_linha] + valores))
        file.write(BlocoCargaPatamar.FIM_BLOCO + "\n")


class BlocoIntercambioPatamarSubsistemas(Section):
    """
    Bloco com o fator de correção do intercâmbio entre subsistemas para
    cada patamar, por mês de estudo, extraído do arquivo `patamar.dat`.
    """

    __slots__ = [
        "__linha",
        "__linha_subsis",
        "__cabecalhos",
    ]

    FIM_BLOCO = "9999"

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line([IntegerField(3, 1), IntegerField(3, 5)])
        campo_ano: List[Field] = [IntegerField(4, 3)]
        campos_intercambios: List[Field] = [
            FloatField(6, 8 + i * 7, 4) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_intercambios)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoIntercambioPatamarSubsistemas):
            return False
        bloco: BlocoIntercambioPatamarSubsistemas = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return compara_dataframes_sem_ordem(
                self.data,
                bloco.data,
                ["submercado_de", "submercado_para", "patamar", "data"],
            )

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(
                data={
                    "submercado_de": repete_vetor(submercados_de),
                    "submercado_para": repete_vetor(submercados_para),
                    "data": prepara_vetor_anos_tabela(anos),  # type: ignore[arg-type]  # numpy array passed where List[str] expected
                    "patamar": repete_vetor(patamares),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(5):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_de_atual = 0
        subsis_para_atual = 0
        ano_atual = 0
        patamar_atual = 0
        submercados_de: List[int] = []
        submercados_para: List[int] = []
        patamares: List[int] = []
        anos: List[int] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF),
            )
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if (
                len(linha) < 3
                or BlocoIntercambioPatamarSubsistemas.FIM_BLOCO in linha[:4]
            ):
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Distingue cabeçalho de subsistemas de linha de tabela pelo
            # conteúdo: a linha de tabela possui valores nas colunas mensais.
            dados = self.__linha.read(linha)
            if all(valor is None for valor in dados[1:]):
                cabecalho = self.__linha_subsis.read(linha)
                subsis_de_atual = cabecalho[0]
                subsis_para_atual = cabecalho[1]
                # Um novo par de subsistemas reinicia a contagem de patamares.
                patamar_atual = 1
            else:
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                    patamar_atual = 1
                submercados_de.append(subsis_de_atual)
                submercados_para.append(subsis_para_atual)
                anos.append(ano_atual)
                patamares.append(patamar_atual)
                tabela[i, :] = dados[1:]
                patamar_atual += 1
                i += 1

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do patamar.dat não foram lidos com sucesso")

        ultimo_subsistema_de = 0
        ultimo_subsistema_para = 0

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        # Ordena pelas chaves de agrupamento para que a escrita do cabeçalho de
        # subsistemas (emitido quando a chave muda) independa da ordem das
        # linhas no DataFrame de entrada.
        df = df.sort_values(
            ["submercado_de", "submercado_para", "ano", "patamar"]
        )
        for _, linha_submercado in (
            df[["submercado_de", "submercado_para", "ano"]]
            .drop_duplicates()
            .iterrows()
        ):
            for patamar in sorted(df["patamar"].unique()):
                df_merc = df.loc[
                    (df["submercado_de"] == linha_submercado["submercado_de"])
                    & (
                        df["submercado_para"]
                        == linha_submercado["submercado_para"]
                    )
                    & (df["ano"] == linha_submercado["ano"])
                    & (df["patamar"] == patamar)
                ]
                df_merc = df_merc.sort_values(["data"])
                if any(
                    [
                        linha_submercado["submercado_de"]
                        != ultimo_subsistema_de,
                        linha_submercado["submercado_para"]
                        != ultimo_subsistema_para,
                    ]
                ):
                    ultimo_subsistema_de = linha_submercado["submercado_de"]
                    ultimo_subsistema_para = linha_submercado["submercado_para"]
                    file.write(
                        self.__linha_subsis.write(
                            linha_submercado[
                                [
                                    "submercado_de",
                                    "submercado_para",
                                ]
                            ].tolist()
                        )
                    )
                ano_linha = (
                    prepara_valor_ano(linha_submercado["ano"])
                    if patamar == 1
                    else None
                )
                valores = df_merc["valor"].tolist()
                file.write(self.__linha.write([ano_linha] + valores))
        file.write(BlocoIntercambioPatamarSubsistemas.FIM_BLOCO + "\n")


class BlocoUsinasNaoSimuladas(Section):
    """
    Bloco com a geração de usinas não simuladas em P.U. para
    cada patamar, por mês de estudo, extraído do arquivo `patamar.dat`.
    """

    __slots__ = [
        "__linha",
        "__linha_subsis",
        "__cabecalhos",
    ]

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha_subsis = Line(
            [IntegerField(3, 1), IntegerField(3, 5), LiteralField(20, 9)]
        )
        campo_ano: List[Field] = [IntegerField(4, 3)]
        campos_usinas: List[Field] = [
            FloatField(6, 8 + i * 7, 4) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_usinas)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoUsinasNaoSimuladas):
            return False
        bloco: BlocoUsinasNaoSimuladas = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return compara_dataframes_sem_ordem(
                self.data,
                bloco.data,
                [
                    "codigo_submercado",
                    "indice_bloco",
                    "fonte",
                    "patamar",
                    "data",
                ],
            )

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(
                data={
                    "codigo_submercado": repete_vetor(submercados),
                    "indice_bloco": repete_vetor(blocos),
                    "fonte": repete_vetor(fontes),
                    "data": prepara_vetor_anos_tabela(anos),  # type: ignore[arg-type]  # numpy array passed where List[str] expected
                    "patamar": repete_vetor(patamares),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(4):
            self.__cabecalhos.append(file.readline())

        i = 0
        subsis_atual = 0
        patamar_atual = 0
        bloco_atual = 0
        fonte_atual = ""
        ano_atual = 0
        submercados: List[int] = []
        blocos: List[int] = []
        fontes: List[str] = []
        patamares: List[int] = []
        anos: List[int] = []
        tabela = np.zeros(
            (
                MAX_SUBMERCADOS * MAX_SUBMERCADOS * MAX_ANOS_ESTUDO,
                len(MESES_DF),
            )
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou de tabela: uma linha de
            # tabela sempre possui valores nas colunas mensais, enquanto a
            # linha de cabeçalho de subsistema/bloco não. Esta classificação
            # por conteúdo (e não por tamanho da linha) suporta cabeçalhos com
            # rótulo textual, p.ex. "   1   1 SUDESTE BIO".
            dados = self.__linha.read(linha)
            if all(valor is None for valor in dados[1:]):
                cabecalho = self.__linha_subsis.read(linha)
                subsis_atual = cabecalho[0]
                bloco_atual = cabecalho[1]
                fonte_atual = cabecalho[2]
                # Um novo bloco/fonte reinicia a contagem de patamares.
                patamar_atual = 1
            else:
                if isinstance(dados[0], int) and dados[0] != ano_atual:
                    ano_atual = dados[0]
                    patamar_atual = 1
                submercados.append(subsis_atual)
                patamares.append(patamar_atual)
                blocos.append(bloco_atual)
                fontes.append(fonte_atual)
                anos.append(ano_atual)
                tabela[i, :] = dados[1:]
                patamar_atual += 1
                i += 1

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do patamar.dat não foram lidos com sucesso")

        ultimo_subsistema = 0
        ultimo_bloco = 0
        ultima_fonte = ""

        df = self.data.copy()
        df["ano"] = df.apply(lambda linha: linha["data"].year, axis=1)
        # Ordena pelas chaves de agrupamento para que a escrita do cabeçalho de
        # subsistema/bloco/fonte (emitido quando a chave muda) independa da
        # ordem das linhas no DataFrame de entrada.
        df = df.sort_values(
            ["codigo_submercado", "indice_bloco", "fonte", "ano", "patamar"]
        )
        for _, linha_submercado in (
            df[["codigo_submercado", "indice_bloco", "fonte", "ano"]]
            .drop_duplicates()
            .iterrows()
        ):
            for patamar in sorted(df["patamar"].unique()):
                df_merc = df.loc[
                    (
                        df["codigo_submercado"]
                        == linha_submercado["codigo_submercado"]
                    )
                    & (df["indice_bloco"] == linha_submercado["indice_bloco"])
                    & (df["fonte"] == linha_submercado["fonte"])
                    & (df["ano"] == linha_submercado["ano"])
                    & (df["patamar"] == patamar)
                ]
                df_merc = df_merc.sort_values(["data"])
                if any(
                    [
                        linha_submercado["codigo_submercado"]
                        != ultimo_subsistema,
                        linha_submercado["indice_bloco"] != ultimo_bloco,
                        linha_submercado["fonte"] != ultima_fonte,
                    ]
                ):
                    ultimo_subsistema = linha_submercado["codigo_submercado"]
                    ultimo_bloco = linha_submercado["indice_bloco"]
                    ultima_fonte = linha_submercado["fonte"]
                    file.write(
                        self.__linha_subsis.write(
                            linha_submercado[
                                [
                                    "codigo_submercado",
                                    "indice_bloco",
                                    "fonte",
                                ]
                            ].tolist()
                        )
                    )
                ano_linha = (
                    prepara_valor_ano(linha_submercado["ano"])
                    if patamar == 1
                    else None
                )
                valores = df_merc["valor"].tolist()
                file.write(self.__linha.write([ano_linha] + valores))
        file.write(BlocoIntercambioPatamarSubsistemas.FIM_BLOCO + "\n")
