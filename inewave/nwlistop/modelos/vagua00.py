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


class BlocoValorAguaREE(Bloco):
    """
    Bloco com as informações das tabelas de valor da água por
    REE por mês/ano de estudo.
    """
    str_inicio = "VALOR DAGUA ($/MWh)"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoValorAguaREE.str_inicio,
                         "",
                         True)

        self._dados = ["", pd.DataFrame()]

    def __eq__(self, o: object):
        if not isinstance(o, BlocoValorAguaREE):
            return False
        bloco: BlocoValorAguaREE = o
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
        reg_ree = RegistroAn(12)
        reg_ano = RegistroIn(4)
        reg_serie = RegistroIn(4)
        reg_energia = RegistroFn(8)
        i = 0
        ano = 0
        # Identifica o submercado
        self._dados[0] = reg_ree.le_registro(self._linha_inicio, 63)
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
                serie[i] = reg_serie.le_registro(linha, 2)
                tabela[i, :] = reg_energia.le_linha_tabela(linha,
                                                           9,
                                                           1,
                                                           len(MESES) + 1)
                i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class LeituraVAgua00(Leitura):
    """
    Realiza a leitura dos arquivos vagua00x.out
    existentes em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de arquivos vagua00x.out, construindo
    objetos `Vagua00` cujas informações são as mesmas dos arquivos.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [BlocoValorAguaREE()]
