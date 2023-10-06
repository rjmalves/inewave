from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from datetime import datetime


class RegistroEolicaCadastro(Register):
    """
    Registro que contém um cadastro de usina eólica.
    """

    IDENTIFIER = "EOLICA-CADASTRO"
    IDENTIFIER_DIGITS = 15
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
            LiteralField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def nome_eolica(self) -> Optional[str]:
        return self.data[1]

    @nome_eolica.setter
    def nome_eolica(self, n: str):
        self.data[1] = n

    @property
    def identificador_eolica(self) -> Optional[str]:
        return self.data[2]

    @identificador_eolica.setter
    def identificador_eolica(self, n: str):
        self.data[2] = n

    @property
    def quantidade_conjuntos(self) -> Optional[int]:
        return self.data[3]

    @quantidade_conjuntos.setter
    def quantidade_conjuntos(self, q: int):
        self.data[3] = q


class RegistroEolicaCadastroConjuntoAerogeradores(Register):
    """
    Registro que contém o cadastro de um conjunto de
    aerogeradores em uma usina eólica.
    """

    IDENTIFIER = "EOLICA-CADASTRO-CONJUNTO-AEROGERADORES"
    IDENTIFIER_DIGITS = 38
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            LiteralField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def indice_conjunto(self) -> Optional[int]:
        return self.data[1]

    @indice_conjunto.setter
    def indice_conjunto(self, c: int):
        self.data[1] = c

    @property
    def nome_conjunto(self) -> Optional[str]:
        return self.data[2]

    @nome_conjunto.setter
    def nome_conjunto(self, n: str):
        self.data[2] = n

    @property
    def quantidade_aerogeradores(self) -> Optional[int]:
        return self.data[3]

    @quantidade_aerogeradores.setter
    def quantidade_aerogeradores(self, c: int):
        self.data[3] = c


class RegistroEolicaCadastroAerogerador(Register):
    """
    Registro que contém o cadastro de um aerogerador
    pertencente a um conjunto de aerogeradores em uma
    usina eólica.
    """

    IDENTIFIER = "EOLICA-CADASTRO-AEROGERADOR"
    IDENTIFIER_DIGITS = 27
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
            FloatField(decimal_digits=3),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def indice_conjunto(self) -> Optional[int]:
        return self.data[1]

    @indice_conjunto.setter
    def indice_conjunto(self, c: int):
        self.data[1] = c

    @property
    def velocidade_cutin(self) -> Optional[float]:
        return self.data[2]

    @velocidade_cutin.setter
    def velocidade_cutin(self, v: float):
        self.data[2] = v

    @property
    def velocidade_nominal(self) -> Optional[float]:
        return self.data[3]

    @velocidade_nominal.setter
    def velocidade_nominal(self, v: float):
        self.data[3] = v

    @property
    def velocidade_cutout(self) -> Optional[float]:
        return self.data[4]

    @velocidade_cutout.setter
    def velocidade_cutout(self, v: float):
        self.data[4] = v

    @property
    def potencia_velocidade_cutin(self) -> Optional[float]:
        return self.data[5]

    @potencia_velocidade_cutin.setter
    def potencia_velocidade_cutin(self, p: float):
        self.data[5] = p

    @property
    def potencia_velocidade_nominal(self) -> Optional[float]:
        return self.data[6]

    @potencia_velocidade_nominal.setter
    def potencia_velocidade_nominal(self, p: float):
        self.data[6] = p

    @property
    def potencia_velocidade_cutout(self) -> Optional[float]:
        return self.data[7]

    @potencia_velocidade_cutout.setter
    def potencia_velocidade_cutout(self, p: float):
        self.data[7] = p

    @property
    def altura_torre(self) -> Optional[float]:
        return self.data[8]

    @altura_torre.setter
    def altura_torre(self, h: float):
        self.data[8] = h


class RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo(Register):
    """
    Registro que contém a informação de início e fim de
    operação de um conjunto de aerogeradores.
    """

    IDENTIFIER = "EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO"
    IDENTIFIER_DIGITS = 57
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def indice_conjunto(self) -> Optional[int]:
        return self.data[1]

    @indice_conjunto.setter
    def indice_conjunto(self, c: int):
        self.data[1] = c

    @property
    def periodo_inicial(self) -> Optional[datetime]:
        return self.data[2]

    @periodo_inicial.setter
    def periodo_inicial(self, p: datetime):
        self.data[2] = p

    @property
    def periodo_final(self) -> Optional[datetime]:
        return self.data[3]

    @periodo_final.setter
    def periodo_final(self, p: datetime):
        self.data[3] = p

    @property
    def numero_aerogeradores(self) -> Optional[int]:
        return self.data[4]

    @numero_aerogeradores.setter
    def numero_aerogeradores(self, n: int):
        self.data[4] = n


class RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva(Register):
    """
    Registro que contém a informação de início e fim de
    operação para uma certa potência efetiva de um conjunto
    de aerogeradores.
    """

    IDENTIFIER = "EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO"
    IDENTIFIER_DIGITS = 53
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=3),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def indice_conjunto(self) -> Optional[int]:
        return self.data[1]

    @indice_conjunto.setter
    def indice_conjunto(self, c: int):
        self.data[1] = c

    @property
    def periodo_inicial(self) -> Optional[datetime]:
        return self.data[2]

    @periodo_inicial.setter
    def periodo_inicial(self, p: datetime):
        self.data[2] = p

    @property
    def periodo_final(self) -> Optional[datetime]:
        return self.data[3]

    @periodo_final.setter
    def periodo_final(self, p: datetime):
        self.data[3] = p

    @property
    def potencia_efetiva(self) -> Optional[float]:
        return self.data[4]

    @potencia_efetiva.setter
    def potencia_efetiva(self, n: float):
        self.data[4] = n


class RegistroPEECadastro(Register):
    """
    Registro que contém um cadastro de um parque eólico equivalente.
    """

    IDENTIFIER = "PEE-CAD"
    IDENTIFIER_DIGITS = 7
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def nome_pee(self) -> Optional[str]:
        return self.data[1]

    @nome_pee.setter
    def nome_pee(self, n: str):
        self.data[1] = n


class RegistroPEEPotenciaInstaladaPeriodo(Register):
    """
    Registro que contém a informação de início e fim de
    operação para uma certa potência instalada de um parque
    eólico equivalente.
    """

    IDENTIFIER = "PEE-POT-INST-PER"
    IDENTIFIER_DIGITS = 16
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=3),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def periodo_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @periodo_inicial.setter
    def periodo_inicial(self, p: datetime):
        self.data[1] = p

    @property
    def periodo_final(self) -> Optional[datetime]:
        return self.data[2]

    @periodo_final.setter
    def periodo_final(self, p: datetime):
        self.data[2] = p

    @property
    def potencia_instalada(self) -> Optional[float]:
        return self.data[3]

    @potencia_instalada.setter
    def potencia_instalada(self, n: float):
        self.data[3] = n


