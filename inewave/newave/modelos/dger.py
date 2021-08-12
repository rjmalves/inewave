# Imports do próprio módulo
from inewave.config import SUBMERCADOS
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave._utils.escrita import Bloco
from inewave._utils.leitura import Leitura
# Imports de módulos externos
from typing import IO, List
import numpy as np  # type: ignore


class BlocoNomeCaso(Bloco):
    """
    Bloco com o nome do caso, existente
    no arquivo `dger.dat` do NEWAVE.
    """

    def __init__(self):

        super().__init__("",
                         "",
                         True)

        self._dados = ""

    # Override
    def le(self, arq: IO):
        reg = RegistroAn(80)
        self._dados = reg.le_registro(self._linha_inicio, 0)

    # Override
    def escreve(self, arq: IO):
        arq.write(self._dados + "\n")


class BlocoTipoExecucao(Bloco):
    """
    Bloco com o tipo de execução do caso,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "TIPO DE EXECUCAO"
    str_fim = "   (1:EXECUCAO COMPLETA; 0:SIMULACAO FINAL)"

    def __init__(self):

        super().__init__(BlocoTipoExecucao.str_inicio,
                         BlocoTipoExecucao.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoTipoExecucao.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoTipoExecucao.str_fim}\n")
        arq.write(linha)


class BlocoDuracaoPeriodo(Bloco):
    """
    Bloco com a duração do período de execução,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "DURACAO DO PERIODO"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoDuracaoPeriodo.str_inicio,
                         BlocoDuracaoPeriodo.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoDuracaoPeriodo.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoDuracaoPeriodo.str_fim}\n")
        arq.write(linha)


class BlocoNumAnosEstudo(Bloco):
    """
    Bloco com o número de anos no período de estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No. DE ANOS DO EST"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoNumAnosEstudo.str_inicio,
                         BlocoNumAnosEstudo.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoNumAnosEstudo.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoNumAnosEstudo.str_fim}\n")
        arq.write(linha)


class BlocoMesInicioPreEstudo(Bloco):
    """
    Bloco com o mês de início do pré-estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "MES INICIO PRE-EST"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoMesInicioPreEstudo.str_inicio,
                         BlocoMesInicioPreEstudo.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoMesInicioPreEstudo.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoMesInicioPreEstudo.str_fim}\n")
        arq.write(linha)


class BlocoMesInicioEstudo(Bloco):
    """
    Bloco com o mês de início do período de estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "MES INICIO DO ESTUDO"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoMesInicioEstudo.str_inicio,
                         BlocoMesInicioEstudo.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoMesInicioEstudo.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoMesInicioEstudo.str_fim}\n")
        arq.write(linha)


class BlocoAnoInicioEstudo(Bloco):
    """
    Bloco com o ano do início do período de estudo
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "ANO INICIO DO ESTUDO"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoAnoInicioEstudo.str_inicio,
                         BlocoAnoInicioEstudo.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoAnoInicioEstudo.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoAnoInicioEstudo.str_fim}\n")
        arq.write(linha)


class BlocoNumAnosPreEstudo(Bloco):
    """
    Bloco com o número de anos do período pré-estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No. DE ANOS PRE"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoNumAnosPreEstudo.str_inicio,
                         BlocoNumAnosPreEstudo.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoNumAnosPreEstudo.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoNumAnosPreEstudo.str_fim}\n")
        arq.write(linha)


class BlocoNumAnosPosEstudo(Bloco):
    """
    Bloco com o número de anos do período pós-estudo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No. DE ANOS POS"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoNumAnosPosEstudo.str_inicio,
                         BlocoNumAnosPosEstudo.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoNumAnosPosEstudo.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoNumAnosPosEstudo.str_fim}\n")
        arq.write(linha)


class BlocoNumAnosPosEstudoSimFinal(Bloco):
    """
    Bloco com o número de anos do período pós-estudo na simulação final,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No. DE ANOS POS FINAL"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoNumAnosPosEstudoSimFinal.str_inicio,
                         BlocoNumAnosPosEstudoSimFinal.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoNumAnosPosEstudoSimFinal.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoNumAnosPosEstudoSimFinal.str_fim}\n")
        arq.write(linha)


class BlocoImprimeDados(Bloco):
    """
    Bloco com a opção de imprimir dados das usinas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMPRIME DADOS"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoImprimeDados.str_inicio,
                         BlocoImprimeDados.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoImprimeDados.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoImprimeDados.str_fim}\n")
        arq.write(linha)


class BlocoImprimeMercados(Bloco):
    """
    Bloco com a opção de imprimir dados de mercados,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMPRIME MERCADOS"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoImprimeMercados.str_inicio,
                         BlocoImprimeMercados.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoImprimeMercados.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoImprimeMercados.str_fim}\n")
        arq.write(linha)


class BlocoImprimeEnergias(Bloco):
    """
    Bloco com a opção de imprimir dados das energias,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMPRIME ENERGIAS"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoImprimeEnergias.str_inicio,
                         BlocoImprimeEnergias.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoImprimeEnergias.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoImprimeEnergias.str_fim}\n")
        arq.write(linha)


class BlocoImprimeModeloEstocastico(Bloco):
    """
    Bloco com a opção de imprimir dados do modelo estocástico,
    de geração de cenários existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMPRIME M. ESTOCAS"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoImprimeModeloEstocastico.str_inicio,
                         BlocoImprimeModeloEstocastico.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoImprimeModeloEstocastico.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoImprimeModeloEstocastico.str_fim}\n")
        arq.write(linha)


class BlocoImprimeSubsistema(Bloco):
    """
    Bloco com a opção de imprimir dados dos subsistemas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMPRIME SUBSISTEMA"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoImprimeSubsistema.str_inicio,
                         BlocoImprimeSubsistema.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoImprimeSubsistema.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoImprimeSubsistema.str_fim}\n")
        arq.write(linha)


