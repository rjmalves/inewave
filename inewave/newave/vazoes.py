from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.vazoes import RegistroVazoesPostos
import pandas as pd  # type: ignore


from typing import TypeVar, List, Optional


class Vazoes(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao cadastro das
    usinas hidroelétricas.
    """

    T = TypeVar("T")

    REGISTERS = [RegistroVazoesPostos]
    POSTOS = 320
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__df: Optional[pd.DataFrame] = None
        RegistroVazoesPostos.set_postos(self.POSTOS)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="vazoes.dat") -> "Vazoes":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vazoes.dat"):
        self.__atualiza_registros()
        self.write(diretorio, nome_arquivo)

    def __monta_df_de_registros(self) -> Optional[pd.DataFrame]:
        registros: List[RegistroVazoesPostos] = [
            r for r in self.data.of_type(RegistroVazoesPostos)
        ]
        if len(registros) == 0:
            return None
        df = pd.DataFrame(columns=list(range(1, self.__class__.POSTOS + 1)))
        for i, r in enumerate(registros):
            df.loc[i] = r.data

        df = df.astype({i: int for i in range(1, self.__class__.POSTOS + 1)})
        return df

    def __atualiza_registros(self):
        registros: List[RegistroVazoesPostos] = [r for r in self.data][1:]
        n_registros = len(registros)
        n_meses = self.vazoes.shape[0]
        # Deleta os registros que sobraram
        for i in range(n_meses, n_registros):
            self.data.remove(registros[i])
        # Cria registros se faltaram
        for i in range(n_registros, n_meses):
            self.data.append(RegistroVazoesPostos())
        # Atualiza os dados
        for (_, linha), r in zip(self.vazoes.iterrows(), registros):
            r.data = linha.tolist()

    @property
    def vazoes(self) -> pd.DataFrame:
        """
        Obtém a tabela com os dados de vazão existentes no arquivo
        binário.

        - 1...N (`int`) - onde N é o número de postos

        :return: A tabela com as vazões por posto
        :rtype: pd.DataFrame
        """
        if self.__df is None:
            self.__df = self.__monta_df_de_registros()
        return self.__df

    @vazoes.setter
    def vazoes(self, df: pd.DataFrame):
        self.__df = df
