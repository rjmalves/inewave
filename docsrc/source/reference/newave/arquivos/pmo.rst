.. _pmo:

=====================================
Acompanhamento do Programa (pmo.dat)
=====================================

.. currentmodule:: inewave.newave.modelos.pmo

Visão geral do modelo
======================

O relatório de acompanhamento do NEWAVE, localizado no arquivo geralmente denominado
pmo.dat, é armazenado na classe:

.. autoclass:: PMO
   :members:


Modelos auxiliares
======================

Devido ao grande número de informações existentes no `pmo.dat`, foram definidos modelos
auxiliares para armazenar todas as informações disponíveis.

.. autoclass:: DadosGeraisPMO
   :members:

.. autoclass:: EnergiasAfluentesPMO
   :members:

.. autoclass:: DemandaLiquidaEnergiaPMO
   :members:

.. autoclass:: RiscoDeficitENSPMO
   :members:

.. autoclass:: CustoOperacaoPMO
   :members:


Leitura
========
.. currentmodule:: inewave.newave.pmo

A leitura do arquivo `pmo.dat` é feita através da classe :class:`LeituraPMO`.

.. autoclass:: LeituraPMO
   :members:
