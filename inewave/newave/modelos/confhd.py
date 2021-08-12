# Imports do próprio módulo
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
# Imports de módulos externos
from typing import IO, List
import pandas as pd  # type: ignore


class BlocoConfUHE(Bloco):
    """
    Bloco de informações das usinas cadastradas
    no arquivo do NEWAVE `confhd.dat`.
    """
    str_inicio = "NUM  NOME"

    def __init__(self):

        super().__init__(BlocoConfUHE.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoConfUHE):
            return False
        bloco: BlocoConfUHE = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def extrai_coluna_de_listas(listas: List[list],
                                    coluna: int) -> list:
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
                     "Fim do Histórico": col_fim_hist
                    }
            return pd.DataFrame(data=dados)

        # Salta a linha com "XXX"
        arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(4)
        reg_nome = RegistroAn(12)
        reg_posto = RegistroIn(4)
        reg_jus = RegistroIn(4)
        reg_ree = RegistroIn(4)
        reg_vinic = RegistroFn(6)
        reg_exis = RegistroAn(4)
        reg_modif = RegistroIn(4)
        reg_inic_hist = RegistroIn(4)
        reg_fim_hist = RegistroIn(4)
        # Para cada usina, lê e processa as informações
        dados_uhes: List[list] = []
        while True:
            linha = arq.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                # Converte para df e salva na variável
                self._dados = transforma_uhes_em_tabela()
                break
            dados_uhe = [reg_num.le_registro(linha, 1),
                         reg_nome.le_registro(linha, 6),
                         reg_posto.le_registro(linha, 19),
                         reg_jus.le_registro(linha, 25),
                         reg_ree.le_registro(linha, 30),
                         reg_vinic.le_registro(linha, 35),
                         reg_exis.le_registro(linha, 42),
                         bool(reg_modif.le_registro(linha, 49)),
                         reg_inic_hist.le_registro(linha, 58),
                         reg_fim_hist.le_registro(linha, 67)]
            dados_uhes.append(dados_uhe)

    # Override
    def escreve(self, arq: IO):
        def escreve_uhe(lin: pd.Series):
            linha = " "
            # Número
            linha += str(lin[0]).rjust(4) + " "
            # Nome
            linha += lin[1].ljust(12) + " "
            # Posto
            linha += str(lin[2]).rjust(4) + "  "
            # Jusante
            linha += str(lin[3]).rjust(4) + " "
            # REE
            linha += str(lin[4]).rjust(4) + " "
            # Volume inicial
            linha += f"{float(lin[5]):3.2f} ".rjust(7)
            # Existente
            linha += f"{lin[6]}".rjust(4)
            # Modificada
            linha += "   " + str(int(lin[7])).rjust(4) + "     "
            # Início do histórico
            linha += str(lin[8]).rjust(4) + "     "
            # Fim do histórico
            linha += str(lin[9]).rjust(4)
            arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = (" NUM  NOME         POSTO JUS   REE V.INIC"
                   + " U.EXIS MODIF INIC.HIST FIM HIST" + "\n")
        cabecalhos = (" XXXX XXXXXXXXXXXX XXXX  XXXX XXXX XXX.XX"
                      + " XXXX   XXXX     XXXX     XXXX" + "\n")
        arq.write(titulos)
        arq.write(cabecalhos)
        # Escreve UHEs
        for _, uhe in self._dados.iterrows():
            escreve_uhe(uhe)


class LeituraConfhd(Leitura):
    """
    Realiza a leitura do arquivo `confhd.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `confhd.dat`, construindo
    um objeto `Confhd` cujas informações são as mesmas do `confhd.dat`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo confhd.dat.
        """
        uhes = BlocoConfUHE()
        return [uhes]