class BlocoNumMaxIteracoes(Bloco):
    """
    Bloco com o número máximo de iterações,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No MAX. DE ITER."
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoNumMaxIteracoes.str_inicio,
                         BlocoNumMaxIteracoes.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoNumMaxIteracoes.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoNumMaxIteracoes.str_fim}\n")
        arq.write(linha)


class BlocoNumForwards(Bloco):
    """
    Bloco com o número de simulações forward,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No DE SIM. FORWARD"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoNumForwards.str_inicio,
                         BlocoNumForwards.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoNumForwards.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoNumForwards.str_fim}\n")
        arq.write(linha)


class BlocoNumAberturas(Bloco):
    """
    Bloco com o número aberturas e se são consideradas
    aberturas variáveis, existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No DE ABERTURAS"
    str_fim = "(CONSIDERA ABERTURA VARIAVEL =0 NAO CONSIDERA, =1 CONSIDERA )"

    def __init__(self):

        super().__init__(BlocoNumAberturas.str_inicio,
                         BlocoNumAberturas.str_fim,
                         True)

        self._dados = 0

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoNumAberturas):
            return False
        bloco: BlocoNumAberturas = o
        return self._dados == bloco._dados

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        num_ab = str(self._dados).rjust(4)
        linha = (f"{BlocoNumAberturas.str_inicio.ljust(21)}" +
                 f"{num_ab}\n")
        arq.write(linha)


class BlocoNumSeriesSinteticas(Bloco):
    """
    Bloco com o número de séries sintéticas utilizadas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No DE SERIES SINT."
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoNumSeriesSinteticas.str_inicio,
                         BlocoNumSeriesSinteticas.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoNumSeriesSinteticas.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoNumSeriesSinteticas.str_fim}\n")
        arq.write(linha)


class BlocoOrdemMaximaPARp(Bloco):
    """
    Bloco com a ordem máxima do modelo PAR(p),
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "ORDEM MAX. PAR(P)"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoOrdemMaximaPARp.str_inicio,
                         BlocoOrdemMaximaPARp.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoOrdemMaximaPARp.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoOrdemMaximaPARp.str_fim}\n")
        arq.write(linha)


class BlocoAnoInicialHistorico(Bloco):
    """
    Bloco com o ano inicial do histórico,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "ANO INICIAL HIST."
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoAnoInicialHistorico.str_inicio,
                         BlocoAnoInicialHistorico.str_fim,
                         True)

        self._dados = [0, 0]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoAnoInicialHistorico):
            return False
        bloco: BlocoAnoInicialHistorico = o
        return all([d1 == d2 for d1, d2 in zip(self._dados,
                                               bloco._dados)])

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados[0] = reg.le_registro(self._linha_inicio, 21)
        reg_flag = RegistroIn(1)
        self._dados[1] = reg_flag.le_registro(self._linha_inicio, 28)

    # Override
    def escreve(self, arq: IO):
        ano = str(self._dados[0]).rjust(4)
        flag = str(self._dados[1]).rjust(4)
        linha = (f"{BlocoAnoInicialHistorico.str_inicio.ljust(21)}" +
                 f"{ano}{flag}{BlocoAnoInicialHistorico.str_fim}\n")
        arq.write(linha)


class BlocoCalculaVolInicial(Bloco):
    """
    Bloco com o ano inicial do histórico,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "CALCULA VOL.INICIAL"
    str_fim = "0=USA REG 20 ; 1= CALCULA EARM. INICIAL"

    def __init__(self):

        super().__init__(BlocoCalculaVolInicial.str_inicio,
                         BlocoCalculaVolInicial.str_fim,
                         True)

        self._dados = 0

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCalculaVolInicial):
            return False
        bloco: BlocoCalculaVolInicial = o
        return self._dados == bloco._dados

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(1)
        self._dados = reg.le_registro(self._linha_inicio, 24)

    # Override
    def escreve(self, arq: IO):
        calcula = str(self._dados).rjust(4)
        linha = (f"{BlocoCalculaVolInicial.str_inicio.ljust(21)}" +
                 f"{calcula}   {BlocoCalculaVolInicial.str_fim}\n")
        arq.write(linha)


class BlocoVolInicialSubsistema(Bloco):
    """
    Bloco com o ano inicial do histórico,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = " POR SUBSISTEMA"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoVolInicialSubsistema.str_inicio,
                         BlocoVolInicialSubsistema.str_fim,
                         True)

        self._dados = np.zeros((len(SUBMERCADOS) + 1,), dtype=np.float64)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoVolInicialSubsistema):
            return False
        bloco: BlocoVolInicialSubsistema = o
        return all([d1 == d2 for d1, d2 in zip(self._dados,
                                               bloco._dados)])

    # Override
    def le(self, arq: IO):
        reg = RegistroFn(5)
        self._dados = reg.le_linha_tabela(self._linha_inicio,
                                          21,
                                          2,
                                          len(SUBMERCADOS) + 1)

    # Override
    def escreve(self, arq: IO):
        dado = ""
        for i in range(len(self._dados)):
            d = f"{self._dados[i]:3.1f}  "
            dado += d.rjust(7)
        linha = (f"{BlocoVolInicialSubsistema.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoVolInicialSubsistema.str_fim}\n")
        arq.write(linha)


class BlocoTolerancia(Bloco):
    """
    Bloco com a tolerância de convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "TOLERANCIA      -%"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoTolerancia.str_inicio,
                         BlocoTolerancia.str_fim,
                         True)

        self._dados = 0.0

    # Override
    def le(self, arq: IO):
        reg = RegistroFn(5)
        self._dados = reg.le_registro(self._linha_inicio,
                                      21)

    # Override
    def escreve(self, arq: IO):
        dado = str(f"{self._dados:2.1f}").rjust(5)
        linha = (f"{BlocoTolerancia.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoTolerancia.str_fim}\n")
        arq.write(linha)


class BlocoTaxaDesconto(Bloco):
    """
    Bloco com a taxa de desconto,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "TAXA DE DESCONTO-%"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoTaxaDesconto.str_inicio,
                         BlocoTaxaDesconto.str_fim,
                         True)

        self._dados = 0.0

    # Override
    def le(self, arq: IO):
        reg = RegistroFn(5)
        self._dados = reg.le_registro(self._linha_inicio,
                                      21)

    # Override
    def escreve(self, arq: IO):
        dado = str(f"{self._dados:2.1f}").rjust(5)
        linha = (f"{BlocoTaxaDesconto.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoTaxaDesconto.str_fim}\n")
        arq.write(linha)


