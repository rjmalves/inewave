from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita
from inewave.newave.modelos.caso import BlocoCaso, LeituraCaso


class Caso(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes ao arquivo
    `caso.dat`.

    Esta classe lida com informações de entrada do NEWAVE e
    que deve se referir ao caminho do `arquivos.dat`.

    **Parâmetros**

    - caso: `str`

    """

    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)
        val = True
        msg = "Erro na criação de Caso: "
        if len(dados.blocos) == 1:
            bloco = dados.blocos[0]
            if isinstance(bloco, BlocoCaso):
                self.__bloco = bloco
            else:
                msg += (f"O bloco deve ser do tipo {BlocoCaso}, " +
                        f"mas foi fornecido do tipo {type(bloco)}")
                val = False
        else:
            msg += "Deve ser fornecido exatamente 1 bloco para Caso"
            val = False
        if not val:
            raise TypeError(msg)

    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="caso.dat") -> 'Caso':
        """
        """
        leitor = LeituraCaso(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="caso.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

    @property
    def arquivo(self) -> str:
        """
        Caminho para o arquivo `arquivos.dat` de entrada do NEWAVE.

        **Retorna**

        `str`

        **Sobre**

        Retorna o caminho completo (unix-like) para o arquivo que direciona
        para os demais dados de entrada do NEWAVE.
        """
        return self.__bloco.dados
