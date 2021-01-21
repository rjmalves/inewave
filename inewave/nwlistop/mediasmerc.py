# Imports do próprio módulo
from inewave.nwlistop.modelos.mediasmerc import MediasMerc
from inewave._utils.leitura import Leitura
from inewave.config import NUM_ANOS_ESTUDO, MESES
from inewave.config import NUM_VARIAVEIS_MEDIAS, SUBMERCADOS
# Imports de módulos externos
import os
import csv
import numpy as np  # type: ignore
from traceback import print_exc


class LeituraMediasMerc(Leitura):
    """
    Realiza a leitura do arquivo MEDIAS-MERC.CSV
    existente em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos do arquivo MEDIAS-MERC.CSV, construindo um
    objeto `MediasMerc` cujas informações são as mesmas do arquivo.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `medias`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraMediasMerc(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> medias = leitor.medias

    """
    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # MediasMerc default, depois é substituído
        self.medias = MediasMerc(0, {})

    def le_arquivo(self) -> MediasMerc:
        """
        Lê um arquivo MEDIAS-MERC.CSV em um diretório.
        """
        try:
            caminho = os.path.join(self.diretorio, "MEDIAS-MERC.CSV")
            n_meses = len(MESES)
            n_submercados = len(SUBMERCADOS)
            linhas_medias = NUM_VARIAVEIS_MEDIAS * n_submercados
            colunas_medias = NUM_ANOS_ESTUDO * n_meses
            mes_pmo = 0
            with open(caminho, newline='') as arq:
                leitor = csv.reader(arq, delimiter=",", quotechar='|')
                tabela = np.zeros((linhas_medias, colunas_medias))
                # Descobre o mês do PMO pela terceira coluna
                # da primeira linha. Depois lê linha a linha.
                primeira_linha = True
                for i, linha in enumerate(leitor):
                    if primeira_linha:
                        mes_pmo = int(linha[2])
                        primeira_linha = False
                        continue
                    # Ignora as linhas após os dados dos submercados
                    if i > linhas_medias:
                        break
                    linha_num = np.array([float(n) for n in linha[2:-1]])
                    tabela[i - 1, mes_pmo-1:] = linha_num
                self.medias = MediasMerc(mes_pmo, tabela)
                return self.medias
        except Exception:
            print_exc()
            return MediasMerc(0, {})

    def _fim_arquivo(self, linha: str) -> bool:
        return False