class BlocoTipoSimFinal(Bloco):
    """
    Bloco com a opção do tipo de simulação final,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "TIPO SIMUL. FINAL"
    str_fim = "(=0 NAO SIMULA; =1 S.SINT.; =2 S.HIST.; =3 CONSIST)"

    def __init__(self):

        super().__init__(BlocoTipoSimFinal.str_inicio,
                         BlocoTipoSimFinal.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoTipoSimFinal.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoTipoSimFinal.str_fim}\n")
        arq.write(linha)


class BlocoImpressaoOperacao(Bloco):
    """
    Bloco com a opção para impressão da operação detalhada,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMPRESSAO DA OPER"
    str_fim = "(=0 SINOPSE; =1 OP. DETALHADA)"

    def __init__(self):

        super().__init__(BlocoImpressaoOperacao.str_inicio,
                         BlocoImpressaoOperacao.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoImpressaoOperacao.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoImpressaoOperacao.str_fim}\n")
        arq.write(linha)


class BlocoImpressaoConvergencia(Bloco):
    """
    Bloco com a opção para impressão da convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMPRESSAO DA CONVERG."
    str_fim = "(=0 CONVERGENCIA FINAL APENAS, =1 TOTAL)"

    def __init__(self):

        super().__init__(BlocoImpressaoConvergencia.str_inicio,
                         BlocoImpressaoConvergencia.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoImpressaoConvergencia.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoImpressaoConvergencia.str_fim}\n")
        arq.write(linha)


class BlocoIntervaloGravar(Bloco):
    """
    Bloco com a opção para impressão do intervalo para gravar,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "INTERVALO P/ GRAVAR"
    str_fim = "SERIES SIMULADAS ( 40  SERIES GRAVADAS )"

    def __init__(self):

        super().__init__(BlocoIntervaloGravar.str_inicio,
                         BlocoIntervaloGravar.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoIntervaloGravar.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoIntervaloGravar.str_fim}\n")
        arq.write(linha)


class BlocoMinIteracoes(Bloco):
    """
    Bloco com o número mínimo de iterações,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No. MIN. ITER."
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoMinIteracoes.str_inicio,
                         BlocoMinIteracoes.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoMinIteracoes.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoMinIteracoes.str_fim}\n")
        arq.write(linha)


class BlocoRacionamentoPreventivo(Bloco):
    """
    Bloco com o uso de racionamento preventivo,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "RACIONAMENTO PREVENT."
    str_fim = "(=0 NAO CONSIDERA NA SIMULACAO FINAL; 1=CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoRacionamentoPreventivo.str_inicio,
                         BlocoRacionamentoPreventivo.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoRacionamentoPreventivo.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoRacionamentoPreventivo.str_fim}\n")
        arq.write(linha)


class BlocoNumAnosManutUTE(Bloco):
    """
    Bloco com o número de anos considerados de manutenção de UTEs,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "No. ANOS MANUT.UTE'S"
    str_fim = "(=0 NAO CONSIDERA, =1 ANO, =2 ANOS)"

    def __init__(self):

        super().__init__(BlocoNumAnosManutUTE.str_inicio,
                         BlocoNumAnosManutUTE.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoNumAnosManutUTE.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoNumAnosManutUTE.str_fim}\n")
        arq.write(linha)


class BlocoTendenciaHidrologica(Bloco):
    """
    Bloco com o uso e a forma de uso da tendência hidrológica,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "TENDENCIA HIDROLOGICA"
    str_fim = "(1 FCF / 2 SF =0 NAO CONDIC., =1 P/ SUBSISTEMA, =2 P/ POSTO)"

    def __init__(self):

        super().__init__(BlocoTendenciaHidrologica.str_inicio,
                         BlocoTendenciaHidrologica.str_fim,
                         True)

        self._dados = [0, 0]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTendenciaHidrologica):
            return False
        bloco: BlocoTendenciaHidrologica = o
        return all([d1 == d2 for d1, d2 in zip(self._dados,
                                               bloco._dados)])

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados[0] = reg.le_registro(self._linha_inicio, 21)
        self._dados[1] = reg.le_registro(self._linha_inicio, 26)

    # Override
    def escreve(self, arq: IO):
        uso = str(self._dados[0]).rjust(4)
        condic = str(self._dados[1]).rjust(4)
        linha = (f"{BlocoTendenciaHidrologica.str_inicio.ljust(21)}" +
                 f"{uso} {condic}   {BlocoTendenciaHidrologica.str_fim}\n")
        arq.write(linha)


class BlocoRestricaoItaipu(Bloco):
    """
    Bloco com a consideração das restrições de Itaipu,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "RESTRICA0 DE ITAIPU"
    str_fim = "(=0 NAO CONSIDERA, =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoRestricaoItaipu.str_inicio,
                         BlocoRestricaoItaipu.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoRestricaoItaipu.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoRestricaoItaipu.str_fim}\n")
        arq.write(linha)


class BlocoBid(Bloco):
    """
    Bloco com a consideração das restrições de Itaipu,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "BID"
    str_fim = "(=0 NAO CONSIDERA, =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoBid.str_inicio,
                         BlocoBid.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoBid.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoBid.str_fim}\n")
        arq.write(linha)


class BlocoPerdasTransmissao(Bloco):
    """
    Bloco com a consideração das perdas na transmissão,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "PERDAS P/ TRANSMISSAO"
    str_fim = "(=0 NAO CONSIDERA, =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoPerdasTransmissao.str_inicio,
                         BlocoPerdasTransmissao.str_fim,
                         True)
        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoPerdasTransmissao.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoPerdasTransmissao.str_fim}\n")
        arq.write(linha)


class BlocoElNino(Bloco):
    """
    Bloco com a consideração do El Nino,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "EL NINO"
    str_fim = "(=0 NAO CONSIDERA, =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoElNino.str_inicio,
                         BlocoElNino.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoElNino.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoElNino.str_fim}\n")
        arq.write(linha)


