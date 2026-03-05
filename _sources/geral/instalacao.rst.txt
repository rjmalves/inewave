Instalação
============

O *inewave* é compatível com versões de Python >= 3.8. 

Em posse de uma instalação local de Python, é recomendado que se use um ambiente virtual para instalação de módulos de terceiros, sendo que o *inewave* não é uma exceção.
Para mais detalhes sobre o uso de ambientes virtuais, recomenda-se a leitura do recurso oficial de Python para ambientes virtuais: `venv <https://docs.python.org/3/library/venv.html>`_.

Antes de prosseguir, é necessário verificar se está instalada a última versão do ``pip``, o gerenciador de pacotes de Python. Isso pode ser feito com, por exemplo::

    $ python -m pip install ---upgrade pip


Instalando a versão distribuída oficialmente
---------------------------------------------

É possível instalar a versão distribuída oficialmente com ``pip``::

    $ pip install inewave

Para atualizar para uma versão mais recente, basta adicionar a flag ``--upgrade``::

    $ pip install --upgrade inewave

Para instalar uma versão específica::

    $ pip install --upgrade inewave==x.y.z

Instalando a versão de desenvolvimento
---------------------------------------

É possível realizar a instalação desta versão fazendo o uso do `Git <https://git-scm.com/>`_. Para instalar a versão de desenvolvimento, é necessário
primeiramente desinstalar a versão instalada (se houve), com::

    $ pip uninstall inewave

Em seguida, basta fazer::

    $ pip install git+https://github.com/rjmalves/inewave

Também é possível selecionar um branch ou release específicos::

    $ pip install git+https://github.com/rjmalves/inewave@v1.0.0
