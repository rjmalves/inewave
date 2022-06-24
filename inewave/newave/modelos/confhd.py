from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore


class BlocoConfUHE(Section):
    """
    Bloco de informações das usinas cadastradas
    no arquivo do NEWAVE `confhd.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_uhe = Line(
            [
                IntegerField(4, 1),
                LiteralField(12, 6),
                IntegerField(4, 19),
                IntegerField(4, 25),
                IntegerField(4, 30),
                FloatField(6, 35, 2),
                LiteralField(4, 42),
                IntegerField(4, 49),
                IntegerField(4, 58),
                IntegerField(4, 67),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConfUHE):
            return False
        bloco: BlocoConfUHE = o
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
        def extrai_coluna_de_listas(listas: List[list], coluna: int) -> list:
            return [lista[coluna] for lista in listas]

        def transforma_uhes_em_tabela() -> pd.DataFrame:
            # Converte as informações de cada linha em colunas
            col_num = extrai_coluna_de_listas(dados_uhes, 0)
            col_nome = extrai_coluna_de_listas(dados_uhes, 1)
            col_posto = extrai_coluna_de_listas(dados_uhes, 2)
            col_jus = extrai_coluna_de_listas(dados_uhes, 3)
            col_ree = extrai_coluna_de_listas(dados_uhes, 4)
            col_vinic = extrai_coluna_de_listas(dados_uhes, 5)
            col_exis = extrai_coluna_de_listas(dados_uhes, 6)
            col_modif = extrai_coluna_de_listas(dados_uhes, 7)
            col_inic_hist = extrai_coluna_de_listas(dados_uhes, 8)
            col_fim_hist = extrai_coluna_de_listas(dados_uhes, 9)
            dados = {
                "Número": col_num,
                "Nome": col_nome,
                "Posto": col_posto,
                "Jusante": col_jus,
                "REE": col_ree,
                "Volume Inicial": col_vinic,
                "Usina Existente": col_exis,
                "Modificada": col_modif,
                "Início do Histórico": col_inic_hist,
                "Fim do Histórico": col_fim_hist,
            }
            return pd.DataFrame(data=dados)

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Para cada usina, lê e processa as informações
        dados_uhes: List[list] = []
        while True:
            linha = file.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                # Converte para df e salva na variável
                if len(dados_uhes) > 0:
                    self.data = transforma_uhes_em_tabela()
                break
            dados_uhe = self.__linha_uhe.read(linha)
            dados_uhes.append(dados_uhe)

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do confhd.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            file.write(self.__linha_uhe.write(lin.tolist()))
