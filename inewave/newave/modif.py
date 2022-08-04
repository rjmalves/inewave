from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.modif import (
    TURBMAXT,
    TURBMINT,
    USINA,
    VAZMAXT,
    VOLMIN,
    VOLMAX,
    NUMCNJ,
    NUMMAQ,
    VAZMIN,
    CFUGA,
    CMONT,
    VMAXT,
    VMINT,
    VMINP,
    VAZMINT,
)


from typing import Type, TypeVar, List, Optional, Union


class Modif(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às alterações nas
    configurações das usinas hidroelétricas.
    """

    T = TypeVar("T")

    REGISTERS = [
        USINA,
        VOLMIN,
        VOLMAX,
        NUMCNJ,
        NUMMAQ,
        VAZMIN,
        CFUGA,
        CMONT,
        VMAXT,
        VMINT,
        VMINP,
        VAZMINT,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="modif.dat") -> "Modif":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="modif.dat"):
        self.write(diretorio, nome_arquivo)

    def __registros_por_tipo(self, registro: Type[T]) -> List[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int

        """
        return [b for b in self.data.of_type(registro)]

    def __obtem_registros(self, tipo: Type[T]) -> List[T]:
        return self.__registros_por_tipo(tipo)

    def __obtem_registros_com_filtros(
        self, tipo_registro: Type[T], **kwargs
    ) -> Optional[Union[T, List[T]]]:
        def __atende(r) -> bool:
            condicoes: List[bool] = []
            for k, v in kwargs.items():
                if v is not None:
                    condicoes.append(getattr(r, k) == v)
            return all(condicoes)

        regs_filtro = [
            r for r in self.__obtem_registros(tipo_registro) if __atende(r)
        ]
        if len(regs_filtro) == 0:
            return None
        elif len(regs_filtro) == 1:
            return regs_filtro[0]
        else:
            return regs_filtro

    def cria_registro(self, anterior: Register, registro: Register):
        """
        Adiciona um registro ao arquivo após um outro registro previamente
        existente.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.add_after(anterior, registro)

    def deleta_registro(self, registro: Register):
        """
        Remove um registro existente no arquivo.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.remove(registro)

    def lista_registros(self, tipo: Type[T]) -> List[T]:
        """
        Lista todos os registros presentes no arquivo que tenham o tipo `T`.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        return [r for r in self.data.of_type(tipo)]

    def append_registro(self, registro: Register):
        """
        Adiciona um registro ao arquivo na última posição.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.append(registro)

    def preppend_registro(self, registro: Register):
        """
        Adiciona um registro ao arquivo na primeira posição.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.preppend(registro)

    def usina(
        self, codigo: Optional[int] = None, nome: Optional[str] = None
    ) -> Optional[Union[USINA, List[USINA]]]:
        """
        Obtém um registro que define a usina modificada.

        :param codigo: código da usina modificada
        :type codigo: int | None
        :param nome: nome da usina
        :type nome: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`USINA` | list[:class:`USINA`] | None
        """
        return self.__obtem_registros_com_filtros(
            USINA, codigo=codigo, nome=nome
        )

    def volmin(
        self, volume: Optional[float] = None, unidade: Optional[str] = None
    ) -> Optional[Union[VOLMIN, List[VOLMIN]]]:
        """
        Obtém um registro que define um volume mínimo.

        :param volume: volume mínimo
        :type volume: float | None
        :param unidade: unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VOLMIN` | list[:class:`VOLMIN`] | None
        """
        return self.__obtem_registros_com_filtros(
            VOLMIN, volume=volume, unidade=unidade
        )

    def volmax(
        self, volume: Optional[float] = None, unidade: Optional[str] = None
    ) -> Optional[Union[VOLMAX, List[VOLMAX]]]:
        """
        Obtém um registro que define um volume máximo.

        :param volume: volume máximo
        :type volume: float | None
        :param unidade: unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VOLMAX` | list[:class:`VOLMAX`] | None
        """
        return self.__obtem_registros_com_filtros(
            VOLMAX, volume=volume, unidade=unidade
        )

    def numcnj(
        self,
        numero: Optional[int] = None,
    ) -> Optional[Union[NUMCNJ, List[NUMCNJ]]]:
        """
        Obtém um registro que um número de conjuntos de máquinas.

        :param numero: o número
        :type numero: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`NUMCNJ` | list[:class:`NUMCNJ`] | None
        """
        return self.__obtem_registros_com_filtros(NUMCNJ, numero=numero)

    def nummaq(
        self,
        conjunto: Optional[int] = None,
        numero_maquinas: Optional[int] = None,
    ) -> Optional[Union[NUMMAQ, List[NUMMAQ]]]:
        """
        Obtém um registro que um número de máquinas por
            conjunto de máquinas.

        :param conjunto: o conjunto
        :type conjunto: int | None
        :param numero_maquinas: o número de máquinas
        :type numero_maquinas: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`NUMMAQ` | list[:class:`NUMMAQ`] | None
        """
        return self.__obtem_registros_com_filtros(
            NUMMAQ, conjunto=conjunto, numero_maquinas=numero_maquinas
        )

    def vazmin(
        self, vazao: Optional[float] = None
    ) -> Optional[Union[VAZMIN, List[VAZMIN]]]:
        """
        Obtém um registro que define uma vazão mínima.

        :param vazao: vazão mínima
        :type vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VAZMIN` | list[:class:`VAZMIN`] | None
        """
        return self.__obtem_registros_com_filtros(VAZMIN, vazao=vazao)

    def cfuga(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        nivel: Optional[float] = None,
    ) -> Optional[Union[CFUGA, List[CFUGA]]]:
        """
        Obtém um registro que define o nível do canal de fuga.

        :param mes: mês de validade do nível
        :type mes: int | None
        :param ano: ano de validade do nível
        :type ano: int | None
        :param nivel: o nível
        :type nivel: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`CFUGA` | list[:class:`CFUGA`] | None
        """
        return self.__obtem_registros_com_filtros(
            CFUGA, mes=mes, ano=ano, nivel=nivel
        )

    def cmont(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        nivel: Optional[float] = None,
    ) -> Optional[Union[CMONT, List[CMONT]]]:
        """
        Obtém um registro que define o nível do canal de montante.

        :param mes: mês de validade do nível
        :type mes: int | None
        :param ano: ano de validade do nível
        :type ano: int | None
        :param nivel: o nível
        :type nivel: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`CMONT` | list[:class:`CMONT`] | None
        """
        return self.__obtem_registros_com_filtros(
            CMONT, mes=mes, ano=ano, nivel=nivel
        )

    def vmaxt(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
    ) -> Optional[Union[VMAXT, List[VMAXT]]]:
        """
        Obtém um registro que define o volume máximo por período.

        :param mes: mês de validade do volume
        :type mes: int | None
        :param ano: ano de validade do volume
        :type ano: int | None
        :param volume: o volume
        :type volume: float | None
        :param unidade: a unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VMAXT` | list[:class:`VMAXT`] | None
        """
        return self.__obtem_registros_com_filtros(
            VMAXT, mes=mes, ano=ano, volume=volume, unidade=unidade
        )

    def vmint(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
    ) -> Optional[Union[VMINT, List[VMINT]]]:
        """
        Obtém um registro que define o volume mínimo por período.

        :param mes: mês de validade do volume
        :type mes: int | None
        :param ano: ano de validade do volume
        :type ano: int | None
        :param volume: o volume
        :type volume: float | None
        :param unidade: a unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VMINT` | list[:class:`VMINT`] | None
        """
        return self.__obtem_registros_com_filtros(
            VMINT, mes=mes, ano=ano, volume=volume, unidade=unidade
        )

    def vminp(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
    ) -> Optional[Union[VMINP, List[VMINP]]]:
        """
        Obtém um registro que define o volume mínimo para penalidade.

        :param mes: mês de validade do volume
        :type mes: int | None
        :param ano: ano de validade do volume
        :type ano: int | None
        :param volume: o volume
        :type volume: float | None
        :param unidade: a unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VMINP` | list[:class:`VMINP`] | None
        """
        return self.__obtem_registros_com_filtros(
            VMINP, mes=mes, ano=ano, volume=volume, unidade=unidade
        )

    def vazmint(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        vazao: Optional[float] = None,
    ) -> Optional[Union[VAZMINT, List[VAZMINT]]]:
        """
        Obtém um registro que define a vazão mínima por período.

        :param mes: mês de validade da vazão
        :type mes: int | None
        :param ano: ano de validade da vazão
        :type ano: int | None
        :param vazao: a vazão mínima
        :type vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VAZMINT` | list[:class:`VAZMINT`] | None
        """
        return self.__obtem_registros_com_filtros(
            VAZMINT, mes=mes, ano=ano, vazao=vazao
        )

    def vazmaxt(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        vazao: Optional[float] = None,
    ) -> Optional[Union[VAZMAXT, List[VAZMAXT]]]:
        """
        Obtém um registro que define a vazão máxima por período.

        :param mes: mês de validade da vazão
        :type mes: int | None
        :param ano: ano de validade da vazão
        :type ano: int | None
        :param vazao: a vazão máxima
        :type vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VAZMAXT` | list[:class:`VAZMAXT`] | None
        """
        return self.__obtem_registros_com_filtros(
            VAZMAXT, mes=mes, ano=ano, vazao=vazao
        )

    def turbmaxt(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        turbinamento: Optional[float] = None,
    ) -> Optional[Union[TURBMAXT, List[TURBMAXT]]]:
        """
        Obtém um registro que define o turbinamento máximo por período.

        :param mes: mês de validade do turbinamento
        :type mes: int | None
        :param ano: ano de validade do turbinamento
        :type ano: int | None
        :param vazao: o turbinamento máximo
        :type vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`TURBMAXT` | list[:class:`TURBMAXT`] | None
        """
        return self.__obtem_registros_com_filtros(
            TURBMAXT, mes=mes, ano=ano, turbinamento=turbinamento
        )

    def turbmint(
        self,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        turbinamento: Optional[float] = None,
    ) -> Optional[Union[TURBMINT, List[TURBMINT]]]:
        """
        Obtém um registro que define o turbinamento mínimo por período.
        :param mes: mês de validade do turbinamento
        :type mes: int | None
        :param ano: ano de validade do turbinamento
        :type ano: int | None
        :param vazao: o turbinamento mínimo
        :type vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`TURBMINT` | list[:class:`TURBMINT`] | None
        """
        return self.__obtem_registros_com_filtros(
            TURBMINT, mes=mes, ano=ano, turbinamento=turbinamento
        )

    def modificacoes_usina(self, codigo: int) -> Optional[List[Register]]:
        """
        Filtra os registros que são associados a uma usina específica.

        :param codigo: O código da usina
        :type codigo: int
        :return: Os registros que modificam a usina
        :rtype: List[Register]
        """
        usinas = self.usina()
        if usinas is None or isinstance(usinas, USINA):
            return None
        reg_usina: List[USINA] = list(
            filter(lambda r: r.codigo == codigo, usinas)
        )
        modificacoes_usina: List[Register] = []
        if len(reg_usina) > 0:
            r = reg_usina[0].next
            while not (isinstance(r, USINA) or r.is_last):
                modificacoes_usina.append(r)
                r = r.next

        return modificacoes_usina
