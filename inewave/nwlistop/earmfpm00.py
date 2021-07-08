# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from inewave._utils.bloco import Bloco
from inewave.config import NUM_CENARIOS
from inewave.config import MESES, SUBMERCADOS
from .modelos.earmfpm00 import Earmfpm00
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO, Dict, Tuple, List


class LeituraEarmfpm00(Leitura):
    """
    Realiza a leitura dos arquivos earmfpm00x.out
    existentes em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de arquivos earmfpm00x.out, construindo
    objetos `Earmfpm00` cujas informações são as mesmas dos arquivos.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `earmfpms`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraEarmfpm00(diretorio)
    >>> leitor.le_arquivos()
    # Ops, esqueci de pegar o objeto
    >>> earm_sudeste = leitor.earmfpms['SUDESTE']

    """
    str_inicio_earmfpms_ano = "     ANO: "
    str_fim_earmfpms_ano = "  MAX         "

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)
        self.arquivos = self._lista_arquivos_por_chave("earmfpm00")
        self.earmfpms: Dict[str, Earmfpm00] = {}

    def _cria_blocos_leitura(self) -> List[Bloco]:
        pass

    def le_arquivos(self) -> Dict[str, Earmfpm00]:
        """
        Lê os arquivos earmfpm00x.out em um diretório.
        """
        caminhos = [os.path.join(self._diretorio, f)
                    for f in self.arquivos]
        for a, c in zip(self.arquivos, caminhos):
            earmfpm = self._le_arquivo(c)
            self.earmfpms[earmfpm.submercado] = earmfpm

        return self.earmfpms

    def _le_arquivo(self, caminho: str) -> Earmfpm00:
        """
        Lê um arquivo earmfpm00x.out.
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
                tabelas = self._le_earmfpm00(arq)
                earmfpm = Earmfpm00(mes, ano, ver, sub, tabelas)
                return earmfpm
        except Exception:
            print_exc()
            return Earmfpm00(0, 0, "", "", {})

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

    def _le_earmfpm00(self, arq: IO) -> Dict[int, np.ndarray]:
        """
        Realiza a leitura das tabelas de valores de um arquivo Earmfpm00.
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
                iniciou = LeituraEarmfpm00.str_inicio_earmfpms_ano in linha
                if iniciou:
                    self._configura_backup()
                continue
            # Extrai o ano da tabela
            ano = int(linha[10:14])
            # Salta uma linha e lê os valores da tabela
            self._le_linha_com_backup(arq)
            tabelas_anos[ano] = self._le_earmfpm00_ano(arq)
            # Reseta a flag de início de tabela
            iniciou = False
        return tabelas_anos

    def _le_earmfpm00_ano(self, arq: IO) -> np.ndarray:
        """
        Lê os dados da tabela de um ano do arquivo earmfpm00x.out.
        """
        n_meses = len(MESES)
        earmfpms_ano = np.zeros((NUM_CENARIOS, n_meses))
        for c in range(NUM_CENARIOS):
            earmfpms_ano[c, :] = self._le_earmfpm00_cenario(arq)
        return earmfpms_ano

    def _le_earmfpm00_cenario(self, arq: IO) -> np.ndarray:
        """
        Lê os dados de um cenário de uma tabela do arquivo earmfpm00x.out.
        Retorna um array M x 1, onde M é o número de meses.
        """
        n_meses = len(MESES)
        earmfpms_cenario = np.zeros((n_meses,))
        cols = 8
        linha = self._le_linha_com_backup(arq)
        col_i = 7
        for m in range(n_meses):
            col_f = col_i + cols
            earmfpms_cenario[m] = float(linha[col_i:col_f])
            col_i = col_f + 2
        return earmfpms_cenario

    def _fim_arquivo(self, linha: str) -> bool:
        return False