class BlocoEnso(Bloco):
    """
    Bloco com a consideração de ENSO,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "ENSO INDEX"
    str_fim = "(FUNCAO NAO IMPLEMENTADA)"

    def __init__(self):

        super().__init__(BlocoEnso.str_inicio,
                         BlocoEnso.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoEnso.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoEnso.str_fim}\n")
        arq.write(linha)


class BlocoDuracaoPorPatamar(Bloco):
    """
    Bloco com a consideração da duração por patamar,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "DURACAO POR PATAMAR"
    str_fim = "(=0 SAZONAL, =1 VARIAVEL POR ANO)"

    def __init__(self):

        super().__init__(BlocoDuracaoPorPatamar.str_inicio,
                         BlocoDuracaoPorPatamar.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoDuracaoPorPatamar.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoDuracaoPorPatamar.str_fim}\n")
        arq.write(linha)


class BlocoOutrosUsosAgua(Bloco):
    """
    Bloco com a consideração dos outros usos da água,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "OUTROS USOS DA AGUA"
    str_fim = "(=0 NAO CONSIDERA, =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoOutrosUsosAgua.str_inicio,
                         BlocoOutrosUsosAgua.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoOutrosUsosAgua.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoOutrosUsosAgua.str_fim}\n")
        arq.write(linha)


class BlocoCorrecaoDesvio(Bloco):
    """
    Bloco com a consideração da correção do desvio,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "CORRECAO DESVIO"
    str_fim = "(=0 CONSTANTE; =1 VARIAVEL COM O ARMAZENAMENTO)"

    def __init__(self):

        super().__init__(BlocoCorrecaoDesvio.str_inicio,
                         BlocoCorrecaoDesvio.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoCorrecaoDesvio.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoCorrecaoDesvio.str_fim}\n")
        arq.write(linha)


class BlocoCurvaAversao(Bloco):
    """
    Bloco com a consideração da curva de penalização por VminP,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "C.AVERSAO/PENAL.VMINP"
    str_fim = "(=0 SEM CAR E VMINP; =1  CAR E/OU VMINP)"

    def __init__(self):

        super().__init__(BlocoCurvaAversao.str_inicio,
                         BlocoCurvaAversao.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoCurvaAversao.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoCurvaAversao.str_fim}\n")
        arq.write(linha)


class BlocoTipoGeracaoENA(Bloco):
    """
    Bloco com a consideração do tipo de geração de ENA,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "TIPO DE GERACAO ENAS"
    str_fim = "(=0 RUIDOS FW SORTEADOS DA BW E COMPENSACAO CORREL.ESPACIAL; =1 COMPENS.BW; =2 COMPENS.BW E FW)"  # noqa

    def __init__(self):

        super().__init__(BlocoTipoGeracaoENA.str_inicio,
                         BlocoTipoGeracaoENA.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoTipoGeracaoENA.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoTipoGeracaoENA.str_fim}\n")
        arq.write(linha)


class BlocoRiscoDeficit(Bloco):
    """
    Bloco com o uso e a forma de consideração do risco de déficit,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "RISCO DE DEFICIT"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoRiscoDeficit.str_inicio,
                         BlocoRiscoDeficit.str_fim,
                         True)

        self._dados = [0, 0]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRiscoDeficit):
            return False
        bloco: BlocoRiscoDeficit = o
        return all([d1 == d2 for d1, d2 in zip(self._dados,
                                               bloco._dados)])

    # Override
    def le(self, arq: IO):
        reg = RegistroFn(4)
        self._dados[0] = reg.le_registro(self._linha_inicio, 21)
        self._dados[1] = reg.le_registro(self._linha_inicio, 27)

    # Override
    def escreve(self, arq: IO):
        prof1 = str(f"{self._dados[0]:2.1f}").rjust(4)
        prof2 = str(f"{self._dados[1]:2.1f}").rjust(4)
        linha = (f"{BlocoRiscoDeficit.str_inicio.ljust(21)}" +
                 f"{prof1}  {prof2} {BlocoRiscoDeficit.str_fim}\n")
        arq.write(linha)


class BlocoIteracaoParaSimFinal(Bloco):
    """
    Bloco com a consideração da iteração para simulação final,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "ITERACAO P/SIM.FINAL"
    str_fim = "(=0 CONSIDERA TODAS AS ITERACOES)"

    def __init__(self):

        super().__init__(BlocoIteracaoParaSimFinal.str_inicio,
                         BlocoIteracaoParaSimFinal.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoIteracaoParaSimFinal.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoIteracaoParaSimFinal.str_fim}\n")
        arq.write(linha)


class BlocoAgrupamentoLivre(Bloco):
    """
    Bloco com a consideração do agrupamento de intercâmbios,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "AGRUPAMENTO LIVRE"
    str_fim = "(=0 NAO CONSIDERA, =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoAgrupamentoLivre.str_inicio,
                         BlocoAgrupamentoLivre.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoAgrupamentoLivre.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoAgrupamentoLivre.str_fim}\n")
        arq.write(linha)


class BlocoEqualizacaoPenalInt(Bloco):
    """
    Bloco com a consideração da equalização da penalização de intercâmbios,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "EQUALIZACAO PEN.INT."
    str_fim = "(FLAG DESABILITADO)"

    def __init__(self):

        super().__init__(BlocoEqualizacaoPenalInt.str_inicio,
                         BlocoEqualizacaoPenalInt.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoEqualizacaoPenalInt.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoEqualizacaoPenalInt.str_fim}\n")
        arq.write(linha)


class BlocoRepresentacaoSubmot(Bloco):
    """
    Bloco com a consideração da representação de submotorização,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "REPRESENT.SUBMOT."
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA SUBSISTEMA, =2 CONSIDERA USINA)"  # noqa

    def __init__(self):

        super().__init__(BlocoRepresentacaoSubmot.str_inicio,
                         BlocoRepresentacaoSubmot.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoRepresentacaoSubmot.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoRepresentacaoSubmot.str_fim}\n")
        arq.write(linha)


class BlocoOrdenacaoAutomatica(Bloco):
    """
    Bloco com a consideração da ordenação automática,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "ORDENACAO AUTOMATICA"
    str_fim = "(=0 NAO CONSIDERA; =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoOrdenacaoAutomatica.str_inicio,
                         BlocoOrdenacaoAutomatica.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoOrdenacaoAutomatica.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoOrdenacaoAutomatica.str_fim}\n")
        arq.write(linha)


