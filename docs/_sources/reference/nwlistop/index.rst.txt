.. _nwlistop:

NWLISTOP
========


A estrutura do *inewave* padroniza os objetos de interface existentes para cada um dos três módulos desenvolvidos. 
A interface com o NWLISTOP segue o padrão de implementar modelos para armazenar cada uma das informações existentes
nos arquivos de entrada e saída, além de classes utilitárias para gerenciar com a leitura e interpretação das informações
dos arquivos, bem como na geração de novos arquivos. As classes de leitura e escrita tem seus nomes padronizados, sendo estes
``LeituraMODELO`` e ``EscritaMODELO``, onde ``MODELO`` varia conforma o arquivo do NWLISTOP em questão.

Classes são nomeadas em ``CamelCase``, enquanto funções, métodos e variáveis recebem seus nomes em ``snake_case``.


Básico da interface NWLISTOP
----------------------------

É recomendado que a importação seja feita sempre de forma a utilizar somente os objetos que serão de fato necessários para 
o estudo em questão. Desta forma, não é recomendado importar todo o módulo ``inewave.nwlistop`` ou utilizar o `wildcard` ``*``.

A importação recomendada é, por exemplo::

    >>> from inewave.nwlistop.eafbm00 import Eafbm00
    >>> from inewave.nwlistop.mediasmerc import MediasMerc

Para a leitura do arquivo `pmo.dat`::

    >>> from inewave.newave.pmo import PMO
    >>>
    >>> diretorio = "/home/usuario/..."
    >>> pmo = PMO.le_arquivo(diretorio)
    <inewave.newave.pmo.PMO object at 0x000001BC7663B340>

Para a leitura dos arquivos `cmarg00x.out`::

    >>> from inewave.nwlistop.cmarg00 import LeituraCmarg00
    >>>
    >>> diretorio = "/home/usuario/..."
    >>> leitor = LeituraCmarg00(diretorio)
    >>> leitor.le_arquivos()
    {'SUDESTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692820>,
    'SUL': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692790>,
    'NORDESTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692910>,
    'NORTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692970>}
    >>> leitor.cmargs
    {'SUDESTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692820>,
    'SUL': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692790>,
    'NORDESTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692910>,
    'NORTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692970>}

Arquivos
---------

.. toctree::
   :maxdepth: 2

   arquivos/cmarg00
   arquivos/eafbm00
   arquivos/earmfpm00
   arquivos/mediasmerc
   arquivos/mediassin
