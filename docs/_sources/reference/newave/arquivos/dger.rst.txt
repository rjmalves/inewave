.. _dger:

========================
Dados gerais (dger.dat)
========================

.. currentmodule:: inewave.newave.modelos.dger

Visão geral do modelo
======================

Os dados gerais de execução do NEWAVE, localizados no arquivo geralmente denominado
dger.dat, são armazenados na classe:

.. autoclass:: DGer
   :members:

Enumeradores auxiliares
========================

Para armazenar completamente o conteúdo especificado no arquivo ``dger.dat``
são definidos enumeradores auxiliares:

.. autoclass:: EnumTipoExecucao

.. autoclass:: EnumTipoSimulacaoFinal

.. autoclass:: EnumImpressaoOperacao

.. autoclass:: EnumImpressaoConvergencia

.. autoclass:: EnumTamanhoArquivoVazoes

.. autoclass:: EnumTendenciaHidrologica

.. autoclass:: EnumDuracaoPatamar

.. autoclass:: EnumCorrecaoEnergiaDesvio

.. autoclass:: EnumTipoGeracaoENAs

.. autoclass:: EnumRepresentacaoSubmotorizacao

.. autoclass:: EnumCVAR

.. autoclass:: EnumTipoReamostragem

.. autoclass:: EnumRepresentanteAgregacao

.. autoclass:: EnumMatrizCorrelacaoEspacial

.. autoclass:: EnumMomentoReamostragem

.. autoclass:: EnumInicioTesteConvergencia


Leitura
========
.. currentmodule:: inewave.newave.dger

A leitura do arquivo `dger.dat` é feita através da classe :class:`LeituraDGer`.

.. autoclass:: LeituraDGer
   :members:


Escrita
========

A escrita do arquivo `dger.dat` é feita através da classe :class:`EscritaDGer`.

.. autoclass:: EscritaDGer
   :members: