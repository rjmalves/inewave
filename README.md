# inewave

> Pacote Python para leitura e escrita dos arquivos de entrada e saída do modelo NEWAVE e dos programas auxiliares NWLISTOP e NWLISTCF.

[![CI](https://github.com/rjmalves/inewave/actions/workflows/main.yml/badge.svg)](https://github.com/rjmalves/inewave/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/rjmalves/inewave/branch/main/graph/badge.svg?token=R9WPQHQGKF)](https://codecov.io/gh/rjmalves/inewave)
[![PyPI version](https://img.shields.io/pypi/v/inewave)](https://pypi.org/project/inewave/)
[![Python versions](https://img.shields.io/pypi/pyversions/inewave)](https://pypi.org/project/inewave/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentacao](https://img.shields.io/badge/docs-online-blue)](https://rjmalves.github.io/inewave)

O `inewave` é um pacote Python para manipulação dos arquivos de entrada e saída do programa [NEWAVE](http://www.cepel.br/pt_br/produtos/newave-modelo-de-planejamento-da-operacao-de-sistemas-hidrotermicos-interligados-de-longo-e-medio-prazo.htm). O NEWAVE é desenvolvido pelo [CEPEL](http://www.cepel.br) e utilizado para os estudos de planejamento e operação do Sistema Interligado Nacional (SIN).

## Funcionalidades

- Leitura e escrita dos arquivos de entrada do NEWAVE, com suporte a modificações programáticas de decks de PMO
- Leitura dos arquivos de saída do NEWAVE e dos programas auxiliares NWLISTCF e NWLISTOP
- Dados tabulares expostos como `DataFrame` do [pandas](https://pandas.pydata.org/), prontos para análise e visualização
- Interface orientada a objetos consistente: cada arquivo corresponde a uma classe com método `read` e, quando aplicável, método `write`
- Suporte a múltiplas versões de formato do mesmo arquivo, com seleção via argumento `version=` no método `read`
- Importação sob demanda (_lazy import_) para inicialização rápida mesmo com dezenas de classes disponíveis

## Exemplo Rapido

Leitura do arquivo de saída `pmo.dat` e acesso aos dados de convergência como DataFrame:

```python
from inewave.newave import Pmo

arq_pmo = Pmo.read("./pmo.dat")
arq_pmo.convergencia
```

Leitura de um arquivo de entrada, modificação de valores e escrita do resultado:

```python
from inewave.newave import Vazoes

arq_vazoes = Vazoes.read("./vazoes.dat")

# Sensibilidade: elevar todas as vazões históricas em 10%
arq_vazoes.vazoes *= 1.1

arq_vazoes.write("./vazoes_sensibilidade.dat")
```

## Instalacao

O `inewave` é compatível com Python 3.10, 3.11 e 3.12.

Instalação a partir do PyPI:

```
pip install inewave
```

Instalação da versão de desenvolvimento diretamente do repositório:

```
pip install git+https://github.com/rjmalves/inewave
```

## Documentacao

A documentação completa do pacote está disponível em [rjmalves.github.io/inewave](https://rjmalves.github.io/inewave) e inclui:

- [Tutorial](https://rjmalves.github.io/inewave/geral/tutorial.html) — exemplos de leitura, escrita e modificação de arquivos
- [Arquitetura](https://rjmalves.github.io/inewave/geral/arquitetura.html) — estrutura interna do pacote e do framework cfinterface
- [Perguntas Frequentes](https://rjmalves.github.io/inewave/geral/faq.html) — dúvidas comuns dos usuários
- [Guia de Desempenho](https://rjmalves.github.io/inewave/geral/desempenho.html) — características de performance e resultados de benchmarks
- [Referencia da API](https://rjmalves.github.io/inewave/referencia) — documentação de todas as classes e propriedades públicas

## Contribuindo

Contribuições são bem-vindas. Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para instruções sobre como configurar o ambiente de desenvolvimento, executar os testes e enviar pull requests.

## Licenca

Distribuído sob a licença [MIT](LICENSE.md).
