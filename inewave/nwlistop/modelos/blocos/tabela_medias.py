from typing import IO, Any, ClassVar, List, Optional

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from cfinterface.components.section import Section


class TabelaMedias(Section):
    """
    Base das tabelas dos arquivos `MEDIAS-*.CSV` do NWLISTOP, com uma linha
    por variável e entidade e uma coluna por estágio.

    As subclasses informam a coluna do arquivo com o código da entidade
    (:attr:`COLUNA_ENTIDADE`) e o nome que ela recebe na tabela lida
    (:attr:`NOME_ENTIDADE`). Sem :attr:`NOME_ENTIDADE`, a primeira coluna
    do arquivo é descartada e todas as linhas são mantidas, como no
    `MEDIAS-SIN.CSV`. Com ela, só são mantidas as linhas de código
    positivo.

    O cabeçalho numera os estágios contando os meses a partir de janeiro do
    primeiro ano do estudo. A tabela lida guarda esse número em
    ``indice_mes`` e numera os estágios a partir de 1 em ``estagio``.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE: ClassVar[str] = ""
    NOME_ENTIDADE: ClassVar[Optional[str]] = None

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        return bool(self.data.equals(o.data))

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        tabela = pd.read_csv(file, skipinitialspace=True)
        cols = tabela.columns.tolist()
        # A última coluna vem vazia, da vírgula no fim de cada linha.
        descartadas = [cols[-1]]
        cols_id: List[str] = ["VAR"]
        entidade = self.__class__.NOME_ENTIDADE
        if entidade is None:
            descartadas.append(cols[0])
        else:
            tabela = tabela.rename(
                columns={self.__class__.COLUNA_ENTIDADE: entidade}
            )
            tabela = tabela.loc[tabela[entidade] > 0]
            cols_id.append(entidade)
        df = tabela.drop(columns=descartadas)
        cols_estagios = [c for c in df.columns.tolist() if c not in cols_id]
        df = df.melt(
            id_vars=cols_id,
            value_vars=cols_estagios,
            var_name="indice_mes",
            value_name="valor",
        )
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df["indice_mes"] = df["indice_mes"].astype(int)
        df["estagio"] = df["indice_mes"] - df["indice_mes"].min() + 1
        indice = ["estagio", "indice_mes"]
        if entidade is not None:
            indice.append(entidade)
        self.data = df.pivot_table(
            index=indice,
            columns="VAR",
            values="valor",
        ).reset_index()
