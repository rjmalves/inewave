.. _desempenho:

Guia de Desempenho
==================

Esta página apresenta as características de desempenho do *inewave*, com base nos resultados
da suite de benchmarks incluída no repositório. Os números apresentados são **aproximados** e
dependem do hardware, da versão do Python e do estado do cache de módulos no momento da execução.

.. note::

   Os valores de tempo apresentados nesta página foram obtidos em um ambiente Linux x86-64
   com Python 3.14. Em outras configurações de hardware ou versão do Python, os tempos
   podem variar significativamente.


Visão Geral de Desempenho
--------------------------

O custo de uso do *inewave* se distribui em três dimensões principais:

- **Tempo de importação**: custo único de carregamento do módulo em cada processo Python.
  É dominado pelo primeiro acesso ao pacote ``inewave`` de nível superior.
- **Tempo de leitura**: custo de parsing e construção do DataFrame para cada arquivo lido
  do disco. Varia conforme a complexidade e o tipo do arquivo (número de patamares,
  quantidade de seções, etc.).
- **Tempo de agregação**: custo de acessar a propriedade ``.valores()`` nas classes de
  agregação do NWLISTOP, que dispara a concatenação dos blocos de dados internos.

A tabela a seguir apresenta um resumo de tempos representativos medidos com dados de
referência (arquivos mockados, sem I/O real de disco):

.. list-table:: Tempos aproximados por operação
   :header-rows: 1
   :widths: 35 35 15 15

   * - Operação
     - Tipo de arquivo / Handler
     - Tempo aproximado
     - Memória pico (Python)
   * - ``import inewave``
     - Pacote de nível superior (cache parcialmente quente)
     - ~360 ms
     - ~33 MB
   * - ``import inewave.nwlistop``
     - Sub-pacote (após importação do nível superior)
     - ~5 ms
     - ~0,3 MB
   * - Leitura — não-patamar (REE/SIN)
     - ``Earmf``, ``Earmfsin``, ``Earmfp``
     - ~70 ms
     - ~9 MB
   * - Leitura — patamar Submercado
     - ``Cmarg``
     - ~210 ms
     - ~28 MB
   * - Leitura — SectionFile Newave
     - ``Pmo``
     - ~644 ms
     - ~21 MB
   * - Leitura — binário Newave
     - ``Hidr`` (agregação)
     - ~84 ms
     - ~1 MB
   * - Agregação ``.valores()``
     - ``Earmf``, ``Cmarg``, ``Earmfp`` (dados mockados)
     - ~0,1 ms
     - < 0,1 MB


Tempos de Importação
--------------------

O *inewave* utiliza o padrão de *importação preguiçosa* (*lazy import*) em todos os seus
sub-pacotes. O mecanismo é implementado via a função especial ``__getattr__`` em cada
``__init__.py``, que registra um dicionário ``_LAZY_IMPORTS`` mapeando nomes de classe
para módulos internos. A classe em questão só é carregada de fato quando é acessada pela
primeira vez — e então armazenada no escopo global do pacote para que acessos subsequentes
sejam imediatos.

Consequência prática:

- ``import inewave`` leva aproximadamente **~360 ms** em um processo com cache parcialmente
  quente (pandas e numpy já carregados). Esse custo reflete a travessia do grafo de módulos
  do Python para um pacote com muitos sub-módulos.
- ``import inewave.nwlistop`` ou ``import inewave.newave`` leva apenas **~5 ms**, pois as
  dependências compartilhadas já estão resolvidas.
- O acesso a uma classe individual como ``inewave.nwlistop.earmf`` leva **~7 ms**.

.. note::

   O custo de ~360 ms ocorre **uma única vez por processo**. Em scripts de processamento em
   lote que processam centenas de arquivos, esse custo é diluído e se torna irrelevante.

Para minimizar o custo de importação em scripts que usam poucas classes, prefira importar
o sub-pacote ou a classe diretamente, em vez de importar o pacote de nível superior:

.. code-block:: python

   # Padrão recomendado para poucos arquivos do mesmo sub-pacote:
   from inewave.newave import Dger, Confhd

   # Ainda mais direto — importa apenas o módulo específico:
   from inewave.newave.dger import Dger

   # Evite isto se o pacote principal ainda não foi importado
   # e você só precisa de uma ou duas classes:
   import inewave  # importa o grafo inteiro (~360 ms)


Tempos de Leitura
-----------------

O custo de leitura de cada arquivo é medido sem I/O real de disco — os benchmarks usam
``mock_open`` com os mesmos arquivos de teste da suite de testes unitários. O tempo
reflete, portanto, o custo de **parsing e construção do DataFrame**, que é o custo
dominante em sistemas com SSD ou em processamento em memória.

Os principais fatores que influenciam o tempo de leitura são:

**Número de patamares**
   Arquivos do NWLISTOP com múltiplos patamares (como ``Cmarg``) são aproximadamente
   **3x mais lentos** que arquivos sem patamar (como ``Earmf``), pois cada patamar
   adiciona um conjunto de chamadas ao campo ``FloatField._textual_read`` no parser.

**Complexidade de seções**
   O ``Pmo`` (``SectionFile`` do Newave) é o arquivo mais lento (~644 ms) porque seu
   método ``converte_tabela_em_df`` aplica ``DataFrame.apply`` e ``DataFrame.melt``
   em cada bloco de seção. O profiler atribui aproximadamente 171 ms dessas operações
   às chamadas ao pandas.

**Distribuição de tempo no pipeline de leitura**
   Para os arquivos do NWLISTOP, o parsing via ``TabularParser.parse_lines`` consome
   entre 28–32% do tempo total. A construção do DataFrame via ``_build_dataframe``
   e ``formata_df_meses_para_datas_nwlistop`` consome cerca de 21%. O restante (~50%)
   corresponde ao despacho de blocos do cfinterface e ao overhead Python.


Otimização para Processamento em Lote
--------------------------------------

Ao processar centenas ou milhares de arquivos NWLISTOP, as estratégias a seguir reduzem
significativamente o tempo total de execução.

**1. Importe a classe uma única vez, fora do loop**

O lazy import é resolvido na primeira vez que a classe é acessada. Importar dentro do
loop provoca a resolução desnecessária do nome a cada iteração:

.. code-block:: python

   from inewave.nwlistop import Cmarg

   caminhos = [f"./nwlistop/cmarg{i:03d}.out" for i in range(1, 201)]

   resultados = []
   for caminho in caminhos:
       arq = Cmarg.read(caminho)
       resultados.append(arq.valores)

**2. Prefira imports de sub-pacote ou de módulo direto**

Se o script utiliza apenas classes de um sub-pacote específico, importe diretamente
do sub-pacote para evitar o custo de travessia do pacote de nível superior:

.. code-block:: python

   # Em vez de:
   from inewave.newave import Dger, Pmo, Confhd

   # Importe o sub-pacote diretamente quando precisar de poucos arquivos:
   from inewave.newave.dger import Dger

**3. Paralelize a leitura com multiprocessing ou concurrent.futures**

Cada chamada a ``read`` é independente e não há estado global compartilhado entre
instâncias. É seguro paralelizar a leitura usando ``ProcessPoolExecutor`` ou
``multiprocessing.Pool``:

.. code-block:: python

   from concurrent.futures import ProcessPoolExecutor
   from inewave.nwlistop import Earmf

   def ler_arquivo(caminho):
       return Earmf.read(caminho).valores

   caminhos = [f"./nwlistop/earmf{i:03d}.out" for i in range(1, 201)]

   with ProcessPoolExecutor() as executor:
       resultados = list(executor.map(ler_arquivo, caminhos))

.. note::

   Use ``ProcessPoolExecutor`` (múltiplos processos) em vez de ``ThreadPoolExecutor``
   (múltiplas threads). O parsing em Python é limitado pelo GIL — o paralelismo real
   só é obtido com processos separados.


Suite de Benchmarks
--------------------

O repositório inclui uma suite de benchmarks em ``benchmarks/`` que pode ser executada
para medir o desempenho na sua própria máquina e comparar resultados entre versões.
Todos os comandos devem ser executados a partir da **raiz do repositório**.

