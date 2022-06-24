from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from typing import List, IO
import pandas as pd  # type: ignore


class BlocoConfUTE(Section):
    """
    Bloco de informações das usinas cadastradas
    no arquivo do NEWAVE `conft.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_ute = Line(
            [
                IntegerField(4, 1),
                LiteralField(12, 6),
                IntegerField(4, 21),
                LiteralField(2, 30),
                IntegerField(4, 35),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConfUTE):
            return False
        bloco: BlocoConfUTE = o
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

        def transforma_utes_em_tabela() -> pd.DataFrame:
            # Converte as informações de cada linha em colunas
            col_num = extrai_coluna_de_listas(dados_utes, 0)
            col_nome = extrai_coluna_de_listas(dados_utes, 1)
            col_subsis = extrai_coluna_de_listas(dados_utes, 2)
            col_exis = extrai_coluna_de_listas(dados_utes, 3)
            col_clas = extrai_coluna_de_listas(dados_utes, 4)
            dados = {
                "Número": col_num,
                "Nome": col_nome,
                "Subsistema": col_subsis,
                "Usina Existente": col_exis,
                "Classe": col_clas,
            }
            return pd.DataFrame(data=dados)

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Para cada usina, lê e processa as informações
        dados_utes: List[list] = []
        while True:
            linha = file.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                # Converte para df e salva na variável
                if len(dados_utes) > 0:
                    self.data = transforma_utes_em_tabela()
                break
            dados_ute = self.__linha_ute.read(linha)
            dados_utes.append(dados_ute)

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do conft.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            file.write(self.__linha_ute.write(lin.tolist()))
