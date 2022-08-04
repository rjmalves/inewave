from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField

from typing import Optional


class USINA(Register):
    """
    Registro que contém a usina modificada.
    """

    IDENTIFIER = " USINA"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(4, 9), LiteralField(20, 44)])

    @property
    def codigo(self) -> Optional[int]:
        """
        O principal conteúdo do registro (código da usina).

        :return: O código da usina
        :rtype: Optional[int]
        """
        return self.data[0]

    @codigo.setter
    def codigo(self, t: int):
        self.data[0] = t

    @property
    def nome(self) -> Optional[str]:
        """
        O nome da usina (opcional).

        :return: O nome da usina
        :rtype: Optional[str]
        """
        return self.data[1]

    @nome.setter
    def nome(self, t: str):
        self.data[1] = t


class VOLMIN(Register):
    """
    Registro que contém uma modificação de volume mínimo
    operativo para uma usina.
    """

    IDENTIFIER = " VOLMIN"
    IDENTIFIER_DIGITS = 8
    LINE = Line([LiteralField(30, 10)])
    # LINE = Line([FloatField(15, 10, 2), LiteralField(3, 26)])

    # @property
    # def volume(self) -> Optional[float]:
    #     """
    #     O novo valor de volume

    #     :return: O novo valor de volume
    #     :rtype: Optional[float]
    #     """
    #     return self.data[0]

    # @volume.setter
    # def volume(self, t: float):
    #     self.data[0] = t

    # @property
    # def unidade(self) -> Optional[str]:
    #     """
    #     A unidade do volume informado

    #     :return: A unidade do volume
    #     :rtype: Optional[str]
    #     """
    #     return self.data[1]

    # @unidade.setter
    # def unidade(self, t: str):
    #     self.data[1] = t


class VOLMAX(Register):
    """
    Registro que contém uma modificação de volume máximo
    operativo para uma usina.
    """

    IDENTIFIER = " VOLMAX"
    IDENTIFIER_DIGITS = 8
    LINE = Line([LiteralField(30, 10)])
    # LINE = Line([FloatField(15, 10, 2), LiteralField(3, 26)])

    # @property
    # def volume(self) -> Optional[float]:
    #     """
    #     O novo valor de volume

    #     :return: O novo valor de volume
    #     :rtype: Optional[float]
    #     """
    #     return self.data[0]

    # @volume.setter
    # def volume(self, t: float):
    #     self.data[0] = t

    # @property
    # def unidade(self) -> Optional[str]:
    #     """
    #     A unidade do volume informado

    #     :return: A unidade do volume
    #     :rtype: Optional[str]
    #     """
    #     return self.data[1]

    # @unidade.setter
    # def unidade(self, t: str):
    #     self.data[1] = t


class NUMCNJ(Register):
    """
    Registro que contém uma modificação de número de conjunto
    de máquinas.
    """

    IDENTIFIER = " NUMCNJ"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(3, 10)])

    @property
    def numero(self) -> int:
        """
        O novo valor do número de conjuntos

        :return: O novo número de conjuntos
        :rtype: Optional[int]
        """
        return self.data[0]

    @numero.setter
    def numero(self, t: int):
        self.data[0] = t


class NUMMAQ(Register):
    """
    Registro que contém uma modificação do número de máquinas em um
    conjunto de máquinas.
    """

    IDENTIFIER = " NUMMAQ"
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(3, 10), IntegerField(3, 14)])

    @property
    def conjunto(self) -> Optional[int]:
        """
        O conjunto de máquinas que terá o número alterado

        :return: O índice do conjunto de máquinas
        :rtype: Optional[int]
        """
        return self.data[0]

    @conjunto.setter
    def conjunto(self, t: int):
        self.data[0] = t

    @property
    def numero_maquinas(self) -> Optional[int]:
        """
        O novo número de máquinas do conjunto

        :return: O número de máquinas do conjunto
        :rtype: Optional[int]
        """
        return self.data[1]

    @numero_maquinas.setter
    def numero_maquinas(self, t: int):
        self.data[1] = t


class VAZMIN(Register):
    """
    Registro que contém uma modificação de vazão mínima (m3/s).
    """

    IDENTIFIER = " VAZMIN "
    IDENTIFIER_DIGITS = 8
    LINE = Line([IntegerField(8, 10)])

    @property
    def vazao(self) -> Optional[int]:
        """
        O valor de vazão mínima

        :return: A nova vazão
        :rtype: Optional[int]
        """
        return self.data[0]

    @vazao.setter
    def vazao(self, t: int):
        self.data[0] = t


class CFUGA(Register):
    """
    Registro que contém uma modificação do nível do canal de fuga.
    """

    IDENTIFIER = " CFUGA"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [IntegerField(2, 10), IntegerField(4, 13), FloatField(7, 18, 3)]
    )

    @property
    def mes(self) -> int:
        """
        O mês de início da modificação

        :return: O mês de início da modificação
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> int:
        """
        O ano de início da modificação

        :return: O ano de início da modificação
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def nivel(self) -> float:
        """
        O novo nivel do canal de fuga

        :return: O novo nível
        :rtype: Optional[int]
        """
        return self.data[2]

    @nivel.setter
    def nivel(self, t: float):
        self.data[2] = t


class CMONT(Register):
    """
    Registro que contém uma modificação do nível do canal de montante.
    """

    IDENTIFIER = " CMONT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [IntegerField(2, 10), IntegerField(4, 13), FloatField(7, 18, 3)]
    )

    @property
    def mes(self) -> Optional[int]:
        """
        O mês de início da modificação

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> Optional[int]:
        """
        O ano de início da modificação

        :return: O ano
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def nivel(self) -> Optional[float]:
        """
        O novo nivel do canal de montante

        :return: O novo nível
        :rtype: Optional[float]
        """
        return self.data[2]

    @nivel.setter
    def nivel(self, t: float):
        self.data[2] = t