**Suite completa de benchmarks**

Executa benchmarks de importação, leitura e agregação com 10 iterações por padrão e
grava os resultados em ``benchmarks/benchmark_results.md``:

.. code-block:: bash

   python benchmarks/run_benchmarks.py

Para aumentar o número de iterações e obter medições mais estáveis:

.. code-block:: bash

   python benchmarks/run_benchmarks.py --iterations 20

Em execuções subsequentes, uma coluna **Delta** é populada automaticamente, comparando
as médias atuais com os valores da execução anterior. Um Delta positivo indica que a
execução atual foi mais lenta.

**Profiler por fase**

Mede o tempo de parede dividido por fase interna (parsing, construção do DataFrame,
formatação, concatenação) para cada tipo de arquivo representativo e grava os
resultados em ``benchmarks/profile_report.md``:

.. code-block:: bash

   python benchmarks/profile_read.py

**Interpretando os resultados**

O arquivo ``benchmarks/benchmark_results.md`` contém três tabelas — importação, leitura
e agregação — com as seguintes colunas:

- **Mean (s)**: média aritmética dos tempos de parede de todas as iterações. É a
  métrica principal de comparação.
- **Median (s)**: mediana dos tempos. Menos sensível a outliers do que a média.
- **Min (s)**: iteração mais rápida. Aproxima o desempenho no melhor caso.
- **Std Dev (s)**: desvio padrão amostral. Valores altos indicam medições ruidosas —
  considere aumentar o número de iterações.
- **Peak Memory (MB)**: pico de heap Python medido pelo ``tracemalloc``. Captura apenas
  alocações Python; buffers C-level do numpy e pandas não são contabilizados.

O arquivo ``benchmarks/profile_report.md`` contém uma tabela de fases com as colunas
**Parsing %**, **DataFrame %**, **Aggregation %** e **Other %**, que indicam qual
fração do tempo total de leitura foi consumida por cada fase.

.. note::

   As porcentagens de fase no ``profile_report.md`` podem não somar 100%. As fases não
   são mutuamente exclusivas: ``_build_dataframe`` chama
   ``formata_df_meses_para_datas_nwlistop`` internamente, de modo que as colunas
   DataFrame % e Parsing % podem se sobrepor.


Limitações Conhecidas
---------------------

.. warning::

   **Escalonamento O(n²) na agregação ``__monta_tabela``**: o método interno
   ``__monta_tabela``, acionado pela propriedade ``.valores()`` das classes de agregação
   do NWLISTOP, utiliza um padrão de ``pd.concat`` incremental que escala como O(n²) em
   relação ao número de blocos de anos no arquivo. Com os dados mockados da suite de
   testes (um único bloco de ano), o tempo medido (~0,1 ms) é desprezível. Em arquivos
   de produção reais com 20 ou mais blocos de anos, o custo pode ser significativamente
   maior do que os benchmarks sugerem. **Não conclua, a partir dos tempos de agregação
   medidos, que essa operação é rápida em produção.**

**Medições de memória são apenas no nível Python**
   A coluna **Peak Memory (MB)** usa ``tracemalloc``, que rastreia apenas alocações
   feitas por objetos Python. Buffers internos do numpy e do pandas (arrays C-level)
   não são capturados. O consumo real de memória residente do processo é maior do que
   o valor registrado.

**Benchmarks usam dados mockados, não arquivos reais**
   Os benchmarks de leitura usam ``mock_open`` com os mesmos arquivos de teste da suite
   de testes unitários. Esses arquivos mockados contêm apenas uma fração dos dados de
   um arquivo real de produção. O tempo de leitura de arquivos reais, que podem ser
   ordens de grandeza maiores, será proporcionalmente maior.

**Estado de cache de importação parcialmente quente**
   Os benchmarks de importação limpam apenas as entradas ``inewave.*`` do ``sys.modules``
   entre iterações. O cfinterface, o pandas e o numpy permanecem carregados. Os tempos
   medidos representam o custo marginal de carregar o próprio grafo de módulos do
   *inewave* — não o custo de um processo totalmente frio.
