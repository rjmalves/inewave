from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from typing import List, IO, Optional
from datetime import datetime
import pandas as pd  # type: ignore


class BlocoUTEExpt(Section):
    """
    Bloco com as expensões das UTEs.
    """

    FIM_BLOCO = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_uhe = Line(
            [
                IntegerField(4, 0),
                LiteralField(6, 5),
                FloatField(8, 11, 2),
                DatetimeField(size=7, starting_position=20, format="%m %Y"),
                DatetimeField(size=7, starting_position=28, format="%m %Y"),
                LiteralField(40, 37),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoUTEExpt):
            return False
        bloco: BlocoUTEExpt = o
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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            df = pd.DataFrame()
            df["codigo_usina"] = codigos
            df["tipo"] = tipos
            df["modificacao"] = modificacoes
            df["data_inicio"] = datas_inicio
            df["data_fim"] = datas_fim
            df["nome_usina"] = nomes
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Variáveis auxiliares
        codigos: List[Optional[int]] = []
        nomes: List[Optional[str]] = []
        tipos: List[Optional[str]] = []
        modificacoes: List[Optional[float]] = []
        datas_inicio: List[Optional[datetime]] = []
        datas_fim: List[Optional[datetime]] = []

        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                if len(codigos) > 0:
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha_uhe.read(linha)
            codigos.append(dados[0])
            tipos.append(dados[1])
            modificacoes.append(dados[2])
            datas_inicio.append(dados[3])
            datas_fim.append(dados[4])
            nomes.append(dados[5])

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do expt.dat não foram lidos com sucesso")

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            dados_linha = linha_lida.tolist()
            file.write(self.__linha_uhe.write(dados_linha))
        file.write(f"{BlocoUTEExpt.FIM_BLOCO}\n")
