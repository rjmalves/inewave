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
