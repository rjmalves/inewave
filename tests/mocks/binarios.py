"""
Utilitários para ler mocks binários versionados comprimidos (`.gz`).

Vários mocks binários do NEWAVE (cabeçalhos, cortes, energias, vazões...) são
majoritariamente preenchidos com zeros e comprimem centenas de vezes. Para
manter o repositório enxuto, são versionados como ``X.dat.gz`` e descomprimidos
em memória nos testes — os leitores aceitam tanto ``bytes`` quanto um objeto de
arquivo binário.
"""

import gzip
from io import BytesIO


def bytes_gz(caminho_dat: str) -> bytes:
    """
    Lê o conteúdo de um mock binário ``caminho_dat`` a partir do arquivo
    comprimido ``caminho_dat + '.gz'``. Use com ``Classe.read(bytes_gz(ARQ))``.
    """
    with gzip.open(f"{caminho_dat}.gz", "rb") as fp:
        return fp.read()


def fp_gz(caminho_dat: str) -> BytesIO:
    """
    Retorna um objeto de arquivo binário (``BytesIO``) com o conteúdo
    descomprimido de ``caminho_dat + '.gz'``. Use no lugar de
    ``open(ARQ, 'rb')`` para leituras via ``Secao().read(fp, storage='BINARY')``.
    """
    return BytesIO(bytes_gz(caminho_dat))
