.. inewave documentation master file, created by
   sphinx-quickstart on Mon Jan 18 09:33:19 2021.

Interface de Programação para o NEWAVE
=======================================

O *inewave* é um pacote Python para manipulação dos arquivos
de entrada e saída do programa `NEWAVE <http://www.cepel.br/pt_br/produtos/newave-modelo-de-planejamento-da-operacao-de-sistemas-hidrotermicos-interligados-de-longo-e-medio-prazo.htm>`_,
desenvolvido pelo `CEPEL <http://www.cepel.br/>`_ e utilizado para os estudos de planejamento e operação do Sistema Interligado Nacional (SIN).

O inewave oferece:

- meios para leitura dos arquivos de entrada e saída do NEWAVE e programas associados: NWLISTCF e NWLISTOP
- armazenamento e processamento de dados otimizados com o uso de `NumPy <https://numpy.org/>`_
- dados estruturados em modelos com o uso do paradigma de orientação a objetos (OOP)
- utilidades de escritas dos arquivos de entrada do NEWAVE para elaboração de estudos personalizados

Com inewave é possível ler os arquivos de texto, característicos do NEWAVE, e salvar as informações em `pickle <https://docs.python.org/3/library/pickle.html>`_, 
para poupar processamento futuro e reduzir o tempo de execução.


Documentação
=============

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Índices e Tabelas
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
