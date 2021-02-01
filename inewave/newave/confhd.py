# Imports do próprio módulo
from inewave._utils.escrita import Escrita
from inewave._utils.leitura import Leitura
from .modelos.confhd import UHEConfhd, Confhd
# Imports de módulos externos
import os
from traceback import print_exc
from typing import IO, Dict


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

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `confhd`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraConfhd(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> confhd = leitor.confhd

    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # Confhd default, depois é substituído
        self.confhd = Confhd({})

    def le_arquivo(self) -> Confhd:
        """
        Faz a leitura do arquivo `confhd.dat`.
        """
        try:
            caminho = os.path.join(self.diretorio, "confhd.dat")
            with open(caminho, "r") as arq:
                self.confhd = self._le_confhd(arq)
                return self.confhd
        except Exception:
            print_exc()
            return self.confhd

    def _le_confhd(self, arq: IO) -> Confhd:
        """
        Faz a leitura do arquivo confhd.dat.
        """
        linha = ""
        # Pula as duas primeiras linhas, com cabeçalhos
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        usinas: Dict[int, UHEConfhd] = {}
        while True:
            # Verifica se o arquivo acabou
            linha = self._le_linha_com_backup(arq)
            if self._fim_arquivo(linha):
                self.confhd = Confhd(usinas)
                break
            # Senão, lê mais uma usina
            u = self._le_dados_uhe(linha)
            usinas[u.numero] = u

        return self.confhd

    def _le_dados_uhe(self, linha: str) -> UHEConfhd:
        """
        Lê a linha com dados do PMO em questão e retorna dados
        sobre o mês e ano de estudo e a versão do NEWAVE usada.
        """
        numero = int(linha[1:5])
        nome = linha[6:18]
        posto = int(linha[19:23])
        jusante = int(linha[25:29])
        ree = int(linha[30:34])
        vol_ini = float(linha[35:41])
        existente = True if linha[42:46].strip() == "EX" else False
        modif = bool(int(linha[49:53]))
        inicio_hist = int(linha[58:62])
        fim_hist = int(linha[67:71])
        return UHEConfhd(numero,
                         nome,
                         posto,
                         jusante,
                         ree,
                         vol_ini,
                         existente,
                         modif,
                         inicio_hist,
                         fim_hist)

    def _fim_arquivo(self, linha: str) -> bool:
        return len(linha) < 1


class EscritaConfhd(Escrita):
    """
    Realiza a escrita do arquivo confhd.dat
    em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para escrever os campos
    de um arquivo confhd.dat, a partir de um objeto `Confhd`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de armazenar as strings auxiliares do arquivo, desenhar tabelas, dentre
    outras tarefas associadas à escrita.

    Se o diretório de escrita não existir, ele será criado.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> # confhd é do tipo Confhd
    >>> escritor = EscritaConfhd(diretorio)
    >>> escritor.escreve_arquivo(confhd)
    """
    def __init__(self, diretorio: str):
        super().__init__()
        self.diretorio = diretorio

    def escreve_arquivo(self, confhd: Confhd):
        """
        Realiza a escrita de um arquivo `confhd.dat`.
        """
        # Confere se o diretório existe. Senão, cria.
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)
        # Inicia a escrita
        caminho = os.path.join(self.diretorio, "confhd.dat")
        with open(caminho, "w") as arq:

            def escreve_uhe(uhe: UHEConfhd):
                linha = " "
                # Número
                linha += str(uhe.numero).rjust(4) + " "
                # Nome
                linha += uhe.nome.ljust(12) + " "
                # Posto
                linha += str(uhe.posto).rjust(4) + "  "
                # Jusante
                linha += str(uhe.jusante).rjust(4) + " "
                # REE
                linha += str(uhe.ree).rjust(4) + " "
                # Volume inicial
                linha += "{:3.2f} ".format(uhe.volume_inicial).rjust(7)
                # Existente
                linha += "  EX   " if uhe.existente else "  NE   "
                # Modificada
                linha += str(int(uhe.modificada)).rjust(4) + "     "
                # Início do histórico
                linha += str(uhe.inicio_historico).rjust(4) + "     "
                # Fim do histórico
                linha += str(uhe.fim_historico).rjust(4)
                arq.write(linha + "\n")

            # Escreve cabeçalhos
            titulos = (" NUM  NOME         POSTO JUS   REE V.INIC"
                       + " U.EXIS MODIF INIC.HIST FIM HIST" + "\n")
            cabecalhos = (" XXXX XXXXXXXXXXXX XXXX  XXXX XXXX XXX.XX"
                          + " XXXX   XXXX     XXXX     XXXX" + "\n")
            arq.write(titulos)
            arq.write(cabecalhos)
            # Escreve UHEs
            for uhe in confhd.usinas.values():
                escreve_uhe(uhe)
