# Imports de módulos externos
from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
import pandas as pd  # type: ignore
from typing import IO, Dict, List


class TabelaAvlDesvFphaS(Block):
    """
    Bloco com os desvios da função de produção no plano de
    vazão vertida (S).
    """

    BEGIN_PATTERN = "-----;--------------;--------;"

    COLUMN_NAMES = [
        "codigo_usina",
        "nome_usina",
        "volume_armazenado_percentual",
        "vazao_turbinada_m3s",
        "vazao_vertida_m3s",
        "desvio_percentual",
    ]
    END_PATTERN = ""

    def _monta_df(self, dados: dict) -> pd.DataFrame:
        return pd.DataFrame(data=dados, columns=self.__class__.COLUMN_NAMES)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TabelaAvlDesvFphaS):
            return False
        else:
            if not all(
                [type(self.data) is pd.DataFrame, type(o.data) is pd.DataFrame]
            ):
                return False
            else:
                return self.data.equals(o.data)

    def read(self, file: IO, *args, **kwargs):
        # Espera o fim do cabeçalho
        linha = file.readline()
        while True:
            linha = file.readline()
            if "VERT" in linha:
                num_vertimentos = linha.count("VERT")
                self.__linha = Line(
                    [
                        IntegerField(size=5),
                        LiteralField(size=14),
                        FloatField(size=8, decimal_digits=2),
                        FloatField(size=9, decimal_digits=2),
                    ]
                    + [
                        FloatField(size=9, decimal_digits=2)
                        for _ in range(num_vertimentos)
                    ],
                    delimiter=";",
                )
            if self.__class__.BEGIN_PATTERN in linha:
                break
            elif len(linha) < 3:
                return
        # Lê os valores das variáveis de um dos eixos
        dados_eixo = self.__linha.read(file.readline())
        valores_vert = dados_eixo[4:]
        num_valores_vert = len(valores_vert)
        # Ignora a segunda linha de cabeçalho
        file.readline()
        # Lê a tabela
        dados: Dict[str, List] = {c: [] for c in self.__class__.COLUMN_NAMES}
        while True:
            linha = file.readline()
            if len(linha) < 3 or "-----;--------------;------;" in linha:
                self.data = self._monta_df(dados)
                return
            dados_linha = self.__linha.read(linha)
            dados["codigo_usina"] += [dados_linha[0]] * num_valores_vert
            dados["nome_usina"] += [dados_linha[1]] * num_valores_vert
            dados["volume_armazenado_percentual"] += [
                dados_linha[2]
            ] * num_valores_vert
            dados["vazao_turbinada_m3s"] += [dados_linha[3]] * num_valores_vert
            dados["vazao_vertida_m3s"] += valores_vert
            dados["desvio_percentual"] += dados_linha[4:]
