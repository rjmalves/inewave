# inewave

O `inewave` é um pacote Python para manipulação dos arquivos de entrada e saída do programa [NEWAVE](http://www.cepel.br/pt_br/produtos/newave-modelo-de-planejamento-da-operacao-de-sistemas-hidrotermicos-interligados-de-longo-e-medio-prazo.htm), desenvolvido pelo [CEPEL](http://www.cepel.br) e utilizado para os estudos de planejamento e operação do Sistema Interligado Nacional (SIN).

O inewave oferece:

- Meios para leitura dos arquivos de entrada e saída do NEWAVE e programas associados: NWLISTCF e NWLISTOP

- Armazenamento e processamento de dados otimizados com o uso de NumPy

- Dados estruturados em modelos com o uso do paradigma de orientação a objetos (OOP)

- Utilidades de escritas dos arquivos de entrada do NEWAVE para elaboração automatizada de estudos

Com inewave é possível ler os arquivos de texto, característicos do NEWAVE, e salvar as informações em pickle, para poupar processamento futuro e reduzir o tempo de execução.

## Instalação

O inewave é compatível com versões de Python >= 3.5. A única dependência formal é o módulo NumPy, que deve sempre ser mantido na versão mais atualizada para a distribuição de Python instalada.

Em posse de uma instalação local de Python, é recomendado que se use um ambiente virtual para instalação de módulos de terceiros, sendo que o inewave não é uma exceção. Para mais detalhes sobre o uso de ambientes virtuais, recomenda-se a leitura do recurso oficial de Python para ambientes virtuais: [venv](https://docs.python.org/3/library/venv.html).

```
python -m pip install inewave
```

## Documentação

Guias, tutoriais e as referências podem ser encontrados no site oficial do pacote: https://rjmalves.github.io/inewave
