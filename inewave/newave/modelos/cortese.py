from cfinterface.components.section import Section
from typing import Any, IO, List
import numpy as np
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package


class SecaoDadosCortese(Section):
    """
    Registro com os estados visitados que geraram os cortes da FCF, presente
    nos arquivos `cortese.dat` (consolidado) e `cortese-<estagio>.dat`
    (particionado por estágio). É o par binário do relatório textual
    `estados.rel`.

    Cada estado ocupa ``tamanho_estado`` bytes::

        int32[3]   = [iteracao_construcao, indice_forward, iteracao_desativacao]
        float64[n] = [funcao_objetivo, estados...]  com n = (tamanho_estado - 12) / 8

    O bloco de estados (individualizado) é::

        funcao_objetivo · EARM(R) · VARM(U) · SGT(St · Pat · E) · [reservado]

    com ``R = numero_rees``, ``U = n_uhes``, ``St = numero_total_submercados``,
    ``Pat = numero_patamares`` e ``E = lag_maximo_gnl + 1`` (bloco SGT ausente
    quando ``lag_maximo_gnl == 0``). VARM está na mesma ordem de
    ``cortesh.dados_uhes``.

    Diferente dos cortes, os estados NÃO formam lista ligada: os registros
    estão em ordem física (um por corte, mesmo índice global) e os arquivos
    particionados NÃO possuem registro sentinela.
    """

    __slots__ = [
        "__numero_estados",
        "__numero_rees",
        "__codigos_uhes",
        "__numero_total_submercados",
        "__numero_patamares",
        "__lag_maximo_gnl",
        "__estados_termicos_gnl",
    ]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SecaoDadosCortese):
            return False
        bloco: SecaoDadosCortese = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(bloco.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    @staticmethod
    def __tamanho_arquivo(file: IO[Any]) -> int:
        posicao_atual = file.tell()
        file.seek(0, 2)
        tamanho = file.tell()
        file.seek(posicao_atual)
        return tamanho

    def __colunas(self) -> List[str]:
        cols = ["funcao_objetivo"]
        cols += [f"earm_ree{r}" for r in range(1, self.__numero_rees + 1)]
        cols += [f"varm_uhe{u}" for u in self.__codigos_uhes]
        bloco_termico = self.__tamanho_bloco_termico()
        if bloco_termico > 0:
            cols += [
                f"sgt_sbm{s}_pat{p}_est{e}"
                for s in range(1, self.__numero_total_submercados + 1)
                for p in range(1, self.__numero_patamares + 1)
                for e in range(1, self.__estados_termicos_gnl + 1)
            ]
        mapeados = 1 + self.__numero_rees + len(self.__codigos_uhes)
        mapeados += bloco_termico
        reservados = self.__numero_estados - mapeados
        cols += [f"reservado_{i}" for i in range(reservados)]
        return cols

    def __tamanho_bloco_termico(self) -> int:
        if self.__lag_maximo_gnl <= 0:
            return 0
        bloco = (
            self.__numero_total_submercados
            * self.__numero_patamares
            * self.__estados_termicos_gnl
        )
        mapeados_sem_termico = 1 + self.__numero_rees + len(self.__codigos_uhes)
        if mapeados_sem_termico + bloco > self.__numero_estados:
            return 0
        return bloco

    def read(  # type: ignore[override]  # signature extends base class
        self,
        file: IO[Any],
        tamanho_estado: int,
        numero_rees: int = 0,
        codigos_uhes: List[int] = [],
        numero_total_submercados: int = 0,
        numero_patamares: int = 3,
        lag_maximo_gnl: int = 0,
        estados_termicos_gnl: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.__numero_rees = numero_rees
        self.__codigos_uhes = codigos_uhes
        self.__numero_total_submercados = numero_total_submercados
        self.__numero_patamares = numero_patamares
        self.__lag_maximo_gnl = lag_maximo_gnl
        self.__estados_termicos_gnl = (
            estados_termicos_gnl
            if estados_termicos_gnl > 0
            else lag_maximo_gnl + 1
        )

        if tamanho_estado <= 12:
            raise ValueError(
                f"tamanho_estado inválido ({tamanho_estado}); deve ser maior "
                "que 12 (3 inteiros de cabeçalho)."
            )
        tamanho_arquivo = self.__tamanho_arquivo(file)
        if tamanho_arquivo % tamanho_estado != 0:
            raise ValueError(
                f"Arquivo de estados inconsistente: tamanho {tamanho_arquivo} "
                f"não é múltiplo de tamanho_estado {tamanho_estado}."
            )
        numero_registros = tamanho_arquivo // tamanho_estado
        self.__numero_estados = (tamanho_estado - 12) // 8

        tabela_int = np.zeros((numero_registros, 3), dtype=np.int32)
        tabela_float = np.zeros(
            (numero_registros, self.__numero_estados), dtype=np.float64
        )
        for i in range(numero_registros):
            file.seek(i * tamanho_estado)
            tabela_int[i, :] = np.frombuffer(
                file.read(3 * 4), dtype=np.int32, count=3
            )
            tabela_float[i, :] = np.frombuffer(
                file.read(self.__numero_estados * 8),
                dtype=np.float64,
                count=self.__numero_estados,
            )

        df_int = pd.DataFrame(
            tabela_int,
            columns=[
                "iteracao_construcao",
                "indice_forward",
                "iteracao_desativacao",
            ],
        )
        df_float = pd.DataFrame(tabela_float, columns=self.__colunas())
        self.data = pd.concat([df_int, df_float], axis=1)
