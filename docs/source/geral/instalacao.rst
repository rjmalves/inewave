Instalação
============

O *inewave* é compatível com versões de Python >= 3.10 (testado em 3.10, 3.11 e 3.12).

Em posse de uma instalação local de Python, é recomendado que se use um ambiente virtual para instalação de módulos de terceiros, sendo que o *inewave* não é uma exceção.
Para mais detalhes sobre o uso de ambientes virtuais, recomenda-se a leitura do recurso oficial de Python para ambientes virtuais: `venv <https://docs.python.org/3/library/venv.html>`_.

Instalando com pip
------------------

É possível instalar a versão distribuída oficialmente com ``pip``:

.. code-block:: bash

    $ pip install inewave

Para atualizar para uma versão mais recente, basta adicionar a flag ``--upgrade``:

.. code-block:: bash

    $ pip install --upgrade inewave

Para instalar uma versão específica:

.. code-block:: bash

    $ pip install inewave==x.y.z

Instalando com uv
-----------------

Caso utilize o `uv <https://docs.astral.sh/uv/>`_ como gerenciador de pacotes, é possível adicionar o *inewave* a um projeto com:

.. code-block:: bash

    $ uv add inewave

Ou instalar diretamente no ambiente ativo com:

.. code-block:: bash

    $ uv pip install inewave

Instalando a versão de desenvolvimento
---------------------------------------

Para contribuir com o projeto ou experimentar funcionalidades ainda não distribuídas, é possível instalar a partir do repositório. Primeiro, clone o repositório com `Git <https://git-scm.com/>`_:

.. code-block:: bash

    $ git clone https://github.com/rjmalves/inewave
    $ cd inewave

Em seguida, instale as dependências de desenvolvimento com ``uv``:

.. code-block:: bash

    $ uv sync --extra dev

Para o guia completo de configuração do ambiente de desenvolvimento, consulte o `CONTRIBUTING.md <https://github.com/rjmalves/inewave/blob/main/CONTRIBUTING.md>`_.

Verificando a instalação
------------------------

Para confirmar que a instalação foi realizada com sucesso, execute:

.. code-block:: python

    import inewave
    print(inewave.__version__)
