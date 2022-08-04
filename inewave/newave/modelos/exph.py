from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from typing import List, IO, Optional
from datetime import datetime
import pandas as pd  # type: ignore


class BlocoUHEExph(Section):
    """
    Bloco com as expensões das UHEs por máquina.
    """

    FIM_BLOCO = "9999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_uhe = Line(
            [
                IntegerField(4, 0),
                LiteralField(12, 5),
                DatetimeField(size=7, starting_position=18, format="%m/%Y"),
                IntegerField(2, 31),
                FloatField(7, 35, decimal_digits=1),
                DatetimeField(size=7, starting_position=44, format="%m/%Y"),
                FloatField(6, 52, decimal_digits=1),
                IntegerField(2, 60),
                IntegerField(1, 64),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoUHEExph):
            return False
        bloco: BlocoUHEExph = o
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
            df = pd.DataFrame()
            df["Código UHE"] = codigo_uhes
            df["Nome UHE"] = nome_uhes
            df["Início Enchimento"] = inicio_enchimento
            df["Duração"] = duracao
            df["Volume Morto"] = volume_morto
            df["Data de Entrada"] = data_entrada
            df["Potência"] = potencia
            df["Máquina"] = maquina
            df["Conjunto"] = conjunto
            return df

        # Salta as linhas adicionais
        for _ in range(3):
            self.__cabecalhos.append(file.readline())

        # Variáveis auxiliares
        codigo_uhes: List[Optional[int]] = []
        nome_uhes: List[Optional[str]] = []
        inicio_enchimento: List[Optional[datetime]] = []
        duracao: List[Optional[int]] = []
        volume_morto: List[Optional[float]] = []
        data_entrada: List[Optional[datetime]] = []
        potencia: List[Optional[float]] = []
        maquina: List[Optional[int]] = []
        conjunto: List[Optional[int]] = []

        codigo_atual: Optional[int] = None
        nome_atual: Optional[str] = None
        inicio_enchimento_atual: Optional[datetime] = None
        duracao_atual: Optional[int] = None
        volume_morto_atual: Optional[float] = None
        data_entrada_atual: Optional[datetime] = None
        potencia_atual: Optional[float] = None
        maquina_atual: Optional[int] = None
        conjunto_atual: Optional[int] = None

        while True:
            linha = file.readline()
            # Confere se acabou
            if len(linha) < 3:
                if len(codigo_uhes) > 0:
                    self.data = converte_tabela_em_df()
                break
            if BlocoUHEExph.FIM_BLOCO in linha:
                codigo_atual = None
                nome_atual = None
                continue
            (
                codigo_atual,
                nome_atual,
                inicio_enchimento_atual,
                duracao_atual,
                volume_morto_atual,
                data_entrada_atual,
                potencia_atual,
                maquina_atual,
                conjunto_atual,
            ) = self.__linha_uhe.read(linha)
            codigo_uhes.append(
                codigo_atual if codigo_atual is not None else codigo_uhes[-1]
            )
            nome_uhes.append(
                nome_atual if nome_atual is not None else nome_uhes[-1]
            )
            inicio_enchimento.append(inicio_enchimento_atual)
            duracao.append(duracao_atual)
            volume_morto.append(volume_morto_atual)
            data_entrada.append(data_entrada_atual)
            potencia.append(potencia_atual)
            maquina.append(maquina_atual)
            conjunto.append(conjunto_atual)

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do exph.dat não foram lidos com sucesso")

        ultima_uhe = 0
        for _, linha in self.data.iterrows():
            linha_lida: pd.Series = linha
            if linha_lida["Código UHE"] != ultima_uhe and ultima_uhe != 0:
                file.write(f"{BlocoUHEExph.FIM_BLOCO}\n")
            ultima_uhe = int(linha_lida["Código UHE"])
            dados_linha = linha_lida.tolist()
            # Corrige posições opcionais
            for i in [3, -1, -2]:
                dados_linha[i] = (
                    int(dados_linha[i])
                    if not pd.isnull(dados_linha[i])
                    else None
                )
            file.write(self.__linha_uhe.write(dados_linha))
        file.write(f"{BlocoUHEExph.FIM_BLOCO}\n")
