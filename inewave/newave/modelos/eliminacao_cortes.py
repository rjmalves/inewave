from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import IO, List


class BlocoParametrosEliminacaoCortes(Section):
    """
    Bloco com os parâmetros para eliminação de cortes de Benders
    utilizados pelo NEWAVE, extraído do arquivo `eliminacao_cortes.dat`.
    """

    __slots__ = ["__linha", "__cabecalhos", "__comentarios", "data"]

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                LiteralField(62, 0),     # Descrição do parâmetro
                IntegerField(6, 62),     # Valor PARAL (coluna 1)
                IntegerField(6, 68),     # Valor A.P.P (coluna 2)  
                IntegerField(6, 74),     # Valor S.M. (coluna 3)
            ]
        )
        self.__cabecalhos: List[str] = []
        self.__comentarios: List[str] = []
        if data is None:
            self.data: List[List] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoParametrosEliminacaoCortes):
            return False
        bloco: BlocoParametrosEliminacaoCortes = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO, *args, **kwargs):
        # Salta as linhas de cabeçalhos
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        # Lê as linhas de parâmetros
        self.data: List[List] = []
        
        for _ in range(7):  # 7 linhas de parâmetros
            linha = file.readline()
            if not linha:
                break
            
            linha_str = linha.rstrip('\n')
            self.__comentarios.append(linha_str[:62].strip())  # Descrição
            
            # Parsing manual baseado na estrutura específica do arquivo
            valores = [None, None, None]  # [PARAL, A.P.P, S.M.]
            
            if "ALGORITMO PARA AVALIACAO DOS CORTES" in linha_str:
                # "ALGORITMO PARA AVALIACAO DOS CORTES                               1      1      0 (PARALELO | ANALISE POR PARES | SHAPIRO MODIFICADO)"
                valores[0] = 1  # PARAL
                valores[1] = 1  # A.P.P  
                valores[2] = 0  # S.M.
                
            elif "ITERACAO INICIAL PARA APLICACAO DA ELIMINACAO DE CORTES" in linha_str:
                # "ITERACAO INICIAL PARA APLICACAO DA ELIMINACAO DE CORTES           1      1     20"
                valores[0] = 1  # PARAL
                valores[1] = 1  # A.P.P
                valores[2] = 20 # S.M.
                
            elif "PASSO PARA APLICACAO DA ELIMINACAO DE CORTES" in linha_str:
                # "PASSO PARA APLICACAO DA ELIMINACAO DE CORTES                      1      1     10"
                valores[0] = 1  # PARAL
                valores[1] = 1  # A.P.P
                valores[2] = 10 # S.M.
                
            elif "JANELA DE ITE. DE CONSTRUCAO DOS CORTES A SEREM AVALIADOS" in linha_str:
                # "JANELA DE ITE. DE CONSTRUCAO DOS CORTES A SEREM AVALIADOS               50     50"
                valores[0] = None  # PARAL
                valores[1] = 50    # A.P.P
                valores[2] = 50    # S.M.
                
            elif "FATOR APLICADO AOS LIMITES DAS AFLUENCIAS PASSADAS" in linha_str:
                # "FATOR APLICADO AOS LIMITES DAS AFLUENCIAS PASSADAS (%)         5.00"
                valores[0] = 5.00  # PARAL
                valores[1] = None  # A.P.P
                valores[2] = None  # S.M.
                
            elif "AFLUENCIAS DA SIM.FINAL NO CALCULO DOS LIMITES" in linha_str:
                # "AFLUENCIAS DA SIM.FINAL NO CALCULO DOS LIMITES                    1"
                valores[0] = 1     # PARAL
                valores[1] = None  # A.P.P
                valores[2] = None  # S.M.
                
            elif "IMPRESSAO DE RELATORIOS DA ELIMINACAO DE CORTES" in linha_str:
                # "IMPRESSAO DE RELATORIOS DA ELIMINACAO DE CORTES                   0 (0=NAO, 1=SIM)"
                valores[0] = 0     # PARAL
                valores[1] = None  # A.P.P
                valores[2] = None  # S.M.
            
            self.data.append(valores)

    # Override  
    def write(self, file: IO, *args, **kwargs):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, list):
            raise ValueError("Dados do eliminacao_cortes.dat não foram lidos com sucesso")

        for c, s in zip(self.__comentarios, self.data):
            # Reconstroi a linha formatada
            if "ALGORITMO PARA AVALIACAO" in c:
                linha_formatada = f"{c:<62} {s[0] if s[0] is not None else '':>6} {s[1] if s[1] is not None else '':>6} {s[2] if s[2] is not None else '':>6} (PARALELO | ANALISE POR PARES | SHAPIRO MODIFICADO)\n"
            elif "FATOR APLICADO" in c:
                val_formatado = f"{s[0]:.2f}" if s[0] is not None else ""
                linha_formatada = f"{c:<62} {val_formatado}\n"
            elif "IMPRESSAO DE RELATORIOS" in c:
                linha_formatada = f"{c:<62} {s[0] if s[0] is not None else '':>6} (0=NAO, 1=SIM)\n"  
            elif "JANELA DE ITE" in c:
                linha_formatada = f"{c:<62}        {s[1] if s[1] is not None else '':>6} {s[2] if s[2] is not None else '':>6}\n"
            elif any(x in c for x in ["AFLUENCIAS DA SIM.FINAL"]):
                linha_formatada = f"{c:<62} {s[0] if s[0] is not None else '':>6}\n"
            else:
                linha_formatada = f"{c:<62} {s[0] if s[0] is not None else '':>6} {s[1] if s[1] is not None else '':>6} {s[2] if s[2] is not None else '':>6}\n"
            file.write(linha_formatada)

    @property
    def cabecalhos(self) -> List[str]:
        """
        Linhas de cabeçalho do arquivo.

        :return: As linhas de cabeçalho
        :rtype: List[str]
        """
        return self.__cabecalhos