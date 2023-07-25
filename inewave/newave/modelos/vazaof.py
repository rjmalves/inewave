from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.floatfield import FloatField
from typing import IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class SecaoDadosVazaof(Section):
    """
    Registro com os dados das séries sintéticas de vazão existentes
    nos arquivos vazaofXXX.dat.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosVazaof):
            return False
        bloco: SecaoDadosVazaof = o
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
        numero_forwards: int = 200,
        numero_uhes: int = 164,
        numero_estagios: int = 60,
        numero_estagios_th: int = 12,
        *args,
        **kwargs,
    ):
        numero_registros = (
            (numero_estagios + numero_estagios_th)
            * numero_uhes
            * numero_forwards
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
        estagios_df = np.repeat(
            indices_estagios, numero_forwards * numero_uhes
        )
        uhes_df = np.tile(
            np.repeat(np.arange(1, numero_uhes + 1), numero_forwards),
            numero_estagios + numero_estagios_th,
        )
        forwards_df = np.tile(
            np.arange(1, numero_forwards + 1),
            numero_uhes * (numero_estagios + numero_estagios_th),
        )
        df = pd.DataFrame(
            data={
                "estagio": estagios_df,
                "uhe": uhes_df,
                "serie": forwards_df,
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
