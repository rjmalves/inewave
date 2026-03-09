.. _faq:

Perguntas Frequentes (FAQ)
==========================

Esta página reúne as dúvidas mais comuns dos usuários do *inewave*, organizadas por tema.
Se a sua dúvida não estiver listada aqui, consulte as outras seções da documentação ou
abra uma discussão no repositório do projeto.

.. seealso::

   :doc:`instalacao` — instruções detalhadas de instalação.

   :doc:`tutorial` — exemplos de uso dos principais padrões da biblioteca.

   :doc:`arquitetura` — visão geral da arquitetura interna do *inewave*.


Instalação
----------

**Como instalo o inewave?**

A forma recomendada é instalar a versão distribuída no PyPI com ``pip``:

.. code-block:: bash

   pip install inewave

Para garantir que está usando a versão mais recente, adicione a flag ``--upgrade``:

.. code-block:: bash

   pip install --upgrade inewave

.. seealso::

   :doc:`instalacao` — detalhes completos sobre instalação, incluindo ambientes virtuais.


**Como instalo uma versão específica do inewave?**

Informe o número da versão desejada diretamente no comando de instalação:

.. code-block:: bash

   pip install inewave==1.12.0

Versões disponíveis podem ser consultadas na página do projeto no
`PyPI <https://pypi.org/project/inewave/#history>`_.


**Qual é a versão mínima do Python necessária para usar o inewave?**

O *inewave* requer **Python >= 3.11**. Versões anteriores não são suportadas.
O projeto é testado com Python 3.11, 3.12, 3.13 e 3.14.

Se ao tentar instalar você receber um erro indicando que a versão do Python é
incompatível, verifique a versão instalada com:

.. code-block:: bash

   python --version


**Como instalo o inewave usando o uv?**

O `uv <https://github.com/astral-sh/uv>`_ é um gerenciador de pacotes Python de alta
performance e pode ser usado como alternativa ao ``pip``:

.. code-block:: bash

   uv pip install inewave

Para criar um projeto novo e adicionar o *inewave* como dependência:

.. code-block:: bash

   uv init meu-projeto
   cd meu-projeto
   uv add inewave


Uso Geral
---------

**Como faço a leitura de um arquivo?**

A leitura é sempre feita pelo método de classe ``read``, passando o caminho do arquivo:

.. code-block:: python

   from inewave.newave import Dger

   arq = Dger.read("./dger.dat")

O método retorna uma instância da classe com todos os dados do arquivo já parseados.
A maioria dos arquivos não exige argumentos adicionais além do caminho.

.. seealso::

   :doc:`tutorial` — exemplos de leitura com e sem argumentos adicionais.


**Como faço a escrita de um arquivo de entrada após modificá-lo?**

A escrita é feita pelo método de instância ``write``, chamado sobre o objeto retornado
pelo ``read``:

.. code-block:: python

   from inewave.newave import Vazoes

   arq_vazoes = Vazoes.read("./vazoes.dat")

   # Modifica os dados: eleva todas as vazões em 10%
   arq_vazoes.vazoes *= 1.1

   # Persiste o arquivo modificado
   arq_vazoes.write("./vazoes_modificadas.dat")

Note que ``read`` é um método de **classe** (chamado em ``Vazoes.read(...)``), enquanto
``write`` é um método de **instância** (chamado em ``arq_vazoes.write(...)``).


**Por que os arquivos de saída do NWLISTOP e do NWLISTCF não têm método write()?**

Os arquivos produzidos pelo NWLISTOP e pelo NWLISTCF são arquivos de **saída** do modelo
NEWAVE — eles são gerados automaticamente pela simulação e não fazem sentido ser
reescritos pelo usuário. Por esse motivo, o *inewave* implementa apenas a leitura para
esses arquivos.

Se você tentar chamar ``write`` em uma instância de um arquivo de saída, receberá uma
exceção indicando que a operação não é suportada. Consulte a documentação da classe
específica para verificar se ``write`` está disponível.


