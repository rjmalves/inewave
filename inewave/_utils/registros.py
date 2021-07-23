from abc import abstractmethod
from typing import Any, List


class Registro:
    """
    Classe geral que modela os registros existentes
    nos arquivos do modelo NEWAVE.
    """
    def __init__(self, tamanho: int):
        self.tamanho = tamanho

    @abstractmethod
    def le_registro(self,
                    linha: str,
                    coluna_inicio: int) -> Any:
        """
        Função genérica para leitura de um valor de registro
        em uma linha de um arquivo.
        """
        pass

    @abstractmethod
    def le_linha_tabela(self,
                        linha: str,
                        coluna_inicio: int,
                        num_espacos: int,
                        num_colunas: int) -> List[Any]:
        """
        Função genérica para leitura de uma linha de uma
        tabela com vários registros iguais.
        """
        pass


class RegistroAn(Registro):
    """
    Registro de strings existente nos arquivos do NEWAVE.
    """
    def __init__(self, tamanho: int):
        super().__init__(tamanho)

    def le_registro(self, linha: str, coluna_inicio: int) -> str:
        """
        Lê o conteúdo de uma string existente numa linha de um arquivo
        do NEWAVE e retorna o valor sem espaços adicionais.
        """
        return linha[coluna_inicio:coluna_inicio+self.tamanho].strip()

    def le_linha_tabela(self,
                        linha: str,
                        coluna_inicio: int,
                        num_espacos: int,
                        num_colunas: int) -> List[str]:
        """
        Lê o conteúdo de uma linha de tabela com strings.
        """
        lista_valores: List[str] = []
        # Gera a lista com as colunas de início de cada valor
        colunas_inicio = [coluna_inicio + i * (self.tamanho + num_espacos)
                          for i in range(num_colunas)]
        for col in colunas_inicio:
            lista_valores.append(self.le_registro(linha,
                                                  col))
        return lista_valores


class RegistroIn(Registro):
    """
    Registro de números inteiros existente nos arquivos do NEWAVE.
    """
    def __init__(self, tamanho: int):
        super().__init__(tamanho)

    def le_registro(self, linha: str, coluna_inicio: int) -> int:
        """
        Lê o conteúdo de um inteiro existente numa linha de um arquivo
        do NEWAVE e retorna o valor já convertido.
        """
        return int(linha[coluna_inicio:coluna_inicio+self.tamanho].strip())

    def le_linha_tabela(self,
                        linha: str,
                        coluna_inicio: int,
                        num_espacos: int,
                        num_colunas: int) -> List[int]:
        """
        Lê o conteúdo de uma linha de tabela com inteiros.
        """
        lista_valores: List[int] = []
        # Gera a lista com as colunas de início de cada valor
        colunas_inicio = [coluna_inicio + i * (self.tamanho + num_espacos)
                          for i in range(num_colunas)]
        for col in colunas_inicio:
            valor = self.le_registro(linha, col)
            if valor is None:
                break
            lista_valores.append(valor)
        return lista_valores


class RegistroFn(Registro):
    """
    Registro de números reais existente nos arquivos do NEWAVE.
    """
    def __init__(self, tamanho: int):
        super().__init__(tamanho)

    def le_registro(self, linha: str, coluna_inicio: int) -> float:
        """
        Lê o conteúdo de um número existente numa linha de um arquivo
        do NEWAVE e retorna o valor já convertido.
        """
        return float(linha[coluna_inicio:coluna_inicio+self.tamanho])

    def le_linha_tabela(self,
                        linha: str,
                        coluna_inicio: int,
                        num_espacos: int,
                        num_colunas: int) -> List[float]:
        """
        Lê o conteúdo de uma linha de tabela com valores reais.
        """
        lista_valores: List[float] = []
        # Gera a lista com as colunas de início de cada valor
        colunas_inicio = [coluna_inicio + i * (self.tamanho + num_espacos)
                          for i in range(num_colunas)]
        for col in colunas_inicio:
            lista_valores.append(self.le_registro(linha,
                                                  col))
        return lista_valores
