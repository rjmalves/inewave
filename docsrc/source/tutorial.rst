Tutorial
=========

Este guia pode ser um bom ponto inicial para o uso do *inewave*. Como interface de desenvolvimento é recomendado
usar algum editor com um `language server` com um recurso de `autocomplete` eficiente para Python, como o
`VSCode <https://code.visualstudio.com/>`_ com `PyLance <https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance>`_
ou a IDE específica `PyCharm <https://www.jetbrains.com/pt-br/pycharm/download/>`_. O `autocomplete` é essencial para fazer uso de todo o potencial do
módulo *inewave*, além de auxiliar na escrita de códigos melhores.

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
    AAAA
    >>> pmo.mes_pmo
    MM
    >>> pmo.versao_newave
    '27.4'


Realizando a leitura do earmfbm00x.out
---------------------------------------

Realizando a leitura do MEDIAS-SIN.CSV
---------------------------------------

Leitura, alteração e escrita do dger.dat
-----------------------------------------
.. currentmodule:: inewave.newave.modelos.dger

A referência à classe :class:`DGer`