**Como acesso os dados de um arquivo como um DataFrame do pandas?**

As propriedades das classes retornam :obj:`~pandas.DataFrame` para dados tabulares.
O nome da propriedade geralmente reflete o conteúdo do dado:

.. code-block:: python

   from inewave.newave import Vazoes

   arq_vazoes = Vazoes.read("./vazoes.dat")

   # Retorna um DataFrame com as vazões históricas
   df = arq_vazoes.vazoes
   print(df.head())

Para dados escalares (um único valor numérico, string ou data), a propriedade retorna
o tipo Python correspondente (``int``, ``float``, ``str``, etc.).


**Como leio um arquivo que não está na codificação padrão (UTF-8)?**

Alguns arquivos gerados por versões antigas do NEWAVE usam a codificação ``latin-1``
(ISO-8859-1). O método ``read`` aceita o argumento ``encoding`` para esses casos:

.. code-block:: python

   from inewave.newave import Hidr

   arq_hidr = Hidr.read("./hidr.dat", encoding="latin-1")

Consulte a documentação da classe específica para saber qual encoding ela usa por padrão.


Compatibilidade com Versões do NEWAVE
--------------------------------------

**Quais versões do NEWAVE são suportadas pelo inewave?**

O *inewave* suporta os formatos de arquivo de múltiplas versões do modelo NEWAVE. As
versões com suporte variam por arquivo — algumas classes oferecem suporte a uma única
versão (a mais recente), enquanto outras suportam múltiplos formatos, especialmente
quando o layout do arquivo foi alterado entre versões do modelo.

As classes que suportam múltiplos formatos expõem o atributo de classe ``VERSIONS``,
que lista as versões disponíveis:

.. code-block:: python

   from inewave.nwlistop import Cmargmed

   print(Cmargmed.VERSIONS)
   # Exemplo de saída: {'28': ..., '29.4.1': ...}


**Como especifico a versão do NEWAVE ao ler um arquivo?**

Use o argumento nomeado ``version=`` no método ``read``:

.. code-block:: python

   from inewave.nwlistop import Cmargmed

   # Arquivo gerado com NEWAVE versão 28
   arq_v28 = Cmargmed.read("./cmarg001-med.out", version="28")

   # Arquivo gerado com a versão mais recente (29.4.1)
   arq_atual = Cmargmed.read("./cmarg001-med.out", version="29.4.1")

Se ``version=`` for omitido, o *inewave* utiliza o formato padrão configurado para a
classe, que geralmente corresponde à versão mais recente suportada.

.. seealso::

   :doc:`tutorial` — exemplo completo de leitura com seleção de versão usando o ``pmo.dat``
   para determinar a versão do modelo automaticamente.


**Qual é a relação entre a versão do cfinterface e a compatibilidade de versões do NEWAVE?**

O `cfinterface <https://github.com/rjmalves/cfi>`_ é o framework subjacente ao *inewave*
que implementa o mecanismo de suporte a múltiplas versões de arquivo. O atributo
``VERSIONS`` e o argumento ``version=`` no ``read`` só estão disponíveis a partir da
versão 1.9.0 do cfinterface.

O *inewave* declara a dependência ``cfinterface>=1.9.0`` para garantir que essa
funcionalidade esteja sempre disponível. Se você vir erros relacionados ao atributo
``VERSIONS`` ou ao argumento ``version=``, verifique a versão instalada do cfinterface:

.. code-block:: bash

   pip show cfinterface


Resolução de Problemas
-----------------------

**Recebo ImportError ao tentar importar uma classe do inewave. O que fazer?**

Verifique se o *inewave* está corretamente instalado no ambiente Python ativo:

.. code-block:: bash

   pip show inewave

Se o pacote não for encontrado, instale-o com ``pip install inewave``.

Caso o erro mencione ``cfinterface``, pode haver um conflito de versão. Verifique a
versão instalada do cfinterface:

.. code-block:: bash

   pip show cfinterface

