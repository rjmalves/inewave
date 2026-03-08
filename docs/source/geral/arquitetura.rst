.. _arquitetura:

Arquitetura do inewave
======================

.. _arquitetura-visao-geral:

Visão Geral
-----------

O *inewave* é uma biblioteca Python de leitura e escrita de arquivos para o modelo de otimização do
planejamento energético NEWAVE e seus programas auxiliares NWLISTOP e NWLISTCF. O modelo NEWAVE produz
e consome dezenas de arquivos de entrada e saída com formatos proprietários — alguns em texto, outros
em binário — cujas especificações são distribuídas pela CEPEL e pelo ONS.

O objetivo do *inewave* é fornecer uma interface Python consistente e orientada a objetos para todos
esses arquivos, expondo seus dados como :obj:`~pandas.DataFrame` e permitindo que analistas e
desenvolvedores manipulem decks de PMO e resultados de simulação sem precisar conhecer os detalhes de
formatação de cada arquivo.

.. note::

   O *inewave* não executa o modelo NEWAVE. Ele apenas lê e escreve os arquivos que o modelo consome
   e produz. A execução do modelo em si é de responsabilidade do ambiente onde o NEWAVE está instalado.

.. _arquitetura-cfinterface:

Framework cfinterface
---------------------

A implementação de cada classe de arquivo do *inewave* é construída sobre o framework
`cfinterface <https://github.com/rjmalves/cfi>`_, que define um modelo de classificação para arquivos
de dados estruturados. O framework abstrai o mecanismo de leitura e escrita, permitindo que cada
classe de arquivo no *inewave* descreva apenas *o que* está no arquivo, e não *como* realizar o
parsing de bytes.

O cfinterface define três modelos de classificação de arquivos:

