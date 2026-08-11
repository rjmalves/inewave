"""
Gerador de mocks binários para os arquivos de cortes (`cortes.dat` /
`cortes-<estagio>.dat`) e de estados (`cortese.dat` / `cortese-<estagio>.dat`).

Reproduz, com dimensões minúsculas, o layout binário validado contra um caso
real do NEWAVE (verificado byte a byte com `nwlistcf.rel`/`estados.rel`):

- registro de corte::

      int32[4]   = [indice_proximo, iteracao_construcao,
                    indice_forward, iteracao_desativacao]
      float64[n] = rhs · PIGTAD(G) · reservado(1) · PIVARM(U) ·
                   PIAFL(U·P) · PIMX_SAR(U)            (individualizado)
      float64[n] = rhs · PIEARM(R) · PIH(R·P) · PIGTAD(G) ·
                   reservado(1) · PIMX_SAR(R)          (agregado em REE)

- partição por estágio: ``N`` cortes reais (lista ligada ``rec_k.next = k-1``,
  ``rec_1.next = 0``) seguidos de UM registro sentinela (``rhs == 0``).

- registro de estado::

      int32[3]   = [iteracao_construcao, indice_forward, iteracao_desativacao]
      float64[m] = funcao_objetivo · EARM(R) · VARM(U) · SGT(...) · reservado
"""

from typing import List
import struct


def _pack_registro_corte(
    indice_proximo: int,
    iteracao_construcao: int,
    indice_forward: int,
    iteracao_desativacao: int,
    coeficientes: List[float],
) -> bytes:
    cabecalho = struct.pack(
        "<4i",
        indice_proximo,
        iteracao_construcao,
        indice_forward,
        iteracao_desativacao,
    )
    corpo = struct.pack(f"<{len(coeficientes)}d", *coeficientes)
    return cabecalho + corpo


def coeficientes_individualizado(
    rhs: float,
    gnl: List[float],
    varm: List[float],
    qafl: List[float],
    mx_sar: List[float],
) -> List[float]:
    """
    Monta o vetor físico de coeficientes de um corte individualizado:
    ``rhs · PIGTAD(G) · reservado(1, =0.0) · PIVARM(U) · PIAFL(U·P) · PIMX_SAR(U)``.
    """
    return [rhs] + list(gnl) + [0.0] + list(varm) + list(qafl) + list(mx_sar)


def coeficientes_individualizado_hibrido(
    rhs: float,
    gnl: List[float],
    varm: List[float],
    qafl: List[float],
    extra: List[float],
    mx_sar: List[float],
) -> List[float]:
    """
    Como :func:`coeficientes_individualizado`, mas com um bloco ``extra`` de
    coeficientes não-nomeados entre ``PIAFL`` e ``PIMX_SAR`` — reproduz o layout
    híbrido observado em campo, em que ``PIMX_SAR`` permanece o ÚLTIMO bloco do
    registro e o leitor o ancora pelo fim (o bloco ``extra`` fica sem
    mapeamento, sem desalinhar ``PIMX_SAR``).
    """
    return (
        [rhs]
        + list(gnl)
        + [0.0]
        + list(varm)
        + list(qafl)
        + list(extra)
        + list(mx_sar)
    )


def coeficientes_ree(
    rhs: float,
    earm: List[float],
    ena: List[float],
    gnl: List[float],
) -> List[float]:
    """
    Monta o vetor físico de um corte agregado em REE (front, sem cauda):
    ``rhs · PIEARM(R) · PIH(R·P) · PIGTAD(G)``.
    """
    return [rhs] + list(earm) + list(ena) + list(gnl)


def coeficientes_ree_completo(
    rhs: float,
    earm: List[float],
    ena: List[float],
    gnl: List[float],
    mx_sar: List[float],
) -> List[float]:
    """
    Layout REE completo (validado contra `nwlistcf.rel`, estágio agregado):
    ``rhs · PIEARM(R) · PIH(R·P) · PIGTAD(G) · reservado(1, =0.0) · PIMX_SAR(R)``.
    """
    return [rhs] + list(earm) + list(ena) + list(gnl) + [0.0] + list(mx_sar)


def gera_particao_cortes(
    registros: List[List[float]],
    tamanho_registro: int,
    com_sentinela: bool = True,
) -> bytes:
    """
    Gera o conteúdo binário de uma partição de cortes a partir dos vetores de
    coeficientes ``registros`` (do mais antigo para o mais novo). Encadeia a
    lista ligada de trás para frente (``rec_1.next = 0``) e acrescenta o
    registro sentinela final quando ``com_sentinela``.
    """
    n = len(registros)
    conteudo = b""
    for k, coefs in enumerate(registros, start=1):
        if len(coefs) * 8 + 16 != tamanho_registro:
            raise ValueError(
                f"registro {k} com {len(coefs)} coeficientes não casa com "
                f"tamanho_registro {tamanho_registro}."
            )
        conteudo += _pack_registro_corte(
            indice_proximo=k - 1,  # aponta para o corte anterior (0 encerra)
            iteracao_construcao=((k - 1) // 1) + 1,
            indice_forward=k,
            iteracao_desativacao=0,
            coeficientes=coefs,
        )
    if com_sentinela:
        sentinela = [0.0] * (len(registros[0]) if registros else 0)
        conteudo += _pack_registro_corte(
            indice_proximo=1,
            iteracao_construcao=2024,
            indice_forward=n,
            iteracao_desativacao=2024,
            coeficientes=sentinela,
        )
    return conteudo


def gera_consolidado_cortes(
    registros: List[List[float]],
    tamanho_registro: int,
) -> bytes:
    """Consolidado: mesmos cortes, sem sentinela (índices globais)."""
    return gera_particao_cortes(
        registros, tamanho_registro, com_sentinela=False
    )


def estado(
    funcao_objetivo: float,
    earm: List[float],
    varm: List[float],
    sgt: List[float],
    reservado: List[float],
) -> List[float]:
    """Monta o vetor físico de um estado: funcobj · EARM · VARM · SGT · reservado."""
    return (
        [funcao_objetivo]
        + list(earm)
        + list(varm)
        + list(sgt)
        + list(reservado)
    )


def gera_estados(
    estados: List[List[float]],
    iteracoes: List[tuple],
    tamanho_estado: int,
) -> bytes:
    """
    Gera o conteúdo binário de um arquivo de estados (sem sentinela). Cada
    entrada de ``iteracoes`` é ``(iteracao_construcao, indice_forward,
    iteracao_desativacao)``.
    """
    conteudo = b""
    for coefs, (itc, fwd, itd) in zip(estados, iteracoes):
        if len(coefs) * 8 + 12 != tamanho_estado:
            raise ValueError(
                f"estado com {len(coefs)} valores não casa com tamanho_estado "
                f"{tamanho_estado}."
            )
        conteudo += struct.pack("<3i", itc, fwd, itd)
        conteudo += struct.pack(f"<{len(coefs)}d", *coefs)
    return conteudo
