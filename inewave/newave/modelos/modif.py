from typing import IO, List

from inewave._utils.registronewave import RegistroNEWAVE
from inewave._utils.leituraregistros import LeituraRegistros


class USINA(RegistroNEWAVE):
    """
    Registro que contém a usina modificada.
    """

    mnemonico = "USINA"

    def __init__(self):
        super().__init__(USINA.mnemonico, True)
        self._dados: list = [0, ""]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = int(dados[1])
        self._dados[1] = " ".join(dados[2:-1])

    def escreve(self, arq: IO):
        linha = (
            f" {USINA.mnemonico}".ljust(9)
            + " "
            + str(self.dados[0]).ljust(21)
            + str(self.dados[1]).ljust(30)
            + "\n"
        )
        arq.write(linha)

    @property
    def codigo(self) -> int:
        """
        O principal conteúdo do registro (código da usina).

        :return: Um `int` com o código da usina
        """
        return self._dados[0]

    @codigo.setter
    def codigo(self, t: int):
        self._dados[0] = t

    @property
    def nome(self) -> str:
        """
        O nome da usina (opcional).

        :return: Um `str` com o nome da usina
        """
        return self._dados[1]

    @nome.setter
    def nome(self, t: str):
        self._dados[1] = t


class VOLMIN(RegistroNEWAVE):
    """
    Registro que contém uma modificação de volume mínimo
    operativo para uma usina.
    """

    mnemonico = "VOLMIN"

    def __init__(self):
        super().__init__(VOLMIN.mnemonico, True)
        self._dados: list = [0, ""]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = float(dados[1])
        self._dados[1] = dados[2].strip()

    def escreve(self, arq: IO):
        linha = (
            f" {VOLMIN.mnemonico}".ljust(9)
            + "        "
            + f"{self.dados[0]:.2f}".rjust(8)
            + " "
            + str(self.dados[1]).ljust(3)
            + "\n"
        )
        arq.write(linha)

    @property
    def volume(self) -> float:
        """
        O novo valor de volume

        :return: Um `float` com o volume
        """
        return self._dados[0]

    @volume.setter
    def volume(self, t: float):
        self._dados[0] = t

    @property
    def unidade(self) -> str:
        """
        A unidade do volume informado

        :return: Um `str` com a unidade do volume
        """
        return self._dados[1]

    @unidade.setter
    def unidade(self, t: str):
        self._dados[1] = t


class VOLMAX(RegistroNEWAVE):
    """
    Registro que contém uma modificação de volume máximo
    operativo para uma usina.
    """

    mnemonico = "VOLMAX"

    def __init__(self):
        super().__init__(VOLMAX.mnemonico, True)
        self._dados: list = [0, ""]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = float(dados[1])
        self._dados[1] = dados[2].strip()

    def escreve(self, arq: IO):
        linha = (
            f" {VOLMAX.mnemonico}".ljust(9)
            + "        "
            + f"{self.dados[0]:.2f}".rjust(8)
            + " "
            + str(self.dados[1]).ljust(3)
            + "\n"
        )
        arq.write(linha)

    @property
    def volume(self) -> float:
        """
        O novo valor de volume

        :return: Um `float` com o volume
        """
        return self._dados[0]

    @volume.setter
    def volume(self, t: float):
        self._dados[0] = t

    @property
    def unidade(self) -> str:
        """
        A unidade do volume informado

        :return: Um `str` com a unidade do volume
        """
        return self._dados[1]

    @unidade.setter
    def unidade(self, t: str):
        self._dados[1] = t


class NUMCNJ(RegistroNEWAVE):
    """
    Registro que contém uma modificação de número de conjunto
    de máquinas.
    """

    mnemonico = "NUMCNJ"

    def __init__(self):
        super().__init__(NUMCNJ.mnemonico, True)
        self._dados = 0

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados = int(dados[1])

    def escreve(self, arq: IO):
        linha = (
            f" {NUMCNJ.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados)}".rjust(3)
            + "\n"
        )
        arq.write(linha)

    @property
    def numero(self) -> int:
        """
        O novo valor de numero

        :return: Um `int` com o numero
        """
        return self._dados

    @numero.setter
    def numero(self, t: int):
        self._dados = t


