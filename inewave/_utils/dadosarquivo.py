from inewave._utils.blocobinario import BlocoBinario
from .registronewave import RegistroNEWAVE
from .bloco import Bloco
from typing import Dict, List, TypeVar, Type


class DadosArquivoBlocos:
    """ """

    def __init__(
        self, blocos: List[Bloco], linhas_fora_blocos: Dict[int, str]
    ) -> None:
        self.__blocos = blocos
        self.__linhas_fora_blocos = linhas_fora_blocos
        pass

    @property
    def blocos(self) -> List[Bloco]:
        return self.__blocos

    @property
    def linhas_fora_blocos(self) -> Dict[int, str]:
        return self.__linhas_fora_blocos


class DadosArquivoRegistros:
    """ """

    T = TypeVar("T")

    def __init__(
        self,
        registros: List[RegistroNEWAVE],
        linhas_fora_registros: Dict[float, str],
    ) -> None:
        self.__registros = registros
        self.__linhas_fora_registros = linhas_fora_registros
        pass

    @property
    def registros(self) -> List[RegistroNEWAVE]:
        return self.__registros

    @property
    def linhas_fora_registros(self) -> Dict[float, str]:
        return self.__linhas_fora_registros

    def cria_registro(
        self, anterior: RegistroNEWAVE, registro: RegistroNEWAVE
    ) -> RegistroNEWAVE:
        # Obtém a ordem do registro anterior
        ant = anterior._ordem
        # Procura dentre linhas e registros a ordem do próximo
        ordens_linhas = list(self.linhas_fora_registros.keys())
        ordens_linhas.sort()
        ordens_linhas = [o for o in ordens_linhas if o > ant]
        prox_linha = ant + 1 if len(ordens_linhas) == 0 else ordens_linhas[0]
        ordens_registros = [r._ordem for r in self.registros]
        ordens_registros.sort()
        ordens_registros = [o for o in ordens_registros if o > ant]
        prox_registro = (
            ant + 1 if len(ordens_registros) == 0 else ordens_registros[0]
        )
        prox = min([prox_linha, prox_registro])
        ordem_novo = (prox + ant) / 2.0
        registro._ordem = ordem_novo
        self.registros.append(registro)
        return registro

    def deleta_registro(self, registro: RegistroNEWAVE) -> bool:
        try:
            self.registros.remove(registro)
            return True
        except ValueError:
            return False

    def lista_registros(self, tipo: Type[T]) -> List[T]:
        registros_tipo: list = []
        for r in self.registros:
            if isinstance(r, tipo):
                registros_tipo.append(r)
        return registros_tipo


class DadosArquivoBinarios:
    """ """

    def __init__(self, blocos: List[BlocoBinario]) -> None:
        self.__blocos = blocos

    @property
    def blocos(self) -> List[BlocoBinario]:
        return self.__blocos