class BlocoConsideraCargaAdicional(Bloco):
    """
    Bloco com a consideração de cargas adicionais,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "CONS. CARGA ADICIONAL"
    str_fim = "(=0 NAO CONSIDERA; =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoConsideraCargaAdicional.str_inicio,
                         BlocoConsideraCargaAdicional.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoConsideraCargaAdicional.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoConsideraCargaAdicional.str_fim}\n")
        arq.write(linha)


class BlocoDeltaZSUP(Bloco):
    """
    Bloco com a tolerância de variação do Zsup,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "DELTA ZSUP"
    str_fim = "(VALOR EM PERCENTUAL)"

    def __init__(self):

        super().__init__(BlocoDeltaZSUP.str_inicio,
                         BlocoDeltaZSUP.str_fim,
                         True)

        self._dados = 0.0

    # Override
    def le(self, arq: IO):
        reg = RegistroFn(4)
        self._dados = reg.le_registro(self._linha_inicio,
                                      21)

    # Override
    def escreve(self, arq: IO):
        dado = str(f"{self._dados:2.1f}").rjust(4)
        linha = (f"{BlocoDeltaZSUP.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoDeltaZSUP.str_fim}\n")
        arq.write(linha)


class BlocoDeltaZINF(Bloco):
    """
    Bloco com a tolerância de variação do Zinf,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "DELTA ZINF"
    str_fim = "(VALOR EM PERCENTUAL)"

    def __init__(self):

        super().__init__(BlocoDeltaZINF.str_inicio,
                         BlocoDeltaZINF.str_fim,
                         True)

        self._dados = 0.0

    # Override
    def le(self, arq: IO):
        reg = RegistroFn(4)
        self._dados = reg.le_registro(self._linha_inicio,
                                      21)

    # Override
    def escreve(self, arq: IO):
        dado = str(f"{self._dados:2.1f}").rjust(4)
        linha = (f"{BlocoDeltaZINF.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoDeltaZINF.str_fim}\n")
        arq.write(linha)


class BlocoDeltasConsecutivos(Bloco):
    """
    Bloco com o número de deltas consecutivos para covnergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "DELTAS CONSECUT."
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoDeltasConsecutivos.str_inicio,
                         BlocoDeltasConsecutivos.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoDeltasConsecutivos.str_inicio.ljust(21)}" +
                 f"{dado}{BlocoDeltasConsecutivos.str_fim}\n")
        arq.write(linha)


class BlocoDespachoAntecipadoGNL(Bloco):
    """
    Bloco com a consideração de despacho antecipado,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "DESP. ANTEC.  GNL"
    str_fim = "(=0 NAO CONSIDERA; =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoDespachoAntecipadoGNL.str_inicio,
                         BlocoDespachoAntecipadoGNL.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoDespachoAntecipadoGNL.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoDespachoAntecipadoGNL.str_fim}\n")
        arq.write(linha)


class BlocoModifAutomaticaAdTerm(Bloco):
    """
    Bloco com a consideração sobre modificação automática de adiantamento
    de térmicas, existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "MODIF.AUTOM.ADTERM"
    str_fim = "(=0 NAO CONSIDERA; =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoModifAutomaticaAdTerm.str_inicio,
                         BlocoModifAutomaticaAdTerm.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoModifAutomaticaAdTerm.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoModifAutomaticaAdTerm.str_fim}\n")
        arq.write(linha)


class BlocoGeracaoHidraulicaMin(Bloco):
    """
    Bloco com a consideração de geração hidraulica mínima,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "CONSIDERA GHMIN"
    str_fim = "(=0 NAO CONSIDERA; =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoGeracaoHidraulicaMin.str_inicio,
                         BlocoGeracaoHidraulicaMin.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoGeracaoHidraulicaMin.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoGeracaoHidraulicaMin.str_fim}\n")
        arq.write(linha)


class BlocoSimFinalComData(Bloco):
    """
    Bloco com a consideração da data na simulação final,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "S.F. COM DATA"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoSimFinalComData.str_inicio,
                         BlocoSimFinalComData.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoSimFinalComData.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoSimFinalComData.str_fim}\n")
        arq.write(linha)


class BlocoGerenciamentoPLs(Bloco):
    """
    Bloco com as configurações do gerenciamento de PLs
    aberturas variáveis, existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "GER.PLs E NV1 E NV2"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoGerenciamentoPLs.str_inicio,
                         BlocoGerenciamentoPLs.str_fim,
                         True)

        self._dados = [0, 0, 0, 0, 0]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoGerenciamentoPLs):
            return False
        bloco: BlocoGerenciamentoPLs = o
        return all([d1 == d2 for d1, d2 in zip(self._dados,
                                               bloco._dados)])

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_linha_tabela(self._linha_inicio,
                                          21,
                                          1,
                                          5)

    # Override
    def escreve(self, arq: IO):
        dado = ""
        for d in self._dados:
            dado += f"{str(d).rjust(4)} "
        linha = (f"{BlocoGerenciamentoPLs.str_inicio.ljust(21)}" +
                 f"{dado} {BlocoGerenciamentoPLs.str_fim}\n")
        arq.write(linha)


class BlocoSAR(Bloco):
    """
    Bloco com a configuração para uso da SAR,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "SAR"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoSAR.str_inicio,
                         BlocoSAR.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoSAR.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoSAR.str_fim}\n")
        arq.write(linha)


class BlocoCVAR(Bloco):
    """
    Bloco com a configuração para uso do CVAR,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "CVAR"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA CTE TEMPO, =2 CONSIDERA VARIAVEL NO TEMP)"  # noqa

    def __init__(self):

        super().__init__(BlocoCVAR.str_inicio,
                         BlocoCVAR.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoCVAR.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoCVAR.str_fim}\n")
        arq.write(linha)


class BlocoZSUPMinConvergencia(Bloco):
    """
    Bloco com a consideração do Zsup mínimo durante a convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "CONS. ZSUP MIN. CONV."
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoZSUPMinConvergencia.str_inicio,
                         BlocoZSUPMinConvergencia.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoZSUPMinConvergencia.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoZSUPMinConvergencia.str_fim}\n")
        arq.write(linha)


