from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura

from typing import List, IO
import pandas as pd  # type: ignore


class BlocoUTEClasT(Bloco):
    """
    Bloco de informações das usinas cadastradas
    no arquivo do NEWAVE `clast.dat`.
    """
    str_inicio = "NUM  NOME CLASSE  TIPO COMB."
    str_fim = "9999"

    def __init__(self):

        super().__init__(BlocoUTEClasT.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoUTEClasT):
            return False
        bloco: BlocoUTEClasT = o
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
            col_tipo = extrai_coluna_de_listas(dados_utes, 2)
            col_custo1 = extrai_coluna_de_listas(dados_utes, 3)
            col_custo2 = extrai_coluna_de_listas(dados_utes, 4)
            col_custo3 = extrai_coluna_de_listas(dados_utes, 5)
            col_custo4 = extrai_coluna_de_listas(dados_utes, 6)
            col_custo5 = extrai_coluna_de_listas(dados_utes, 7)
            dados = {
                     "Número": col_num,
                     "Nome": col_nome,
                     "Tipo Combustível": col_tipo,
                     "Custo 1": col_custo1,
                     "Custo 2": col_custo2,
                     "Custo 3": col_custo3,
                     "Custo 4": col_custo4,
                     "Custo 5": col_custo5
                    }
            return pd.DataFrame(data=dados)

        # Salta a linha com "XXX"
        arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(4)
        reg_nome = RegistroAn(12)
        reg_tipo = RegistroAn(10)
        reg_custo = RegistroFn(7)
        # Para cada usina, lê e processa as informações
        dados_utes: List[list] = []
        while True:
            linha = arq.readline()
            # Confere se terminaram as usinas
            if BlocoUTEClasT.str_fim in linha:
                # Converte para df e salva na variável
                self._dados = transforma_utes_em_tabela()
                break
            dados_ute = [
                         reg_num.le_registro(linha, 1),
                         reg_nome.le_registro(linha, 6),
                         reg_tipo.le_registro(linha, 19)
                        ]
            dados_ute += reg_custo.le_linha_tabela(linha, 30, 1, 5)
            dados_utes.append(dados_ute)

    # Override
    def escreve(self, arq: IO):
        def escreve_ute(lin: pd.Series):
            linha = " "
            # Número
            linha += str(lin[0]).rjust(4) + " "
            # Nome
            linha += str(lin[1]).ljust(12) + " "
            # Tipo Combustível
            linha += str(lin[2]).ljust(10)
            # Custos
            linha += f" {float(lin[3]):.2f}".rjust(8)
            linha += f" {float(lin[4]):.2f}".rjust(8)
            linha += f" {float(lin[5]):.2f}".rjust(8)
            linha += f" {float(lin[6]):.2f}".rjust(8)
            linha += f" {float(lin[7]):.2f}".rjust(8)
            arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = (" NUM  NOME CLASSE  TIPO COMB.  CUSTO   CUSTO" +
                   "   CUSTO   CUSTO   CUSTO" + "\n")
        cabecalhos = (" XXXX XXXXXXXXXXXX XXXXXXXXXX XXXX.XX XXXX.XX" +
                      " XXXX.XX XXXX.XX XXXX.XX" + "\n")
        arq.write(titulos)
        arq.write(cabecalhos)
        # Escreve UHEs
        for _, ute in self._dados.iterrows():
            escreve_ute(ute)
        arq.write(" " + BlocoUTEClasT.str_fim + "\n")


class BlocoModificacaoUTEClasT(Bloco):
    """
    Bloco de modificações das informações das
    usinas cadastradas no arquivo do NEWAVE `clast.dat`.
    """
    str_inicio = " NUM     CUSTO"

    def __init__(self):

        super().__init__(BlocoModificacaoUTEClasT.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoModificacaoUTEClasT):
            return False
        bloco: BlocoModificacaoUTEClasT = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def extrai_coluna_de_listas(listas: List[list],
                                    coluna: int) -> list:
            return [lista[coluna] for lista in listas]

        def transforma_utes_em_tabela() -> pd.DataFrame:
            # Converte as informações de cada linha em colunas
            col_num = extrai_coluna_de_listas(dados_utes, 0)
            col_custo = extrai_coluna_de_listas(dados_utes, 1)
            col_mes_inic = extrai_coluna_de_listas(dados_utes, 2)
            col_ano_inic = extrai_coluna_de_listas(dados_utes, 3)
            col_mes_fim = extrai_coluna_de_listas(dados_utes, 4)
            col_ano_fim = extrai_coluna_de_listas(dados_utes, 5)
            col_nome = extrai_coluna_de_listas(dados_utes, 6)
            dados = {
                     "Número": col_num,
                     "Nome": col_nome,
                     "Custo": col_custo,
                     "Mês Início": col_mes_inic,
                     "Ano Início": col_ano_inic,
                     "Mês Fim": col_mes_fim,
                     "Ano Fim": col_ano_fim,
                    }
            return pd.DataFrame(data=dados)

        # Salta a linha com "XXX"
        arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(4)
        reg_custo = RegistroFn(7)
        reg_mes = RegistroIn(2)
        reg_ano = RegistroIn(4)
        reg_nome = RegistroAn(12)
        # Para cada usina, lê e processa as informações
        dados_utes: List[list] = []
        while True:
            linha = arq.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                # Converte para df e salva na variável
                self._dados = transforma_utes_em_tabela()
                break
            s_mes_fim = linha[26:28]
            mes_fim = int(s_mes_fim) if s_mes_fim != "  " else None
            s_ano_fim = linha[29:33]
            ano_fim = int(s_ano_fim) if s_ano_fim != "    " else None
            dados_ute = [
                         reg_num.le_registro(linha, 1),
                         reg_custo.le_registro(linha, 8),
                         reg_mes.le_registro(linha, 17),
                         reg_ano.le_registro(linha, 20),
                         mes_fim,
                         ano_fim,
                         reg_nome.le_registro(linha, 35)
                        ]
            dados_utes.append(dados_ute)

    # Override
    def escreve(self, arq: IO):
        def escreve_ute(lin: pd.Series):
            linha = " "
            # Número
            linha += str(lin[0]).rjust(4) + "   "
            # Custo
            linha += f"{float(lin[2]):.2f}".rjust(7) + "  "
            # Mês Início
            linha += f"{int(lin[3])}".rjust(2) + " "
            # Ano Início
            linha += f"{int(lin[4])}".rjust(4) + "  "
            # Mês Fim
            if not pd.isna(lin[5]):
                linha += f"{int(lin[5])}".rjust(2) + " "
            else:
                linha += "   "
            # Ano Fim
            if not pd.isna(lin[6]):
                linha += f"{int(lin[6])}".rjust(4) + "  "
            else:
                linha += "      "
            # Nome
            linha += str(lin[1]).ljust(12)
            arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = (" NUM     CUSTO" + "\n")
        cabecalhos = (" XXXX   XXXX.XX  XX XXXX  XX XXXX" + "\n")
        arq.write(titulos)
        arq.write(cabecalhos)
        # Escreve UHEs
        for _, ute in self._dados.iterrows():
            escreve_ute(ute)


class LeituraClasT(Leitura):
    """
    Realiza a leitura do arquivo `clast.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `clast.dat`, construindo
    um objeto `ClasT` cujas informações são as mesmas do clast.dat.

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
        Cria a lista de blocos a serem lidos no arquivo clast.dat.
        """
        return [BlocoUTEClasT(),
                BlocoModificacaoUTEClasT()]
