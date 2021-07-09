from inewave.newave.modelos.patamar import BlocoDuracaoPatamar
from inewave.newave.modelos.patamar import LeituraPatamar
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.arquivo import Arquivo
from inewave._utils.escrita import Escrita
from inewave.config import NUM_PATAMARES

from typing import Dict
import numpy as np  # type: ignore


class Patamar(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    patamares de carga por submercado.

    Esta classe pode lidar com um número qualquer de patamares
    de carga, desde que as informações fornecidas a ela por meio
    da tabela de valores seja compatível com o parâmetro `num_patamares`
    da mesma.

    A tabela de patamares de carga é armazenada através de uma array
    em `NumPy`, para otimizar cálculos futuros e espaço ocupado
    em memória. A tabela interna é transformada em dicionários
    e outras estruturas de dados mais palpáveis através das propriedades
    da própria classe.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)
        # Interpreta o resultado da leitura
        val = True
        msg = "Erro na criação de Patamar: "
        if len(dados.blocos) == 1:
            bloco = dados.blocos[0]
            if isinstance(bloco, BlocoDuracaoPatamar):
                self.__bloco = bloco
            else:
                msg += (f"O bloco deve ser do tipo {BlocoDuracaoPatamar}, " +
                        f"mas foi fornecido do tipo {type(bloco)}")
                val = False
        else:
            msg += "Deve ser fornecido exatamente 1 bloco para Patamar"
            val = False
        if not val:
            raise TypeError(msg)

    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="patamar.dat") -> 'Patamar':
        """
        """
        leitor = LeituraPatamar(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="patamar.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

    @property
    def anos_estudo(self) -> np.ndarray:
        """
        Valores não-nulos da primeira coluna da tabela de duração
         mensal dos patamares, que contém os anos de estudo.

        **Retorna**

        `np.ndarray`

        **Sobre**

        """
        primeira_col = self.__bloco.dados[:, 0]
        return np.array(primeira_col[primeira_col > 0],
                        dtype=np.int64)

    @anos_estudo.setter
    def anos_estudo(self, anos: np.ndarray):
        anos_espacados: np.ndarray = np.zeros((self.__bloco.dados.shape[0],),
                                              dtype=np.float64)
        if anos_espacados.shape[0] > self.__bloco.dados.shape[0]:
            raise ValueError("Número de anos de estudo muito grande!")
        anos_espacados[::NUM_PATAMARES] = anos
        self.__bloco.dados[:, 0] = anos_espacados

    @property
    def patamares_por_ano(self) -> Dict[int, np.ndarray]:
        """
        Valores contidos na tabela de patamares, organizados
        por ano.

        **Retorna**

        `Dict[int, np.ndarray]`

        **Sobre**

        O acesso é feito com [ano] e o valor fornecido
        é uma array 2-D do `NumPy` com os valores dos patamares para todo
        os meses de um ano, semelhante a uma linha do arquivo patamar.dat.
        """
        patamares_ano: Dict[int, np.ndarray] = {}
        # Preenche com os valores
        for i, a in enumerate(self.anos_estudo):
            li = NUM_PATAMARES * i
            lf = li + NUM_PATAMARES
            patamares_ano[a] = self.__bloco.dados[li:lf, 1:]
        return patamares_ano