class RegistroEolicaConfiguracao(Register):
    """
    Registro que contém um estado de operação de uma usina por
    período.
    """

    IDENTIFIER = "EOLICA-CONFIGURACAO-PERIODO"
    IDENTIFIER_DIGITS = 27
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def data_inicial_estado_operacao(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial_estado_operacao.setter
    def data_inicial_estado_operacao(self, n: datetime):
        self.data[1] = n

    @property
    def data_final_estado_operacao(self) -> Optional[datetime]:
        return self.data[2]

    @data_final_estado_operacao.setter
    def data_final_estado_operacao(self, n: datetime):
        self.data[2] = n

    @property
    def estado_operacao(self) -> Optional[str]:
        return self.data[3]

    @estado_operacao.setter
    def estado_operacao(self, n: str):
        self.data[3] = n


class RegistroPEEConfiguracaoPeriodo(Register):
    """
    Registro que contém um estado de operação de um PEE por
    período.
    """

    IDENTIFIER = "PEE-CONFIG-PER"
    IDENTIFIER_DIGITS = 14
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def data_inicial_estado_operacao(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial_estado_operacao.setter
    def data_inicial_estado_operacao(self, n: datetime):
        self.data[1] = n

    @property
    def data_final_estado_operacao(self) -> Optional[datetime]:
        return self.data[2]

    @data_final_estado_operacao.setter
    def data_final_estado_operacao(self, n: datetime):
        self.data[2] = n

    @property
    def estado_operacao(self) -> Optional[str]:
        return self.data[3]

    @estado_operacao.setter
    def estado_operacao(self, n: str):
        self.data[3] = n


class RegistroEolicaFTE(Register):
    """
    Registro que contém as informações da função de produção
    linear vento-potência para as usinas eólicas.
    """

    IDENTIFIER = "EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO"
    IDENTIFIER_DIGITS = 55
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=8),
            FloatField(decimal_digits=8),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c

    @property
    def coeficiente_linear(self) -> Optional[float]:
        return self.data[3]

    @coeficiente_linear.setter
    def coeficiente_linear(self, c: float):
        self.data[3] = c

    @property
    def coeficiente_angular(self) -> Optional[float]:
        return self.data[4]

    @coeficiente_angular.setter
    def coeficiente_angular(self, c: float):
        self.data[4] = c


class RegistroPEEFTE(Register):
    """
    Registro que contém as informações da função de produção
    linear vento-potência para um PEE.
    """

    IDENTIFIER = "PEE-FPVP-LIN-PU-PER"
    IDENTIFIER_DIGITS = 19
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(size=20, decimal_digits=17),
            FloatField(size=20, decimal_digits=17),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c

    @property
    def coeficiente_linear(self) -> Optional[float]:
        return self.data[3]

    @coeficiente_linear.setter
    def coeficiente_linear(self, c: float):
        self.data[3] = c

    @property
    def coeficiente_angular(self) -> Optional[float]:
        return self.data[4]

    @coeficiente_angular.setter
    def coeficiente_angular(self, c: float):
        self.data[4] = c


class RegistroEolicaGeracaoPeriodo(Register):
    """
    Registro que contém os valores de geração de uma usina
    eólica.
    """

    IDENTIFIER = "EOLICA-GERACAO-PERIODO"
    IDENTIFIER_DIGITS = 22
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c


class RegistroEolicaGeracaoPatamar(Register):
    """
    Registro que contém as profundidades dos patamares de cada
    período para o histórico de geração.
    """

    IDENTIFIER = "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR"
    IDENTIFIER_DIGITS = 43
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            FloatField(decimal_digits=4),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c

    @property
    def indice_patamar(self) -> Optional[int]:
        return self.data[3]

    @indice_patamar.setter
    def indice_patamar(self, c: int):
        self.data[3] = c

    @property
    def profundidade(self) -> Optional[float]:
        return self.data[4]

    @profundidade.setter
    def profundidade(self, c: float):
        self.data[4] = c


class RegistroPEEGeracaoPatamar(Register):
    """
    Registro que contém as profundidades dos patamares de cada
    período para o histórico de geração de um PEE.
    """

    IDENTIFIER = "PEE-GER-PROF-PER-PAT"
    IDENTIFIER_DIGITS = 20
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            FloatField(decimal_digits=4),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c

    @property
    def indice_patamar(self) -> Optional[int]:
        return self.data[3]

    @indice_patamar.setter
    def indice_patamar(self, c: int):
        self.data[3] = c

    @property
    def profundidade(self) -> Optional[float]:
        return self.data[4]

    @profundidade.setter
    def profundidade(self, c: float):
        self.data[4] = c


class RegistroEolicaHistoricoVentoHorizonte(Register):
    """
    Registro que contém o horizonte de históricos de vento.
    """

    IDENTIFIER = "EOLICA-HISTORICO-VENTO-HORIZONTE"
    IDENTIFIER_DIGITS = 32
    LINE = Line(
        [
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[0]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[0] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[1]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[1] = c


class RegistroEolicaHistoricoVento(Register):
    """
    Registro que contém os históricos de vento para o horizonte
    considerado.
    """

    IDENTIFIER = "EOLICA-HISTORICO-VENTO"
    IDENTIFIER_DIGITS = 22
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=2),
            FloatField(decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c

    @property
    def velocidade(self) -> Optional[float]:
        return self.data[3]

    @velocidade.setter
    def velocidade(self, c: float):
        self.data[3] = c

    @property
    def direcao(self) -> Optional[float]:
        return self.data[4]

    @direcao.setter
    def direcao(self, c: float):
        self.data[4] = c


class RegistroHistoricoVentoHorizonte(Register):
    """
    Registro que contém o horizonte de históricos de vento.
    """

    IDENTIFIER = "VENTO-HIST-HORIZ"
    IDENTIFIER_DIGITS = 16
    LINE = Line(
        [
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[0]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[0] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[1]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[1] = c


class RegistroHistoricoVento(Register):
    """
    Registro que contém os históricos de vento para o horizonte
    considerado em um PEE.
    """

    IDENTIFIER = "VENTO-HIST"
    IDENTIFIER_DIGITS = 10
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=2),
            FloatField(decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_posto(self) -> Optional[int]:
        return self.data[0]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c

    @property
    def velocidade(self) -> Optional[float]:
        return self.data[3]

    @velocidade.setter
    def velocidade(self, c: float):
        self.data[3] = c

    @property
    def direcao(self) -> Optional[float]:
        return self.data[4]

    @direcao.setter
    def direcao(self, c: float):
        self.data[4] = c


class RegistroPostoVentoCadastro(Register):
    """
    Registro que contém um cadastro de um posto de vento.
    """

    IDENTIFIER = "POSTO-VENTO-CAD"
    IDENTIFIER_DIGITS = 15
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_posto(self) -> Optional[int]:
        return self.data[0]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[0] = c

    @property
    def nome_posto(self) -> Optional[str]:
        return self.data[1]

    @nome_posto.setter
    def nome_posto(self, n: str):
        self.data[1] = n


class RegistroPEEPostoVento(Register):
    """
    Registro que contém um mapeamento de PEE para posto de vento
    """

    IDENTIFIER = "PEE-POSTO"
    IDENTIFIER_DIGITS = 9
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def codigo_posto(self) -> Optional[int]:
        return self.data[1]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[1] = c


class RegistroEolicaSubmercado(Register):
    """
    Registro que contém uma relação entre usina eólica e submercado.
    """

    IDENTIFIER = "EOLICA-SUBMERCADO"
    IDENTIFIER_DIGITS = 17
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def codigo_submercado(self) -> Optional[int]:
        return self.data[1]

    @codigo_submercado.setter
    def codigo_submercado(self, c: int):
        self.data[1] = c


class RegistroPEESubmercado(Register):
    """
    Registro que contém uma relação entre PEE e submercado.
    """

    IDENTIFIER = "PEE-SUBM"
    IDENTIFIER_DIGITS = 8
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
        self.data[0] = c

    @property
    def codigo_submercado(self) -> Optional[int]:
        return self.data[1]

    @codigo_submercado.setter
    def codigo_submercado(self, c: int):
        self.data[1] = c
