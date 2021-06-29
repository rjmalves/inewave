import os

from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita


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
        super().__init__(diretorio)
