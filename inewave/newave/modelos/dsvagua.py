import numpy as np  # type: ignore


class DSVAgua:
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    desvios de água por usina.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que podem ser modificadas através do arquivo `dsvagua.dat`.

    **Parâmetros**

    - tabela: `np.ndarray`

    """
    def __init__(self,
                 tabela: np.ndarray):
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre DSVAgua avalia toda a tabela.
        """
        if not isinstance(o, DSVAgua):
            return False
        dsv: DSVAgua = o
        return np.array_equal(self.tabela, dsv.tabela)
