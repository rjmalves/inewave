Instalação
============

O *inewave* é compatível com versões de Python >= 3.5. A única dependência formal é o módulo NumPy, que deve sempre ser mantido na versão mais atualizada para a distribuição de Python instalada.

Em posse de uma instalação local de Python, é recomendado que se use um ambiente virtual para instalação de módulos de terceiros, sendo que o *inewave* não é uma exceção.
Para mais detalhes sobre o uso de ambientes virtuais, recomenda-se a leitura do recurso oficial de Python para ambientes virtuais: `venv <https://docs.python.org/3/library/venv.html>`_.

Antes de prosseguir, é necessário verificar se está instalada a última versão do ``pip``, o gerenciador de pacotes de Python. Isso pode ser feito com, por exemplo::

    $ python -m pip install ---upgrade pip

Para maiores informações, é recomendado visitar a documentação oficial do `pip <https://pip.pypa.io/en/stable/installing/>`_.


Instalando a versão distribuída oficialmente
---------------------------------------------

É possível instalar a versão distribuída oficialmente com ``pip``::

    $ pip install inewave

Para atualizar para uma versão mais recente, basta adicionar a flag ``--upgrade``::

    $ pip install --upgrade inewave

Para instalar uma versão específica::

    $ pip install --upgrade inewave==x.y.z

É possível instalar também a partir do código fonte. Basta acessar a página de `releases <https://github.com/rjmalves/inewave/tags>`_, baixar o
arquivo comprimido com o código do módulo e executar no diretório::

    $ pip install .


Instalando a versão de desenvolvimento
---------------------------------------

É possível realizar a instalação desta versão fazendo o uso do `Git <https://git-scm.com/>`_. Para instalar a versão de desenvolvimento, é necessário
primeiramente desinstalar a versão instalada (se houve), com::

    $ pip uninstall inewave

Em seguida, basta fazer::

    $ git clone https://github.com/rjmalves/inewave
    $ cd inewave
    $ pip install -e


Procedimentos de teste
-----------------------

O *inewave* realiza testes utilizando o pacote de testes de Python ``pytest``. Para maiores informações, é recomendado acessar a `página <https://pytest.org>`_.

Além dos testes, o código também tem sua qualidade aferida com o uso de `flake8 <https://flake8.pycqa.org/en/latest/>`_ e `mypy <http://mypy-lang.org/>`_.