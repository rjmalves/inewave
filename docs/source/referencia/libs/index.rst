.. _libs:

LIBS
===========

O módulo ``inewave.libs`` contém as classes para leitura e escrita dos
arquivos de bibliotecas compartilhadas entre os modelos NEWAVE e NWLISTOP.
Esses arquivos incluem dados cadastrais de usinas eólicas, usinas
hidrelétricas e restrições operativas do sistema, além do arquivo de
índices (``indices.csv``), que indica o arquivo de cada card das LIBS.

.. currentmodule:: inewave.libs

.. autosummary::
   :nosignatures:

   Eolica
   Indices
   Restricoes
   UsinasHidreletricas

.. toctree::
   :maxdepth: 2

   arquivos/eolica
   arquivos/indices
   arquivos/restricoes
   arquivos/usinas_hidreletricas
