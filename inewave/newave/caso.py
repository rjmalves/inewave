# Imports do próprio módulo
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.escrita import Escrita
from inewave._utils.registros import RegistroAn
from inewave.newave.modelos.caso import Caso
# Imports de módulos externos
from typing import IO, List
import os


class LeituraCaso(Leitura):
    """
    Realiza a leitura do arquivo `caso.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `caso.dat`, construindo
    um objeto `Caso` cujas informações são as mesmas do caso.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `caso`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraCaso(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> caso = leitor.caso

    """

    def __init__(self,
                 diretorio: str):
        super().__init__()
        self.diretorio = diretorio
        # Caso default, depois é substituído
        self.caso = Caso("")

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo caso.dat.
        """
        caminho_arquivo = Bloco("", "",
                                True,
                                self._le_caminho_arquivos)
        return [caminho_arquivo]

    # Override
    def _inicia_variaveis_leitura(self):
        """
        Inicia variáveis temporárias que são escritas durante
        a leitura do arquivo.
        """
        self._caminho_arquivo = ""

    # Override
    def _prepara_dados_saida(self):
        """
        Trata os dados obtidos do arquivo para ser retornado.
        """
        self.caso = Caso(self._caminho_arquivo)


    # Override
    def _fim_arquivo(self, linha: str) -> bool:
        return len(linha) == 0

    # Override
    def le_arquivo(self, nome_arquivo="caso.dat") -> Caso:
        """
        Faz a leitura do arquivo `caso.dat`.
        """
        self._le_arquivo_em_diretorio(self.diretorio,
                                      nome_arquivo)
        return self.caso

    def _le_caminho_arquivos(self,
                             arq: IO,
                             cab: str = ""):
        """
        Lê o caminho para o arquivo `arquivos.dat`
        """
        self.usa_backup = True
        linha = self._le_linha_com_backup(arq)
        reg = RegistroAn(12)
        self._caminho_arquivo = reg.le_registro(linha, 0)


class EscritaCaso(Escrita):
    """
    Realiza a escrita do arquivo `caso.dat`
    em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para escrever os campos
    de um arquivo caso.dat, a partir de um objeto `Caso`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de armazenar as strings auxiliares do arquivo, desenhar tabelas, dentre
    outras tarefas associadas à escrita.

    Se o diretório de escrita não existir, ele será criado.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> # caso é do tipo Caso
    >>> escritor = EscritaCaso(diretorio)
    >>> escritor.escreve_arquivo(caso)
    """
    def __init__(self, diretorio: str):
        super().__init__()
        self.diretorio = diretorio

    def escreve_arquivo(self,
                        caso: Caso,
                        nome_arquivo="caso.dat"):
        """
        Realiza a escrita de um arquivo `caso.dat`.
        """
        # Confere se o diretório existe. Senão, cria.
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)
        # Inicia a escrita
        caminho = os.path.join(self.diretorio, nome_arquivo)
        with open(caminho, "w") as arq:
            arq.write(caso.arquivo)
