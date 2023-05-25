from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.forward import SecaoDadosForward


from typing import TypeVar, Optional, Union, List

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Forward(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às simulações
    forward.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosForward]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def read(
        cls,
        content: Union[str, bytes],
        tamanho_registro: int = 41264,
        numero_estagios: int = 60,
        numero_forwards: int = 200,
        numero_rees: int = 12,
        numero_submercados: int = 4,
        numero_total_submercados: int = 5,
        numero_patamares_carga: int = 3,
        numero_patamares_deficit: int = 1,
        numero_agrupamentos_intercambio: int = 1,
        numero_classes_termicas_submercados: List[int] = [],
        numero_usinas_hidreletricas: int = 164,
        lag_maximo_usinas_gnl: int = 2,
        numero_parques_eolicos_equivalentes: int = 2,
        numero_estacoes_bombeamento: int = 0,
        *args,
        **kwargs
    ) -> "Forward":
        return super().read(
            content,
            tamanho_registro=tamanho_registro,
            numero_estagios=numero_estagios,
            numero_forwards=numero_forwards,
            numero_rees=numero_rees,
            numero_submercados=numero_submercados,
            numero_total_submercados=numero_total_submercados,
            numero_patamares_carga=numero_patamares_carga,
            numero_patamares_deficit=numero_patamares_deficit,
            numero_agrupamentos_intercambio=numero_agrupamentos_intercambio,
            numero_classes_termicas_submercados=numero_classes_termicas_submercados,
            numero_usinas_hidreletricas=numero_usinas_hidreletricas,
            lag_maximo_usinas_gnl=lag_maximo_usinas_gnl,
            numero_parques_eolicos_equivalentes=numero_parques_eolicos_equivalentes,
            numero_estacoes_bombeamento=numero_estacoes_bombeamento,
            *args,
            **kwargs
        )

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="forward.dat"
    ) -> "Forward":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="forward.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def dados(self) -> Optional[SecaoDadosForward]:
        dados = [r for r in self.data.of_type(SecaoDadosForward)]
        if len(dados) == 1:
            return dados[0]
        else:
            return None
