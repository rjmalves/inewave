from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from typing import List, IO
from datetime import datetime
import pandas as pd  # type: ignore


class BlocoManutencaoUTE(Section):
    """
    Bloco de informações de manutenção das térmicas
    no arquivo do NEWAVE `manutt.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_uhe = Line(
            [
                IntegerField(2, 0),
                LiteralField(11, 2),
                IntegerField(3, 17),
                LiteralField(13, 21),
                IntegerField(2, 37),
                DatetimeField(8, 40, format="%d%m%Y"),
                IntegerField(3, 49),
                FloatField(7, 55, 2),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoManutencaoUTE):
            return False
        bloco: BlocoManutencaoUTE = o
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
        def transforma_em_tabela() -> pd.DataFrame:
            # Converte as informações de cada linha em colunas
            dados = {
                "codigo_empresa": codigos_empresa,
                "nome_empresa": nomes_empresa,
                "codigo_usina": codigos_usina,
                "nome_usina": nomes_usina,
                "codigo_unidade": codigos_unidade,
                "data_inicio": data_inicio,
                "duracao": duracao,
                "potencia": potencia,
            }
            return pd.DataFrame(data=dados)

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Para cada usina, lê e processa as informações
        codigos_empresa: List[int] = []
        nomes_empresa: List[str] = []
        codigos_usina: List[int] = []
        nomes_usina: List[str] = []
        codigos_unidade: List[int] = []
        data_inicio: List[datetime] = []
        duracao: List[int] = []
        potencia: List[float] = []
        while True:
            linha = file.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                if len(codigos_empresa) > 0:
                    # Converte para df e salva na variável
                    self.data = transforma_em_tabela()
                break
            dados_uhe = self.__linha_uhe.read(linha)
            codigos_empresa.append(dados_uhe[0])
            nomes_empresa.append(dados_uhe[1])
            codigos_usina.append(dados_uhe[2])
            nomes_usina.append(dados_uhe[3])
            codigos_unidade.append(dados_uhe[4])
            data_inicio.append(dados_uhe[5])
            duracao.append(dados_uhe[6])
            potencia.append(dados_uhe[7])

    # Override
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do manutt.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            file.write(self.__linha_uhe.write(lin.tolist()))
