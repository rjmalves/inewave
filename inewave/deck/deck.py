from inewave.newave import Caso
from inewave.newave import Arquivos
from inewave.newave import Dger
from inewave.newave import Sistema
from inewave.newave import Confhd
from inewave.newave import Modif
from inewave.newave import Conft
from inewave.newave import Term
from inewave.newave import Clast
from inewave.newave import Exph
from inewave.newave import Expt
from inewave.newave import Patamar
from inewave.newave import Cortesh
from inewave.newave import Cortes
from inewave.newave import Pmo
from inewave.newave import Parp
from inewave.newave import Parpeol
from inewave.newave import Parpvaz
from inewave.newave import Forward
from inewave.newave import Forwarh
from inewave.newave import Shist
from inewave.newave import Manutt
from inewave.newave import Vazpast
from inewave.newave import Eafpast
from inewave.newave import Cadic
from inewave.newave import Dsvagua
from inewave.newave import Penalid
from inewave.newave import Curva
from inewave.newave import Agrint
from inewave.newave import Adterm
from inewave.newave import Ghmin
from inewave.newave import Cvar
from inewave.newave import Ree
from inewave.newave import Re

from inewave.newave import Engnat
from inewave.newave import Energiaf
from inewave.newave import Energiab
from inewave.newave import Energias
from inewave.newave import Enavazf
from inewave.newave import Enavazb
from inewave.newave import Enavazs
from inewave.newave import Vazaof
from inewave.newave import Vazaob
from inewave.newave import Vazaos
from inewave.newave import Hidr
from inewave.newave import Vazoes

from typing import Dict, Any, Union, Type, TypeVar
from datetime import datetime, timedelta
from os.path import join
import pathlib
import pandas as pd  # type: ignore