Arquivos por blocos (:obj:`~cfinterface.files.blockfile.BlockFile`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um :obj:`~cfinterface.files.blockfile.BlockFile` é composto por blocos independentes e autocontidos.
Cada bloco possui um padrão de início — textual ou binário — que sinaliza o começo de um conjunto
coerente de informações. Opcionalmente, um padrão de terminação pode ser definido, ou o próprio bloco
pode determinar seus limites por outros critérios.

Cada bloco é modelado como uma subclasse de :obj:`~cfinterface.components.block.Block`. Um mesmo tipo
de bloco pode aparecer múltiplas vezes dentro de um arquivo, o que torna esse modelo adequado para
arquivos que repetem estruturas para diferentes entidades (usinas, estágios, cenários).

Exemplos de arquivos do *inewave* implementados como ``BlockFile``: :ref:`pmo.dat <pmo>` e
:ref:`parp.dat <parp>`.

Arquivos por seções (:obj:`~cfinterface.files.sectionfile.SectionFile`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um :obj:`~cfinterface.files.sectionfile.SectionFile` é composto por seções obrigatórias que sempre
aparecem em uma ordem fixa e predeterminada. Diferentemente do modelo por blocos, não há flexibilidade
na sequência ou na presença das seções: todas devem estar presentes e na ordem declarada.

Cada seção é modelada como uma subclasse de :obj:`~cfinterface.components.section.Section`, que pode
definir seu próprio critério de fim, permitindo alguma variação no comprimento interno de cada seção.
Esse modelo é adequado para arquivos cujo layout é rígido e bem especificado.

Exemplos de arquivos do *inewave* implementados como ``SectionFile``: :ref:`dger.dat <dger>` e
:ref:`sistema.dat <sistema>`.

Arquivos por registros (:obj:`~cfinterface.files.registerfile.RegisterFile`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um :obj:`~cfinterface.files.registerfile.RegisterFile` é composto por registros — unidades mínimas
de conteúdo que ocupam exatamente uma linha e possuem formato constante. Registros podem ser vistos
como blocos de uma única linha, mas sua simplicidade permite uma definição ainda mais direta: basta
declarar os campos do registro como uma subclasse de :obj:`~cfinterface.components.register.Register`,
e o framework infere automaticamente a leitura e a escrita a partir dos tipos e posições dos campos.

No *inewave*, o arquivo :ref:`modif.dat <modif>` é o principal exemplo implementado com esse modelo.

.. seealso::

   Documentação completa do framework cfinterface em
   `https://rjmalves.github.io/cfinterface/ <https://rjmalves.github.io/cfinterface/>`_.

.. _arquitetura-modulos:

Estrutura de Módulos
--------------------

O *inewave* organiza seus arquivos em quatro módulos públicos, refletindo a origem e a finalidade de
cada tipo de arquivo no contexto do NEWAVE:

``inewave.newave``
~~~~~~~~~~~~~~~~~~

Contém as classes que representam os **arquivos de entrada e saída do modelo NEWAVE** propriamente
dito. Inclui tanto arquivos de configuração (como :ref:`dger.dat <dger>` e :ref:`arquivos.dat <arquivos>`)
quanto arquivos de dados de entrada (como :ref:`vazoes.dat <vazoes>` e :ref:`hidr.dat <hidr>`) e
arquivos de saída da simulação (como :ref:`pmo.dat <pmo>` e arquivos binários de forward/backward).

``inewave.nwlistop``
~~~~~~~~~~~~~~~~~~~~

Contém as classes que representam os **arquivos de saída do programa NWLISTOP**, que pós-processa
os resultados da simulação do NEWAVE e gera relatórios de variáveis operativas (geração térmica,
armazenamento, custo marginal, entre outros). Esses arquivos são apenas de leitura no *inewave*.

``inewave.nwlistcf``
~~~~~~~~~~~~~~~~~~~~

Contém as classes que representam os **arquivos relacionados ao programa NWLISTCF**, que processa
os cortes de Benders gerados pelo NEWAVE. Este módulo é menor e possui estrutura de importação direta
(sem lazy imports), pois contém poucos arquivos.

``inewave.libs``
~~~~~~~~~~~~~~~~

Contém **utilitários e estruturas de dados compartilhados** entre os demais módulos, como modelos de
usinas hidrelétricas, restrições e fontes de geração eólica, que são referenciados em múltiplos
contextos dentro da biblioteca.

.. note::

   Além dos módulos públicos, o pacote conta com ``inewave._utils`` (funções internas de suporte)
   e ``inewave.config`` (constantes e configurações globais da biblioteca). Esses módulos não fazem
   parte da API pública e podem mudar entre versões sem aviso.

.. _arquitetura-lazy-import:

Mecanismo de Lazy Import
------------------------

Os módulos ``inewave.newave`` e ``inewave.nwlistop`` expõem dezenas de classes de arquivos. Para
evitar que a importação de ``inewave`` carregue todo o código de parsing na memória antes que qualquer
classe seja utilizada, esses módulos utilizam o padrão de *lazy import* introduzido pela
:pep:`562`.

O mecanismo funciona da seguinte forma:

1. O ``__init__.py`` de cada subpacote define um dicionário ``_LAZY_IMPORTS`` que mapeia o nome da
   classe (chave) para o nome do módulo interno onde ela está definida (valor):

.. code-block:: python

   # inewave/newave/__init__.py (trecho ilustrativo)
   _LAZY_IMPORTS: dict[str, str] = {
       "Vazoes": "vazoes",
       "Dger": "dger",
       "Pmo": "pmo",
       # ... demais classes
   }

2. Uma função ``__getattr__`` no nível do módulo intercepta qualquer acesso a atributo não definido
   explicitamente no namespace do pacote. Quando o nome solicitado está presente em ``_LAZY_IMPORTS``,
   o módulo interno correspondente é carregado dinamicamente via ``importlib.import_module``, a classe
   é extraída e armazenada em ``globals()`` para uso futuro (evitando reimportação):

.. code-block:: python

   def __getattr__(name: str) -> Any:
       if name in _LAZY_IMPORTS:
           module = importlib.import_module(f".{_LAZY_IMPORTS[name]}", __name__)
           value = getattr(module, name)
           globals()[name] = value  # cache para acessos subsequentes
           return value
       raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

3. A função ``__dir__`` é sobrescrita para retornar todos os nomes do dicionário, garantindo que
   ferramentas de introspecção (como ``dir(inewave.newave)`` e o autocompletar de IDEs) enxerguem
   todas as classes disponíveis mesmo antes de elas serem carregadas.

O efeito prático é que ``from inewave.newave import Vazoes`` carrega apenas o módulo ``vazoes.py``,
sem incorrer no custo de inicializar todas as outras classes do subpacote.

.. _arquitetura-nomenclatura:

Convenções de Nomenclatura
--------------------------

O *inewave* adota um conjunto de convenções que garantem consistência entre os nomes dos arquivos
do NEWAVE e as classes e propriedades Python correspondentes.

Nomes de classes
~~~~~~~~~~~~~~~~

Cada arquivo do NEWAVE é representado por uma classe cujo nome segue **PascalCase**, derivado do nome
do arquivo em disco. Abreviações presentes no nome do arquivo são mantidas no nome da classe sem
alteração de caso. Por exemplo:

- ``arquivos.dat`` → classe :ref:`Arquivos <arquivos>`
- ``confhd.dat`` → classe :ref:`Confhd <confhd>`
- ``dger.dat`` → classe :ref:`Dger <dger>`
- ``earmfpXXX.out`` → classe :ref:`Earmfp <earmfp>`
- ``gttotsin.out`` → classe :ref:`Gttotsin <gttotsin>`

Nomes de propriedades e colunas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As propriedades das classes e as colunas dos :obj:`~pandas.DataFrame` retornados seguem
**snake_case**. Evita-se ao máximo ambiguidades na escolha dos nomes:

- Atributos que identificam usinas hidrelétricas ou termelétricas são nomeados ``codigo_usina`` (para
  o identificador inteiro) e ``nome_usina`` (para a string de nome).
- Atributos relacionados a submercados de energia são sempre nomeados ``codigo_submercado`` e
  ``nome_submercado``, independentemente de o arquivo original usar o termo "subsistema".
- O mesmo padrão se aplica a REEs e demais entidades do modelo.

Dados tabulares
~~~~~~~~~~~~~~~

Sempre que possível, os dados são expostos em formato **normalizado** (formato longo, ou *tidy data*),
com uma coluna por variável e uma linha por observação. Isso facilita a integração com ferramentas de
análise como pandas, mesmo quando o arquivo original armazena os dados em formato de tabela cruzada.

.. _arquitetura-fluxo:

Fluxo de Dados
--------------

O ciclo completo de leitura de um arquivo percorre as seguintes etapas:

**1. Invocação do método ``read``**

O usuário chama o método de classe ``read``, passando o caminho do arquivo:

.. code-block:: python

   from inewave.newave import Dger

   arq = Dger.read("./dger.dat")

**2. Abertura do arquivo e despacho para o cfinterface**

Internamente, ``read`` delega ao cfinterface a abertura do arquivo em disco (modo texto ou binário,
conforme declarado na classe). O cfinterface instancia o objeto de arquivo e inicia o parsing.

**3. Parsing pelos componentes (Block / Section / Register)**

O cfinterface percorre o conteúdo do arquivo e, conforme encontra os padrões de início de cada
componente, invoca o método de leitura do :obj:`~cfinterface.components.block.Block`,
:obj:`~cfinterface.components.section.Section` ou :obj:`~cfinterface.components.register.Register`
correspondente. Cada componente é responsável por interpretar sua própria porção do arquivo e
armazenar os dados em atributos internos.

**4. Acesso às propriedades**

Após a leitura, o objeto Python resultante expõe os dados por meio de propriedades que retornam
:obj:`~pandas.DataFrame` (para dados tabulares) ou tipos escalares (inteiros, floats, strings):

.. code-block:: python

   # Acesso a uma propriedade escalar
   print(arq.num_anos_estudo)

   # Acesso a dados tabulares como DataFrame
   df = arq.sistema
   print(df.head())

**5. Modificação e escrita (opcional)**

Para arquivos de entrada, é possível modificar as propriedades e persistir o resultado com ``write``:

.. code-block:: python

   from inewave.newave import Vazoes

   arq_vazoes = Vazoes.read("./vazoes.dat")

   # Sensibilidade: elevar todas as vazões em 10%
   arq_vazoes.vazoes *= 1.1

   # Persistir o arquivo modificado
   arq_vazoes.write("./vazoes_sensibilidade.dat")

O método ``write`` delega novamente ao cfinterface, que percorre os componentes na ordem de
declaração e serializa cada um de volta ao formato original do arquivo.

.. note::

   Arquivos de saída do NEWAVE e do NWLISTOP são somente leitura no *inewave*. A tentativa de
   chamar ``write`` em uma instância dessas classes levantará uma exceção. Verifique a documentação
   da classe específica para confirmar se a escrita é suportada.
