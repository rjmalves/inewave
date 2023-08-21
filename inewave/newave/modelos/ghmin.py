from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from typing import List, IO, Optional
import pandas as pd  # type: ignore
from datetime import datetime


class BlocoUHEGhmin(Section):
    """
    Bloco com os valores de geração hidráulica mínima.
    """

    FIM_BLOCO = "999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_uhe = Line(
            [
                IntegerField(3, 0),
                DatetimeField(7, 5, format="%m %Y"),
                IntegerField(1, 14),
                FloatField(6, 17, 0),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoUHEGhmin):
            return False
        bloco: BlocoUHEGhmin = o
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
            df["data"] = datas
            df["patamar"] = patamares
            df["geracao"] = geracoes
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Variáveis auxiliares
        codigos: List[Optional[int]] = []
        datas: List[Optional[datetime]] = []
        patamares: List[Optional[int]] = []
        geracoes: List[Optional[float]] = []

        while True:
            linha = file.readline()
            # Confere se acabou
            if BlocoUHEGhmin.FIM_BLOCO in linha[:3] or len(linha) < 3:
                if len(codigos) > 0:
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha_uhe.read(linha)
            codigos.append(dados[0])
            datas.append(dados[1])
            patamares.append(dados[2])
            geracoes.append(dados[3])

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do ghmin.dat não foram lidos com sucesso")

        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            dados_linha = linha_lida.tolist()
            file.write(self.__linha_uhe.write(dados_linha))
        file.write(f"{BlocoUHEGhmin.FIM_BLOCO}\n")
