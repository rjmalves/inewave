# inewave

![tests](https://github.com/rjmalves/inewave/workflows/tests/badge.svg)  
[![codecov](https://codecov.io/gh/rjmalves/inewave/branch/main/graph/badge.svg?token=R9WPQHQGKF)](https://codecov.io/gh/rjmalves/inewave)

O `inewave` é um pacote Python para manipulação dos arquivos de entrada e saída do programa [NEWAVE](http://www.cepel.br/pt_br/produtos/newave-modelo-de-planejamento-da-operacao-de-sistemas-hidrotermicos-interligados-de-longo-e-medio-prazo.htm). O NEWAVE é desenvolvido pelo [CEPEL](http://www.cepel.br) e utilizado para os estudos de planejamento e operação do Sistema Interligado Nacional (SIN).

O inewave oferece:

- Meios para leitura dos arquivos de entrada e saída do NEWAVE e programas associados: NWLISTCF e NWLISTOP

- Facilidades para estudo e análise dos dados utilizando DataFrames do pandas

- Dados estruturados em modelos com o uso do paradigma de orientação a objetos (OOP)


## Instalação

O inewave é compatível com versões de Python >= 3.8.

É possível instalar a versão distribuída oficialmente com pip:

```
python -m pip install inewave
```

É possível realizar a instalação da versão de desenvolvimento fazendo o uso do Git.

```
pip install git+https://github.com/rjmalves/inewave
```

## Documentação

Guias, tutoriais e as referências podem ser encontrados no site oficial do pacote: https://rjmalves.github.io/inewave
