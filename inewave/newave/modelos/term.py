from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroAn
from inewave._utils.registros import RegistroIn
from inewave._utils.registros import RegistroFn
from inewave.config import MESES_DF

from typing import List, IO
import pandas as pd  # type: ignore


class BlocoTermUTE(Bloco):
    """
    Bloco de informações das classes de usinas térmicas
    existentes no arquivo do NEWAVE `term.dat`.
    """
    str_inicio = "NUM NOME"

    def __init__(self):

        super().__init__(BlocoTermUTE.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoTermUTE):
            return False
        bloco: BlocoTermUTE = o
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
            col_pot = extrai_coluna_de_listas(dados_utes, 2)
            col_fcmx = extrai_coluna_de_listas(dados_utes, 3)
            col_teif = extrai_coluna_de_listas(dados_utes, 4)
            col_ip = extrai_coluna_de_listas(dados_utes, 5)
            col_gtmin: List[list] = []
            for i in range(6, 6 + 13):
                col_gtmin.append(extrai_coluna_de_listas(dados_utes,
                                                         i))
            dados = {"Número": col_num,
                     "Nome": col_nome,
                     "Potência Instalada": col_pot,
                     "FC Máximo": col_fcmx,
                     "TEIF": col_teif,
                     "Indisponibilidade Programada": col_ip}
            for i in range(12):
                dados[f"GT Min {MESES_DF[i]}"] = col_gtmin[i]
            dados["GT Min D+ Anos"] = col_gtmin[-1]
            return pd.DataFrame(data=dados)

        # Salta a linha com "XXX"
        arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(3)
        reg_nome = RegistroAn(12)
        reg_pot = RegistroFn(6)
        reg_fcmx = RegistroFn(4)
        reg_teif = RegistroFn(6)
        reg_ip = RegistroFn(6)
        reg_gtmin = RegistroFn(6)
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
                         reg_nome.le_registro(linha, 5),
                         reg_pot.le_registro(linha, 19),
                         reg_fcmx.le_registro(linha, 25),
                         reg_teif.le_registro(linha, 31),
                         reg_ip.le_registro(linha, 38)]
            dados_ute += reg_gtmin.le_linha_tabela(linha,
                                                   45,
                                                   1,
                                                   13)
            dados_utes.append(dados_ute)

    # Override
    def escreve(self, arq: IO):

        def formata_num(n: float, digitos: int) -> str:
            f = f"{n:.2f}"
            if len(f) > digitos:
                f = f"{round(n, 1):.1f}"
                if len(f) > digitos:
                    f = f"{round(n)}"
                    if len(f) < digitos:
                        f = f"{f}."
            return f

        def escreve_ute(lin: pd.Series):
            linha = " "
            # Número
            linha += str(lin[0]).rjust(3) + " "
            # Nome
            linha += str(lin[1]).ljust(12) + "  "
            # Potência
            linha += str(int(lin[2])).rjust(4) + ". "
            # FCMX
            linha += str(int(lin[3])).rjust(3) + ".  "
            # TEIF
            linha += f"{lin[4]:.2f}".rjust(6) + " "
            # IP
            linha += f"{lin[5]:.2f}".rjust(6)
            for i in range(13):
                linha += " " + formata_num(lin[6 + i], 6).rjust(6)
            arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = (" NUM NOME          POT  FCMX    TEIF   IP"
                   + "    <-------------------- GTMIN PARA O PRIM"
                   + "EIRO ANO DE ESTUDO ------------------------|"
                   + "D+ ANOS" + "\n")
        cabecalhos = (" XXX XXXXXXXXXXXX  XXXX. XXX.  XXX.XX XXX.X"
                      + "X JAN.XX FEV.XX MAR.XX ABR.XX MAI.XX JUN.XX"
                      + " JUL.XX AGO.XX SET.XX OUT.XX NOV.XX DEZ.XX X"
                      + "XX.XX" + "\n")
        arq.write(titulos)
        arq.write(cabecalhos)
        # Escreve UHEs
        for _, ute in self._dados.iterrows():
            escreve_ute(ute)


class LeituraTerm(Leitura):
    """
    Realiza a leitura do arquivo `term.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `term.dat`, construindo
    um objeto `Term` cujas informações são as mesmas do term.dat.

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
        Cria a lista de blocos a serem lidos no arquivo term.dat.
        """
        return [BlocoTermUTE()]
