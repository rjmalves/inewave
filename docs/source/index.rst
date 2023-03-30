.. inewave documentation master file, created by
   sphinx-quickstart on Mon Jan 18 09:33:19 2021.

Interface de Programação para o NEWAVE
=======================================

**Versão:** |release|

**Data:** |today|

O *inewave* é um pacote Python para manipulação dos arquivos
de entrada e saída do programa `NEWAVE <http://www.cepel.br/pt_br/produtos/newave-modelo-de-planejamento-da-operacao-de-sistemas-hidrotermicos-interligados-de-longo-e-medio-prazo.htm>`_. O NEWAVE é
desenvolvido pelo `CEPEL <http://www.cepel.br/>`_ e utilizado para os estudos de planejamento e operação do Sistema Interligado Nacional (SIN).

O inewave oferece:

- Meios para leitura dos arquivos de entrada e saída do NEWAVE e programas associados: NWLISTCF e NWLISTOP
- Armazenamento e processamento de dados otimizados com o uso de `NumPy <https://numpy.org/>`_
- Facilidades para estudo e análise dos dados utilizando DataFrames de `Pandas <https://pandas.pydata.org/pandas-docs/stable/index.html>`_
- Dados estruturados em modelos com o uso do paradigma de orientação a objetos (OOP)
- Utilidades de escritas dos arquivos de entrada do NEWAVE para elaboração automatizada de estudos


* :ref:`genindex`

.. toctree::
   :caption: Apresentação 
   :maxdepth: 3
   :hidden:

   ./install.rst

.. toctree::
   :caption: Referência - NEWAVE
   :maxdepth: 3
   :hidden:

   reference/newave/index.rst

.. toctree::
   :caption: Referência - NWLISTCF
   :maxdepth: 3
   :hidden:

   reference/nwlistcf/index.rst

.. toctree::
   :caption: Referência - NWLISTOP
   :maxdepth: 3
   :hidden:

   reference/nwlistop/index.rst

.. toctree::
   :caption: Exemplos 
   :maxdepth: 3
   :hidden:

   examples/index.rst