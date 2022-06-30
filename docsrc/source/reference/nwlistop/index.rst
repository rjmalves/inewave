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

    >>> from inewave.nwlistop.cmarg00 import Cmarg00
    >>>
    >>> diretorio = "/home/usuario/..."
    >>> cmarg = Cmarg00.le_arquivo(diretorio, "cmarg001.out")
    >>> cmarg
    <inewave.nwlistop.cmarg00.Cmarg00 object at 0x0000020BE9349E20>
    >>> cmarg.custos
            Ano  Série  Patamar  Janeiro  Fevereiro  Março  Abril    Maio   Junho    Julho  Agosto  Setembro  Outubro  Novembro  Dezembro   Média
    0      2021      1        1     0.00       0.00   0.00   0.00    0.00    0.00   497.03  268.43    358.91   249.64    236.99    153.67  294.11
    1      2021      1        2     0.00       0.00   0.00   0.00    0.00    0.00   497.03  268.43    358.91   249.64    236.99    153.67  294.11
    2      2021      1        3     0.00       0.00   0.00   0.00    0.00    0.00   493.85  256.40    358.91   249.64    236.99    153.67  291.58
    3      2021      2        1     0.00       0.00   0.00   0.00    0.00    0.00  1364.30  930.22    671.00  1018.98    544.53    509.76  839.80
    4      2021      2        2     0.00       0.00   0.00   0.00    0.00    0.00  1364.30  930.22    671.00  1018.98    544.53    509.76  839.80
    ...     ...    ...      ...      ...        ...    ...    ...     ...     ...      ...     ...       ...      ...       ...       ...     ...
    29995  2025   1999        2    26.91      46.48  97.01  86.55  117.21  122.39   117.12   84.47    124.37   131.95    105.20     12.64   89.36
    29996  2025   1999        3    26.91      46.48  97.01  86.54  117.21  122.39   115.47   84.47    124.37   131.95    105.20     12.64   89.22
    29997  2025   2000        1     0.00       0.00   0.00   0.00   52.97   74.26    62.60   74.46     86.24    14.08      6.07      5.90   31.38
    29998  2025   2000        2     0.00       0.00   0.00   0.00   52.97   74.26    62.60   74.46     86.24    14.08      6.07      5.90   31.38
    29999  2025   2000        3     0.00       0.00   0.00   0.00   52.97   74.26    62.60   74.46     86.24    14.08      6.07      5.90   31.38

    [30000 rows x 16 columns]


Arquivos
---------

.. toctree::
   :maxdepth: 2

   arquivos/cmarg00
   arquivos/cmarg00med
   arquivos/coper
   arquivos/eafbm00
   arquivos/earmfp00
   arquivos/earmfpm00
   arquivos/earmfpsin
   arquivos/earmfsin
   arquivos/ghtot00
   arquivos/ghtotm00
   arquivos/ghtotsin
   arquivos/gttot00
   arquivos/gttotsin
   arquivos/mediasmerc
   arquivos/mediassin
   arquivos/vagua00
