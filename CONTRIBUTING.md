# Contribuindo para o inewave

Obrigado pelo interesse em contribuir com o _inewave_! Este guia descreve o fluxo de trabalho esperado, as ferramentas utilizadas e as convenções adotadas no projeto.

## Configuracao do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.10 ou superior
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes e ambientes)
- Git

### Instalacao

Clone o repositório e instale todas as dependências de desenvolvimento (testes, lint, tipagem e documentação):

```sh
$ git clone https://github.com/rjmalves/inewave.git
$ cd inewave
$ uv sync --extra dev
```

O grupo `dev` é um meta-grupo que instala automaticamente os grupos `test`, `lint` e `docs`.

### Configuracao dos hooks de pre-commit

Após instalar as dependências, ative os hooks de pre-commit para garantir que linting e formatação sejam verificados automaticamente a cada commit:

```sh
$ uv run pre-commit install
```

Os hooks configurados em `.pre-commit-config.yaml` executam `ruff` (lint + formatação) automaticamente no momento do commit. O `mypy` está configurado como hook de estágio manual — veja a seção abaixo para executá-lo explicitamente.

---

## Ferramentas de Qualidade de Codigo

O projeto utiliza `ruff` para linting e formatação, e `mypy` para verificação de tipos estáticos. Todos esses passos são executados no CI em jobs paralelos.

### Linting

```sh
$ uv run ruff check ./inewave
```

Para corrigir automaticamente os problemas que o ruff consegue resolver:

```sh
$ uv run ruff check --fix ./inewave
```

### Formatacao

```sh
$ uv run ruff format ./inewave
```

Para verificar sem aplicar mudanças:

```sh
$ uv run ruff format --check ./inewave
```

### Verificacao de tipos (mypy)

O projeto usa mypy em modo estrito para todos os submódulos de `inewave`. Para executar a verificação de tipos:

```sh
$ uv run mypy ./inewave
```

O mypy também pode ser executado como hook manual do pre-commit:

```sh
$ uv run pre-commit run mypy --hook-stage manual
```

### Execucao completa antes de um push

Antes de abrir um pull request, execute os três passos de qualidade para garantir que o CI passará:

```sh
$ uv run ruff check ./inewave
$ uv run ruff format ./inewave
$ uv run mypy ./inewave
```

---

## Executando Testes

O projeto usa `pytest` com `pytest-xdist` para execução paralela e `pytest-cov` para cobertura de código.

### Execucao básica

```sh
$ uv run pytest ./tests
```

### Execucao paralela

Para acelerar a execução dos testes usando todos os núcleos disponíveis:

```sh
$ uv run pytest -n auto ./tests
```

### Execucao com cobertura

```sh
$ uv run pytest --cov=inewave ./tests
```

Para gerar um relatório XML (formato utilizado no CI para envio ao Codecov):

```sh
$ uv run pytest --cov-report=xml --cov=inewave ./tests
```

O CI executa os testes em matriz para Python 3.10, 3.11 e 3.12. Recomenda-se testar localmente na versão mais antiga suportada (3.10) caso haja dúvidas sobre compatibilidade.

---

## Convencoes de Codigo

### Nomenclatura de classes

Cada arquivo de entrada ou saída do modelo NEWAVE é mapeado para uma classe Python. O nome da classe segue o nome do arquivo correspondente, convertido para `PascalCase`. Abreviações presentes nos nomes dos arquivos são preservadas na conversão. Exemplos:

- `arquivos.dat` → classe `Arquivos`
- `confhd.dat` → classe `Confhd`
- `earmfpXXX.out` → classe `Earmfp`

### Nomenclatura de propriedades e colunas

Propriedades das classes e colunas de `DataFrame` devem ser nomeadas em `snake_case`. Evite ambiguidades:

- Atributos de usinas: use `nome_usina` e `codigo_usina`
- Atributos de submercados: use `nome_submercado` e `codigo_submercado`
- Atributos de REE: use `nome_ree` e `codigo_ree`

### Tipagem estatica

Toda variável deve ter tipo inferível ou anotado explicitamente. Não use `Any` sem justificativa. O mypy é executado em modo estrito (`strict = true`) para todos os submódulos do `inewave`.

### Docstrings e comentarios

Docstrings e comentários devem ser escritos em **português brasileiro**.

### Formatacao de dados tabulares

Sempre que possível, os dados lidos dos arquivos devem ser retornados em `DataFrame` no formato normal: uma coluna para cada dimensão (por exemplo, `data`, `patamar`, `serie`, `valor`), mesmo quando o arquivo original apresenta o dado em formato pivotado.

---

## Modelagem de Arquivos com cfinterface

O _inewave_ é desenvolvido sobre o framework [cfinterface](https://github.com/rjmalves/cfi), que classifica os arquivos processados em três tipos:

- **BlockFile**: arquivos estruturados em blocos com padrão de início identificável (e opcionalmente de fim). Um mesmo bloco pode aparecer múltiplas vezes. Exemplos: `pmo.dat`, `parp.dat`.
- **SectionFile**: arquivos com seções fixas que sempre aparecem na mesma ordem e são obrigatórias. Exemplos: `dger.dat`, `sistema.dat`.
- **RegisterFile**: arquivos estruturados em registros de linha única com formato constante. Exemplo: `modif.dat`.

Cada tipo pode ser textual ou binário — essa informação é declarada na classe que modela o arquivo.

Para uma descrição completa do framework com referências cruzadas à API do cfinterface, consulte a [documentação Sphinx do projeto](https://rjmalves.github.io/inewave/).

---

## Fluxo de Pull Request

1. **Fork** o repositório para sua conta no GitHub.
2. **Crie uma branch** a partir de `main` com um nome descritivo:
   ```sh
   $ git checkout -b minha-contribuicao
   ```
3. **Implemente** as alterações seguindo as convenções deste guia.
4. **Execute** os passos de qualidade e testes localmente (veja seções acima).
5. **Commit** as alterações com uma mensagem descritiva:
   ```sh
   $ git commit -m "fix: corrige leitura do campo X no arquivo Y"
   ```
6. **Push** para o seu fork:
   ```sh
   $ git push origin minha-contribuicao
   ```
7. **Abra um Pull Request** para a branch `main` do repositório original.
8. **Aguarde o CI**: os jobs de lint, typecheck, test (Python 3.10–3.12) e docs devem passar antes da revisão.

Dúvidas ou sugestões podem ser abertas como [Issues](https://github.com/rjmalves/inewave/issues) no repositório.
