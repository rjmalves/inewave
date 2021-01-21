Tutorial
=========

Este guia pode ser um bom ponto inicial para o uso do *inewave*. Como interface de desenvolvimento é recomendado
usar algum editor com um `language server` com um recurso de `autocomplete` eficiente para Python, como o
`VSCode <https://code.visualstudio.com/>`_ com `PyLance <https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance>`_
ou a IDE específica `PyCharm <https://www.jetbrains.com/pt-br/pycharm/download/>`_. O `autocomplete` é essencial para fazer uso de todo o potencial do
módulo *inewave*, além de auxiliar na escrita de códigos melhores.


Leitura, alteração e escrita do dger.dat
-----------------------------------------

Seja um sistema de arquivos no qual, dentro de um diretório cujo caminho é::

    $ pwd
    $ /home/usuario/estudo/pmo_MM_AAAA/

E neste diretório exista um arquivo ``dger.dat``, então o conteúdo deste pode ser lido 
através do código::

    >>> from inewave.newave.dger import LeituraDGer, EscritaDGer
    >>> leitor = LeituraDGer("/home/usuario/estudo/pmo_MM_AAAA/")
    >>> dger = leitor.le_arquivo()

.. currentmodule:: inewave.newave.modelos.dger

É possível analisar todos os parâmetros existentes no arquivo `dger.dat`::

    >>> dger.ano_inicio_estudo
    1995
    >>> dger.imprime_dados_mercados
    True

Se comparado com o conteúdo do arquivo `dger.dat`:

.. image:: figures/dger_antes.png
  :width: 180

Como o `dger.dat` também é um arquivo de entrada para o NEWAVE, este também possui
um recurso de escrita, que pode ser usado na geração de novos decks.

    >>> dger.ano_inicio_estudo = 2000
    >>> dger.imprime_dados_mercados = False
    >>> escritor = EscritaDGer("/home/usuario/estudo/pmo_MM_AAAA/")
    >>> escritor.escreve_arquivo()

Ao visualizar as diferenças entre os arquivos:

.. image:: figures/dger_diff.png
  :width: 550

Para mais informações, basta consultar a referência do objeto `DGer`.

Realizando a leitura do pmo.dat
--------------------------------

Seja um sistema de arquivos no qual, dentro de um diretório cujo caminho é::

    $ pwd
    $ /home/usuario/estudo/pmo_MM_AAAA/

E neste diretório exista um arquivo ``pmo.dat``, então o conteúdo deste pode ser lido 
através do código::

    >>> from inewave.newave.pmo import LeituraPMO
    >>> leitor = LeituraPMO("/home/usuario/estudo/pmo_MM_AAAA/")
    >>> pmo = leitor.le_arquivo()

.. currentmodule:: inewave.newave.modelos.pmo

É então constrúido um objeto :class:`PMO`, que fornece os dados do arquivo através de seus métodos::

    >>> pmo
    <inewave.newave.modelos.pmo.PMO object at 0x000001BC7663B340>
    >>> pmo.ano_pmo
    1995
    >>> pmo.mes_pmo
    5
    >>> pmo.versao_newave
    '27.4'

Os dados extraídos pelo módulo encontram-se no cabeçalho do arquivo:

.. image:: figures/pmo_cabecalho.png
  :width: 800

É possível obter também outras informações sobre o arquivo `pmo.dat`, como o custo total de operação::

    >>> pmo.custo_series_simuladas
    <inewave.newave.modelos.pmo.CustoOperacaoPMO object at 0x0000023B14525640>
    >>> leitor.pmo.custo_series_simuladas.custos
    [[1.895133e+04 1.292100e+02 9.082000e+01]
    [2.228000e+01 2.228000e+01 1.100000e-01]
    [8.800000e-01 1.000000e-02 0.000000e+00]
    [0.000000e+00 0.000000e+00 0.000000e+00]
    [1.010490e+03 9.999000e+01 4.840000e+00]
    [0.000000e+00 0.000000e+00 0.000000e+00]
    [7.061000e+01 1.486000e+01 3.400000e-01]
    [1.837600e+02 2.226000e+01 8.800000e-01]
    [0.000000e+00 0.000000e+00 0.000000e+00]
    [1.530000e+00 1.000000e-02 1.000000e-02]
    [0.000000e+00 0.000000e+00 0.000000e+00]
    [1.150000e+00 1.000000e-02 1.000000e-02]
    [6.257700e+02 1.387200e+02 3.000000e+00]
    [0.000000e+00 0.000000e+00 0.000000e+00]
    [0.000000e+00 0.000000e+00 0.000000e+00]
    [0.000000e+00 0.000000e+00 0.000000e+00]]

Os dados extraídos pelo módulo encontram-se na respectiva tabela do arquivo:

.. image:: figures/pmo_custos_series.png
  :width: 400

Informações específicas de cada custo estão disponíveis através de propriedades do objeto. Maiores detalhes podem ser obtidos na referência do objeto `CustoOperacaoPMO`.

Realizando a leitura do earmfbm00x.out
---------------------------------------

Realizando a leitura do MEDIAS-SIN.CSV
---------------------------------------