A versão instalada deve satisfazer ``cfinterface>=1.9.0``. Se for menor, atualize com:

.. code-block:: bash

   pip install --upgrade cfinterface


**Recebo UnicodeDecodeError ao ler um arquivo. Como resolver?**

Esse erro ocorre quando o arquivo foi gerado com uma codificação diferente da esperada
pela classe. Tente passar explicitamente o encoding ``latin-1``:

.. code-block:: python

   from inewave.newave import Hidr

   arq_hidr = Hidr.read("./hidr.dat", encoding="latin-1")

Se o erro persistir com ``latin-1``, tente ``cp1252`` (Windows-1252), que é comum em
arquivos gerados em ambientes Windows:

.. code-block:: python

   arq_hidr = Hidr.read("./hidr.dat", encoding="cp1252")


**Recebo AttributeError ou KeyError ao acessar uma propriedade. O que pode ser?**

As causas mais comuns são:

1. **Versão incorreta**: o arquivo foi lido sem especificar o argumento ``version=``,
   mas o formato do arquivo corresponde a uma versão diferente da padrão. Consulte o
   atributo ``VERSIONS`` da classe e passe a versão correta no ``read``.

2. **Arquivo corrompido ou incompleto**: o arquivo no disco pode estar truncado ou
   ter sido gerado por uma execução parcial do NEWAVE. Verifique o arquivo com um
   editor de texto.

3. **Propriedade não disponível nessa versão**: algumas propriedades só existem em
   determinadas versões do formato de arquivo. Consulte a documentação da classe para
   verificar a disponibilidade por versão.


**O arquivo existe em disco, mas o inewave retorna um erro de arquivo não encontrado. Por quê?**

Verifique se o caminho passado ao ``read`` está correto em relação ao diretório de
trabalho atual. O *inewave* repassa o caminho diretamente ao cfinterface, que usa a
semântica padrão do sistema operacional para resolução de caminhos.

Uma prática recomendada é usar caminhos absolutos ou construir caminhos com
:obj:`pathlib.Path`:

.. code-block:: python

   from pathlib import Path
   from inewave.newave import Dger

   caminho = Path("/home/usuario/casos/pmo_abril_2024/dger.dat")
   arq = Dger.read(caminho)


Desempenho
----------

**Por que a primeira importação do inewave é lenta?**

O *inewave* utiliza o padrão de *lazy import* (importação preguiçosa) nos módulos
``inewave.newave`` e ``inewave.nwlistop``. Isso significa que as classes de arquivo
**não** são carregadas na memória no momento em que você escreve
``import inewave.newave`` — elas são carregadas individualmente apenas quando você
acessa cada classe pela primeira vez.

Portanto, a "lentidão" percebida na primeira importação é, na verdade, o custo de
carregar o módulo específico da classe que você está usando. Acessos subsequentes à
mesma classe são instantâneos, pois o módulo já está em cache.

.. seealso::

   :ref:`arquitetura-lazy-import` — explicação detalhada do mecanismo de lazy import.


**Como otimizar o processamento de um grande número de arquivos?**

Para processar muitos arquivos do mesmo tipo em sequência, as principais estratégias são:

1. **Reutilize a importação**: importe a classe fora do loop para que o custo de lazy
   import ocorra apenas uma vez:

.. code-block:: python

   from inewave.nwlistop import Cmargmed

   resultados = []
   for caminho in lista_de_arquivos:
       arq = Cmargmed.read(caminho)
       resultados.append(arq.valores)

2. **Paralelismo com multiprocessing**: como cada chamada a ``read`` é independente e
   não há estado global compartilhado entre instâncias, é seguro paralelizar a leitura
   usando :obj:`multiprocessing.Pool` ou :obj:`concurrent.futures.ProcessPoolExecutor`.

.. note::

   Um guia completo de otimização de desempenho, com benchmarks e estratégias detalhadas
   de paralelismo, estará disponível na seção **Desempenho** da documentação.
