# Imports do próprio módulo
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.escrita import Escrita
from inewave._utils.registros import RegistroAn
from inewave.newave.modelos.arquivos import Arquivos
# Imports de módulos externos
from typing import IO, List
import os


class LeituraArquivos(Leitura):
    """
    Realiza a leitura do arquivo `arquivos.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `arquivos.dat`, construindo
    um objeto `Arquivos` cujas informações são as mesmas do arquivos.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `arquivos`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraArquivos(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> arquivos = leitor.arquivos

    """

    def __init__(self,
                 diretorio: str):
        super().__init__()
        self.diretorio = diretorio
        # Arquivos default, depois é substituído
        self.arquivos = Arquivos.constroi_de_lista([""] * 41)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo arquivos.dat.
        """
        nomes_arquivos = Bloco("", "",
                               True,
                               self._le_nomes_arquivos)
        return [nomes_arquivos]

    # Override
    def _inicia_variaveis_leitura(self):
        """
        Inicia variáveis temporárias que são escritas durante
        a leitura do arquivo.
        """
        self._nomes = [""] * len(Arquivos.legendas)

    # Override
    def _prepara_dados_saida(self):
        """
        Trata os dados obtidos do arquivo para ser retornado.
        """
        self.arquivos = Arquivos.constroi_de_lista(self._nomes)

    # Override
    def _fim_arquivo(self, linha: str) -> bool:
        return len(linha) == 0

    # Override
    def le_arquivo(self, nome_arquivo="arquivos.dat") -> Arquivos:
        """
        Faz a leitura do arquivo `arquivos.dat`.
        """
        self._le_arquivo_em_diretorio(self.diretorio,
                                      nome_arquivo)
        return self.arquivos

    def _le_nomes_arquivos(self,
                           arq: IO,
                           cab: str = ""):
        """
        Lê o caminho para o arquivo `arquivos.dat`
        """
        self.usa_backup = True
        for i in range(len(self._nomes)):
            linha = self._le_linha_com_backup(arq)
            # Confere se já terminou (possíveis \n ao final)
            if len(linha) < 3:
                break
            reg = RegistroAn(12)
            self._nomes[i] = reg.le_registro(linha, 30)


class EscritaArquivos(Escrita):
    """
    Realiza a escrita do arquivo `arquivos.dat`
    em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para escrever os campos
    de um arquivo arquivos.dat, a partir de um objeto `Arquivos`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de armazenar as strings auxiliares do arquivo, desenhar tabelas, dentre
    outras tarefas associadas à escrita.

    Se o diretório de escrita não existir, ele será criado.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> # arquivos é do tipo Arquivos
    >>> escritor = EscritaArquivos(diretorio)
    >>> escritor.escreve_arquivo(arquivos)
    """
    def __init__(self, diretorio: str):
        super().__init__()
        self.diretorio = diretorio

    def escreve_arquivo(self,
                        arquivos: Arquivos,
                        nome_arquivo="arquivos.dat"):
        """
        Realiza a escrita de um arquivo `arquivos.dat`.
        """
        # Confere se o diretório existe. Senão, cria.
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)
        # Inicia a escrita
        caminho = os.path.join(self.diretorio, nome_arquivo)
        with open(caminho, "w") as arq:
            for leg, nome in zip(arquivos.legendas,
                                 arquivos.__slots__):
                arq.write(f"{leg} {arquivos.__getattribute__(nome)}\n")
