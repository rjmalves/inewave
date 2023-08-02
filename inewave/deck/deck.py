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

from typing import Dict, Any, Union, Type, TypeVar, Optional
from datetime import datetime, timedelta
from os.path import join, isfile
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
        diretorio = str(pathlib.Path(caminho_caso).parent.resolve())
        arquivo = pathlib.Path(caminho_caso).parts[-1]
        return cls(diretorio, arquivo)

    def write(self, *args, **kwargs):
        pass

    def __valida(self, data, type: Type[T]) -> T:
        if not isinstance(data, type):
            raise RuntimeError()
        return data

    def __numero_estagios_individualizados(self) -> int:
        dger = self.dger
        if not dger:
            return 0
        ree = self.ree
        if not ree:
            return 0
        agregacao = (
            self.__valida(dger.agregacao_simulacao_final, int)
            if dger.agregacao_simulacao_final is not None
            else None
        )
        anos_estudo = self.__valida(dger.num_anos_estudo, int)
        ano_inicio = self.__valida(dger.ano_inicio_estudo, int)
        mes_inicio = self.__valida(dger.mes_inicio_estudo, int)
        if agregacao == 1:
            return anos_estudo * 12
        rees = self.__valida(ree.rees, pd.DataFrame)
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
    def caso(self) -> Optional[Caso]:
        """
        A instância da classe com o conteúdo do arquivo `caso.dat`.

        :return: O objeto
        :rtype: :class:`Caso`
        """
        if self.__arquivo_caso:
            if self.__arquivo_caso not in self.__arquivos_processados:
                caminho = join(self.__diretorio_base, self.__arquivo_caso)
                if isfile(caminho):
                    self.__arquivos_processados[
                        self.__arquivo_caso
                    ] = Caso.read(caminho)
            return self.__arquivos_processados.get(self.__arquivo_caso)
        return None

    @property
    def arquivos(self) -> Optional[Arquivos]:
        """
        A instância da classe com o conteúdo do arquivo `arquivos.dat`.

        :return: O objeto
        :rtype: :class:`Arquivo`
        """
        if self.caso:
            if self.caso.arquivos:
                if self.caso.arquivos not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.caso.arquivos)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.caso.arquivos
                        ] = Arquivos.read(caminho)
                return self.__arquivos_processados.get(self.caso.arquivos)
        return None

    @property
    def indices(self) -> Optional[pd.DataFrame]:
        """
        O :class:`pd.DataFrame` com o conteúdo do arquivo `indices.csv`.

        :return: O objeto
        :rtype: :class:`pd.DataFrame`
        """
        if "indices.csv" not in self.__arquivos_processados:
            caminho = pathlib.Path(self.__diretorio_base).joinpath(
                "indices.csv"
            )
            if isfile(caminho):
                self.__arquivos_processados["indices.csv"] = pd.read_csv(
                    caminho, sep=";", header=None, index_col=0
                )
                self.__arquivos_processados["indices.csv"].columns = [
                    "vazio",
                    "arquivo",
                ]
                self.__arquivos_processados["indices.csv"].index = [
                    i.strip()
                    for i in list(
                        self.__arquivos_processados["indices.csv"].index
                    )
                ]
                self.__arquivos_processados["indices.csv"][
                    "arquivo"
                ] = self.__arquivos_processados["indices.csv"].apply(
                    lambda linha: linha["arquivo"].strip(), axis=1
                )
        return self.__arquivos_processados.get("indices.csv")

    @property
    def dger(self) -> Optional[Dger]:
        """
        A instância da classe com o conteúdo do arquivo `dger.dat`.

        :return: O objeto
        :rtype: :class:`Dger`
        """
        if self.arquivos:
            if self.arquivos.dger:
                if self.arquivos.dger not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.dger)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.dger
                        ] = Dger.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.dger)
        return None

    @property
    def sistema(self) -> Optional[Sistema]:
        """
        A instância da classe com o conteúdo do arquivo `sistema.dat`.

        :return: O objeto
        :rtype: :class:`Sistema`
        """
        if self.arquivos:
            if self.arquivos.sistema:
                if self.arquivos.sistema not in self.__arquivos_processados:
                    caminho = join(
                        self.__diretorio_base, self.arquivos.sistema
                    )
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.sistema
                        ] = Sistema.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.sistema)
        return None

    @property
    def confhd(self) -> Optional[Confhd]:
        """
        A instância da classe com o conteúdo do arquivo `confhd.dat`.

        :return: O objeto
        :rtype: :class:`Confhd`
        """
        if self.arquivos:
            if self.arquivos.confhd:
                if self.arquivos.confhd not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.confhd)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.confhd
                        ] = Confhd.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.confhd)
        return None

    @property
    def modif(self) -> Optional[Modif]:
        """
        A instância da classe com o conteúdo do arquivo `modif.dat`.

        :return: O objeto
        :rtype: :class:`Modif`
        """
        if self.arquivos:
            if self.arquivos.modif:
                if self.arquivos.modif not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.modif)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.modif
                        ] = Modif.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.modif)
        return None

    @property
    def conft(self) -> Optional[Conft]:
        """
        A instância da classe com o conteúdo do arquivo `conft.dat`.

        :return: O objeto
        :rtype: :class:`Conft`
        """
        if self.arquivos:
            if self.arquivos.conft:
                if self.arquivos.conft not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.conft)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.conft
                        ] = Conft.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.conft)
        return None

    @property
    def term(self) -> Optional[Term]:
        """
        A instância da classe com o conteúdo do arquivo `term.dat`.

        :return: O objeto
        :rtype: :class:`Term`
        """
        if self.arquivos:
            if self.arquivos.term:
                if self.arquivos.term not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.term)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.term
                        ] = Term.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.term)
        return None

    @property
    def clast(self) -> Optional[Clast]:
        """
        A instância da classe com o conteúdo do arquivo `clast.dat`.

        :return: O objeto
        :rtype: :class:`Clast`
        """
        if self.arquivos:
            if self.arquivos.clast:
                if self.arquivos.clast not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.clast)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.clast
                        ] = Clast.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.clast)
        return None

    @property
    def exph(self) -> Optional[Exph]:
        """
        A instância da classe com o conteúdo do arquivo `exph.dat`.

        :return: O objeto
        :rtype: :class:`Exph`
        """
        if self.arquivos:
            if self.arquivos.exph:
                if self.arquivos.exph not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.exph)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.exph
                        ] = Exph.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.exph)
        return None

    @property
    def expt(self) -> Optional[Expt]:
        """
        A instância da classe com o conteúdo do arquivo `expt.dat`.

        :return: O objeto
        :rtype: :class:`Expt`
        """
        if self.arquivos:
            if self.arquivos.expt:
                if self.arquivos.expt not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.expt)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.expt
                        ] = Expt.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.expt)
        return None

    @property
    def patamar(self) -> Optional[Patamar]:
        """
        A instância da classe com o conteúdo do arquivo `patamar.dat`.

        :return: O objeto
        :rtype: :class:`Patamar`
        """
        if self.arquivos:
            if self.arquivos.patamar:
                if self.arquivos.patamar not in self.__arquivos_processados:
                    caminho = join(
                        self.__diretorio_base, self.arquivos.patamar
                    )
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.patamar
                        ] = Patamar.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.patamar)
        return None

    # TODO - fazer o processamento adequado no forward e cortes

    @property
    def cortes(self) -> Optional[Cortes]:
        """
        A instância da classe com o conteúdo do arquivo `cortes.dat`.

        :return: O objeto
        :rtype: :class:`Cortes`
        """
        if self.arquivos:
            if self.arquivos.cortes:
                if self.arquivos.cortes not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.cortes)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.cortes
                        ] = Cortes.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.cortes)
        return None

    @property
    def cortesh(self) -> Optional[Cortesh]:
        """
        A instância da classe com o conteúdo do arquivo `cortesh.dat`.

        :return: O objeto
        :rtype: :class:`Cortesh`
        """
        if self.arquivos:
            if self.arquivos.cortesh:
                if self.arquivos.cortesh not in self.__arquivos_processados:
                    caminho = join(
                        self.__diretorio_base, self.arquivos.cortesh
                    )
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.cortesh
                        ] = Cortesh.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.cortesh)
        return None

    @property
    def pmo(self) -> Optional[Pmo]:
        """
        A instância da classe com o conteúdo do arquivo `pmo.dat`.

        :return: O objeto
        :rtype: :class:`Pmo`
        """
        if self.arquivos:
            if self.arquivos.pmo:
                if self.arquivos.pmo not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.pmo)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.pmo
                        ] = Pmo.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.pmo)
        return None

    @property
    def parp(self) -> Optional[Parp]:
        """
        A instância da classe com o conteúdo do arquivo `parp.dat`.

        :return: O objeto
        :rtype: :class:`Parp`
        """
        if self.arquivos:
            if self.arquivos.parp:
                if self.arquivos.parp not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.parp)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.parp
                        ] = Parp.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.parp)
        return None

    @property
    def parpeol(self) -> Optional[Parpeol]:
        """
        A instância da classe com o conteúdo do arquivo `parpeol.dat`.

        :return: O objeto
        :rtype: :class:`Parpeol`
        """
        if "parpeol.dat" not in self.__arquivos_processados:
            caminho = join(self.__diretorio_base, "parpeol.dat")
            if isfile(caminho):
                self.__arquivos_processados["parpeol.dat"] = Parpeol.read(
                    caminho
                )
        return self.__arquivos_processados.get("parpeol.dat")

    @property
    def parpvaz(self) -> Optional[Parpvaz]:
        """
        A instância da classe com o conteúdo do arquivo `parpvaz.dat`.

        :return: O objeto
        :rtype: :class:`Parpvaz`
        """
        if "parpvaz.dat" not in self.__arquivos_processados:
            caminho = join(self.__diretorio_base, "parpvaz.dat")
            if isfile(caminho):
                self.__arquivos_processados["parpvaz.dat"] = Parpvaz.read(
                    caminho
                )
        return self.__arquivos_processados.get("parpvaz.dat")

    @property
    def forward(self) -> Optional[Forward]:
        """
        A instância da classe com o conteúdo do arquivo `forward.dat`.

        :return: O objeto
        :rtype: :class:`Forward`
        """
        if self.arquivos:
            if self.arquivos.forward:
                if self.arquivos.forward not in self.__arquivos_processados:
                    caminho = join(
                        self.__diretorio_base, self.arquivos.forward
                    )
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.forward
                        ] = Forward.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.forward)
        return None

    @property
    def forwarh(self) -> Optional[Forwarh]:
        """
        A instância da classe com o conteúdo do arquivo `forwarh.dat`.

        :return: O objeto
        :rtype: :class:`Forwarh`
        """
        if self.arquivos:
            if self.arquivos.forwardh:
                if self.arquivos.forwardh not in self.__arquivos_processados:
                    caminho = join(
                        self.__diretorio_base, self.arquivos.forwardh
                    )
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.forwardh
                        ] = Forwarh.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.forwardh)
        return None

    @property
    def shist(self) -> Optional[Shist]:
        """
        A instância da classe com o conteúdo do arquivo `shist.dat`.

        :return: O objeto
        :rtype: :class:`Shist`
        """
        if self.arquivos:
            if self.arquivos.shist:
                if self.arquivos.shist not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.shist)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.shist
                        ] = Shist.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.shist)
        return None

    @property
    def manutt(self) -> Optional[Manutt]:
        """
        A instância da classe com o conteúdo do arquivo `manutt.dat`.

        :return: O objeto
        :rtype: :class:`Manutt`
        """
        if self.arquivos:
            if self.arquivos.manutt:
                if self.arquivos.manutt not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.manutt)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.manutt
                        ] = Manutt.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.manutt)
        return None

    @property
    def vazpast(self) -> Optional[Union[Vazpast, Eafpast]]:
        """
        A instância da classe com o conteúdo do arquivo `vazpast.dat`
        ou `eafpast.dat`.

        :return: O objeto
        :rtype: :class:`Vazpast` | :class:`Eafpast`
        """
        dger = self.dger
        if not dger:
            return None
        if self.arquivos:
            if self.arquivos.vazpast:
                if self.arquivos.vazpast not in self.__arquivos_processados:
                    somente_sim_final = dger.tipo_execucao == 1
                    eafpast_sim_final = (
                        dger.considera_tendencia_hidrologica_sim_final == 2
                    )
                    executa_politica = dger.tipo_execucao == 0
                    eafpast_politica = (
                        dger.considera_tendencia_hidrologica_calculo_politica
                        == 2
                    )
                    usa_eafpast = (
                        somente_sim_final and eafpast_sim_final
                    ) or (executa_politica and eafpast_politica)
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
                return self.__arquivos_processados.get(self.arquivos.vazpast)
        return None

    @property
    def c_adic(self) -> Optional[Cadic]:
        """
        A instância da classe com o conteúdo do arquivo `c_adic.dat`.

        :return: O objeto
        :rtype: :class:`Cadic`
        """
        if self.arquivos:
            if self.arquivos.c_adic:
                if self.arquivos.c_adic not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.c_adic)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.c_adic
                        ] = Cadic.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.c_adic)
        return None

    @property
    def dsvagua(self) -> Optional[Dsvagua]:
        """
        A instância da classe com o conteúdo do arquivo `dsvagua.dat`.

        :return: O objeto
        :rtype: :class:`Dsvagua`
        """
        if self.arquivos:
            if self.arquivos.dsvagua:
                if self.arquivos.dsvagua not in self.__arquivos_processados:
                    caminho = join(
                        self.__diretorio_base, self.arquivos.dsvagua
                    )
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.dsvagua
                        ] = Dsvagua.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.dsvagua)
        return None

    @property
    def penalid(self) -> Optional[Penalid]:
        """
        A instância da classe com o conteúdo do arquivo `penalid.dat`.

        :return: O objeto
        :rtype: :class:`Penalid`
        """
        if self.arquivos:
            if self.arquivos.penalid:
                if self.arquivos.penalid not in self.__arquivos_processados:
                    caminho = join(
                        self.__diretorio_base, self.arquivos.penalid
                    )
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.penalid
                        ] = Penalid.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.penalid)
        return None

    @property
    def curva(self) -> Optional[Curva]:
        """
        A instância da classe com o conteúdo do arquivo `curva.dat`.

        :return: O objeto
        :rtype: :class:`Curva`
        """
        if self.arquivos:
            if self.arquivos.curva:
                if self.arquivos.curva not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.curva)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.curva
                        ] = Curva.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.curva)
        return None

    @property
    def agrint(self) -> Optional[Agrint]:
        """
        A instância da classe com o conteúdo do arquivo `agrint.dat`.

        :return: O objeto
        :rtype: :class:`Agrint`
        """
        if self.arquivos:
            if self.arquivos.agrint:
                if self.arquivos.agrint not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.agrint)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.agrint
                        ] = Agrint.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.agrint)
        return None

    @property
    def adterm(self) -> Optional[Adterm]:
        """
        A instância da classe com o conteúdo do arquivo `adterm.dat`.

        :return: O objeto
        :rtype: :class:`Adterm`
        """
        if self.arquivos:
            if self.arquivos.adterm:
                if self.arquivos.adterm not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.adterm)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.adterm
                        ] = Adterm.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.adterm)
        return None

    @property
    def ghmin(self) -> Optional[Ghmin]:
        """
        A instância da classe com o conteúdo do arquivo `ghmin.dat`.

        :return: O objeto
        :rtype: :class:`Ghmin`
        """
        if self.arquivos:
            if self.arquivos.ghmin:
                if self.arquivos.ghmin not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.ghmin)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.ghmin
                        ] = Ghmin.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.ghmin)
        return None

    @property
    def cvar(self) -> Optional[Cvar]:
        """
        A instância da classe com o conteúdo do arquivo `cvar.dat`.

        :return: O objeto
        :rtype: :class:`Cvar`
        """
        if self.arquivos:
            if self.arquivos.cvar:
                if self.arquivos.cvar not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.cvar)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.cvar
                        ] = Cvar.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.cvar)
        return None

    @property
    def ree(self) -> Optional[Ree]:
        """
        A instância da classe com o conteúdo do arquivo `ree.dat`.

        :return: O objeto
        :rtype: :class:`Ree`
        """
        if self.arquivos:
            if self.arquivos.ree:
                if self.arquivos.ree not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.ree)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.ree
                        ] = Ree.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.ree)
        return None

    @property
    def re(self) -> Optional[Re]:
        """
        A instância da classe com o conteúdo do arquivo `re.dat`.

        :return: O objeto
        :rtype: :class:`Re`
        """
        if self.arquivos:
            if self.arquivos.re:
                if self.arquivos.re not in self.__arquivos_processados:
                    caminho = join(self.__diretorio_base, self.arquivos.re)
                    if isfile(caminho):
                        self.__arquivos_processados[
                            self.arquivos.re
                        ] = Re.read(caminho)
                return self.__arquivos_processados.get(self.arquivos.re)
        return None

    @property
    def hidr(self) -> Optional[Hidr]:
        """
        A instância da classe com o conteúdo do arquivo `hidr.dat`.

        :return: O objeto
        :rtype: :class:`Hidr`
        """
        if "hidr.dat" not in self.__arquivos_processados:
            caminho = join(self.__diretorio_base, "hidr.dat")
            if isfile(caminho):
                self.__arquivos_processados["hidr.dat"] = Hidr.read(caminho)
        return self.__arquivos_processados.get("hidr.dat")

    @property
    def vazoes(self) -> Optional[Vazoes]:
        """
        A instância da classe com o conteúdo do arquivo `vazoes.dat`.

        :return: O objeto
        :rtype: :class:`Vazoes`
        """
        if "vazoes.dat" not in self.__arquivos_processados:
            caminho = join(self.__diretorio_base, "vazoes.dat")
            if isfile(caminho):
                self.__arquivos_processados["vazoes.dat"] = Vazoes.read(
                    caminho
                )
        return self.__arquivos_processados.get("vazoes.dat")

    @property
    def engnat(self) -> Optional[Engnat]:
        """
        A instância da classe com o conteúdo do arquivo `engnat.dat`.

        :return: O objeto
        :rtype: :class:`Engnat`
        """
        if "engnat.dat" not in self.__arquivos_processados:
            caminho = join(self.__diretorio_base, "engnat.dat")
            if isfile(caminho):
                self.__arquivos_processados["engnat.dat"] = Engnat.read(
                    caminho
                )
        return self.__arquivos_processados.get("engnat.dat")

    def energiaf(self, iteracao: int) -> Optional[Energiaf]:
        """
        A instância da classe com o conteúdo do arquivo `energiaf.dat`.

        :return: O objeto
        :rtype: :class:`Energiaf`
        """
        dger = self.dger
        if not dger:
            return None
        ree = self.ree
        if not ree:
            return None
        nome_arq = (
            f"energiaf{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "energiaf.dat"
        )
        if "energiaf.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["energiaf.dat"] = {}
        if self.__arquivos_processados["energiaf.dat"].get(iteracao) is None:
            try:
                anos_estudo = self.__valida(dger.num_anos_estudo, int)
                num_forwards = self.__valida(dger.num_forwards, int)
                parpa = self.__valida(
                    dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(dger.ordem_maxima_parp, int)

                rees = self.__valida(ree.rees, pd.DataFrame)

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

    def get_enavazf(self, iteracao: int) -> Optional[Enavazf]:
        dger = self.dger
        if not dger:
            return None
        ree = self.ree
        if not ree:
            return None
        nome_arq = (
            f"enavazf{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "enavazf.dat"
        )
        if "enavazf.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["enavazf.dat"] = {}
        if self.__arquivos_processados["enavazf.dat"].get(iteracao) is None:
            try:
                mes_inicio = self.__valida(dger.mes_inicio_estudo, int)
                num_forwards = self.__valida(dger.num_forwards, int)
                parpa = self.__valida(
                    dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(dger.ordem_maxima_parp, int)

                n_rees = self.__valida(ree.rees, pd.DataFrame).shape[0]
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

    def vazaof(self, iteracao: int) -> Optional[Vazaof]:
        dger = self.dger
        if not dger:
            return None
        confhd = self.confhd
        if not confhd:
            return None
        nome_arq = (
            f"vazaof{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "vazaof.dat"
        )
        if "vazaof.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["vazaof.dat"] = {}
        if self.__arquivos_processados["vazaof.dat"].get(iteracao) is None:
            try:
                mes_inicio = self.__valida(dger.mes_inicio_estudo, int)
                num_forwards = self.__valida(dger.num_forwards, int)

                parpa = self.__valida(
                    dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(dger.ordem_maxima_parp, int)

                n_uhes = self.__valida(confhd.usinas, pd.DataFrame).shape[0]
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

    def get_energiab(self, iteracao: int) -> Optional[Energiab]:
        dger = self.dger
        if not dger:
            return None
        ree = self.ree
        if not ree:
            return None
        nome_arq = (
            f"energiab{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "energiab.dat"
        )
        if "energiab.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["energiab.dat"] = {}
        if self.__arquivos_processados["energiab.dat"].get(iteracao) is None:
            try:
                anos_estudo = self.__valida(dger.num_anos_estudo, int)
                num_forwards = self.__valida(dger.num_forwards, int)
                num_aberturas = self.__valida(dger.num_aberturas, int)

                n_rees = self.__valida(ree.rees, pd.DataFrame).shape[0]
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

    def get_enavazb(self, iteracao: int) -> Optional[Enavazb]:
        dger = self.dger
        if not dger:
            return None
        ree = self.ree
        if not ree:
            return None
        nome_arq = (
            f"enavazb{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "enavazb.dat"
        )
        if "enavazb.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["enavazb.dat"] = {}
        if self.__arquivos_processados["enavazb.dat"].get(iteracao) is None:
            try:
                mes_inicio = self.__valida(dger.mes_inicio_estudo, int)
                num_forwards = self.__valida(dger.num_forwards, int)
                num_aberturas = self.__valida(dger.num_aberturas, int)

                n_rees = self.__valida(ree.rees, pd.DataFrame).shape[0]
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

    def get_vazaob(self, iteracao: int) -> Optional[Vazaob]:
        dger = self.dger
        if not dger:
            return None
        confhd = self.confhd
        if not confhd:
            return None
        nome_arq = (
            f"vazaob{str(iteracao).zfill(3)}.dat"
            if iteracao != 1
            else "vazaob.dat"
        )
        if "vazaob.dat" not in self.__arquivos_processados:
            self.__arquivos_processados["vazaob.dat"] = {}
        if self.__arquivos_processados["vazaob.dat"].get(iteracao) is None:
            try:
                mes_inicio = self.__valida(dger.mes_inicio_estudo, int)
                num_forwards = self.__valida(dger.num_forwards, int)
                num_aberturas = self.__valida(dger.num_aberturas, int)

                n_uhes = self.__valida(confhd.usinas, pd.DataFrame).shape[0]
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

    def get_energias(self) -> Optional[Energias]:
        dger = self.dger
        if not dger:
            return None
        ree = self.ree
        if not ree:
            return None
        if "energias.dat" not in self.__arquivos_processados:
            try:
                anos_estudo = self.__valida(dger.num_anos_estudo, int)
                ano_inicio = self.__valida(dger.ano_inicio_estudo, int)
                ano_inicio_historico = self.__valida(
                    dger.ano_inicial_historico, int
                )
                num_series_sinteticas = self.__valida(
                    dger.num_series_sinteticas, int
                )
                tipo_simulacao_final = self.__valida(
                    dger.tipo_simulacao_final, int
                )
                parpa = self.__valida(
                    dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(dger.ordem_maxima_parp, int)

                n_rees = self.__valida(ree.rees, pd.DataFrame).shape[0]
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

    def get_enavazs(self) -> Optional[Enavazs]:
        dger = self.dger
        if not dger:
            return None
        ree = self.ree
        if not ree:
            return None
        if "enavazs.dat" not in self.__arquivos_processados:
            try:
                mes_inicio = self.__valida(dger.mes_inicio_estudo, int)
                ano_inicio = self.__valida(dger.ano_inicio_estudo, int)
                ano_inicio_historico = self.__valida(
                    dger.ano_inicial_historico, int
                )
                num_series_sinteticas = self.__valida(
                    dger.num_series_sinteticas, int
                )
                tipo_simulacao_final = self.__valida(
                    dger.tipo_simulacao_final, int
                )
                parpa = self.__valida(
                    dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(dger.ordem_maxima_parp, int)

                n_rees = self.__valida(ree.rees, pd.DataFrame).shape[0]
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

    def get_vazaos(self) -> Optional[Vazaos]:
        dger = self.dger
        if not dger:
            return None
        confhd = self.confhd
        if not confhd:
            return None
        if "vazaos.dat" not in self.__arquivos_processados:
            try:
                mes_inicio = self.__valida(dger.mes_inicio_estudo, int)
                parpa = self.__valida(
                    dger.consideracao_media_anual_afluencias, int
                )
                ordem_maxima = self.__valida(dger.ordem_maxima_parp, int)
                num_series_sinteticas = self.__valida(
                    dger.num_series_sinteticas, int
                )
                ano_inicio = self.__valida(dger.ano_inicio_estudo, int)
                ano_inicial_historico = self.__valida(
                    dger.ano_inicial_historico, int
                )
                n_uhes = self.__valida(confhd.usinas, pd.DataFrame).shape[0]
                n_estagios = (
                    self.__numero_estagios_individualizados() + mes_inicio - 1
                )
                n_estagios_th = 12 if parpa == 3 else ordem_maxima
                if dger.tipo_simulacao_final == 1:
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
