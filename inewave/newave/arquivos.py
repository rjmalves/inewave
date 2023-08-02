from inewave.newave.modelos.arquivos import BlocoNomesArquivos

from cfinterface.files.sectionfile import SectionFile

from typing import List, TypeVar, Optional
import pandas as pd  # type: ignore


class Arquivos(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao arquivo
    `arquivos.dat`.

    Esta classe lida com informações de entrada do NEWAVE e
    que deve se referir aos nomes dos demais arquivos de entrada
    utilizados para o caso em questão.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoNomesArquivos]

    def __le_nome_por_indice(self, indice: int) -> Optional[str]:
        b = self.data.get_sections_of_type(BlocoNomesArquivos)
        if isinstance(b, BlocoNomesArquivos):
            if indice in b.data.index:
                dado = b.data.iloc[indice, 1]
                if isinstance(dado, str):
                    return dado
        return None

    def __atualiza_nome_por_indice(self, indice: int, nome: str):
        b = self.data.get_sections_of_type(BlocoNomesArquivos)
        if isinstance(b, BlocoNomesArquivos):
            dif = indice - b.data.shape[0] + 1
            if dif > 0:
                col_vazia = [None] * dif
                b.data = pd.concat(
                    [
                        b.data,
                        pd.DataFrame(
                            data={
                                "legenda": col_vazia,
                                "nome": col_vazia,
                            }
                        ),
                    ],
                    ignore_index=True,
                )
            b.data.iloc[indice, 1] = nome

    @property
    def arquivos(self) -> List[str]:
        """
        Os nomes dos arquivos utilizados.

        :return: Os arquivos na mesma ordem em que são declarados
        :rtype: List[str]
        """
        b = self.data.get_sections_of_type(BlocoNomesArquivos)
        return (
            [] if not isinstance(b, BlocoNomesArquivos) else b.data.iloc[:, 1]
        )

    @property
    def dger(self) -> Optional[str]:
        """
        Nome do arquivo de dados gerais utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(0)

    @dger.setter
    def dger(self, arq: str):
        self.__atualiza_nome_por_indice(0, arq)

    @property
    def sistema(self) -> Optional[str]:
        """
        Nome do arquivo de subsistemas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(1)

    @sistema.setter
    def sistema(self, arq: str):
        self.__atualiza_nome_por_indice(1, arq)

    @property
    def confhd(self) -> Optional[str]:
        """
        Nome do arquivo de configuração hidráulica utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(2)

    @confhd.setter
    def confhd(self, arq: str):
        self.__atualiza_nome_por_indice(2, arq)

    @property
    def modif(self) -> Optional[str]:
        """
        Nome do arquivo de modificações hidráulicas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(3)

    @modif.setter
    def modif(self, arq: str):
        self.__atualiza_nome_por_indice(3, arq)

    @property
    def conft(self) -> Optional[str]:
        """
        Nome do arquivo de configuração térmica utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(4)

    @conft.setter
    def conft(self, arq: str):
        self.__atualiza_nome_por_indice(4, arq)

    @property
    def term(self) -> Optional[str]:
        """
        Nome do arquivo de dados de térmicas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(5)

    @term.setter
    def term(self, arq: str):
        self.__atualiza_nome_por_indice(5, arq)

    @property
    def clast(self) -> Optional[str]:
        """
        Nome do arquivo de classes térmicas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(6)

    @clast.setter
    def clast(self, arq: str):
        self.__atualiza_nome_por_indice(6, arq)

    @property
    def exph(self) -> Optional[str]:
        """
        Nome do arquivo de expansão hidráulica utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(7)

    @exph.setter
    def exph(self, arq: str):
        self.__atualiza_nome_por_indice(7, arq)

    @property
    def expt(self) -> Optional[str]:
        """
        Nome do arquivo de expansão térmica utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(8)

    @expt.setter
    def expt(self, arq: str):
        self.__atualiza_nome_por_indice(8, arq)

    @property
    def patamar(self) -> Optional[str]:
        """
        Nome do arquivo de patamares de mercado utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(9)

    @patamar.setter
    def patamar(self, arq: str):
        self.__atualiza_nome_por_indice(9, arq)

    @property
    def cortes(self) -> Optional[str]:
        """
        Nome do arquivo de cortes utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(10)

    @cortes.setter
    def cortes(self, arq: str):
        self.__atualiza_nome_por_indice(10, arq)

    @property
    def cortesh(self) -> Optional[str]:
        """
        Nome do arquivo de cabeçalho de cortes utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(11)

    @cortesh.setter
    def cortesh(self, arq: str):
        self.__atualiza_nome_por_indice(11, arq)

    @property
    def pmo(self) -> Optional[str]:
        """
        Nome do arquivo de relatório de execução utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(12)

    @pmo.setter
    def pmo(self, arq: str):
        self.__atualiza_nome_por_indice(12, arq)

    @property
    def parp(self) -> Optional[str]:
        """
        Nome do arquivo de séries sintéticas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(13)

    @parp.setter
    def parp(self, arq: str):
        self.__atualiza_nome_por_indice(13, arq)

    @property
    def forward(self) -> Optional[str]:
        """
        Nome do arquivo de relatório da forward utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(14)

    @forward.setter
    def forward(self, arq: str):
        self.__atualiza_nome_por_indice(14, arq)

    @property
    def forwardh(self) -> Optional[str]:
        """
        Nome do arquivo de cabeçalho da forward utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(15)

    @forwardh.setter
    def forwardh(self, arq: str):
        self.__atualiza_nome_por_indice(15, arq)

    @property
    def shist(self) -> Optional[str]:
        """
        Nome do arquivo de séries históricas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(16)

    @shist.setter
    def shist(self, arq: str):
        self.__atualiza_nome_por_indice(16, arq)

    @property
    def manutt(self) -> Optional[str]:
        """
        Nome do arquivo de programação da manutenção de
        térmicas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(17)

    @manutt.setter
    def manutt(self, arq: str):
        self.__atualiza_nome_por_indice(17, arq)

    @property
    def newdesp(self) -> Optional[str]:
        """
        Nome do arquivo de despacho hidrotérmico utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(18)

    @newdesp.setter
    def newdesp(self, arq: str):
        self.__atualiza_nome_por_indice(18, arq)

    @property
    def vazpast(self) -> Optional[str]:
        """
        Nome do arquivo de tendência hidrológica utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(19)

    @vazpast.setter
    def vazpast(self, arq: str):
        self.__atualiza_nome_por_indice(19, arq)

    @property
    def itaipu(self) -> Optional[str]:
        """
        Nome do arquivo de dados de Itaipu utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(20)

    @itaipu.setter
    def itaipu(self, arq: str):
        self.__atualiza_nome_por_indice(20, arq)

    @property
    def bid(self) -> Optional[str]:
        """
        Nome do arquivo de bidding utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(21)

    @bid.setter
    def bid(self, arq: str):
        self.__atualiza_nome_por_indice(21, arq)

    @property
    def c_adic(self) -> Optional[str]:
        """
        Nome do arquivo de cargas adicionais utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(22)

    @c_adic.setter
    def c_adic(self, arq: str):
        self.__atualiza_nome_por_indice(22, arq)

    @property
    def perda(self) -> Optional[str]:
        """
        Nome do arquivo de fatores de perdas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(23)

    @perda.setter
    def perda(self, arq: str):
        self.__atualiza_nome_por_indice(23, arq)

    @property
    def gtminpat(self) -> Optional[str]:
        """
        Nome do arquivo de patamares de geração térmica
        mínima utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(24)

    @gtminpat.setter
    def gtminpat(self, arq: str):
        self.__atualiza_nome_por_indice(24, arq)

    @property
    def elnino(self) -> Optional[str]:
        """
        Nome do arquivo de ENSO 1 utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(25)

    @elnino.setter
    def elnino(self, arq: str):
        self.__atualiza_nome_por_indice(25, arq)

    @property
    def ensoaux(self) -> Optional[str]:
        """
        Nome do arquivo de ENSO 2 utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(26)

    @ensoaux.setter
    def ensoaux(self, arq: str):
        self.__atualiza_nome_por_indice(26, arq)

    @property
    def dsvagua(self) -> Optional[str]:
        """
        Nome do arquivo de desvio de água utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(27)

    @dsvagua.setter
    def dsvagua(self, arq: str):
        self.__atualiza_nome_por_indice(27, arq)

    @property
    def penalid(self) -> Optional[str]:
        """
        Nome do arquivo de penalidades por desvio utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(28)

    @penalid.setter
    def penalid(self, arq: str):
        self.__atualiza_nome_por_indice(28, arq)

    @property
    def curva(self) -> Optional[str]:
        """
        Nome do arquivo com a curva guia de penalidades por
        volume mínimo armazenado utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(29)

    @curva.setter
    def curva(self, arq: str):
        self.__atualiza_nome_por_indice(29, arq)

    @property
    def agrint(self) -> Optional[str]:
        """
        Nome do arquivo de agrupamento livre de intercâmbios
        utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(30)

    @agrint.setter
    def agrint(self, arq: str):
        self.__atualiza_nome_por_indice(30, arq)

    @property
    def adterm(self) -> Optional[str]:
        """
        Nome do arquivo de atencipação de despacho GNL
        utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(31)

    @adterm.setter
    def adterm(self, arq: str):
        self.__atualiza_nome_por_indice(31, arq)

    @property
    def ghmin(self) -> Optional[str]:
        """
        Nome do arquivo de geração hidraulica mínima utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(32)

    @ghmin.setter
    def ghmin(self, arq: str):
        self.__atualiza_nome_por_indice(32, arq)

    @property
    def sar(self) -> Optional[str]:
        """
        Nome do arquivo de aversão a risco SAR utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(33)

    @sar.setter
    def sar(self, arq: str):
        self.__atualiza_nome_por_indice(33, arq)

    @property
    def cvar(self) -> Optional[str]:
        """
        Nome do arquivo de aversão a risco CVAR utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(34)

    @cvar.setter
    def cvar(self, arq: str):
        self.__atualiza_nome_por_indice(34, arq)

    @property
    def ree(self) -> Optional[str]:
        """
        Nome do arquivo de configuração das REEs utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(35)

    @ree.setter
    def ree(self, arq: str):
        self.__atualiza_nome_por_indice(35, arq)

    @property
    def re(self) -> Optional[str]:
        """
        Nome do arquivo de restrições elétricas utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(36)

    @re.setter
    def re(self, arq: str):
        self.__atualiza_nome_por_indice(36, arq)

    @property
    def tecno(self) -> Optional[str]:
        """
        Nome do arquivo de tecnologias utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(37)

    @tecno.setter
    def tecno(self, arq: str):
        self.__atualiza_nome_por_indice(37, arq)

    @property
    def abertura(self) -> Optional[str]:
        """
        Nome do arquivo de aberturas por período utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(38)

    @abertura.setter
    def abertura(self, arq: str):
        self.__atualiza_nome_por_indice(38, arq)

    @property
    def gee(self) -> Optional[str]:
        """
        Nome do arquivo de emissões GEE utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(39)

    @gee.setter
    def gee(self, arq: str):
        self.__atualiza_nome_por_indice(39, arq)

    @property
    def clasgas(self) -> Optional[str]:
        """
        Nome do arquivo de restrições de gás utilizado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(40)

    @clasgas.setter
    def clasgas(self, arq: str):
        self.__atualiza_nome_por_indice(40, arq)

    @property
    def dados_simulacao_final(self) -> Optional[str]:
        """
        Nome do arquivo com saídas da simulação final escrito
        pelo NEWAVE.
        """
        return self.__le_nome_por_indice(41)

    @dados_simulacao_final.setter
    def dados_simulacao_final(self, arq: str):
        self.__atualiza_nome_por_indice(41, arq)

    @property
    def cortes_pos_estudo(self) -> Optional[str]:
        """
        Nome do arquivo com cortes para uso no final do horizonte
        de estudo.
        """
        return self.__le_nome_por_indice(42)

    @cortes_pos_estudo.setter
    def cortes_pos_estudo(self, arq: str):
        self.__atualiza_nome_por_indice(42, arq)

    @property
    def cortesh_pos_estudo(self) -> Optional[str]:
        """
        Nome do arquivo com cabeçalho dos cortes para uso
        no final do horizonte de estudo.
        """
        return self.__le_nome_por_indice(43)

    @cortesh_pos_estudo.setter
    def cortesh_pos_estudo(self, arq: str):
        self.__atualiza_nome_por_indice(43, arq)
