from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from typing import IO, List
import pandas as pd  # type: ignore


class BlocoNomesArquivos(Section):
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
        "ARQUIVO DE RESTRICAO DE GAS :",
    ]

    FIM_BLOCO = " 9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(30, 0), LiteralField(40, 29)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNomesArquivos):
            return False
        bloco: BlocoNomesArquivos = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(data={"Legenda": legendas, "Nome": nomes})
            return df

        legendas: List[str] = []
        nomes: List[str] = []
        while True:
            linha = file.readline()
            if len(linha) < 3:
                self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            legendas.append(dados[0])
            nomes.append(dados[1])

    # Override
    def write(self, file: IO):
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do arquivos.dat não foram lidos")
        for _, linha in self.data.iterrows():
            file.write(self.__linha.write(linha.tolist()))
