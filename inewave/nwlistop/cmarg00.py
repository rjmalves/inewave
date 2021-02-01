# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from inewave.config import NUM_CENARIOS
from inewave.config import NUM_PATAMARES, MESES, SUBMERCADOS
from .modelos.cmarg00 import Cmarg00
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO, Dict, Tuple


class LeituraCmarg00(Leitura):
    """
    Realiza a leitura dos arquivos cmarg00x.out
    existentes em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de arquivos cmarg00x.out, construindo
    objetos `Cmarg00` cujas informações são as mesmas dos arquivos.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `cmargs`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraCmarg00(diretorio)
    >>> leitor.le_arquivos()
    # Ops, esqueci de pegar o objeto
    >>> cmarg_sudeste = leitor.cmargs['SUDESTE']

    """
    str_inicio_cmargs_ano = "     ANO: "
    str_fim_cmargs_ano = "  MAX         "

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        self.arquivos = self._lista_arquivos_por_chave("cmarg00")
        self.cmargs: Dict[str, Cmarg00] = {}

    def le_arquivos(self) -> Dict[str, Cmarg00]:
        """
        Lê os arquivos cmarg00x.out em um diretório.
        """
        caminhos = [os.path.join(self.diretorio, f)
                    for f in self.arquivos]
        for a, c in zip(self.arquivos, caminhos):
            cmarg = self._le_arquivo(c)
            self.cmargs[cmarg.submercado] = cmarg

        return self.cmargs

    def _le_arquivo(self, caminho: str) -> Cmarg00:
        """
        Lê um arquivo cmarg00x.out.
        """
        try:
            with open(caminho, "r") as arq:
                # A primeira linha contém as informações gerais
                # da execução do NEWAVE associada
                linha = self._le_linha_com_backup(arq)
                mes, ano, ver = self._infere_informacoes_execucao(linha)
                # Em seguida, infere o submercado e inicia a leitura
                # dos valores
                linha = self._le_linha_com_backup(arq)
                sub = self._infere_submercado(linha)
                # Lê a tabela de valores
                tabelas = self._le_cmarg00(arq)
                cmarg = Cmarg00(mes, ano, ver, sub, tabelas)
                return cmarg
        except Exception:
            print_exc()
            return Cmarg00(0, 0, "", "", {})

    def _infere_informacoes_execucao(self, linha: str) -> Tuple[int,
                                                                int,
                                                                str]:
        """
        """
        # Confere se a linha passada contém as informações.
        # Se não, lança exceção
        if "NW Versao" in linha:
            # Procura o mês de execução
            mes_na_linha = 0
            for i, m in enumerate(MESES):
                if m in linha:
                    mes_na_linha = i
                    break
            mes = MESES[mes_na_linha]
            indice_mes = MESES.index(MESES[mes_na_linha]) + 1
            # Quebra a linha no mês e extrai o ano
            _, linha_sem_mes = linha.split(mes)
            ano = int(linha_sem_mes[3:7])
            # Extrai a versão
            versao = linha.split("NW Versao")[1].strip()
            return indice_mes, ano, versao
        else:
            raise Exception("Linha sem as informações de execução")

    def _infere_submercado(self, linha: str) -> str:
        """
        """
        encontrou = False
        submercado = ""
        for sub in SUBMERCADOS:
            if sub in linha:
                encontrou = True
                submercado = sub
                break
        if encontrou:
            return submercado
        # Se não encontrou o submercado, lança exceção
        raise Exception("Submercado não encontrado")

    def _le_cmarg00(self, arq: IO) -> Dict[int, np.ndarray]:
        """
        Realiza a leitura das tabelas de valores de um arquivo CMarg00.
        """
        iniciou = False
        linha = ""
        tabelas_anos: Dict[int, np.ndarray] = {}
        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se já leu todos os anos de estudo
            if len(linha) < 1:
                break
            # Procura pelo início da tabela de CMarg do ano
            if not iniciou:
                iniciou = LeituraCmarg00.str_inicio_cmargs_ano in linha
                if iniciou:
                    self._configura_backup()
                continue
            # Extrai o ano da tabela
            ano = int(linha[10:14])
            # Salta uma linha e lê os valores da tabela
            self._le_linha_com_backup(arq)
            tabelas_anos[ano] = self._le_cmarg00_ano(arq)
            # Reseta a flag de início de tabela
            iniciou = False
        return tabelas_anos

    def _le_cmarg00_ano(self, arq: IO) -> np.ndarray:
        """
        Lê os dados da tabela de um ano do arquivo cmarg00x.out.
        """
        n_meses = len(MESES)
        cmargs_ano = np.zeros((NUM_PATAMARES * NUM_CENARIOS, n_meses))
        for c in range(NUM_CENARIOS):
            li = NUM_PATAMARES * c
            lf = li + NUM_PATAMARES
            cmargs_ano[li:lf, :] = self._le_cmarg00_cenario(arq)
        return cmargs_ano

    def _le_cmarg00_cenario(self, arq: IO) -> np.ndarray:
        """
        Lê os dados de um cenário de uma tabela do arquivo cmarg00x.out.
        Retorna um array P x M, onde P é o número de patamares e M é o
        número de meses. O acesso é feito com [p, m].
        """
        n_meses = len(MESES)
        cmargs_cenario = np.zeros((NUM_PATAMARES, n_meses))
        cols = 8
        for p in range(NUM_PATAMARES):
            linha = self._le_linha_com_backup(arq)
            col_i = 15
            for m in range(n_meses):
                col_f = col_i + cols
                cmargs_cenario[p, m] = float(linha[col_i:col_f])
                col_i = col_f + 1
        return cmargs_cenario

    def _fim_arquivo(self, linha: str) -> bool:
        return False
