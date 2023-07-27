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
- Facilidades para estudo e análise dos dados utilizando DataFrames de `pandas <https://pandas.pydata.org/pandas-docs/stable/index.html>`_
- Dados estruturados em modelos com o uso do paradigma de orientação a objetos (OOP)


.. toctree::
   :caption: Apresentação 
   :maxdepth: 3

   apresentacao/apresentacao.rst

.. toctree::
   :caption: Geral 
   :maxdepth: 3

   geral/instalacao
   geral/tutorial
   geral/contribuicao
   examples/index.rst

.. toctree::
   :caption: Referência
   :maxdepth: 3

   reference/newave/index.rst
   reference/nwlistcf/index.rst
   reference/nwlistop/index.rst


:ref:`genindex`