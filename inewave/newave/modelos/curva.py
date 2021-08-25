from inewave.config import REES, MAX_ANOS_ESTUDO, MESES_DF
from inewave._utils.registros import RegistroIn, RegistroFn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura

from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class BlocoConfiguracoesPenalizacaoCurva(Bloco):
    """
    Bloco com as informações de configurações de
    penalização da curva de volume mínimo.
    """
    str_inicio = ""
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoConfiguracoesPenalizacaoCurva.str_inicio,
                         "",
                         True)

        self._dados: np.ndarray = np.zeros((3,),
                                           dtype=np.int64)

    def __eq__(self, o: object):
        if not isinstance(o, BlocoConfiguracoesPenalizacaoCurva):
            return False
        bloco: BlocoConfiguracoesPenalizacaoCurva = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(3)
        linha = arq.readline()
        self._dados = np.array(reg.le_linha_tabela(linha, 1, 1, 3),
                               dtype=np.int64)
        return

    # Override
    def escreve(self, arq: IO):
        cab = (" XXX XXX XXX (TIPO DE PENALIZACAO DAS VIOLACOES: 0-FIXA" +
               " 1-MAXIMA; MES DE PENALIZACAO;VMINOP SAZONAL NO PRE/POS:" +
               " 0-NAO CONSIDERA 1-CONSIDERA)")
        arq.write(cab + "\n")
        linha = ""
        for d in self._dados:
            linha += f" {str(d).rjust(3)}"
        arq.write(linha + "\n")


class BlocoPenalidadesViolacaoREECurva(Bloco):
    """
    Bloco com informações das penalidades por violação para cada
    ree.
    """
    str_inicio = "SISTEMA   CUSTO"
    str_fim = "999"

    def __init__(self):

        super().__init__(BlocoPenalidadesViolacaoREECurva.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoPenalidadesViolacaoREECurva):
            return False
        bloco: BlocoPenalidadesViolacaoREECurva = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = ["Subsistema", "Custo"]
            df = df.astype({"Subsistema": 'int32'})
            return df

        # Variáveis auxiliares
        reg_subsis = RegistroIn(3)
        reg_custo = RegistroFn(7)
        # Pula uma linha, com cabeçalhos
        arq.readline()
        i = 0
        tabela = np.zeros((len(REES),
                          2))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if (BlocoPenalidadesViolacaoREECurva.str_fim
               == linha.strip()):
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            tabela[i, 0] = reg_subsis.le_registro(linha, 1)
            tabela[i, 1] = reg_custo.le_registro(linha, 11)
            i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_custos():
            lin_tab = self._dados.shape[0]
            for i in range(lin_tab):
                linha = f" {str(int(self._dados.iloc[i, 0])).zfill(3)}"
                linha += f"       {self._dados.iloc[i, 1]:4.2f}"
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f" {BlocoPenalidadesViolacaoREECurva.str_inicio}\n")
        arq.write(" XXX       XXXX.XX\n")
        escreve_custos()
        # Escreve a linha de terminação
        arq.write(f" {BlocoPenalidadesViolacaoREECurva.str_fim}\n")


class BlocoCurvaSegurancaSubsistema(Bloco):
    """
    Bloco com informações da curva de segurança de operação por mês/ano
    e por subsistema.
    """
    str_inicio = "CURVA DE SEGURANCA"
    str_fim = "9999"

    def __init__(self):

        super().__init__(BlocoCurvaSegurancaSubsistema.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoCurvaSegurancaSubsistema):
            return False
        bloco: BlocoCurvaSegurancaSubsistema = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df["REE"] = subsistema
            df = df[["Ano", "REE"] + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_subsis = RegistroIn(3)
        reg_ano = RegistroIn(4)
        reg_curva = RegistroFn(5)
        # Pula duas linhas, com cabeçalhos
        arq.readline()
        arq.readline()
        i = 0
        anos = []
        subsistema = []
        subsistema_atual = 0

        tabela = np.zeros((MAX_ANOS_ESTUDO * len(REES),
                          len(MESES_DF)))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if BlocoCurvaSegurancaSubsistema.str_fim == linha.strip():
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            if len(linha.strip()) < 10:
                subsistema_atual = reg_subsis.le_registro(linha, 1)
            else:
                # Ano
                anos.append(reg_ano.le_registro(linha, 0))
                # Subsistema
                subsistema.append(subsistema_atual)
                # Limites
                tabela[i, :] = reg_curva.le_linha_tabela(linha,
                                                         6,
                                                         1,
                                                         len(MESES_DF))
                i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_curva():
            lin_tab = self._dados.shape[0]
            subsistema_anterior = 0
            for i in range(lin_tab):
                linha = ""
                # Subsistema
                subsistema = self._dados.iloc[i, 1]
                if subsistema != subsistema_anterior:
                    subsistema_anterior = subsistema
                    linha = " " + str(subsistema).rjust(3)
                    arq.write(linha + "\n")
                    subsistema_anterior = subsistema
                # Curva de cada mês
                linha = f"{str(self._dados.iloc[i, 0]).ljust(4)} "
                for j in range(len(MESES_DF)):
                    v = self._dados.iloc[i, j + 2]
                    linha += " " + "{:3.1f}".format(v).rjust(5)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f" {BlocoCurvaSegurancaSubsistema.str_inicio}\n")
        arq.write(" XXX\n")
        cab = ("      JAN.X FEV.X MAR.X ABR.X MAI.X JUN.X JUL.X" +
               " AGO.X SET.X OUT.X NOV.X DEZ.X\n")
        arq.write(cab)
        escreve_curva()
        # Escreve a linha de terminação
        arq.write(f"{BlocoCurvaSegurancaSubsistema.str_fim}\n")


class LeituraCurva(Leitura):
    """
    Realiza a leitura do arquivo `curva.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `curva.dat`, construindo
    um objeto `Curva` cujas informações são as mesmas do curva.dat.

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
        Cria a lista de blocos a serem lidos no arquivo curva.dat.
        """
        return [BlocoConfiguracoesPenalizacaoCurva(),
                BlocoPenalidadesViolacaoREECurva(),
                BlocoCurvaSegurancaSubsistema()]