class BlocoDesconsideraVazaoMinima(Bloco):
    """
    Bloco com a configuração para desconsiderar vazao mínima,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "DESCONSIDERA VAZMIN"
    str_fim = "(=0 NAO , =1 SIM)"

    def __init__(self):

        super().__init__(BlocoDesconsideraVazaoMinima.str_inicio,
                         BlocoDesconsideraVazaoMinima.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoDesconsideraVazaoMinima.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoDesconsideraVazaoMinima.str_fim}\n")
        arq.write(linha)


class BlocoRestricoesEletricas(Bloco):
    """
    Bloco com a consideração de restrições elétricas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "RESTRICOES ELETRICAS"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoRestricoesEletricas.str_inicio,
                         BlocoRestricoesEletricas.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoRestricoesEletricas.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoRestricoesEletricas.str_fim}\n")
        arq.write(linha)


class BlocoSelecaoCortes(Bloco):
    """
    Bloco com a consideração da seleção de cortes,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "SELECAO DE CORTES"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoSelecaoCortes.str_inicio,
                         BlocoSelecaoCortes.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoSelecaoCortes.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoSelecaoCortes.str_fim}\n")
        arq.write(linha)


class BlocoJanelaCortes(Bloco):
    """
    Bloco com a consideração da janela de cortes,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "JANELA DE CORTES"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoJanelaCortes.str_inicio,
                         BlocoJanelaCortes.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoJanelaCortes.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoJanelaCortes.str_fim}\n")
        arq.write(linha)


class BlocoReamostragemCenarios(Bloco):
    """
    Bloco com as configurações de reamostragem de cenários,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "REAMOST. CENARIOS"
    str_fim = "(UTILIZA REAMOSTRAGEM: =0 NAO; =1 SIM     TIPO: =0 RECOMB; =1 PLENA     PASSO: 0 - 45 )"  # noqa

    def __init__(self):

        super().__init__(BlocoReamostragemCenarios.str_inicio,
                         BlocoReamostragemCenarios.str_fim,
                         True)

        self._dados = [0, 0, 0]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoReamostragemCenarios):
            return False
        bloco: BlocoReamostragemCenarios = o
        return all([d1 == d2 for d1, d2 in zip(self._dados,
                                               bloco._dados)])

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_linha_tabela(self._linha_inicio,
                                          21,
                                          1,
                                          3)

    # Override
    def escreve(self, arq: IO):
        dado = ""
        for d in self._dados:
            dado += f"{str(d).zfill(4)} "
        linha = (f"{BlocoReamostragemCenarios.str_inicio.ljust(21)}" +
                 f"{dado} {BlocoReamostragemCenarios.str_fim}\n")
        arq.write(linha)


class BlocoConvergeNoZero(Bloco):
    """
    Bloco com a consideração da convergência no 0,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "CONVERGE NO ZERO"
    str_fim = "(=0 CONVERGENCIA TRADICIONAL, =1 CONVERGENCIA CALCULADA NO ZERO)"  # noqa

    def __init__(self):

        super().__init__(BlocoConvergeNoZero.str_inicio,
                         BlocoConvergeNoZero.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoConvergeNoZero.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoConvergeNoZero.str_fim}\n")
        arq.write(linha)


class BlocoConsultaFCF(Bloco):
    """
    Bloco com a consideração da consulta à FCF,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "CONSULTA FCF"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoConsultaFCF.str_inicio,
                         BlocoConsultaFCF.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoConsultaFCF.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoConsultaFCF.str_fim}\n")
        arq.write(linha)


class BlocoImpressaoENA(Bloco):
    """
    Bloco com a consideração da impressão da ENA,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMPRESSAO ENA"
    str_fim = "(=0 NAO IMPRIME , =1 IMPRIME)"

    def __init__(self):

        super().__init__(BlocoImpressaoENA.str_inicio,
                         BlocoImpressaoENA.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).zfill(4)
        linha = (f"{BlocoImpressaoENA.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoImpressaoENA.str_fim}\n")
        arq.write(linha)


class BlocoImpressaoCortesAtivosSimFinal(Bloco):
    """
    Bloco com a consideração da impressão dos cortes ativos
    na simulação final, existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "IMP. CATIVO S.FINAL"
    str_fim = "(=0 NAO IMPRIME , =1 IMPRIME)"

    def __init__(self):

        super().__init__(BlocoImpressaoCortesAtivosSimFinal.str_inicio,
                         BlocoImpressaoCortesAtivosSimFinal.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).zfill(4)
        linha = (f"{BlocoImpressaoCortesAtivosSimFinal.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoImpressaoCortesAtivosSimFinal.str_fim}\n")
        arq.write(linha)


class BlocoRepresentacaoAgregacao(Bloco):
    """
    Bloco com a representação da agregação,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "REP. AGREGACAO"
    str_fim = "(=0 MAIS PROXIMO, =1 CENTROIDE)"

    def __init__(self):

        super().__init__(BlocoRepresentacaoAgregacao.str_inicio,
                         BlocoRepresentacaoAgregacao.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).zfill(4)
        linha = (f"{BlocoRepresentacaoAgregacao.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoRepresentacaoAgregacao.str_fim}\n")
        arq.write(linha)


class BlocoMatrizCorrelacaoEspacial(Bloco):
    """
    Bloco com a representação da correlação espacial,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "MATRIZ CORR.ESPACIAL"
    str_fim = "(=0 ANUAL, =1 MENSAL)"

    def __init__(self):

        super().__init__(BlocoMatrizCorrelacaoEspacial.str_inicio,
                         BlocoMatrizCorrelacaoEspacial.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).zfill(4)
        linha = (f"{BlocoMatrizCorrelacaoEspacial.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoMatrizCorrelacaoEspacial.str_fim}\n")
        arq.write(linha)


class BlocoDesconsideraConvEstatistica(Bloco):
    """
    Bloco com a desconsideração do critério estatístico para convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "DESCONS. CONV. ESTAT"
    str_fim = "(=0 NAO, =1 SIM)"

    def __init__(self):

        super().__init__(BlocoDesconsideraConvEstatistica.str_inicio,
                         BlocoDesconsideraConvEstatistica.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).zfill(4)
        linha = (f"{BlocoDesconsideraConvEstatistica.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoDesconsideraConvEstatistica.str_fim}\n")
        arq.write(linha)


