# Imports do próprio módulo
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave.config import MAX_ANOS_ESTUDO
from inewave.config import MAX_MESES_ESTUDO
from inewave.config import MAX_ANOS_HISTORICO
from inewave.config import MAX_CONFIGURACOES
from inewave.config import MESES, REES, ORDEM_MAX_PARP
# Imports de módulos externos
import numpy as np  # type: ignore
from typing import IO, List


class BlocoSerieEnergiaREE(Bloco):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de energia por REE.
    """

    str_inicio = "SERIE  DE ENERGIAS DO REE"
    str_fim = "CORRELOGRAMO"

    def __init__(self):
        super().__init__(BlocoSerieEnergiaREE.str_inicio,
                         BlocoSerieEnergiaREE.str_fim,
                         True)
        self._dados = np.zeros((MAX_ANOS_HISTORICO,
                                len(MESES) + 1,
                                MAX_CONFIGURACOES))
        self.__cfg = 0

    def __eq__(self, o: object):
        if not isinstance(o, BlocoSerieEnergiaREE):
            return False
        bloco: BlocoSerieEnergiaREE = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):

        def _identifica_cfg(linha: str):
            """
            Processa uma linha e extrai o número da configuração.
            """
            self.__cfg = int(linha.split(STR_CFG)[1][:-2].strip())

        def _le_tabela_serie():
            """
            Lê a tabela de séries de energia de uma configuração.
            """
            # Variáveis auxiliares
            regi = RegistroIn(4)  # PEP8
            regf = RegistroFn(9)  # PEP8
            i_linha = 0
            # Salta 1 linha
            arq.readline()
            # Lê a tabela
            while True:
                linha = arq.readline()
                # Verifica se a tabela já acabou
                if len(linha) < 3:  # Tolerância a caracteres especiais
                    self._dados = self._dados[:i_linha, :, :]
                    break
                # Senão, lê mais uma linha
                # Ano
                self._dados[i_linha, 0, self.__cfg-1] = regi.le_registro(linha,
                                                                         0)
                # Energias de cada mês
                self._dados[i_linha,
                            1:,
                            self.__cfg-1] = regf.le_linha_tabela(linha,
                                                                 5,
                                                                 2,
                                                                 len(MESES))
                i_linha += 1

        STR_CFG = "CONFIGURACAO No."
        ultima_cfg_lida = 0
        # Identifica a primeira cfg no cabeçalho
        _identifica_cfg(self._linha_inicio)
        while True:
            # Confere se a leitura não acabou
            linha = arq.readline()
            if BlocoSerieEnergiaREE.str_fim in linha:
                self._dados = self._dados[:,
                                          :,
                                          :self.__cfg]
                break
            # Atualiza a última cfg quando for a linha devida
            if STR_CFG in linha:
                _identifica_cfg(linha)
            # Se for um cabeçalho de tabela, começa a ler
            if (linha[8:11] == "JAN" and
                    self.__cfg != ultima_cfg_lida):
                _le_tabela_serie()
                ultima_cfg_lida = self.__cfg

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoCorrelParcialREE(Bloco):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às séries de autocorrelações parciais
    das energias por REE.
    """

    str_inicio = "CORRELOGRAMO PARCIAL DA SERIE DE ENERGIAS"
    str_fim = ""

    def __init__(self):
        super().__init__(BlocoCorrelParcialREE.str_inicio,
                         BlocoCorrelParcialREE.str_fim,
                         True)
        self._dados = np.zeros((MAX_MESES_ESTUDO,
                                len(MESES)))

    def __eq__(self, o: object):
        if not isinstance(o, BlocoCorrelParcialREE):
            return False
        bloco: BlocoCorrelParcialREE = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):
        # Variáveis auxiliares
        i_mes = 0
        regi = RegistroIn(4)
        regf = RegistroFn(8)
        # Salta 2 linhas
        arq.readline()
        arq.readline()
        # Lê a tabela
        while True:
            # Verifica se a tabela já acabou
            linha: str = arq.readline()
            if len(linha) < 3:
                self._dados = self._dados[:i_mes, :]
                break
            # Senão, lê mais uma linha
            # Ano
            str_ano = linha[5:9]
            if not linha[5:9].isnumeric():
                idx_ano_passado = i_mes - len(MESES) - 1
                str_ano = str(self._dados[idx_ano_passado, 0] + 1)

            self._dados[i_mes,
                        0] = regi.le_registro(str_ano,
                                              0)
            # Correlação de cada mês
            self._dados[i_mes,
                        1:] = regf.le_linha_tabela(linha,
                                                   11,
                                                   2,
                                                   len(MESES) - 1)
            i_mes += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoOrdensFinaisCoefsREE(Bloco):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às ordens finais ajustadas do modelo e aos
    seus coeficientes por REE.
    """

    str_inicio = "ORDEM FINAL DO MODELO AUTORREGRESSIVO"
    str_fim = "SERIE DE RUIDOS"

    def __init__(self):
        super().__init__(BlocoOrdensFinaisCoefsREE.str_inicio,
                         BlocoOrdensFinaisCoefsREE.str_fim,
                         True)
        self._dados = [
                       np.zeros((MAX_ANOS_ESTUDO,
                                 len(MESES) + 1),
                                dtype=np.int32),
                       np.zeros((MAX_MESES_ESTUDO,
                                 ORDEM_MAX_PARP,
                                 4))
                      ]
        self.__ano = "0"

    def __eq__(self, o: object):
        if not isinstance(o, BlocoOrdensFinaisCoefsREE):
            return False
        bloco: BlocoOrdensFinaisCoefsREE = o
        return all([np.array_equal(d1, d2)
                    for d1, d2 in zip(self._dados, bloco._dados)])

    def __le_ordens(self, arq: IO) -> int:

        def _identifica_ano_estudo(linha: str):
            """
            Identifica o ano de estudo em questão.
            """
            # Não pode usar uma leitura simples de registro
            # pois pode ter "POS" no lugar
            ano: str = linha[32:36]
            self.__ano = (ano if ano.isnumeric()
                          else str(int(self.__ano) + 1))

        # Variáveis auxiliares
        i_ano = 0
        reg = RegistroIn(3)
        # Salta 3 linhas
        for _ in range(3):
            arq.readline()
        while True:
            linha: str = arq.readline()
            # Confere se a tabela já acabou
            if len(linha) < 3:  # Tolerância a caracteres especiais
                self._dados[0] = self._dados[0][:i_ano, :]
                break
            # Extrai o ano
            _identifica_ano_estudo(linha)
            self._dados[0][i_ano, 0] = int(self.__ano)
            # As ordens de cada mês
            self._dados[0][i_ano,
                           1:] = reg.le_linha_tabela(linha,
                                                     38,
                                                     2,
                                                     len(MESES))
            i_ano += 1
        return i_ano

    def __le_coeficientes(self, arq: IO, n_anos: int):

        def _le_tabela():

            def _extrai_ordem_modelo(linha: str):
                """
                """
                return int(linha.split("AR(")[1][:-2])

            def _le_coefs_periodo():
                """
                """
                for o in range(2):
                    linha: str = arq.readline()
                    self._dados[1][i_coefs,
                                   :ordem,
                                   o] = regf.le_linha_tabela(linha,
                                                             0,
                                                             2,
                                                             ordem)

            def _le_coef_media():
                """
                """
                for o in range(2, 4):
                    linha: str = arq.readline()
                    # Se não possui dados de média, não lê
                    if len(linha) < 3:
                        break
                    self._dados[1][i_coefs,
                                   0,
                                   o] = regf.le_registro(linha,
                                                         0)

            # Variaveis auxiliares
            regf = RegistroFn(9)
            linha = ""
            # Procura pelo cabeçalho dos coeficientes do período
            while "COEFICIENTES DA EQUACAO" not in linha:
                linha: str = arq.readline()
            ordem = _extrai_ordem_modelo(linha)
            _le_coefs_periodo()
            _le_coef_media()

        n_periodos = n_anos * len(MESES)
        for i_coefs in range(n_periodos):
            _le_tabela()

        self._dados[1] = self._dados[1][:n_periodos, :, :]

    # Override
    def le(self, arq: IO):

        nanos = self.__le_ordens(arq)
        self.__le_coeficientes(arq, nanos)

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoOrdensOriginaisREE(Bloco):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às ordens originais do modelo por REE.
    """

    str_inicio = "ORDEM ORIGINAL DO MODELO AUTORREGRESSIVO"
    str_fim = ""

    def __init__(self):
        super().__init__(BlocoOrdensOriginaisREE.str_inicio,
                         BlocoOrdensOriginaisREE.str_fim,
                         False)
        self._dados = np.zeros((MAX_ANOS_ESTUDO,
                                len(MESES) + 1),
                               dtype=np.int32)
        self.__ano = "0"

    def __eq__(self, o: object):
        if not isinstance(o, BlocoOrdensOriginaisREE):
            return False
        bloco: BlocoOrdensOriginaisREE = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):

        def _identifica_ano_estudo(linha: str):
            """
            Identifica o ano de estudo em questão.
            """
            # Não pode usar uma leitura simples de registro
            # pois pode ter "POS" no lugar
            ano: str = linha[32:36]
            self.__ano = (ano if ano.isnumeric()
                          else str(int(self.__ano) + 1))

        # Variáveis auxiliares
        i_ano = 0
        reg = RegistroIn(3)
        # Salta 3 linhas
        for _ in range(3):
            arq.readline()
        while True:
            linha: str = arq.readline()
            # Confere se a tabela já acabou
            if len(linha) < 3:  # Tolerância a caracteres especiais
                self._dados = self._dados[:i_ano, :]
                break
            # Extrai o ano
            _identifica_ano_estudo(linha)
            self._dados[i_ano, 0] = int(self.__ano)
            # As ordens de cada mês
            self._dados[i_ano,
                        1:] = reg.le_linha_tabela(linha,
                                                  38,
                                                  2,
                                                  len(MESES))
            i_ano += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoSerieMediaREE(Bloco):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo à série de média de 12 meses por REE.
    """

    str_inicio = "SERIE MEDIA 12 MESES "
    str_fim = "CORRELACAO CRUZADA VARIAVEL ANUAL"

    def __init__(self):
        super().__init__(BlocoSerieMediaREE.str_inicio,
                         BlocoSerieMediaREE.str_fim,
                         True)
        self._dados = np.zeros((MAX_ANOS_HISTORICO,
                                len(MESES),
                                MAX_ANOS_ESTUDO))
        self.__ano = 0

    def __eq__(self, o: object):
        if not isinstance(o, BlocoSerieMediaREE):
            return False
        bloco: BlocoSerieMediaREE = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):

        def _identifica_ano_estudo(linha: str):
            """
            Identifica o ano de estudo em questão.
            """
            # Não pode usar uma leitura simples de registro
            # pois pode ter "POS" no lugar
            if STR_ANO in linha:
                ano = linha.split(STR_ANO)[1].strip()
                self.__ano = (ano if ano.isnumeric()
                              else str(int(self.__ano) + 1))

        def _le_tabela_media() -> bool:
            """
            Lê uma tabela de médias anuais.
            """
            # Variáveis auxiliares
            reg = RegistroFn(9)
            i_linha = 0
            # Salta 1 linha
            arq.readline()
            # Lê a tabela
            while True:
                # Verifica se a tabela já acabou
                linha = arq.readline()
                if len(linha) < 3:  # Tolerância a caracteres especiais
                    self._dados = self._dados[:i_linha, :, :]
                    return True
                # Senão, lê mais uma linha
                self._dados[i_linha,
                            :,
                            i_ano] = reg.le_linha_tabela(linha,
                                                         5,
                                                         2,
                                                         len(MESES))
                i_linha += 1

        # Variáveis auxiliares
        STR_ANO = "ANO:"
        i_ano = 0
        ultimo_ano_lido = ""
        # Identifica o primeiro ano no cabeçalho
        _identifica_ano_estudo(self._linha_inicio)
        while True:
            # Confere se a leitura não acabou
            linha = arq.readline()
            if BlocoSerieMediaREE.str_fim in linha:
                self._dados = self._dados[:, :, :i_ano]
                break
            # Atualiza a detecção de uma nova tabela
            _identifica_ano_estudo(linha)
            # Se existe uma nova tabela, lê
            if linha[8:11] == "JAN" and ultimo_ano_lido != self.__ano:
                _le_tabela_media()
                i_ano += 1
                ultimo_ano_lido = self.__ano

        return linha

    # Override
    def escreve(self,
                arq: IO):
        pass


class BlocoCorrelCruzMediaREE(Bloco):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às correlações cruzadas com a média por REE.
    """

    str_inicio = "CORRELACAO CRUZADA VARIAVEL ANUAL"
    str_fim = ""

    def __init__(self):
        super().__init__(BlocoCorrelCruzMediaREE.str_inicio,
                         BlocoCorrelCruzMediaREE.str_fim,
                         True)
        self._dados = np.zeros((MAX_ANOS_HISTORICO,
                                len(MESES) + 1))

    def __eq__(self, o: object):
        if not isinstance(o, BlocoCorrelCruzMediaREE):
            return False
        bloco: BlocoCorrelCruzMediaREE = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):
        # Variáveis auxiliares
        i_mes = 0
        regi = RegistroIn(4)
        regf = RegistroFn(8)
        # Salta 4 linhas
        for _ in range(4):
            arq.readline()
        # Lê a tabela
        while True:
            # Verifica se a tabela já acabou
            linha: str = arq.readline()
            if len(linha) < 3:
                self._dados = self._dados[:i_mes, :]
                break
            # Senão, lê mais uma linha
            # Ano
            str_ano = linha[5:9]
            if not linha[5:9].isnumeric():
                idx_ano_passado = i_mes - len(MESES) - 1
                str_ano = str(self._dados[idx_ano_passado, 0] + 1)
            self._dados[i_mes, 0] = regi.le_registro(str_ano,
                                                     0)
            # Correlação de cada mês
            self._dados[i_mes,
                        1:] = regf.le_linha_tabela(linha,
                                                   11,
                                                   2,
                                                   len(MESES))
            i_mes += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoCorrelEspAnual(Bloco):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às correlações espaciais anuais.
    """

    str_inicio = "CORRELACAO ESPACIAL HISTORICA ANUAL"
    str_fim = ""

    i = 0

    def __init__(self):
        super().__init__(BlocoCorrelEspAnual.str_inicio,
                         BlocoCorrelEspAnual.str_fim,
                         True)
        self._dados = np.zeros((len(REES),
                                len(REES)))

    def __eq__(self, o: object):
        if not isinstance(o, BlocoCorrelEspAnual):
            return False
        bloco: BlocoCorrelEspAnual = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):

        def _extrai_ordem_rees(linha: str) -> List[int]:
            """
            Obtém a ordem de disposição das REEs nas colunas.
            """
            str_rees = [s for s in linha.split(" ") if len(s) > 1]
            return [REES.index(s) for s in str_rees]

        def _ordena_correls(correls: List[float],
                            idx: List[int]):
            """
            """
            return [correls[idx.index(i)]
                    for i in range(len(idx))]

        reg = RegistroFn(7)
        # Salta 1 linha
        arq.readline()
        idx = _extrai_ordem_rees(arq.readline())
        i_ree = 0
        # Lê a tabela
        while True:
            # Verifica se a tabela já acabou
            linha: str = arq.readline()
            if len(linha) < 3:  # Tolerância a caracteres especiais
                break
            # Senão, lê mais uma linha
            correls = reg.le_linha_tabela(linha, 18, 6, len(MESES))
            self._dados[idx[i_ree],
                        :] = _ordena_correls(correls,
                                             idx)
            i_ree += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoCorrelEspMensal(Bloco):
    """
    Bloco de informações do arquivo `parp.dat`
    relativo às correlações espaciais mensais.
    """

    str_inicio = "CORRELACAO ESPACIAL HISTORICA MENSAL"
    str_fim = "////////////////////"

    def __init__(self):
        super().__init__(BlocoCorrelEspMensal.str_inicio,
                         BlocoCorrelEspMensal.str_fim,
                         True)
        self._dados = np.zeros((len(REES),
                                len(MESES),
                                len(REES)))

    def __eq__(self, o: object):
        if not isinstance(o, BlocoCorrelEspMensal):
            return False
        bloco: BlocoCorrelEspMensal = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):

        def _le_tabela_correl_esp_m(cabecalho: str):
            """
            """

            def _extrai_ordem_rees(linha: str) -> List[int]:
                """
                Obtém a ordem de disposição das REEs nas colunas.
                """
                str_rees = [s for s in linha.split(" ") if len(s) > 1]
                return [REES.index(s) for s in str_rees]

            def _ordena_correls(correls: List[float],
                                idx: List[int]):
                """
                """
                return [correls[idx.index(i)]
                        for i in range(len(idx))]

            # Variáveis auxiliares
            rega = RegistroAn(12)
            regf = RegistroFn(7)
            idx = _extrai_ordem_rees(cabecalho[18:])
            # Lê a tabela
            i_ree = 0
            while True:
                # Verifica se a tabela já acabou
                linha: str = arq.readline()
                if len(linha) < 3:  # Tolerância a caracteres especiais
                    break
                # Senão, lê mais uma linha
                # Identifica a REE da linha
                ree = REES.index(rega.le_registro(linha, 0))
                cor = regf.le_linha_tabela(linha, 18, 6, len(MESES))
                self._dados[ree,
                            i_ree,
                            :] = _ordena_correls(cor,
                                                 idx)
                i_ree += 1

        # Salta 1 linha
        arq.readline()
        # Lê a tabela
        i_tabela = 0
        while True:
            # Verifica se a tabela já acabou
            linha: str = arq.readline()
            if (BlocoCorrelEspMensal.str_fim in linha or
                    BlocoCorrelEspAnual.str_inicio in linha or
                    len(linha) == 0):
                break

            # Senão, procura e lê mais uma tabela
            if "MES" not in linha:
                continue

            _le_tabela_correl_esp_m(linha)
            i_tabela += 1

        return linha

    # Override
    def escreve(self, arq: IO):
        pass


class LeituraPARp(Leitura):
    """
    Realiza a leitura do arquivo `parp.dat`
    existente em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `parp.dat`, construindo
    um objeto `PARp` cujas informações são as mesmas do parp.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo parp.dat.
        """
        series_energia: List[Bloco] = [BlocoSerieEnergiaREE()
                                       for _ in range(len(REES))]
        series_correls: List[Bloco] = [BlocoCorrelParcialREE()
                                       for _ in range(len(REES))]
        ordens_finais_coefs: List[Bloco] = [BlocoOrdensFinaisCoefsREE()
                                            for _ in range(len(REES))]
        ordens_originais: List[Bloco] = [BlocoOrdensOriginaisREE()
                                         for _ in range(len(REES))]
        series_medias: List[Bloco] = [BlocoSerieMediaREE()
                                      for _ in range(len(REES))]
        correls_cruzada_media: List[Bloco] = [BlocoCorrelCruzMediaREE()
                                              for _ in range(len(REES))]
        correls_esp_anuais: List[Bloco] = [BlocoCorrelEspAnual()
                                           for _ in range(MAX_CONFIGURACOES)]
        correls_esp_mensais: List[Bloco] = [BlocoCorrelEspMensal()
                                            for _ in range(MAX_CONFIGURACOES)]

        return (series_energia +
                series_correls +
                ordens_finais_coefs +
                ordens_originais +
                series_medias +
                correls_cruzada_media +
                correls_esp_anuais +
                correls_esp_mensais)

    # Override
    def _fim_arquivo(self, linha: str) -> bool:
        return (len(linha) == 0 or
                BlocoCorrelEspMensal.str_fim in linha)