class NUMMAQ(RegistroNEWAVE):
    """
    Registro que contém uma modificação de número de máquinas por
    conjunto.
    """

    mnemonico = "NUMMAQ"

    def __init__(self):
        super().__init__(NUMMAQ.mnemonico, True)
        self._dados = [0, 0]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = int(dados[1])
        self._dados[1] = int(dados[2])

    def escreve(self, arq: IO):
        linha = (
            f" {NUMMAQ.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados[0])}".rjust(3)
            + " "
            + f"{str(self.dados[1])}".rjust(3)
            + "\n"
        )
        arq.write(linha)

    @property
    def conjunto(self) -> int:
        """
        O conjunto de máquinas

        :return: Um `int` com o conjunto de máquinas
        """
        return self._dados[0]

    @conjunto.setter
    def conjunto(self, t: int):
        self._dados[0] = t

    @property
    def numero_maquinas(self) -> int:
        """
        O novo número de máquinas do conjunto

        :return: Um `int` com o número de máquinas do conjunto
        """
        return self._dados[1]

    @numero_maquinas.setter
    def numero_maquinas(self, t: int):
        self._dados[1] = t


class VAZMIN(RegistroNEWAVE):
    """
    Registro que contém uma modificação de vazão mínima (m3/s).
    """

    mnemonico = "VAZMIN "

    def __init__(self):
        super().__init__(VAZMIN.mnemonico, True)
        self._dados = 0

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados = float(dados[1])

    def escreve(self, arq: IO):
        linha = (
            f" {VAZMIN.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados)}".rjust(8)
            + "\n"
        )
        arq.write(linha)

    @property
    def vazao(self) -> float:
        """
        O valor de vazão mínima

        :return: Um `float` com a vazão
        """
        return self._dados

    @vazao.setter
    def vazao(self, t: float):
        self._dados = t


class CFUGA(RegistroNEWAVE):
    """
    Registro que contém uma modificação do nível do canal de fuga.
    """

    mnemonico = "CFUGA"

    def __init__(self):
        super().__init__(CFUGA.mnemonico, True)
        self._dados = [0, 0, 0.0]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = int(dados[1])
        self._dados[1] = int(dados[2])
        self._dados[2] = float(dados[3])

    def escreve(self, arq: IO):
        linha = (
            f" {CFUGA.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados[0])}".rjust(2)
            + " "
            + f"{str(self.dados[1])}".rjust(4)
            + " "
            + f"{self.dados[2]:.2f}".rjust(7)
            + "\n"
        )
        arq.write(linha)

    @property
    def mes(self) -> int:
        """
        O mês de início da modificação

        :return: Um `int` com o mês
        """
        return self._dados[0]

    @mes.setter
    def mes(self, t: int):
        self._dados[0] = t

    @property
    def ano(self) -> int:
        """
        O ano de início da modificação

        :return: Um `int` com o ano
        """
        return self._dados[1]

    @ano.setter
    def ano(self, t: int):
        self._dados[1] = t

    @property
    def nivel(self) -> float:
        """
        O novo nivel do canal de fuga

        :return: Um `float` com o nivel
        """
        return self._dados[2]

    @nivel.setter
    def nivel(self, t: float):
        self._dados[2] = t


class CMONT(RegistroNEWAVE):
    """
    Registro que contém uma modificação do nível do canal de montante.
    """

    mnemonico = "CMONT"

    def __init__(self):
        super().__init__(CMONT.mnemonico, True)
        self._dados = [0, 0, 0.0]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = int(dados[1])
        self._dados[1] = int(dados[2])
        self._dados[2] = float(dados[3])

    def escreve(self, arq: IO):
        linha = (
            f" {CMONT.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados[0])}".rjust(2)
            + " "
            + f"{str(self.dados[1])}".rjust(4)
            + " "
            + f"{self.dados[2]:.2f}".rjust(7)
            + "\n"
        )
        arq.write(linha)

    @property
    def mes(self) -> int:
        """
        O mês de início da modificação

        :return: Um `int` com o mês
        """
        return self._dados[0]

    @mes.setter
    def mes(self, t: int):
        self._dados[0] = t

    @property
    def ano(self) -> int:
        """
        O ano de início da modificação

        :return: Um `int` com o ano
        """
        return self._dados[1]

    @ano.setter
    def ano(self, t: int):
        self._dados[1] = t

    @property
    def nivel(self) -> float:
        """
        O novo nivel do canal de montante

        :return: Um `float` com o nivel
        """
        return self._dados[2]

    @nivel.setter
    def nivel(self, t: float):
        self._dados[2] = t


