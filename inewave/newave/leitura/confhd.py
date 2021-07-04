# Imports do próprio módulo
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
# Imports de módulos externos
from typing import IO, List


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


class BlocoConfUHE(Bloco):
    """
    Bloco de informações das usinas cadastradas
    no arquivo do NEWAVE `confhd.dat`.
    """
    str_inicio = "NUM  NOME"

    def __init__(self):

        super().__init__(BlocoConfUHE.str_inicio,
                         "",
                         True)

        self._dados: List[UHEConfhd] = []

    # Override
    def le(self, arq: IO):
        # Salta a linha com "XXX"
        arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(4)
        reg_nome = RegistroAn(12)
        reg_posto = RegistroIn(4)
        reg_jus = RegistroIn(4)
        reg_ree = RegistroIn(4)
        reg_vinic = RegistroFn(6)
        reg_exis = RegistroAn(4)
        reg_modif = RegistroIn(4)
        reg_inic_hist = RegistroIn(4)
        reg_fim_hist = RegistroIn(4)
        # Para cada usina, lê e processa as informações
        while True:
            linha = arq.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                break
            uhe = UHEConfhd(reg_num.le_registro(linha, 1),
                            reg_nome.le_registro(linha, 6),
                            reg_posto.le_registro(linha, 19),
                            reg_jus.le_registro(linha, 25),
                            reg_ree.le_registro(linha, 30),
                            reg_vinic.le_registro(linha, 35),
                            bool(reg_exis.le_registro(linha, 42)),
                            bool(reg_modif.le_registro(linha, 49)),
                            reg_inic_hist.le_registro(linha, 58),
                            reg_fim_hist.le_registro(linha, 67))
            self._dados.append(uhe)

    # Override
    def escreve(self, arq: IO):
        def escreve_uhe(uhe: UHEConfhd):
            linha = " "
            # Número
            linha += str(uhe.numero).rjust(4) + " "
            # Nome
            linha += uhe.nome.ljust(12) + " "
            # Posto
            linha += str(uhe.posto).rjust(4) + "  "
            # Jusante
            linha += str(uhe.jusante).rjust(4) + " "
            # REE
            linha += str(uhe.ree).rjust(4) + " "
            # Volume inicial
            linha += "{:3.2f} ".format(uhe.volume_inicial).rjust(7)
            # Existente
            linha += "  EX   " if uhe.existente else "  NE   "
            # Modificada
            linha += str(int(uhe.modificada)).rjust(4) + "     "
            # Início do histórico
            linha += str(uhe.inicio_historico).rjust(4) + "     "
            # Fim do histórico
            linha += str(uhe.fim_historico).rjust(4)
            arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = (" NUM  NOME         POSTO JUS   REE V.INIC"
                    + " U.EXIS MODIF INIC.HIST FIM HIST" + "\n")
        cabecalhos = (" XXXX XXXXXXXXXXXX XXXX  XXXX XXXX XXX.XX"
                        + " XXXX   XXXX     XXXX     XXXX" + "\n")
        arq.write(titulos)
        arq.write(cabecalhos)
        # Escreve UHEs
        for uhe in self._dados:
            escreve_uhe(uhe)


class LeituraConfhd(Leitura):
    """
    Realiza a leitura do arquivo `confhd.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `confhd.dat`, construindo
    um objeto `Confhd` cujas informações são as mesmas do `confhd.dat`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo confhd.dat.
        """
        uhes = BlocoConfUHE()
        return [uhes]
