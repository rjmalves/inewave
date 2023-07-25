from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.floatfield import FloatField
from typing import IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class SecaoDadosEnergias(Section):
    """
    Registro com os dados das séries sintéticas de energia existentes
    no arquivo energias.dat.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosEnergias):
            return False
        bloco: SecaoDadosEnergias = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    def read(
        self,
        file: IO,
        numero_series: int = 2000,
        numero_rees: int = 12,
        numero_estagios: int = 60,
        numero_estagios_th: int = 12,
        *args,
        **kwargs,
    ):
        numero_registros = (
            (numero_estagios + numero_estagios_th)
            * numero_rees
            * numero_series
        )
        self.__linha = Line(
            [
                FloatField(size=8, starting_position=8 * i)
                for i in range(numero_registros)
            ],
            storage="BINARY",
        )
        dados = self.__linha.read(file.read(self.__linha.size))
        indices_estagios = np.arange(
            1 - numero_estagios_th, numero_estagios + 1
        )
        estagios_df = np.repeat(indices_estagios, numero_series * numero_rees)
        rees_df = np.tile(
            np.repeat(np.arange(1, numero_rees + 1), numero_series),
            numero_estagios + numero_estagios_th,
        )
        series_df = np.tile(
            np.arange(1, numero_series + 1),
            numero_rees * (numero_estagios + numero_estagios_th),
        )
        df = pd.DataFrame(
            data={
                "estagio": estagios_df,
                "ree": rees_df,
                "serie": series_df,
                "valor": dados,
            }
        )
        self.data = df

    def write(self, file: IO, *args, **kwargs):
        dados = self.data["valor"].to_numpy()
        linha = Line(
            [
                FloatField(size=8, starting_position=8 * i)
                for i in range(len(dados))
            ],
            storage="BINARY",
        )
        file.write(linha.write(dados))
