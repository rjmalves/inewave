import re
from datetime import datetime
from typing import Any, IO, List, Optional

import numpy as np
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from cfinterface.components.datetimefield import DatetimeField
from cfinterface.components.field import Field
from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.section import Section

from inewave._utils.formatacao import (
    repete_vetor,
)
from inewave.config import (
    MAX_AGRUPAMENTOS_INTERCAMBIOS,
    MAX_MESES_ESTUDO,
    MAX_SUBMERCADOS,
)


class BlocoGruposAgrint(Section):
    """
    Bloco com informações dos intercâmbios pertencentes aos
    grupos.
    """

    __slots__ = ["__linha", "__cabecalhos"]

    FIM_BLOCO = " 999"

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
                IntegerField(3, 5),
                IntegerField(3, 9),
                FloatField(7, 13, 4),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoGruposAgrint):
            return False
        bloco: BlocoGruposAgrint = o
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
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        def converte_tabela_em_df() -> pd.DataFrame:
            cols = [
                "agrupamento",
                "submercado_de",
                "submercado_para",
                "coeficiente",
            ]
            df = pd.DataFrame(tabela, columns=cols)
            df = df.astype(
                {
                    "agrupamento": "int64",
                    "submercado_de": "int64",
                    "submercado_para": "int64",
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_AGRUPAMENTOS_INTERCAMBIOS * MAX_SUBMERCADOS, 4))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoGruposAgrint.FIM_BLOCO in linha[:4]:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                tabela[i, :] = dados
                i += 1

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do agrint.dat não foram lidos com sucesso")

        for _, linha in self.data.iterrows():
            linha_escrita = []
            for v in linha:
                linha_escrita.append(None if np.isnan(v) else int(v))
            file.write(self.__linha.write(linha_escrita))
        file.write(BlocoGruposAgrint.FIM_BLOCO + "\n")


