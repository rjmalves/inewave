# Imports do próprio módulo
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroAn
# Imports de módulos externos
from typing import IO, List


class BlocoNomesArquivos(Bloco):
    """
    Bloco de informações do arquivo de
    entrada do NEWAVE `arquivos.dat`.
    """

    legendas = [
                "DADOS GERAIS                :",
                "DADOS DOS SUBSIST/SUBMERCADO:",
                "CONFIGURACAO HIDRAULICA     :",
                "ALTERACAO DADOS USINAS HIDRO:",
                "CONFIGURACAO TERMICA        :",
                "DADOS DAS USINAS TERMICAS   :",
                "DADOS DAS CLASSES TERMICAS  :",
                "DADOS DE EXPANSAO HIDRAULICA:",
                "ARQUIVO DE EXPANSAO TERMICA :",
                "ARQUIVO DE PATAMARES MERCADO:",
                "ARQUIVO DE CORTES DE BENDERS:",
                "ARQUIVO DE CABECALHO CORTES :",
                "RELATORIO DE CONVERGENCIA   :",
                "RELATORIO DE E. SINTETICAS  :",
                "RELATORIO DETALHADO FORWARD :",
                "ARQUIVO DE CABECALHO FORWARD:",
                "ARQUIVO DE S.HISTORICAS S.F.:",
                "ARQUIVO DE MANUT.PROG. UTE'S:",
                "ARQUIVO P/DESPACHO HIDROTERM:",
                "ARQUIVO C/TEND. HIDROLOGICA :",
                "ARQUIVO C/DADOS DE ITAIPU   :",
                "ARQUIVO C/DEMAND S. BIDDING :",
                "ARQUIVO C/CARGAS ADICIONAIS :",
                "ARQUIVO C/FATORES DE PERDAS :",
                "ARQUIVO C/PATAMARES GTMIN   :",
                "ARQUIVO ENSO 1              :",
                "ARQUIVO ENSO 2              :",
                "ARQUIVO DSVAGUA             :",
                "ARQUIVO P/PENALID. POR DESV.:",
                "ARQUIVO C.GUIA / PENAL.VMINT:",
                "ARQUIVO AGRUPAMENTO LIVRE   :",
                "ARQUIVO ANTEC.DESP.GNL      :",
                "ARQUIVO GER. HIDR. MIN.     :",
                "ARQUIVO AVERSAO RISCO - SAR :",
                "ARQUIVO AVERSAO RISCO - CVAR:",
                "DADOS DOS RESER.EQ.ENERGIA  :",
                "DADOS DOS REST. ELETRICAS   :",
                "ARQUIVO DE TECNOLOGIAS      :",
                "DADOS DE ABERTURAS          :",
                "ARQUIVO DE EMISSOES GEE     :",
                "ARQUIVO DE RESTRICAO DE GAS :"
               ]

    def __init__(self,
                 str_inicio: str,
                 str_final: str,
                 obrigatorio: bool):

        super().__init__(str_inicio,
                         str_final,
                         obrigatorio)

        self._dados = [""] * len(BlocoNomesArquivos.legendas)

    # Override
    def le(self, arq: IO):
        reg = RegistroAn(12)
        self._dados[0] = reg.le_registro(self._linha_inicio, 30)
        for i in range(len(self._dados)):
            linha = arq.readline()
            # Confere se já terminou (possíveis \n ao final)
            if len(linha) < 3:
                break
            reg = RegistroAn(12)
            self._dados[i + 1] = reg.le_registro(linha, 30)

    # Override
    def escreve(self, arq: IO):
        for leg, nome in zip(BlocoNomesArquivos.legendas,
                             self._dados):
            arq.write(f"{leg} {nome}\n")


class LeituraArquivos(Leitura):
    """
    Realiza a leitura do arquivo `arquivos.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `arquivos.dat`, construindo
    um objeto `Arquivos` cujas informações são as mesmas do arquivos.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str):
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo arquivos.dat.
        """
        nomes_arquivos = BlocoNomesArquivos("", "", True)
        return [nomes_arquivos]