class BlocoMomentoReamostragem(Bloco):
    """
    Bloco com a escolha do momento de reamostragem,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "MOMENTO REAMOSTRAGEM"
    str_fim = "(=0 BACKWARD, =1 FORWARD)"

    def __init__(self):

        super().__init__(BlocoMomentoReamostragem.str_inicio,
                         BlocoMomentoReamostragem.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).zfill(4)
        linha = (f"{BlocoMomentoReamostragem.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoMomentoReamostragem.str_fim}\n")
        arq.write(linha)


class BlocoMantemArquivosEnergias(Bloco):
    """
    Bloco com a escolha de manter ou não os arquivos de energias,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "ARQUIVOS ENA"
    str_fim = "(=0 APAGA APOS EXECUCAO, =1 MANTEM)"

    def __init__(self):

        super().__init__(BlocoMantemArquivosEnergias.str_inicio,
                         BlocoMantemArquivosEnergias.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).zfill(4)
        linha = (f"{BlocoMantemArquivosEnergias.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoMantemArquivosEnergias.str_fim}\n")
        arq.write(linha)


class BlocoInicioTesteConvergencia(Bloco):
    """
    Bloco com a iteração de início para o teste de convergência,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "INICIO TESTE CONVERG."
    str_fim = "(=0 PRIMEIRA ITERACAO, =1 ITERACAO MINIMA)"

    def __init__(self):

        super().__init__(BlocoInicioTesteConvergencia.str_inicio,
                         BlocoInicioTesteConvergencia.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoInicioTesteConvergencia.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoInicioTesteConvergencia.str_fim}\n")
        arq.write(linha)


class BlocoSazonalizarVminT(Bloco):
    """
    Bloco com a escolha de sazonalizar o VminT nos períodos estáticos,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "SAZ. VMINT PER. EST."
    str_fim = "(=0 PRE E POS NAO SAZONAIS, =1 PRE E POS SAZONAIS)"

    def __init__(self):

        super().__init__(BlocoSazonalizarVminT.str_inicio,
                         BlocoSazonalizarVminT.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoSazonalizarVminT.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoSazonalizarVminT.str_fim}\n")
        arq.write(linha)


class BlocoSazonalizarVmaxT(Bloco):
    """
    Bloco com a escolha de sazonalizar o VmaxT nos períodos estáticos,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "SAZ. VMAXT PER. EST."
    str_fim = "(=0 PRE E POS NAO SAZONAIS, =1 PRE E POS SAZONAIS)"

    def __init__(self):

        super().__init__(BlocoSazonalizarVmaxT.str_inicio,
                         BlocoSazonalizarVmaxT.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoSazonalizarVmaxT.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoSazonalizarVmaxT.str_fim}\n")
        arq.write(linha)


class BlocoSazonalizarVminP(Bloco):
    """
    Bloco com a escolha de sazonalizar o VminP nos períodos estáticos,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "SAZ. VMINP PER. EST."
    str_fim = "(=0 PRE E POS NAO SAZONAIS, =1 PRE E POS SAZONAIS)"

    def __init__(self):

        super().__init__(BlocoSazonalizarVminP.str_inicio,
                         BlocoSazonalizarVminP.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoSazonalizarVminP.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoSazonalizarVminP.str_fim}\n")
        arq.write(linha)


class BlocoSazonalizarCfugaCmont(Bloco):
    """
    Bloco com a escolha de sazonalizar Cfuga e Cmont nos períodos
    estáticos, existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "SAZ. CFUGA E CMONT"
    str_fim = "(=0 PRE E POS NAO SAZONAIS, =1 PRE E POS SAZONAIS)"

    def __init__(self):

        super().__init__(BlocoSazonalizarCfugaCmont.str_inicio,
                         BlocoSazonalizarCfugaCmont.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoSazonalizarCfugaCmont.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoSazonalizarCfugaCmont.str_fim}\n")
        arq.write(linha)


class BlocoRestricoesEmissaoGEE(Bloco):
    """
    Bloco com a escolha de habilitar ou não as retrições de GEE,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "REST. EMISSAO GEE"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoRestricoesEmissaoGEE.str_inicio,
                         BlocoRestricoesEmissaoGEE.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoRestricoesEmissaoGEE.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoRestricoesEmissaoGEE.str_fim}\n")
        arq.write(linha)


class BlocoAfluenciaAnualPARp(Bloco):
    """
    Bloco com a consideração da componente de afluência anual
    para o PAR(p), existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "AFLUENCIA ANUAL PARP"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA; REDUCAO DA ORDEM: =0 CONSIDERA,  =1 NAO CONSIDERA, =2 CONSIDERA COM IMPRESSAO RELATORIO)"  # noqa

    def __init__(self):

        super().__init__(BlocoAfluenciaAnualPARp.str_inicio,
                         BlocoAfluenciaAnualPARp.str_fim,
                         True)

        self._dados = [0, 0]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoAfluenciaAnualPARp):
            return False
        bloco: BlocoAfluenciaAnualPARp = o
        return all([d1 == d2 for d1, d2 in zip(self._dados,
                                               bloco._dados)])

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_linha_tabela(self._linha_inicio,
                                          21,
                                          1,
                                          2)

    # Override
    def escreve(self, arq: IO):
        dado = ""
        for d in self._dados:
            dado += f"{str(d).rjust(4)} "
        linha = (f"{BlocoAfluenciaAnualPARp.str_inicio.ljust(21)}" +
                 f"{dado}  {BlocoAfluenciaAnualPARp.str_fim}\n")
        arq.write(linha)


class BlocoRestricoesFornecGas(Bloco):
    """
    Bloco com a escolha de habilitar ou não as retrições de fornecimento
    de gás, existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "REST. FORNEC. GAS"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoRestricoesFornecGas.str_inicio,
                         BlocoRestricoesFornecGas.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoRestricoesFornecGas.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoRestricoesFornecGas.str_fim}\n")
        arq.write(linha)


