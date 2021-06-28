class Caso:
    """
    Armazena os dados de entrada do NEWAVE referentes ao arquivo
    `caso.dat`.

    Esta classe lida com informações de entrada do NEWAVE e
    que deve se referir ao caminho do `arquivos.dat`.

    **Parâmetros**

    - caso: `str`

    """

    def __init__(self,
                 arquivo: str):
        self._arquivo = arquivo

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre Caso avalia o único campo.
        """
        if not isinstance(o, Caso):
            return False
        caso: Caso = o
        return caso._arquivo == o._arquivo

    @property
    def arquivo(self):
        """
        Caminho para o arquivo `arquivos.dat` de entrada do NEWAVE.

        **Retorna**

        `str`

        **Sobre**

        Retorna o caminho completo (unix-like) para o arquivo que direciona
        para os demais dados de entrada do NEWAVE.
        """
        return self._arquivo
