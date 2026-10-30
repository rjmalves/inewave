# Rotinas de testes da base comum das tabelas MEDIAS-*.CSV do NWLISTOP
import io
from typing import List, Optional, Type

import pytest
from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.mediasmerc import Mediasmerc
from inewave.nwlistop.mediasree import Mediasree
from inewave.nwlistop.mediasrep import Mediasrep
from inewave.nwlistop.mediasrhq import Mediasrhq
from inewave.nwlistop.mediasrhv import Mediasrhv
from inewave.nwlistop.mediassin import Mediassin
from inewave.nwlistop.mediasusie import Mediasusie
from inewave.nwlistop.mediasusih import Mediasusih
from inewave.nwlistop.mediasusit import Mediasusit
from inewave.nwlistop.modelos.mediasmerc import TabelaMediasmerc
from inewave.nwlistop.modelos.mediassin import TabelaMediassin


@pytest.mark.parametrize(
    "classe, arquivo, entidade, primeiro_mes",
    [
        (Mediasmerc, "MEDIAS-MERC.CSV", "codigo_submercado", 4),
        (Mediasree, "MEDIAS-REE.CSV", "codigo_ree", 1),
        (Mediasrep, "MEDIAS-REP.CSV", "codigo_restricao", None),
        (Mediasrhq, "MEDIAS-RHQ.CSV", "codigo_restricao", None),
        (Mediasrhv, "MEDIAS-RHV.CSV", "codigo_restricao", None),
        (Mediassin, "MEDIAS-SIN.CSV", None, 4),
        (Mediasusie, "MEDIAS-USIE.CSV", "codigo_usina", None),
        (Mediasusih, "MEDIAS-USIH.CSV", "codigo_usina", 1),
        (Mediasusih, "MEDIAS-USIH-2.CSV", "codigo_usina", 4),
        (Mediasusit, "MEDIAS-USIT.CSV", "codigo_usina", 1),
    ],
)
def test_indice_mes_guarda_o_estagio_do_arquivo(
    classe: Type[SectionFile],
    arquivo: str,
    entidade: Optional[str],
    primeiro_mes: Optional[int],
):
    valores = classe.read(f"tests/_arquivos/{arquivo}").valores
    esperadas: List[str] = ["estagio", "indice_mes"]
    if entidade is not None:
        esperadas.append(entidade)
    assert valores.columns.tolist()[: len(esperadas)] == esperadas
    if primeiro_mes is None:
        assert valores.empty
        return
    assert valores["estagio"].min() == 1
    assert valores["indice_mes"].min() == primeiro_mes
    deslocamento = valores["indice_mes"] - valores["estagio"]
    assert (deslocamento == primeiro_mes - 1).all()


CSV_MERC = (
    "    SBM_ext, VAR,        9,       10,\n"
    "   1,      EARMF,  10.00,  11.00,\n"
    "   2,      EARMF,  20.00,  21.00,\n"
    "  99,      EARMF,  30.00,  31.00,\n"
    "   0,      EARMF,  99.00,  99.00,\n"
)


def test_tabela_com_entidade_descarta_codigos_nao_positivos():
    tabela = TabelaMediasmerc()
    tabela.read(io.StringIO(CSV_MERC))
    df = tabela.data
    assert df.columns.tolist() == [
        "estagio",
        "indice_mes",
        "codigo_submercado",
        "EARMF",
    ]
    assert df["estagio"].tolist() == [1, 1, 1, 2, 2, 2]
    assert df["indice_mes"].tolist() == [9, 9, 9, 10, 10, 10]
    assert df["codigo_submercado"].tolist() == [1, 2, 99, 1, 2, 99]
    assert df["EARMF"].tolist() == [10.0, 20.0, 30.0, 11.0, 21.0, 31.0]


def test_tabela_sem_virgula_final_mantem_o_ultimo_estagio():
    tabela = TabelaMediasmerc()
    tabela.read(
        io.StringIO(
            "    SBM_ext, VAR,        9,       10\n"
            "   1,      EARMF,  10.00,  11.00\n"
            "   2,      EARMF,  20.00,  21.00\n"
        )
    )
    df = tabela.data
    assert df["indice_mes"].tolist() == [9, 9, 10, 10]
    assert df["codigo_submercado"].tolist() == [1, 2, 1, 2]
    assert df["EARMF"].tolist() == [10.0, 20.0, 11.0, 21.0]


def test_tabela_sem_entidade_mantem_todas_as_linhas():
    tabela = TabelaMediassin()
    tabela.read(
        io.StringIO(
            "     SIN    ,     VAR,       72,       73,\n"
            "   0,           EARMF,  1.50,  2.50,\n"
            "   0,            GHID,  3.00,      *,\n"
        )
    )
    df = tabela.data
    assert df.columns.tolist() == ["estagio", "indice_mes", "EARMF", "GHID"]
    assert df["indice_mes"].tolist() == [72, 73]
    assert df["EARMF"].tolist() == [1.5, 2.5]
    # Um valor que não é número vira NaN em vez de interromper a leitura.
    assert df["GHID"].iloc[0] == 3.0
    assert df["GHID"].isna().iloc[1]


def test_tabelas_de_tipos_diferentes_nao_sao_iguais():
    merc = TabelaMediasmerc()
    merc.read(io.StringIO(CSV_MERC))
    sin = TabelaMediassin()
    sin.data = merc.data
    assert merc != sin
    outra = TabelaMediasmerc()
    outra.read(io.StringIO(CSV_MERC))
    assert merc == outra