class VMAXT(Register):
    """
    Registro que contém uma modificação do volume máximo
    com data.
    """

    IDENTIFIER = " VMAXT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 3),
            LiteralField(3, 26),
        ]
    )

    @property
    def mes(self) -> Optional[int]:
        """
        O mês de início da modificação

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> Optional[int]:
        """
        O ano de início da modificação

        :return: O ano
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def volume(self) -> Optional[float]:
        """
        O novo volume máximo

        :return: O novo volume
        :rtype: Optional[float]
        """
        return self.data[2]

    @volume.setter
    def volume(self, t: float):
        self.data[2] = t

    @property
    def unidade(self) -> Optional[str]:
        """
        A unidade de fornecimento do volume

        :return: A unidade
        :rtype: Optional[str]
        """
        return self.data[3]

    @unidade.setter
    def unidade(self, t: str):
        self.data[3] = t


class VMINT(Register):
    """
    Registro que contém uma modificação do volume mínimo
    com data.
    """

    IDENTIFIER = " VMINT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 3),
            LiteralField(3, 26),
        ]
    )

    @property
    def mes(self) -> Optional[int]:
        """
        O mês de início da modificação

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> Optional[int]:
        """
        O ano de início da modificação

        :return: O ano
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def volume(self) -> Optional[float]:
        """
        O novo volume mínimo

        :return: O novo volume
        :rtype: Optional[float]
        """
        return self.data[2]

    @volume.setter
    def volume(self, t: float):
        self.data[2] = t

    @property
    def unidade(self) -> Optional[str]:
        """
        A unidade de fornecimento do volume

        :return: A unidade
        :rtype: Optional[str]
        """
        return self.data[3]

    @unidade.setter
    def unidade(self, t: str):
        self.data[3] = t


class VMINP(Register):
    """
    Registro que contém uma modificação do volume mínimo
    com data para adoção de penalidade.
    """

    IDENTIFIER = " VMINP"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 3),
            LiteralField(3, 26),
        ]
    )

    @property
    def mes(self) -> Optional[int]:
        """
        O mês de início da modificação

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> Optional[int]:
        """
        O ano de início da modificação

        :return: O ano
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def volume(self) -> Optional[float]:
        """
        O novo volume mínimo a partir da data

        :return: O novo volume
        :rtype: Optional[float]
        """
        return self.data[2]

    @volume.setter
    def volume(self, t: float):
        self.data[2] = t

    @property
    def unidade(self) -> Optional[str]:
        """
        A unidade do volume fornecido

        :return: A unidade
        :rtype: Optional[str]
        """
        return self.data[3]

    @unidade.setter
    def unidade(self, t: str):
        self.data[3] = t


class VAZMINT(Register):
    """
    Registro que contém uma modificação da vazão mínima
    com data.
    """

    IDENTIFIER = " VAZMINT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def mes(self) -> Optional[int]:
        """
        O mês de início da modificação

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> Optional[int]:
        """
        O ano de início da modificação

        :return: O ano
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def vazao(self) -> Optional[float]:
        """
        A nova vazão mínima a partir da data

        :return: A nova vazão
        :rtype: Optional[float]
        """
        return self.data[2]

    @vazao.setter
    def vazao(self, t: float):
        self.data[2] = t


class VAZMAXT(Register):
    """
    Registro que contém uma modificação da vazão máxima
    com data.
    """

    IDENTIFIER = " VAZMAXT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def mes(self) -> Optional[int]:
        """
        O mês de início da modificação

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> Optional[int]:
        """
        O ano de início da modificação

        :return: O ano
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def vazao(self) -> Optional[float]:
        """
        A nova vazão máxima a partir da data

        :return: A nova vazão
        :rtype: Optional[float]
        """
        return self.data[2]

    @vazao.setter
    def vazao(self, t: float):
        self.data[2] = t


class TURBMAXT(Register):
    """
    Registro que contém uma modificação da turbinamento máximo
    com data.
    """

    IDENTIFIER = " TURBMAXT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def mes(self) -> Optional[int]:
        """
        O mês de início da modificação

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> Optional[int]:
        """
        O ano de início da modificação

        :return: O ano
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def turbinamento(self) -> Optional[float]:
        """
        O novo turbinamento máximo a partir da data

        :return: O novo turbinamento
        :rtype: Optional[float]
        """
        return self.data[2]

    @turbinamento.setter
    def turbinamento(self, t: float):
        self.data[2] = t


class TURBMINT(Register):
    """
    Registro que contém uma modificação da turbinamento mínimo
    com data.
    """

    IDENTIFIER = " TURBMINT"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(2, 10),
            IntegerField(4, 13),
            FloatField(7, 18, 2),
        ]
    )

    @property
    def mes(self) -> Optional[int]:
        """
        O mês de início da modificação

        :return: O mês
        :rtype: Optional[int]
        """
        return self.data[0]

    @mes.setter
    def mes(self, t: int):
        self.data[0] = t

    @property
    def ano(self) -> Optional[int]:
        """
        O ano de início da modificação

        :return: O ano
        :rtype: Optional[int]
        """
        return self.data[1]

    @ano.setter
    def ano(self, t: int):
        self.data[1] = t

    @property
    def turbinamento(self) -> Optional[float]:
        """
        O novo turbinamento mínimo a partir da data

        :return: O novo turbinamento
        :rtype: Optional[float]
        """
        return self.data[2]

    @turbinamento.setter
    def turbinamento(self, t: float):
        self.data[2] = t