class VMAXT(RegistroNEWAVE):
    """
    Registro que contém uma modificação do volume máximo
    com data
    """

    mnemonico = "VMAXT"

    def __init__(self):
        super().__init__(VMAXT.mnemonico, True)
        self._dados = [0, 0, 0.0, ""]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = int(dados[1])
        self._dados[1] = int(dados[2])
        self._dados[2] = float(dados[3])
        self._dados[3] = dados[4].strip()

    def escreve(self, arq: IO):
        linha = (
            f" {VMAXT.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados[0])}".rjust(2)
            + " "
            + f"{str(self.dados[1])}".rjust(4)
            + " "
            + f"{self.dados[2]:.3f}".rjust(7)
            + " "
            + f"{self.dados[3]}".rjust(3)
            + "\n"
        )
        arq.write(linha)

    @property
    def mes(self) -> int:
        """
        O mês de início da modificação

        :return: Um `int` com o mês
        """
        return self._dados[0]

    @mes.setter
    def mes(self, t: int):
        self._dados[0] = t

    @property
    def ano(self) -> int:
        """
        O ano de início da modificação

        :return: Um `int` com o ano
        """
        return self._dados[1]

    @ano.setter
    def ano(self, t: int):
        self._dados[1] = t

    @property
    def volume(self) -> float:
        """
        O novo volume máximo a partir da data

        :return: Um `float` com o volume
        """
        return self._dados[2]

    @volume.setter
    def volume(self, t: float):
        self._dados[2] = t

    @property
    def unidade(self) -> str:
        """
        A unidade do volume fornecido

        :return: Um `str` com o unidade
        """
        return self._dados[3]

    @unidade.setter
    def unidade(self, t: str):
        self._dados[3] = t


class VMINT(RegistroNEWAVE):
    """
    Registro que contém uma modificação do volume mínimo
    com data
    """

    mnemonico = "VMINT"

    def __init__(self):
        super().__init__(VMINT.mnemonico, True)
        self._dados = [0, 0, 0.0, ""]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = int(dados[1])
        self._dados[1] = int(dados[2])
        self._dados[2] = float(dados[3])
        self._dados[3] = dados[4].strip()

    def escreve(self, arq: IO):
        linha = (
            f" {VMINT.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados[0])}".rjust(2)
            + " "
            + f"{str(self.dados[1])}".rjust(4)
            + " "
            + f"{self.dados[2]:.3f}".rjust(7)
            + " "
            + f"{self.dados[3]}".rjust(3)
            + "\n"
        )
        arq.write(linha)

    @property
    def mes(self) -> int:
        """
        O mês de início da modificação

        :return: Um `int` com o mês
        """
        return self._dados[0]

    @mes.setter
    def mes(self, t: int):
        self._dados[0] = t

    @property
    def ano(self) -> int:
        """
        O ano de início da modificação

        :return: Um `int` com o ano
        """
        return self._dados[1]

    @ano.setter
    def ano(self, t: int):
        self._dados[1] = t

    @property
    def volume(self) -> float:
        """
        O novo volume mínimo a partir da data

        :return: Um `float` com o volume
        """
        return self._dados[2]

    @volume.setter
    def volume(self, t: float):
        self._dados[2] = t

    @property
    def unidade(self) -> str:
        """
        A unidade do volume fornecido

        :return: Um `str` com o unidade
        """
        return self._dados[3]

    @unidade.setter
    def unidade(self, t: str):
        self._dados[3] = t


class VMINP(RegistroNEWAVE):
    """
    Registro que contém uma modificação do volume mínimo
    com data para adoção de penalidade
    """

    mnemonico = "VMINP"

    def __init__(self):
        super().__init__(VMINP.mnemonico, True)
        self._dados = [0, 0, 0.0, ""]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = int(dados[1])
        self._dados[1] = int(dados[2])
        self._dados[2] = float(dados[3])
        self._dados[3] = dados[4].strip()

    def escreve(self, arq: IO):
        linha = (
            f" {VMINP.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados[0])}".rjust(2)
            + " "
            + f"{str(self.dados[1])}".rjust(4)
            + " "
            + f"{self.dados[2]:.3f}".rjust(7)
            + " "
            + f"{self.dados[3]}".rjust(3)
            + "\n"
        )
        arq.write(linha)

    @property
    def mes(self) -> int:
        """
        O mês de início da modificação

        :return: Um `int` com o mês
        """
        return self._dados[0]

    @mes.setter
    def mes(self, t: int):
        self._dados[0] = t

    @property
    def ano(self) -> int:
        """
        O ano de início da modificação

        :return: Um `int` com o ano
        """
        return self._dados[1]

    @ano.setter
    def ano(self, t: int):
        self._dados[1] = t

    @property
    def volume(self) -> float:
        """
        O novo volume mínimo a partir da data

        :return: Um `float` com o volume
        """
        return self._dados[2]

    @volume.setter
    def volume(self, t: float):
        self._dados[2] = t

    @property
    def unidade(self) -> str:
        """
        A unidade do volume fornecido

        :return: Um `str` com o unidade
        """
        return self._dados[3]

    @unidade.setter
    def unidade(self, t: str):
        self._dados[3] = t