class BlocoIncertezaGeracaoEolica(Bloco):
    """
    Bloco com a escolha de habilitar ou não as incertezas na geração
    eólica, existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "INCERTEZA GER.EOLICA"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoIncertezaGeracaoEolica.str_inicio,
                         BlocoIncertezaGeracaoEolica.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoIncertezaGeracaoEolica.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoIncertezaGeracaoEolica.str_fim}\n")
        arq.write(linha)


class BlocoIncertezaGeracaoSolar(Bloco):
    """
    Bloco com a escolha de habilitar ou não as incertezas na geração
    solar, existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "INCERTEZA GER.SOLAR"
    str_fim = "(=0 NAO CONSIDERA , =1 CONSIDERA)"

    def __init__(self):

        super().__init__(BlocoIncertezaGeracaoSolar.str_inicio,
                         BlocoIncertezaGeracaoSolar.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoIncertezaGeracaoSolar.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoIncertezaGeracaoSolar.str_fim}\n")
        arq.write(linha)


class BlocoRepresentacaoIncerteza(Bloco):
    """
    Bloco com a escolha da representação das incertezas,
    existente no arquivo `dger.dat` do NEWAVE.
    """

    str_inicio = "REPRESENTACAO INCERT"
    str_fim = "(=1 HISTORICO, =2 PARAMETROS DA DISTRIBUICAO, =3 CENARIOS)"

    def __init__(self):

        super().__init__(BlocoRepresentacaoIncerteza.str_inicio,
                         BlocoRepresentacaoIncerteza.str_fim,
                         True)

        self._dados = 0

    # Override
    def le(self, arq: IO):
        reg = RegistroIn(4)
        self._dados = reg.le_registro(self._linha_inicio, 21)

    # Override
    def escreve(self, arq: IO):
        dado = str(self._dados).rjust(4)
        linha = (f"{BlocoRepresentacaoIncerteza.str_inicio.ljust(21)}" +
                 f"{dado}   {BlocoRepresentacaoIncerteza.str_fim}\n")
        arq.write(linha)


class LeituraDGer(Leitura):
    """
    Realiza a leitura do arquivo dger.dat
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo dger.dat, construindo
    um objeto `DGer` cujas informações são as mesmas do dger.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    """
    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [
                BlocoNomeCaso(),
                BlocoTipoExecucao(),
                BlocoDuracaoPeriodo(),
                BlocoNumAnosEstudo(),
                BlocoMesInicioPreEstudo(),
                BlocoMesInicioEstudo(),
                BlocoAnoInicioEstudo(),
                BlocoNumAnosPreEstudo(),
                BlocoNumAnosPosEstudo(),
                BlocoNumAnosPosEstudoSimFinal(),
                BlocoImprimeDados(),
                BlocoImprimeMercados(),
                BlocoImprimeEnergias(),
                BlocoImprimeModeloEstocastico(),
                BlocoImprimeSubsistema(),
                BlocoNumMaxIteracoes(),
                BlocoNumForwards(),
                BlocoNumAberturas(),
                BlocoNumSeriesSinteticas(),
                BlocoOrdemMaximaPARp(),
                BlocoAnoInicialHistorico(),
                BlocoCalculaVolInicial(),
                BlocoVolInicialSubsistema(),
                BlocoTolerancia(),
                BlocoTaxaDesconto(),
                BlocoTipoSimFinal(),
                BlocoImpressaoOperacao(),
                BlocoImpressaoConvergencia(),
                BlocoIntervaloGravar(),
                BlocoMinIteracoes(),
                BlocoRacionamentoPreventivo(),
                BlocoNumAnosManutUTE(),
                BlocoTendenciaHidrologica(),
                BlocoRestricaoItaipu(),
                BlocoBid(),
                BlocoPerdasTransmissao(),
                BlocoElNino(),
                BlocoEnso(),
                BlocoDuracaoPorPatamar(),
                BlocoOutrosUsosAgua(),
                BlocoCorrecaoDesvio(),
                BlocoCurvaAversao(),
                BlocoTipoGeracaoENA(),
                BlocoRiscoDeficit(),
                BlocoIteracaoParaSimFinal(),
                BlocoAgrupamentoLivre(),
                BlocoEqualizacaoPenalInt(),
                BlocoRepresentacaoSubmot(),
                BlocoOrdenacaoAutomatica(),
                BlocoConsideraCargaAdicional(),
                BlocoDeltaZSUP(),
                BlocoDeltaZINF(),
                BlocoDeltasConsecutivos(),
                BlocoDespachoAntecipadoGNL(),
                BlocoModifAutomaticaAdTerm(),
                BlocoGeracaoHidraulicaMin(),
                BlocoSimFinalComData(),
                BlocoGerenciamentoPLs(),
                BlocoSAR(),
                BlocoCVAR(),
                BlocoZSUPMinConvergencia(),
                BlocoDesconsideraVazaoMinima(),
                BlocoRestricoesEletricas(),
                BlocoSelecaoCortes(),
                BlocoJanelaCortes(),
                BlocoReamostragemCenarios(),
                BlocoConvergeNoZero(),
                BlocoConsultaFCF(),
                BlocoImpressaoENA(),
                BlocoImpressaoCortesAtivosSimFinal(),
                BlocoRepresentacaoAgregacao(),
                BlocoMatrizCorrelacaoEspacial(),
                BlocoDesconsideraConvEstatistica(),
                BlocoMomentoReamostragem(),
                BlocoMantemArquivosEnergias(),
                BlocoInicioTesteConvergencia(),
                BlocoSazonalizarVminT(),
                BlocoSazonalizarVmaxT(),
                BlocoSazonalizarVminP(),
                BlocoSazonalizarCfugaCmont(),
                BlocoRestricoesEmissaoGEE(),
                BlocoAfluenciaAnualPARp(),
                BlocoRestricoesFornecGas(),
                BlocoIncertezaGeracaoEolica(),
                BlocoIncertezaGeracaoSolar(),
                BlocoRepresentacaoIncerteza()
               ]