class BlocoLimitesPorGrupoAgrint(Section):
    """
    Bloco com informações de configuração dos limites dos agrupamentos
    de intercâmbio por período de estudo.

    O número de colunas de limite, uma por patamar de carga (até 5, pelo
    manual do NEWAVE, seção 3.26), é contado na linha de template do
    cabeçalho (`` XXX  XX XXXX XX XXXX XXXXXX. ...``).
    """

    __slots__ = [
        "__linha_leitura",
        "__linha_escrita",
        "__cabecalhos",
        "__numero_patamares",
    ]

    FIM_BLOCO = " 999"

    # Layout posicional dos limites por patamar no agrint.dat
    INICIO_LIMITES = 22
    LARGURA_LIMITE = 8
    MAX_PATAMARES = 5
    # O comentário não faz parte do leiaute do manual. Nos arquivos com 3
    # patamares, ele começa 4 colunas depois do fim do último limite.
    AFASTAMENTO_COMENTARIO = 4

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__numero_patamares = 3
        self.__linha_leitura = self.__monta_linha(3, leitura=True)
        self.__linha_escrita = self.__monta_linha(3, leitura=False)
        self.__cabecalhos: List[str] = []

    @classmethod
    def __monta_linha(cls, numero_patamares: int, leitura: bool) -> Line:
        fim_limites = cls.INICIO_LIMITES + cls.LARGURA_LIMITE * numero_patamares
        # A leitura do comentário começa logo depois dos limites, para não
        # truncá-lo em um leiaute com outro afastamento.
        comentario = (
            LiteralField(40 + cls.AFASTAMENTO_COMENTARIO, fim_limites)
            if leitura
            else LiteralField(40, fim_limites + cls.AFASTAMENTO_COMENTARIO)
        )
        campos: List[Field] = [
            IntegerField(3, 1),
            DatetimeField(7, 6, format="%m %Y"),
            DatetimeField(7, 14, format="%m %Y"),
        ]
        campos += [
            FloatField(7, cls.INICIO_LIMITES + cls.LARGURA_LIMITE * i, 0)
            for i in range(numero_patamares)
        ]
        return Line(campos + [comentario])

    @classmethod
    def __conta_colunas_limite(cls, template: str) -> Optional[int]:
        """
        Conta as colunas de limite na linha de template do cabeçalho.
        """
        n = len(re.findall(r"X+\.", template))
        return n if 1 <= n <= cls.MAX_PATAMARES else None

    @classmethod
    def __ajusta_cabecalho(cls, texto: str, n_antigo: int, n_novo: int) -> str:
        """
        Acrescenta ou remove colunas de limite em uma linha do cabeçalho,
        derivando cada coluna nova da última (``LIM_P3`` -> ``LIM_P4``).
        Linhas que não chegam às colunas de limite ficam como estão.
        """
        inicio, largura = cls.INICIO_LIMITES, cls.LARGURA_LIMITE
        corpo = texto.rstrip("\n\r")
        quebra = texto[len(corpo) :]
        fim = inicio + largura * n_antigo
        if len(corpo) <= fim - largura:
            return texto
        corpo = corpo.ljust(fim)
        unidades = [
            corpo[inicio + largura * i : inicio + largura * (i + 1)]
            for i in range(min(n_antigo, n_novo))
        ]
        ultima = corpo[fim - largura : fim]
        unidades += [
            ultima.replace(str(n_antigo), str(k))
            for k in range(n_antigo + 1, n_novo + 1)
        ]
        novo = corpo[:inicio] + "".join(unidades) + corpo[fim:]
        return novo.rstrip() + quebra

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoLimitesPorGrupoAgrint):
            return False
        bloco: BlocoLimitesPorGrupoAgrint = o
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
    def read(  # type: ignore[override]  # signature extends base class
        self,
        file: IO[Any],
        numero_patamares: int = 3,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        def converte_tabela_em_df() -> pd.DataFrame:
            n = self.__numero_patamares
            df = pd.DataFrame(
                data={
                    "agrupamento": repete_vetor(agrupamentos, n),
                    "data_inicio": repete_vetor(datas_inicio, n),
                    "data_fim": repete_vetor(datas_fim, n),
                    "comentario": repete_vetor(comentarios, n),
                    "patamar": np.tile(
                        np.arange(1, n + 1),
                        len(agrupamentos),
                    ),
                    "valor": tabela.flatten(),
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        # A linha de template é a fonte de verdade do número de patamares
        # dentro do próprio arquivo; o argumento só vale como fallback.
        colunas_template = self.__conta_colunas_limite(self.__cabecalhos[-1])
        self.__numero_patamares = (
            colunas_template
            if colunas_template is not None
            else numero_patamares
        )
        self.__linha_leitura = self.__monta_linha(
            self.__numero_patamares, leitura=True
        )
        self.__linha_escrita = self.__monta_linha(
            self.__numero_patamares, leitura=False
        )

        i = 0
        agrupamentos: List[int] = []
        datas_inicio: List[datetime] = []
        datas_fim: List[datetime] = []
        comentarios: List[str] = []
        tabela = np.zeros(
            (
                MAX_AGRUPAMENTOS_INTERCAMBIOS * MAX_MESES_ESTUDO,
                self.__numero_patamares,
            )
        )
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoGruposAgrint.FIM_BLOCO in linha[:4]:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha_leitura.read(linha)
                agrupamentos.append(dados[0])
                tabela[i, :] = dados[3:-1]
                datas_inicio.append(dados[1])
                datas_fim.append(dados[2])
                comentarios.append(dados[-1])
                i += 1

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do agrint.dat não foram lidos com sucesso")

        # O DataFrame pode ter ganhado ou perdido patamares desde a leitura.
        # O cabeçalho precisa acompanhar, senão a releitura trunca os dados
        # de volta ao leiaute antigo.
        numero_patamares_dados = int(self.data["patamar"].max())
        if numero_patamares_dados != self.__numero_patamares:
            self.__cabecalhos = [
                self.__ajusta_cabecalho(
                    c, self.__numero_patamares, numero_patamares_dados
                )
                for c in self.__cabecalhos
            ]
            self.__numero_patamares = numero_patamares_dados
            self.__linha_leitura = self.__monta_linha(
                numero_patamares_dados, leitura=True
            )
            self.__linha_escrita = self.__monta_linha(
                numero_patamares_dados, leitura=False
            )

        for linha in self.__cabecalhos:
            file.write(linha)

        df = self.data.copy()
        for _, linha_agrupamento in (
            self.data[["agrupamento", "data_inicio", "data_fim", "comentario"]]
            .drop_duplicates()
            .iterrows()
        ):
            df_agrupamento = df.loc[
                (df["agrupamento"] == linha_agrupamento["agrupamento"])
                & (df["data_inicio"] == linha_agrupamento["data_inicio"])
            ]
            if not pd.isna(linha_agrupamento["data_fim"]):
                df_agrupamento = df_agrupamento.loc[
                    (
                        df_agrupamento["data_fim"]
                        == linha_agrupamento["data_fim"]
                    )
                ]
            file.write(
                self.__linha_escrita.write(
                    [
                        linha_agrupamento["agrupamento"],
                        linha_agrupamento["data_inicio"],
                        linha_agrupamento["data_fim"],
                    ]
                    + df_agrupamento.sort_values("patamar")["valor"].tolist()
                    + [linha_agrupamento["comentario"]]
                )
            )
        file.write(BlocoGruposAgrint.FIM_BLOCO + "\n")
