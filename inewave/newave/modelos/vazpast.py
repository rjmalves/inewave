import warnings
from typing import Any, IO, List, Optional

import numpy as np
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.section import Section

from inewave._utils.formatacao import (
    repete_vetor,
)
from inewave.config import MAX_UHES, MESES_DF


class BlocoVazPast(Section):
    """
    Bloco de informações de vazões passadas
    por posto, existentes no arquivo `vazpast.dat`
    do NEWAVE.
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
            [IntegerField(4, 1), LiteralField(12, 6)]
            + [FloatField(10, 18 + 10 * i, 2) for i in range(len(MESES_DF))]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoVazPast):
            return False
        bloco: BlocoVazPast = o
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
            df = pd.DataFrame(
                data={
                    "codigo_posto": repete_vetor(codigos_postos),
                    "nome_posto": repete_vetor(nomes_postos),
                    "mes": np.tile(np.arange(1, 13), len(nomes_postos)),
                    "valor": tabela.flatten(),
                }
            )
            # Colunas descontinuadas, com os mesmos valores, mantidas por
            # uma versão para quem ainda usa os nomes antigos.
            df["codigo_usina"] = df["codigo_posto"]
            df["nome_usina"] = df["nome_posto"]
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_UHES, len(MESES_DF)))
        codigos_postos: List[int] = []
        nomes_postos: List[str] = []
        while True:
            linha = file.readline()
            # Confere se terminaram os postos
            if len(linha) < 3:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            codigos_postos.append(dados[0])
            nomes_postos.append(dados[1])
            tabela[i, :] = dados[2:]
            i += 1

    # Override
    def write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do vazpast.dat não foram lidos com sucesso")

        df = self.data
        codigo, nome = BlocoVazPast.__colunas_posto(df)
        for posto in df[codigo].unique():
            df_posto = df.loc[df[codigo] == posto].sort_values(["mes"])
            file.write(
                self.__linha.write(
                    [df_posto[codigo].iloc[0], df_posto[nome].iloc[0]]
                    + df_posto["valor"].tolist()
                )
            )

    @staticmethod
    def __colunas_posto(df: pd.DataFrame) -> List[str]:
        """
        Escolhe as colunas de código e nome do posto lidas na escrita. Um
        DataFrame só com as colunas descontinuadas ainda é aceito, com
        aviso. Com as duas versões de uma coluna, os valores precisam
        coincidir, para que uma edição feita só em uma delas não seja
        descartada sem aviso.
        """
        colunas: List[str] = []
        descontinuadas: List[str] = []
        for nova, descontinuada in [
            ("codigo_posto", "codigo_usina"),
            ("nome_posto", "nome_usina"),
        ]:
            if nova not in df.columns:
                colunas.append(descontinuada)
                descontinuadas.append(descontinuada)
            elif descontinuada in df.columns and not df[nova].equals(
                df[descontinuada]
            ):
                raise ValueError(
                    f"As colunas {nova} e {descontinuada} (descontinuada) do"
                    + " vazpast.dat têm valores diferentes. Edite apenas a"
                    + f" coluna {nova} ou remova a coluna {descontinuada}."
                )
            else:
                colunas.append(nova)
        if descontinuadas:
            warnings.warn(
                f"As colunas {', '.join(descontinuadas)} do vazpast.dat estão"
                + " descontinuadas. Utilize codigo_posto e nome_posto no"
                + " lugar.",
                DeprecationWarning,
                stacklevel=2,
            )
        return colunas
