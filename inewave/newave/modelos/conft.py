from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroAn, RegistroIn

import pandas as pd  # type: ignore
from typing import List, IO


class BlocoConfUTE(Bloco):
    """
    Bloco de informações das usinas cadastradas
    no arquivo do NEWAVE `conft.dat`.
    """
    str_inicio = "NUM  NOME"

    def __init__(self):

        super().__init__(BlocoConfUTE.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoConfUTE):
            return False
        bloco: BlocoConfUTE = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def extrai_coluna_de_listas(listas: List[list],
                                    coluna: int) -> list:
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
                     "Classe": col_clas
                    }
            return pd.DataFrame(data=dados)

        # Salta a linha com "XXX"
        arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(4)
        reg_nome = RegistroAn(12)
        reg_subsis = RegistroAn(4)
        reg_exis = RegistroAn(2)
        reg_clas = RegistroIn(4)
        # Para cada usina, lê e processa as informações
        dados_utes: List[list] = []
        while True:
            linha = arq.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                # Converte para df e salva na variável
                self._dados = transforma_utes_em_tabela()
                break
            dados_ute = [reg_num.le_registro(linha, 1),
                         reg_nome.le_registro(linha, 6),
                         reg_subsis.le_registro(linha, 21),
                         reg_exis.le_registro(linha, 30),
                         reg_clas.le_registro(linha, 35)]
            dados_utes.append(dados_ute)

    # Override
    def escreve(self, arq: IO):
        def escreve_ute(lin: pd.Series):
            linha = " "
            # Número
            linha += str(lin[0]).rjust(4) + " "
            # Nome
            linha += str(lin[1]).ljust(12) + "   "
            # Subsistema
            linha += str(lin[2]).rjust(4) + "     "
            # Existente
            linha += str(lin[3]) + "   "
            # Classe
            linha += str(lin[4]).rjust(4)
            arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = (" NUM  NOME           SSIS  U.EXIS CLASSE"
                   + "\n")
        cabecalhos = (" XXXX XXXXXXXXXXXX   XXXX     XX   XXXX"
                      + "\n")
        arq.write(titulos)
        arq.write(cabecalhos)
        # Escreve UHEs
        for _, ute in self._dados.iterrows():
            escreve_ute(ute)


class LeituraConfT(Leitura):
    """
    Realiza a leitura do arquivo `conft.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `conft.dat`, construindo
    um objeto `ConfT` cujas informações são as mesmas do conft.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str):
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo conft.dat.
        """
        return [BlocoConfUTE()]