class Deck:
    """
    Classe para processamento de todos os arquivos de um deck
    de NEWAVE, lendo os arquivos que contém metadados sobre o
    estudo em questão, e extraindo as informações necessárias
    para o processamento dos demais arquivos.
    """

    T = TypeVar("T")

    def __init__(self, diretorio_base: str, arquivo_caso: str):
        self.__diretorio_base = diretorio_base
        self.__arquivo_caso = arquivo_caso
        self.__arquivos_processados: Dict[str, Any] = {}

    @classmethod
    def read(cls, caminho_caso: str, *args, **kwargs) -> "Deck":
        diretorio = pathlib.Path(caminho_caso).parent.resolve()
        return cls(diretorio)

    def write(self):
        pass

    def __valida(self, data, type: Type[T]) -> T:
        if not isinstance(data, type):
            raise RuntimeError()
        return data

    def __numero_estagios_individualizados(self) -> int:
        agregacao = (
            self.__valida(self.dger.agregacao_simulacao_final, int)
            if self.dger.agregacao_simulacao_final is not None
            else None
        )
        anos_estudo = self.__valida(self.dger.num_anos_estudo, int)
        ano_inicio = self.__valida(self.dger.ano_inicio_estudo, int)
        mes_inicio = self.__valida(self.dger.mes_inicio_estudo, int)
        if agregacao == 1:
            return anos_estudo * 12
        rees = self.__valida(self.ree.rees, pd.DataFrame)
        mes_fim_hib = rees["Mês Fim Individualizado"].iloc[0]
        ano_fim_hib = rees["Ano Fim Individualizado"].iloc[0]

        if mes_fim_hib is not None and ano_fim_hib is not None:
            data_inicio_estudo = datetime(
                year=ano_inicio,
                month=mes_inicio,
                day=1,
            )
            data_fim_individualizado = datetime(
                year=int(ano_fim_hib),
                month=int(mes_fim_hib),
                day=1,
            )
            tempo_individualizado = (
                data_fim_individualizado - data_inicio_estudo
            )
            return int(tempo_individualizado / timedelta(days=30))
        else:
            return 0

    @property
    def caso(self) -> Caso:
        """
        A instância da classe com o conteúdo do arquivo `caso.dat`.

        :return: O objeto
        :rtype: :class:`Caso`
        """
        if self.__arquivo_caso not in self.__arquivos_processados:
            self.__arquivos_processados[self.__arquivo_caso] = Caso.read(
                join(self.__diretorio_base, self.__arquivo_caso)
            )
        return self.__arquivos_processados[self.__arquivo_caso]

    @property
    def arquivos(self) -> Arquivos:
        """
        A instância da classe com o conteúdo do arquivo `arquivos.dat`.

        :return: O objeto
        :rtype: :class:`Arquivo`
        """
        if self.caso.arquivos not in self.__arquivos_processados:
            self.__arquivos_processados[self.caso.arquivos] = Arquivos.read(
                join(self.__diretorio_base, self.caso.arquivos)
            )
        return self.__arquivos_processados[self.caso.arquivos]

    @property
    def indices(self) -> pd.DataFrame:
        """
        O :class:`pd.DataFrame` com o conteúdo do arquivo `indices.csv`.

        :return: O objeto
        :rtype: :class:`Arquivo`
        """
        if "indices.csv" not in self.__arquivos_processados:
            caminho = pathlib.Path(self.__diretorio_base).joinpath(
                "indices.csv"
            )
            self.__arquivos_processados[self.caso.arquivos] = pd.read_csv(
                caminho, sep=";", header=None, index_col=0
            )
            self.__arquivos_processados[self.caso.arquivos].columns = [
                "vazio",
                "arquivo",
            ]
            self.__arquivos_processados[self.caso.arquivos].index = [
                i.strip()
                for i in list(
                    self.__arquivos_processados[self.caso.arquivos].index
                )
            ]
        self.__arquivos_processados[self.caso.arquivos][
            "arquivo"
        ] = self.__arquivos_processados[self.caso.arquivos].apply(
            lambda linha: linha["arquivo"].strip(), axis=1
        )
        return self.__arquivos_processados[self.caso.arquivos]

    @property
    def dger(self) -> Dger:
        """
        A instância da classe com o conteúdo do arquivo `dger.dat`.

        :return: O objeto
        :rtype: :class:`Dger`
        """
        if self.arquivos.dger not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.dger] = Dger.read(
                join(self.__diretorio_base, self.arquivos.dger)
            )
        return self.__arquivos_processados[self.arquivos.dger]

    @property
    def sistema(self) -> Sistema:
        """
        A instância da classe com o conteúdo do arquivo `sistema.dat`.

        :return: O objeto
        :rtype: :class:`Sistema`
        """
        if self.arquivos.sistema not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.sistema] = Sistema.read(
                join(self.__diretorio_base, self.arquivos.sistema)
            )
        return self.__arquivos_processados[self.arquivos.sistema]

    @property
    def confhd(self) -> Confhd:
        """
        A instância da classe com o conteúdo do arquivo `confhd.dat`.

        :return: O objeto
        :rtype: :class:`Confhd`
        """
        if self.arquivos.confhd not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.confhd] = Confhd.read(
                join(self.__diretorio_base, self.arquivos.confhd)
            )
        return self.__arquivos_processados[self.arquivos.confhd]

    @property
    def modif(self) -> Modif:
        """
        A instância da classe com o conteúdo do arquivo `modif.dat`.

        :return: O objeto
        :rtype: :class:`Modif`
        """
        if self.arquivos.modif not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.modif] = Modif.read(
                join(self.__diretorio_base, self.arquivos.modif)
            )
        return self.__arquivos_processados[self.arquivos.modif]

    @property
    def conft(self) -> Conft:
        """
        A instância da classe com o conteúdo do arquivo `conft.dat`.

        :return: O objeto
        :rtype: :class:`Conft`
        """
        if self.arquivos.conft not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.conft] = Conft.read(
                join(self.__diretorio_base, self.arquivos.conft)
            )
        return self.__arquivos_processados[self.arquivos.conft]

    @property
    def term(self) -> Term:
        """
        A instância da classe com o conteúdo do arquivo `term.dat`.

        :return: O objeto
        :rtype: :class:`Term`
        """
        if self.arquivos.term not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.term] = Term.read(
                join(self.__diretorio_base, self.arquivos.term)
            )
        return self.__arquivos_processados[self.arquivos.term]

    @property
    def clast(self) -> Clast:
        """
        A instância da classe com o conteúdo do arquivo `clast.dat`.

        :return: O objeto
        :rtype: :class:`Clast`
        """
        if self.arquivos.clast not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.clast] = Clast.read(
                join(self.__diretorio_base, self.arquivos.clast)
            )
        return self.__arquivos_processados[self.arquivos.clast]

    @property
    def exph(self) -> Exph:
        """
        A instância da classe com o conteúdo do arquivo `exph.dat`.

        :return: O objeto
        :rtype: :class:`Exph`
        """
        if self.arquivos.exph not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.exph] = Exph.read(
                join(self.__diretorio_base, self.arquivos.exph)
            )
        return self.__arquivos_processados[self.arquivos.exph]

    @property
    def expt(self) -> Expt:
        """
        A instância da classe com o conteúdo do arquivo `expt.dat`.

        :return: O objeto
        :rtype: :class:`Expt`
        """
        if self.arquivos.expt not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.expt] = Expt.read(
                join(self.__diretorio_base, self.arquivos.expt)
            )
        return self.__arquivos_processados[self.arquivos.expt]

    @property
    def patamar(self) -> Patamar:
        """
        A instância da classe com o conteúdo do arquivo `patamar.dat`.

        :return: O objeto
        :rtype: :class:`Patamar`
        """
        if self.arquivos.patamar not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.patamar] = Patamar.read(
                join(self.__diretorio_base, self.arquivos.patamar)
            )
        return self.__arquivos_processados[self.arquivos.patamar]

    # TODO - fazer o processamento adequado no forward e cortes

    @property
    def cortes(self) -> Cortes:
        """
        A instância da classe com o conteúdo do arquivo `cortes.dat`.

        :return: O objeto
        :rtype: :class:`Cortes`
        """
        if self.arquivos.cortes not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.cortes] = Cortes.read(
                join(self.__diretorio_base, self.arquivos.cortes)
            )
        return self.__arquivos_processados[self.arquivos.cortes]

    @property
    def cortesh(self) -> Cortesh:
        """
        A instância da classe com o conteúdo do arquivo `cortesh.dat`.

        :return: O objeto
        :rtype: :class:`Cortesh`
        """
        if self.arquivos.cortesh not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.cortesh] = Cortesh.read(
                join(self.__diretorio_base, self.arquivos.cortesh)
            )
        return self.__arquivos_processados[self.arquivos.cortesh]

    @property
    def pmo(self) -> Pmo:
        """
        A instância da classe com o conteúdo do arquivo `pmo.dat`.

        :return: O objeto
        :rtype: :class:`Pmo`
        """
        if self.arquivos.pmo not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.pmo] = Pmo.read(
                join(self.__diretorio_base, self.arquivos.pmo)
            )
        return self.__arquivos_processados[self.arquivos.pmo]

    @property
    def parp(self) -> Parp:
        """
        A instância da classe com o conteúdo do arquivo `parp.dat`.

        :return: O objeto
        :rtype: :class:`Parp`
        """
        if self.arquivos.parp not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.parp] = Parp.read(
                join(self.__diretorio_base, self.arquivos.parp)
            )
        return self.__arquivos_processados[self.arquivos.parp]

    @property
    def parpeol(self) -> Parpeol:
        """
        A instância da classe com o conteúdo do arquivo `parpeol.dat`.

        :return: O objeto
        :rtype: :class:`Parpeol`
        """
        if "parpeol.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["parpeol.dat"] = Parpeol.read(
                join(self.__diretorio_base, "parpeol.dat")
            )
        return self.__arquivos_processados["parpeol.dat"]

    @property
    def parpvaz(self) -> Parpvaz:
        """
        A instância da classe com o conteúdo do arquivo `parpvaz.dat`.

        :return: O objeto
        :rtype: :class:`Parpvaz`
        """
        if "parpvaz.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["parpvaz.dat"] = Parpvaz.read(
                join(self.__diretorio_base, "parpvaz.dat")
            )
        return self.__arquivos_processados["parpvaz.dat"]

    @property
    def forward(self) -> Forward:
        """
        A instância da classe com o conteúdo do arquivo `forward.dat`.

        :return: O objeto
        :rtype: :class:`Forward`
        """
        if self.arquivos.forward not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.forward] = Forward.read(
                join(self.__diretorio_base, self.arquivos.forward)
            )
        return self.__arquivos_processados[self.arquivos.forward]

    @property
    def shist(self) -> Forwarh:
        """
        A instância da classe com o conteúdo do arquivo `forwarh.dat`.

        :return: O objeto
        :rtype: :class:`Forwarh`
        """
        if self.arquivos.forwardh not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.forwardh] = Forwarh.read(
                join(self.__diretorio_base, self.arquivos.forwardh)
            )
        return self.__arquivos_processados[self.arquivos.forwardh]

    @property
    def shist(self) -> Shist:
        """
        A instância da classe com o conteúdo do arquivo `shist.dat`.

        :return: O objeto
        :rtype: :class:`Shist`
        """
        if self.arquivos.shist not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.shist] = Shist.read(
                join(self.__diretorio_base, self.arquivos.shist)
            )
        return self.__arquivos_processados[self.arquivos.shist]

    @property
    def manutt(self) -> Manutt:
        """
        A instância da classe com o conteúdo do arquivo `manutt.dat`.

        :return: O objeto
        :rtype: :class:`Manutt`
        """
        if self.arquivos.manutt not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.manutt] = Manutt.read(
                join(self.__diretorio_base, self.arquivos.manutt)
            )
        return self.__arquivos_processados[self.arquivos.manutt]

    @property
    def vazpast(self) -> Union[Vazpast, Eafpast]:
        """
        A instância da classe com o conteúdo do arquivo `vazpast.dat`
        ou `eafpast.dat`.

        :return: O objeto
        :rtype: :class:`Vazpast` | :class:`Eafpast`
        """
        if self.arquivos.vazpast not in self.__arquivos_processados:
            somente_sim_final = self.dger.tipo_execucao == 1
            eafpast_sim_final = (
                self.dger.considera_tendencia_hidrologica_sim_final == 2
            )
            executa_politica = self.dger.tipo_execucao == 0
            eafpast_politica = (
                self.dger.considera_tendencia_hidrologica_calculo_politica == 2
            )
            usa_eafpast = (somente_sim_final and eafpast_sim_final) or (
                executa_politica and eafpast_politica
            )
            if usa_eafpast:
                self.__arquivos_processados[
                    self.arquivos.vazpast
                ] = Eafpast.read(
                    join(self.__diretorio_base, self.arquivos.vazpast)
                )
            else:
                self.__arquivos_processados[
                    self.arquivos.vazpast
                ] = Vazpast.read(
                    join(self.__diretorio_base, self.arquivos.vazpast)
                )
        return self.__arquivos_processados[self.arquivos.vazpast]

    @property
    def c_adic(self) -> Cadic:
        """
        A instância da classe com o conteúdo do arquivo `c_adic.dat`.

        :return: O objeto
        :rtype: :class:`Cadic`
        """
        if self.arquivos.c_adic not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.c_adic] = Cadic.read(
                join(self.__diretorio_base, self.arquivos.c_adic)
            )
        return self.__arquivos_processados[self.arquivos.c_adic]

    @property
    def dsvagua(self) -> Dsvagua:
        """
        A instância da classe com o conteúdo do arquivo `dsvagua.dat`.

        :return: O objeto
        :rtype: :class:`Dsvagua`
        """
        if self.arquivos.dsvagua not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.dsvagua] = Dsvagua.read(
                join(self.__diretorio_base, self.arquivos.dsvagua)
            )
        return self.__arquivos_processados[self.arquivos.dsvagua]

    @property
    def penalid(self) -> Penalid:
        """
        A instância da classe com o conteúdo do arquivo `penalid.dat`.

        :return: O objeto
        :rtype: :class:`Penalid`
        """
        if self.arquivos.penalid not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.penalid] = Penalid.read(
                join(self.__diretorio_base, self.arquivos.penalid)
            )
        return self.__arquivos_processados[self.arquivos.penalid]

    @property
    def curva(self) -> Curva:
        """
        A instância da classe com o conteúdo do arquivo `curva.dat`.

        :return: O objeto
        :rtype: :class:`Curva`
        """
        if self.arquivos.curva not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.curva] = Curva.read(
                join(self.__diretorio_base, self.arquivos.curva)
            )
        return self.__arquivos_processados[self.arquivos.curva]

    @property
    def agrint(self) -> Agrint:
        """
        A instância da classe com o conteúdo do arquivo `agrint.dat`.

        :return: O objeto
        :rtype: :class:`Agrint`
        """
        if self.arquivos.agrint not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.agrint] = Agrint.read(
                join(self.__diretorio_base, self.arquivos.agrint)
            )
        return self.__arquivos_processados[self.arquivos.agrint]

    @property
    def adterm(self) -> Adterm:
        """
        A instância da classe com o conteúdo do arquivo `adterm.dat`.

        :return: O objeto
        :rtype: :class:`Adterm`
        """
        if self.arquivos.adterm not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.adterm] = Adterm.read(
                join(self.__diretorio_base, self.arquivos.adterm)
            )
        return self.__arquivos_processados[self.arquivos.adterm]

    @property
    def ghmin(self) -> Ghmin:
        """
        A instância da classe com o conteúdo do arquivo `ghmin.dat`.

        :return: O objeto
        :rtype: :class:`Ghmin`
        """
        if self.arquivos.ghmin not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.ghmin] = Ghmin.read(
                join(self.__diretorio_base, self.arquivos.ghmin)
            )
        return self.__arquivos_processados[self.arquivos.ghmin]

    @property
    def cvar(self) -> Cvar:
        """
        A instância da classe com o conteúdo do arquivo `cvar.dat`.

        :return: O objeto
        :rtype: :class:`Cvar`
        """
        if self.arquivos.cvar not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.cvar] = Cvar.read(
                join(self.__diretorio_base, self.arquivos.cvar)
            )
        return self.__arquivos_processados[self.arquivos.cvar]

    @property
    def ree(self) -> Ree:
        """
        A instância da classe com o conteúdo do arquivo `ree.dat`.

        :return: O objeto
        :rtype: :class:`Ree`
        """
        if self.arquivos.ree not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.ree] = Ree.read(
                join(self.__diretorio_base, self.arquivos.ree)
            )
        return self.__arquivos_processados[self.arquivos.ree]

    @property
    def re(self) -> Re:
        """
        A instância da classe com o conteúdo do arquivo `re.dat`.

        :return: O objeto
        :rtype: :class:`Re`
        """
        if self.arquivos.re not in self.__arquivos_processados:
            self.__arquivos_processados[self.arquivos.re] = Re.read(
                join(self.__diretorio_base, self.arquivos.re)
            )
        return self.__arquivos_processados[self.arquivos.re]

    @property
    def hidr(self) -> Hidr:
        """
        A instância da classe com o conteúdo do arquivo `hidr.dat`.

        :return: O objeto
        :rtype: :class:`Hidr`
        """
        if "hidr.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["hidr.dat"] = Hidr.read(
                join(self.__diretorio_base, "hidr.dat")
            )
        return self.__arquivos_processados["hidr.dat"]

    @property
    def vazoes(self) -> Vazoes:
        """
        A instância da classe com o conteúdo do arquivo `vazoes.dat`.

        :return: O objeto
        :rtype: :class:`Vazoes`
        """
        if "vazoes.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["vazoes.dat"] = Vazoes.read(
                join(self.__diretorio_base, "vazoes.dat")
            )
        return self.__arquivos_processados["vazoes.dat"]

    @property
    def engnat(self) -> Engnat:
        """
        A instância da classe com o conteúdo do arquivo `engnat.dat`.

        :return: O objeto
        :rtype: :class:`Engnat`
        """
        if "engnat.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["engnat.dat"] = Engnat.read(
                join(self.__diretorio_base, "engnat.dat")
            )
        return self.__arquivos_processados["engnat.dat"]

    def energiaf(self, iteracao: int) -> Energiaf:
        """
        A instância da classe com o conteúdo do arquivo `energiaf.dat`.

        :return: O objeto
        :rtype: :class:`Energiaf`
        """

        nome_arq = (
            f"energiaf{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "energiaf.dat"
        )
        if "energiaf.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["energiaf.dat"] = {}
        if self.__arquivos_processados["energiaf.dat"].get(iteracao) is None:
            try:
                anos_estudo = self.__valida(self.dger.num_anos_estudo, int)
                num_forwards = self.__valida(self.dger.num_forwards, int)
                parpa = self.__valida(
                    self.dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(self.dger.ordem_maxima_parp, int)

                rees = self.__valida(self.ree.rees, pd.DataFrame)

                n_rees = rees.shape[0]
                n_estagios = anos_estudo * 12
                n_estagios_th = 12 if parpa == 3 else ordem_maxima
                self.__arquivos_processados["energiaf.dat"][
                    iteracao
                ] = Energiaf.le_arquivo(
                    self.__diretorio_base,
                    nome_arq,
                    num_forwards,
                    n_rees,
                    n_estagios,
                    n_estagios_th,
                )
            except Exception:
                pass
        return self.__arquivos_processados["energiaf.dat"].get(iteracao)

    def get_enavazf(self, iteracao: int) -> Enavazf:
        nome_arq = (
            f"enavazf{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "enavazf.dat"
        )
        if "enavazf.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["enavazf.dat"] = {}
        if self.__arquivos_processados["enavazf.dat"].get(iteracao) is None:
            try:
                mes_inicio = self.__valida(self.dger.mes_inicio_estudo, int)
                num_forwards = self.__valida(self.dger.num_forwards, int)
                parpa = self.__valida(
                    self.dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(self.dger.ordem_maxima_parp, int)

                n_rees = self.__valida(self.ree.rees, pd.DataFrame).shape[0]
                n_estagios = (
                    self.__numero_estagios_individualizados() + mes_inicio - 1
                )
                n_estagios_th = 12 if parpa == 3 else ordem_maxima
                self.__arquivos_processados["enavazf.dat"][
                    iteracao
                ] = Enavazf.le_arquivo(
                    self.__diretorio_base,
                    nome_arq,
                    num_forwards,
                    n_rees,
                    n_estagios,
                    n_estagios_th,
                )
            except Exception:
                pass
        return self.__arquivos_processados["enavazf.dat"].get(iteracao)

    def vazaof(self, iteracao: int) -> Vazaof:
        nome_arq = (
            f"vazaof{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "vazaof.dat"
        )
        if "vazaof.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["vazaof.dat"] = {}
        if self.__arquivos_processados["vazaof.dat"].get(iteracao) is None:
            try:
                mes_inicio = self.__valida(self.dger.mes_inicio_estudo, int)
                num_forwards = self.__valida(self.dger.num_forwards, int)

                parpa = self.__valida(
                    self.dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(self.dger.ordem_maxima_parp, int)

                n_uhes = self.__valida(self.confhd.usinas, pd.DataFrame).shape[
                    0
                ]
                n_estagios = (
                    self.__numero_estagios_individualizados() + mes_inicio - 1
                )
                n_estagios_th = 12 if parpa == 3 else ordem_maxima
                self.__arquivos_processados["vazaof.dat"][
                    iteracao
                ] = Vazaof.le_arquivo(
                    self.__diretorio_base,
                    nome_arq,
                    num_forwards,
                    n_uhes,
                    n_estagios,
                    n_estagios_th,
                )
            except Exception:
                pass
        return self.__arquivos_processados["vazaof.dat"].get(iteracao)

    def get_energiab(self, iteracao: int) -> Energiab:
        nome_arq = (
            f"energiab{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "energiab.dat"
        )
        if "energiab.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["energiab.dat"] = {}
        if self.__arquivos_processados["energiab.dat"].get(iteracao) is None:
            try:
                anos_estudo = self.__valida(self.dger.num_anos_estudo, int)
                num_forwards = self.__valida(self.dger.num_forwards, int)
                num_aberturas = self.__valida(self.dger.num_aberturas, int)

                n_rees = self.__valida(self.ree.rees, pd.DataFrame).shape[0]
                n_estagios = anos_estudo * 12
                self.__arquivos_processados["energiab.dat"][
                    iteracao
                ] = Energiab.le_arquivo(
                    self.__diretorio_base,
                    nome_arq,
                    num_forwards,
                    num_aberturas,
                    n_rees,
                    n_estagios,
                )
            except Exception:
                pass
        return self.__arquivos_processados["energiab.dat"].get(iteracao)

    def get_enavazb(self, iteracao: int) -> Enavazb:
        nome_arq = (
            f"enavazb{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "enavazb.dat"
        )
        if "enavazb.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["enavazb.dat"] = {}
        if self.__arquivos_processados["enavazb.dat"].get(iteracao) is None:
            try:
                mes_inicio = self.__valida(self.dger.mes_inicio_estudo, int)
                num_forwards = self.__valida(self.dger.num_forwards, int)
                num_aberturas = self.__valida(self.dger.num_aberturas, int)

                n_rees = self.__valida(self.ree.rees, pd.DataFrame).shape[0]
                n_estagios = (
                    self.__numero_estagios_individualizados() + mes_inicio - 1
                )
                self.__arquivos_processados["enavazb.dat"][
                    iteracao
                ] = Enavazb.le_arquivo(
                    self.__diretorio_base,
                    nome_arq,
                    num_forwards,
                    num_aberturas,
                    n_rees,
                    n_estagios,
                )
            except Exception:
                pass
        return self.__arquivos_processados["vazaob.dat"].get(iteracao)

    def get_vazaob(self, iteracao: int) -> Vazaob:
        nome_arq = (
            f"vazaob{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "vazaob.dat"
        )
        if "vazaob.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["vazaob.dat"] = {}
        if self.__arquivos_processados["vazaob.dat"].get(iteracao) is None:
            try:
                mes_inicio = self.__valida(self.dger.mes_inicio_estudo, int)
                num_forwards = self.__valida(self.dger.num_forwards, int)
                num_aberturas = self.__valida(self.dger.num_aberturas, int)

                n_uhes = self.__valida(self.confhd.usinas, pd.DataFrame).shape[
                    0
                ]
                n_estagios_hib = (
                    self.__numero_estagios_individualizados() + mes_inicio - 1
                )
                self.__arquivos_processados["vazaob.dat"][
                    iteracao
                ] = Vazaob.le_arquivo(
                    self.__diretorio_base,
                    nome_arq,
                    num_forwards,
                    num_aberturas,
                    n_uhes,
                    n_estagios_hib,
                )
            except Exception:
                pass
        return self.__arquivos_processados["vazaob.dat"].get(iteracao)

    def get_energias(self) -> Energias:
        if "energias.dat" not in self.__arquivos_processados:
            try:
                anos_estudo = self.__valida(self.dger.num_anos_estudo, int)
                ano_inicio = self.__valida(self.dger.ano_inicio_estudo, int)
                ano_inicio_historico = self.__valida(
                    self.dger.ano_inicial_historico, int
                )
                num_series_sinteticas = self.__valida(
                    self.dger.num_series_sinteticas, int
                )
                tipo_simulacao_final = self.__valida(
                    self.dger.tipo_simulacao_final, int
                )
                parpa = self.__valida(
                    self.dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(self.dger.ordem_maxima_parp, int)

                n_rees = self.__valida(self.ree.rees, pd.DataFrame).shape[0]
                n_estagios = anos_estudo * 12
                n_estagios_th = 12 if parpa == 3 else ordem_maxima
                if tipo_simulacao_final == 1:
                    num_series = num_series_sinteticas
                else:
                    num_series = ano_inicio - ano_inicio_historico - 1
                self.__arquivos_processados[
                    "energias.dat"
                ] = Energias.le_arquivo(
                    self.__diretorio_base,
                    "energias.dat",
                    num_series,
                    n_rees,
                    n_estagios,
                    n_estagios_th,
                )
            except Exception:
                pass
        return self.__arquivos_processados["energias.dat"]

    def get_enavazs(self) -> Enavazs:
        if "enavazs.dat" not in self.__arquivos_processados:
            try:
                mes_inicio = self.__valida(self.dger.mes_inicio_estudo, int)
                ano_inicio = self.__valida(self.dger.ano_inicio_estudo, int)
                ano_inicio_historico = self.__valida(
                    self.dger.ano_inicial_historico, int
                )
                num_series_sinteticas = self.__valida(
                    self.dger.num_series_sinteticas, int
                )
                tipo_simulacao_final = self.__valida(
                    self.dger.tipo_simulacao_final, int
                )
                parpa = self.__valida(
                    self.dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(self.dger.ordem_maxima_parp, int)

                n_rees = self.__valida(self.ree.rees, pd.DataFrame).shape[0]
                n_estagios = (
                    self.__numero_estagios_individualizados() + mes_inicio - 1
                )
                n_estagios_th = 12 if parpa == 3 else ordem_maxima
                if tipo_simulacao_final == 1:
                    num_series = num_series_sinteticas
                else:
                    num_series = ano_inicio - ano_inicio_historico - 1
                self.__arquivos_processados[
                    "enavazs.dat"
                ] = Enavazs.le_arquivo(
                    self.__diretorio_base,
                    "enavazs.dat",
                    num_series,
                    n_rees,
                    n_estagios,
                    n_estagios_th,
                )
            except Exception:
                pass
        return self.__arquivos_processados["enavazs.dat"]

    def get_vazaos(self) -> Vazaos:
        if "vazaos.dat" not in self.__arquivos_processados:
            try:
                mes_inicio = self.__valida(self.dger.mes_inicio_estudo, int)
                parpa = self.__valida(
                    self.dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(self.dger.ordem_maxima_parp, int)
                num_series_sinteticas = self.__valida(
                    self.dger.num_series_sinteticas, int
                )
                ano_inicio = self.__valida(self.dger.ano_inicio_estudo, int)
                ano_inicial_historico = self.__valida(
                    self.dger.ano_inicial_historico, int
                )
                n_uhes = self.__valida(self.confhd.usinas, pd.DataFrame).shape[
                    0
                ]
                n_estagios = (
                    self.__numero_estagios_individualizados() + mes_inicio - 1
                )
                n_estagios_th = 12 if parpa == 3 else ordem_maxima
                if self.dger.tipo_simulacao_final == 1:
                    num_series = num_series_sinteticas
                else:
                    num_series = ano_inicio - ano_inicial_historico - 1
                self.__arquivos_processados["vazaos.dat"] = Vazaos.le_arquivo(
                    self.__diretorio_base,
                    "vazaos.dat",
                    num_series,
                    n_uhes,
                    n_estagios,
                    n_estagios_th,
                )
            except Exception:
                pass
        return self.__arquivos_processados["vazaos.dat"]
