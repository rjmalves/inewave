# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from inewave._utils.bloco import Bloco
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave.config import NUM_CENARIOS, MAX_ANOS_ESTUDO
from inewave.config import MESES, MESES_DF
# Imports de módulos externos
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List


class BlocoEnergiaArmazenadaFinalPercentual(Bloco):
    """
    Bloco com as informações das tabelas de energias armazenada final
    por série e por mês/ano de estudo.
    """
    str_inicio = "ENERGIA ARMAZENADA FINAL"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoEnergiaArmazenadaFinalPercentual.str_inicio,
                         "",
                         True)

        self._dados = ["", pd.DataFrame()]

    def __eq__(self, o: object):
        if not isinstance(o, BlocoEnergiaArmazenadaFinalPercentual):
            return False
        bloco: BlocoEnergiaArmazenadaFinalPercentual = o
        return all([
                    self._dados[0] == bloco.dados[0],
                    self._dados[1].equals(bloco._dados[1])
                   ])

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF + ["Média"]
            df["Ano"] = anos
            df["Série"] = serie
            df = df[["Ano", "Série"] + MESES_DF + ["Média"]]
            return df

        # Salta a primeira linha
        arq.readline()
        # Variáveis auxiliares
        anos = np.zeros((NUM_CENARIOS * MAX_ANOS_ESTUDO,),
                        dtype=np.int64)
        serie = np.zeros((NUM_CENARIOS * MAX_ANOS_ESTUDO,),
                         dtype=np.int64)
        tabela = np.zeros((NUM_CENARIOS * MAX_ANOS_ESTUDO,
                           len(MESES_DF) + 1))
        reg_mercado = RegistroAn(12)
        reg_ano = RegistroIn(4)
        reg_serie = RegistroIn(4)
        reg_energia = RegistroFn(9)
        i = 0
        ano = 0
        # Identifica o submercado
        self._dados[0] = reg_mercado.le_registro(self._linha_inicio, 70)
        while True:
            linha = arq.readline()
            # Confere se acabou
            if len(linha) == 0:
                anos = anos[:i]
                serie = serie[:i]
                tabela = tabela[:i, :]
                self._dados[1] = converte_tabela_em_df()
                break
            # Confere se acabou uma tabela
            if " MEDIA " in linha:
                ano = 0
            # Confere se começou uma tabela
            if "     ANO: " in linha:
                ano = reg_ano.le_registro(linha, 10)
                # Pula a linha de cabeçalhos
                arq.readline()
            # Se está numa tabela, lê
            elif ano != 0:
                anos[i] = ano
                serie[i] = reg_serie.le_registro(linha, 1)
                tabela[i, :] = reg_energia.le_linha_tabela(linha,
                                                           7,
                                                           1,
                                                           len(MESES) + 1)
                i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class LeituraEarmfpM00(Leitura):
    """
    Realiza a leitura dos arquivos earmfpm00x.out
    existentes em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de arquivos earmfpm00x.out, construindo
    objetos `Earmfpm00` cujas informações são as mesmas dos arquivos.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [BlocoEnergiaArmazenadaFinalPercentual()]
