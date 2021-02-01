from typing import Dict


class UHEConfhd:
    """
    Armazena dados de uma UHE conforme configurada no
    arquivo `confhd.dat`.

    **Parâmetros**

    - numero: `int`
    - nome: `str`
    - posto: `int`
    - jusante: `int`
    - ree: `int`
    - volume_inicial: `float`
    - existente: `bool`
    - modificada: `bool`
    - numero: `int`
    - inicio_historico: `int`
    - fim_historico: `int`

    """
    __slots__ = ["numero",
                 "nome",
                 "posto",
                 "jusante",
                 "ree",
                 "volume_inicial",
                 "existente",
                 "modificada",
                 "inicio_historico",
                 "fim_historico"]

    def __init__(self,
                 numero: int,
                 nome: str,
                 posto: int,
                 jusante: int,
                 ree: int,
                 volume_inicial: float,
                 existente: bool,
                 modificada: bool,
                 inicio_historico: int,
                 fim_historico: int):
        self.numero = numero
        self.nome = nome
        self.posto = posto
        self.jusante = jusante
        self.ree = ree
        self.volume_inicial = volume_inicial
        self.existente = existente
        self.modificada = modificada
        self.inicio_historico = inicio_historico
        self.fim_historico = fim_historico

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre UHEConfhd avalia todos os campos.
        """
        if not isinstance(o, UHEConfhd):
            return False
        uhe: UHEConfhd = o
        dif = False
        for s1, s2 in zip(self.__slots__,
                          uhe.__slots__):
            if s1 != s2 or getattr(self, s1) != getattr(uhe, s2):
                dif = True
                break
        return not dif


class Confhd:
    """
    Armazena os dados de entrada do NEWAVE referentes às
    configurações das usinas hidrelétricas.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que podem ser modificadas através do arquivo `modif.dat`.

    **Parâmetros**

    - usinas: `Dict[int, UHEConfhd]`

    """
    def __init__(self,
                 usinas: Dict[int, UHEConfhd]):
        self.usinas = usinas

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre Confhd avalia todas as usinas.
        """
        if not isinstance(o, Confhd):
            return False
        confhd: Confhd = o
        dif = False
        for (n1, uhe1), (n2, uhe2) in zip(self.usinas.items(),
                                          confhd.usinas.items()):
            if n1 != n2 or uhe1 != uhe2:
                dif = True
                break
        return not dif
