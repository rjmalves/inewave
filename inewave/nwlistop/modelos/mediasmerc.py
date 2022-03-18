# Imports do próprio módulo
from inewave._utils.leituracsv import LeituraCSV

# Imports de módulos externos


class LeituraMediasMerc(LeituraCSV):
    """
    Realiza a leitura do arquivo MEDIAS-MERC.CSV
    existente em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos do arquivo MEDIAS-MERC.CSV, construindo um
    objeto `MediasMerc` cujas informações são as mesmas do arquivo.

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
        cols_novas[0] = "Submercado"
        self._dados.columns = cols_novas
        # Exclui a última coluna (em branco)
        self._dados.drop(columns=[cols_novas[-1]], inplace=True)
        # Substitui os elementos da primeira coluna pelos submercados
        mapa_termos = {0: "SIN", 1: "SE", 2: "S", 3: "NE", 4: "N"}
        nova_coluna = [mapa_termos[i] for i in self._dados["Submercado"]]
        self._dados["Submercado"] = nova_coluna
