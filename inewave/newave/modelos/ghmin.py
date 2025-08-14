from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.literalfield import LiteralField
from typing import List, IO, Optional
import pandas as pd  # type: ignore

from inewave._utils.formatacao import (
    prepara_valor_ano,
    prepara_vetor_ano_mes_tabela,
)


class BlocoUHEGhmin(Section):
    """
    Bloco com os valores de geração hidráulica mínima.
    """

    __slots__ = ["__linha_uhe", "__cabecalhos"]

    FIM_BLOCO = "999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_uhe = Line(
            [
                IntegerField(3, 0),
                LiteralField(2, 5),
                LiteralField(4, 8),
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
            df["data"] = prepara_vetor_ano_mes_tabela(anos, meses)
            df["patamar"] = patamares
            df["geracao"] = geracoes
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Variáveis auxiliares
        codigos: List[Optional[int]] = []
        meses: List[Optional[str]] = []
        anos: List[Optional[str]] = []
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
            meses.append(dados[1])
            anos.append(dados[2])
            patamares.append(dados[3])
            geracoes.append(dados[4])

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do ghmin.dat não foram lidos com sucesso")
        
        self.data['ano'] = self.data['data'].apply(lambda x: prepara_valor_ano(x.year))
        self.data['mes'] = self.data['data'].apply(lambda x: f"{x.month:2d}")
        self.data.drop("data", inplace=True, axis=1)

        for _, linha in self.data[['codigo_usina','mes','ano','patamar','geracao']].iterrows():
            linha_lida: pd.Series = linha
            dados_linha = linha_lida.tolist()
            file.write(self.__linha_uhe.write(dados_linha))
        file.write(f"{BlocoUHEGhmin.FIM_BLOCO}\n")
