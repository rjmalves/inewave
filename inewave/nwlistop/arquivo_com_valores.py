from typing import Optional, Protocol

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package


class ArquivoComValores(Protocol):
    """
    Interface comum aos arquivos de saída do NWLISTOP que expõem os seus
    dados em uma tabela, na propriedade ``valores``, como :class:`Cmarg`,
    :class:`Ghtot` e :class:`Mediasmerc`. Todos os arquivos do módulo,
    exceto o :class:`Nwlistopdat`, satisfazem esta interface.

    A interface é estrutural: as classes não herdam dela, e qualquer
    classe com a propriedade ``valores`` a satisfaz. Ela serve para
    anotar o código que trata esses arquivos da mesma forma, como uma
    função que aceita qualquer um deles.
    """

    @property
    def valores(self) -> Optional[pd.DataFrame]:
        """
        A tabela com os dados do arquivo.

        :return: A tabela, ou ``None`` quando o arquivo não tem valores.
        :rtype: pd.DataFrame | None
        """
        ...
