# Imports do próprio módulo
from inewave._utils.leituracsv import LeituraCSV

# Imports de módulos externos


class LeituraMediasSIN(LeituraCSV):
    """
    Realiza a leitura do arquivo MEDIAS-SIN.CSV
    existente em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos do arquivo MEDIAS-SIN.CSV, construindo um
    objeto `MediasSIN` cujas informações são as mesmas do arquivo.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    """

    def __init__(self, diretorio: str) -> None:
        super().__init__(diretorio)

    def processa_dados_lidos(self):
        # Remove os espaços dos índices
        vars_atuais = list(self._dados.index)
        vars_novas = [v.strip() for v in vars_atuais]
        self._dados.index = vars_novas
        # Renomeia as colunas
        cols_atuais = list(self._dados.columns)
        cols_novas = [c.strip() for c in cols_atuais]
        self._dados.columns = cols_novas
        # Exclui a primeira e a última coluna (todos 0 | em branco)
        self._dados.drop(columns=[cols_novas[0], cols_novas[-1]], inplace=True)
