.. _nwlistcfindex:

NWLISTCF
========


A estrutura do *inewave* padroniza os objetos de interface existentes para cada um dos três módulos desenvolvidos. 
A interface com o NWLISTCF segue o padrão de implementar modelos para armazenar cada uma das informações existentes
nos arquivos de entrada e saída, além de classes utilitárias para gerenciar com a leitura e interpretação das informações
dos arquivos, bem como na geração de novos arquivos. As classes de leitura e escrita tem seus nomes padronizados, sendo estes
``LeituraMODELO`` e ``EscritaMODELO``, onde ``MODELO`` varia conforma o arquivo do NWLISTCF em questão.

Classes são nomeadas em ``CamelCase``, enquanto funções, métodos e variáveis recebem seus nomes em ``snake_case``.


Básico da interface NWLISTCF
----------------------------

É recomendado que a importação seja feita sempre de forma a utilizar somente os objetos que serão de fato necessários para 
o estudo em questão. Desta forma, não é recomendado importar todo o módulo ``inewave.nwlistcf`` ou utilizar o `wildcard` ``*``.

A importação recomendada é, por exemplo::

    >>> from inewave.nwlistcf.estados import LeituraEstados
    >>> from inewave.nwlistcf.nwlistcf import LeituraNwlistcf

Em geral, os objetos de leitura são instanciados recebendo um único atributo, que é o diretório de leitura e possuem um dos dois métodos: ``le_arquivo()`` ou ``le_arquivos()``. 
Os métodos de leitura, além de retornarem os objetos arquiridos dos arquivos de entrada de texto, também armazenam os dados internamente ao objeto de leitura.

Para a leitura do arquivo `pmo.dat`::

    >>> from inewave.newave.pmo import LeituraPMO
    >>>
    >>> diretorio = "/home/usuario/..."
    >>> leitor = LeituraPMO(diretorio)
    >>> leitor.le_arquivo()
    <inewave.newave.modelos.pmo.PMO object at 0x000001BC7663B340>
    >>> leitor.pmo
    <inewave.newave.modelos.pmo.PMO object at 0x000001BC7663B340>

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

   arquivos/estados
   arquivos/nwlistcf
