from abc import abstractmethod
from typing import IO, List, Dict
import os
from traceback import print_exc

from inewave._utils.registronewave import RegistroNEWAVE
from .dadosarquivo import DadosArquivoRegistros


class LeituraRegistros:
    """
    Classe com utilidades gerais para leitura de arquivos
    do DECOMP com comentários.
    """

    def __init__(self, diretorio: str):
        self._usa_backup = False
        self._linha_backup = ""
        self._diretorio = diretorio
        self._linhas_fora_registros: Dict[float, str] = {}
        self._registros: List[RegistroNEWAVE] = []
        self._registros_encontrados: List[RegistroNEWAVE] = []
        self._registros_lidos: List[RegistroNEWAVE] = []

    def _le_linha_com_backup(self, arq: IO) -> str:
        """
        Faz uma leitura de linha de um arquivo, mas com a opção de usar
        um backup de leitura anterior sinalizado anteriormente.
        """
        linha = ""
        if self._usa_backup:
            self._usa_backup = False
            linha = self._linha_backup
        else:
            linha = arq.readline()
            self._linha_backup = linha
        return linha

    def _configura_backup(self):
        """
        Prepara a próxima leitura para ser uma feita a partir de um
        backup armazenado.
        """
        self._usa_backup = True

    def _lista_arquivos_por_chave(self, chave: str) -> List[str]:
        """
        Retorna a lista de caminhos completos para os arquivos em um
        diretório, desde que tenham uma certa chave no nome.
        """
        return [f for f in os.listdir(self._diretorio) if chave in f]

    def _verifica_inicio_registros(
        self, linha: str, ordem: int, registros: List[RegistroNEWAVE]
    ) -> bool:
        """
        Verifica se a linha atual é a linha de início de algum
        dos registros a serem lidos.
        """
        for i, b in enumerate(registros):
            if b.e_inicio_de_registro(linha):
                b.inicia_registro(linha, ordem)
                self._registros_encontrados.append(registros.pop(i))
                return True

        self._linhas_fora_registros[ordem] = linha
        return False

    def _le_registros_encontrados(self, registros: List[RegistroNEWAVE]):
        """
        Faz a leitura dos registros encontrados até o momento e que
        ainda não foram lidos.
        """
        for i, b in enumerate(registros):
            if b.encontrado:
                res = b.le_registro()
                self._registros_lidos.append(registros.pop(i))
                return res

    def _le_registros_arquivo(self, arq: IO):
        """
        Faz a leitura dos registros de dados do arquivo.
        """
        self._registros = self._cria_registros_leitura()
        linha = ""
        i = 0
        while True:
            # Decide se lê uma linha nova ou usa a última lida
            linha = self._le_linha_com_backup(arq)
            if self._fim_arquivo(linha):
                self._prepara_dados_saida()
                break

            self._verifica_inicio_registros(linha, i, self._registros)
            # Caso a função de leitura retorne True, é configurado
            #  o backup da linha atual.
            bkp = self._le_registros_encontrados(self._registros_encontrados)
            if bkp:
                self._linha_backup = bkp
                self._configura_backup()
            i += 1

    def _le_arquivo_em_diretorio(
        self, diretorio: str, nome_arquivo: str
    ) -> None:
        """
        Faz a leitura do arquivo em um diretorio.
        """
        try:
            caminho = os.path.join(diretorio, nome_arquivo)
            with open(caminho, "r") as arq:
                self._le_registros_arquivo(arq)
        except Exception:
            print_exc()

    @abstractmethod
    def _cria_registros_leitura(self) -> List[RegistroNEWAVE]:
        """
        Método que cria a lista de registros a serem lidos no arquivo.
        Implementa o Factory Pattern.
        """
        pass

    def _prepara_dados_saida(self):
        """
        Trata os dados obtidos do arquivo para ser retornado.
        """
        self._registros = self._registros_lidos

    def _fim_arquivo(self, linha: str) -> bool:
        """
        Método que deve ser implementado para cada arquivo, com o
        conteúdo da linha que indica o fim do próprio, para impedir loops
        de leitura eterna.
        """
        return len(linha) == 0

    def le_arquivo(self, nome_arquivo: str) -> DadosArquivoRegistros:
        """
        Método para ler um arquivo e retornar o objeto
        devido da classe em particular.
        """
        self._le_arquivo_em_diretorio(self._diretorio, nome_arquivo)
        return DadosArquivoRegistros(
            self._registros, self._linhas_fora_registros
        )