class VAZMINT(RegistroNEWAVE):
    """
    Registro que contém uma modificação da vazão mínima
    com data.
    """

    mnemonico = "VAZMINT"

    def __init__(self):
        super().__init__(VAZMINT.mnemonico, True)
        self._dados = [0, 0, 0.0, ""]

    def le(self):
        dados = [d for d in self._linha.split(" ") if len(d) > 0]
        self._dados[0] = int(dados[1])
        self._dados[1] = int(dados[2])
        self._dados[2] = float(dados[3])

    def escreve(self, arq: IO):
        linha = (
            f" {VAZMINT.mnemonico}".ljust(9)
            + " "
            + f"{str(self.dados[0])}".rjust(2)
            + " "
            + f"{str(self.dados[1])}".rjust(4)
            + " "
            + f"{self.dados[2]:.2f}".rjust(7)
            + "\n"
        )
        arq.write(linha)

    @property
    def mes(self) -> int:
        """
        O mês de início da modificação

        :return: Um `int` com o mês
        """
        return self._dados[0]

    @mes.setter
    def mes(self, t: int):
        self._dados[0] = t

    @property
    def ano(self) -> int:
        """
        O ano de início da modificação

        :return: Um `int` com o ano
        """
        return self._dados[1]

    @ano.setter
    def ano(self, t: int):
        self._dados[1] = t

    @property
    def vazao(self) -> float:
        """
        A nova vazão mínima a partir da data

        :return: Um `float` com a vazão
        """
        return self._dados[2]

    @vazao.setter
    def vazao(self, t: float):
        self._dados[2] = t


class LeituraModif(LeituraRegistros):
    """
    Realiza a leitura do arquivo `modif.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `modif.dat`, construindo
    um objeto `Modif` cujas informações são as mesmas do modif.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self, diretorio: str):
        super().__init__(diretorio)

    # Override
    def _cria_registros_leitura(self) -> List[RegistroNEWAVE]:
        """
        Cria a lista de registros a serem lidos no arquivo modif.dat.
        """
        MAX_UHE = 200
        MAX_CNJ = 10
        MAX_EST = 60
        usina: List[RegistroNEWAVE] = [USINA() for _ in range(MAX_UHE)]
        volmin: List[RegistroNEWAVE] = [VOLMIN() for _ in range(MAX_UHE)]
        volmax: List[RegistroNEWAVE] = [VOLMAX() for _ in range(MAX_UHE)]
        numcnj: List[RegistroNEWAVE] = [NUMCNJ() for _ in range(MAX_UHE)]
        nummaq: List[RegistroNEWAVE] = [
            NUMMAQ() for _ in range(MAX_UHE * MAX_CNJ)
        ]
        vazmin: List[RegistroNEWAVE] = [VAZMIN() for _ in range(MAX_UHE)]
        cfuga: List[RegistroNEWAVE] = [
            CFUGA() for _ in range(MAX_UHE * MAX_EST)
        ]
        cmont: List[RegistroNEWAVE] = [
            CMONT() for _ in range(MAX_UHE * MAX_EST)
        ]
        vmaxt: List[RegistroNEWAVE] = [
            VMAXT() for _ in range(MAX_UHE * MAX_EST)
        ]
        vmint: List[RegistroNEWAVE] = [
            VMINT() for _ in range(MAX_UHE * MAX_EST)
        ]
        vminp: List[RegistroNEWAVE] = [
            VMINP() for _ in range(MAX_UHE * MAX_EST)
        ]
        vazmint: List[RegistroNEWAVE] = [
            VAZMINT() for _ in range(MAX_UHE * MAX_EST)
        ]
        return (
            usina
            + volmin
            + volmax
            + numcnj
            + nummaq
            + vazmin
            + cfuga
            + cmont
            + vmaxt
            + vmint
            + vminp
            + vazmint
        )
