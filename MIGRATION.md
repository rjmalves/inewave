# Guia de Migração para v1.13.0

Este documento descreve as mudanças introduzidas no _inewave_ v1.13.0 e orienta
consumidores da biblioteca sobre o que deve ser atualizado em projetos existentes.

---

## 1. Requisitos de dependências

A v1.13.0 eleva os requisitos mínimos de todas as dependências diretas:

| Dependência | Versão mínima anterior | Versão mínima em v1.13.0 |
| ----------- | ---------------------- | ------------------------ |
| Python      | >= 3.10                | >= 3.10 (sem mudança)    |
| cfinterface | >= 1.8.x               | **>= 1.9.0**             |
| numpy       | >= 1.x                 | **>= 2.2.1**             |
| pandas      | >= 2.x                 | **>= 2.2.3**             |

A exigência de `cfinterface >= 1.9.0` é necessária para o suporte ao argumento
`version=` no método `read` e ao método `validate()`, ambos introduzidos nesta
versão. Projetos que fixam versões de dependências devem atualizar seus
`requirements.txt` ou `pyproject.toml` adequadamente.

---

## 2. Alterações de API sem quebra de compatibilidade

### 2.1 Argumento `version=` no método `read`

Arquivos que possuem mais de um formato suportado — identificados pela presença
do atributo de classe `VERSIONS` — agora aceitam o argumento nomeado `version=`
diretamente no método `read`, eliminando a necessidade de chamar `set_version`
antes da leitura:

```python
from inewave.nwlistop import Cmargmed

# Antes (ainda funciona, mantido por compatibilidade retroativa)
Cmargmed.set_version("28")
arq = Cmargmed.read("./cmarg001-med.out")

# Agora (idioma preferencial a partir da v1.13.0)
arq = Cmargmed.read("./cmarg001-med.out", version="28")
```

O valor passado para `version=` deve ser uma das chaves do dicionário `VERSIONS`
da respectiva classe (ver tabela abaixo). Caso `version=` seja omitido, o
comportamento padrão permanece o mesmo de versões anteriores: o arquivo é lido
com os blocos definidos em `BLOCKS`.

### 2.2 Classes com suporte a `version=` e seus valores válidos

| Classe                                       | Módulo             | Chaves válidas de `VERSIONS` |
| -------------------------------------------- | ------------------ | ---------------------------- |
| `Cmarg`                                      | `inewave.nwlistop` | `"27"`, `"29.4.1"`           |
| `Cmargmed`                                   | `inewave.nwlistop` | `"28"`, `"29.4.1"`           |
| `Pivarm`                                     | `inewave.nwlistop` | `"28.12"`, `"29.2"`          |
| `Pivarmincr`                                 | `inewave.nwlistop` | `"28.12"`, `"29.2"`          |
| `AvlCortesFpha` (descontinuada, ver seção 3) | `inewave.newave`   | `"28"`, `"28.16"`            |

Os valores de chave correspondem às versões do modelo NEWAVE em que houve
alteração de formato. Consulte a propriedade `VERSIONS` de cada classe para
verificar os valores disponíveis.

### 2.3 Método `validate()`

Todas as classes que possuem o atributo `VERSIONS` expõem o método `validate()`,
que compara os blocos efetivamente encontrados no arquivo lido com o conjunto de
blocos esperados para uma determinada versão, retornando um objeto
`VersionMatchResult` (do `cfinterface.versioning`):

```python
from cfinterface.versioning import VersionMatchResult
from inewave.nwlistop import Cmarg

arq = Cmarg.read("./cmarg001.out", version="27")
resultado: VersionMatchResult = arq.validate(version="27")

# Validação bem-sucedida: listas vazias indicam correspondência perfeita
assert resultado.missing_types == []
assert resultado.unexpected_types == []

# Detecção de incompatibilidade de versão
resultado_errado = arq.validate(version="29.4.1")
# resultado_errado.missing_types — blocos esperados mas não encontrados
# resultado_errado.unexpected_types — blocos encontrados mas não esperados
```

Isso é útil para diagnóstico quando o formato exato do arquivo gerado pelo
NEWAVE não é conhecido previamente.

### 2.4 Importações lazy nos módulos `inewave.newave` e `inewave.nwlistop`

Os módulos `inewave.newave` e `inewave.nwlistop` passaram a utilizar importações
lazy via `__getattr__` e `importlib.import_module`. Cada classe de arquivo é
carregada somente quando referenciada pela primeira vez, o que reduz
significativamente o tempo de importação inicial do pacote.

O mecanismo é completamente transparente para o usuário final: a sintaxe de
importação não muda:

```python
from inewave.newave import Pmo      # continua funcionando normalmente
from inewave.nwlistop import Cmarg  # idem
```

---

## 3. Classes descontinuadas (deprecated)

### 3.1 Blocos internos: `ValoresSerie` e `ValoresSeriePatamar`

As classes `ValoresSerie`
(`inewave.nwlistop.modelos.blocos.valoresserie`) e `ValoresSeriePatamar`
(`inewave.nwlistop.modelos.blocos.valoresseriepatamar`) foram marcadas como
descontinuadas. Ao instanciar qualquer subclasse que as utilize diretamente, um
`DeprecationWarning` será emitido:

```
DeprecationWarning: ValoresSerie is deprecated. Use TabelaSerieAnual instead.
DeprecationWarning: ValoresSeriePatamar is deprecated. Use TabelaSeriePatamarAnual instead.
```

Estas classes são substituídas por `TabelaSerieAnual`
(`inewave.nwlistop.modelos.blocos.tabela_serie_anual`) e
`TabelaSeriePatamarAnual`
(`inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual`),
respectivamente. As substitutas produzem DataFrames com colunas, tipos e valores
idênticos, portanto o código que consome a propriedade `.valores` das classes de
arquivo **não precisa ser alterado**.

O aviso afeta apenas desenvolvedores que estendem o framework criando novos
arquivos com blocos customizados baseados nas classes antigas. Nenhum prazo de
remoção está definido para estas classes.

### 3.2 Classe de arquivo `AvlCortesFpha` (newave)

A classe `AvlCortesFpha` (`inewave.newave.avl_cortesfpha_nwv`) já estava
marcada como descontinuada em versões anteriores (substituída por `FphaCortes`
em `inewave.newave.fpha_cortes`). O aviso de `DeprecationWarning` é emitido na
instanciação. Nenhum prazo de remoção está definido.

---

## 4. Mudanças internas

Esta seção descreve mudanças na camada interna da biblioteca. Consumidores que
utilizam apenas a API pública (`from inewave.newave import ...`,
`from inewave.nwlistop import ...`) não são afetados.

### 4.1 Novas classes base: `TabelaSerieAnual` e `TabelaSeriePatamarAnual`

As classes `TabelaSerieAnual`
(`inewave.nwlistop.modelos.blocos.tabela_serie_anual`) e
`TabelaSeriePatamarAnual`
(`inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual`) foram introduzidas
como bases para todos os blocos de dados tabulares agrupados por ano dos arquivos
do NWLISTOP. Elas utilizam `TabularParser` do `cfinterface` para leitura e
escrita, substituindo a implementação manual linha a linha das classes
descontinuadas.

### 4.2 Classes base para arquivos: `_ArquivoSerieBase` e `_ArquivoSeriePatamarBase`

As classes `_ArquivoSerieBase`
(`inewave.nwlistop.modelos.arquivos._base_serie`) e
`_ArquivoSeriePatamarBase`
(`inewave.nwlistop.modelos.arquivos._base_serie_patamar`) centralizam a lógica
de montagem do DataFrame `valores` para todos os arquivos de série do NWLISTOP
sem e com patamar, respectivamente. Subclasses que antes reimplementavam
`_monta_tabela` ou a propriedade `valores` passam a herdar estas implementações.

### 4.3 Uso de `IO[Any]` nas assinaturas de leitura e escrita

As assinaturas dos métodos `read` e `write` dos blocos internos utilizam
`IO[Any]` (`from typing import IO, Any`) de forma consistente em todos os blocos
das novas classes base, alinhando-se ao padrão do `cfinterface` e satisfazendo
a verificação estrita do `mypy`.

### 4.4 Verificação estrita de tipos com `mypy`

A configuração `strict = true` do `mypy` foi ativada para todos os submódulos
do pacote (`inewave.newave`, `inewave.nwlistop`, `inewave.nwlistcf`,
`inewave._utils`, `inewave.libs`) via `pyproject.toml`. Contribuidores que
adicionarem novos módulos devem garantir que o código passe em
`mypy --strict` antes de submeter um pull request.

---

## 5. Desempenho

### 5.1 Importações lazy

Ver seção 2.4. A suíte de benchmarks em `benchmarks/` contém medições
reproduzíveis do custo de importação.

### 5.2 Suíte de benchmarks

O repositório inclui uma suíte de benchmarks em `benchmarks/`. Consulte
`benchmarks/README.md` para a descrição dos scripts e instruções de execução.
Os resultados mais recentes são registrados em `benchmarks/benchmark_results.md`.

---

## 6. Testes

### 6.1 Cobertura e quantidade

A v1.13.0 conta com **1140 testes** coletados pelo pytest, cobrindo leitura,
escrita, round-trip (leitura seguida de escrita com comparação de igualdade) e
validação de versão para todos os arquivos suportados.

Os testes de round-trip verificam que `Arquivo.read(path)` seguido de
`arq.write(path_saida)` e `Arquivo.read(path_saida)` produz um objeto igual ao
original (via `__eq__`), garantindo que a serialização é fiel ao formato do
arquivo fonte.

### 6.2 Execução paralela com `pytest-xdist`

Os testes podem ser executados em paralelo utilizando `pytest-xdist`:

```bash
pytest -n auto
```

A separação entre testes de leitura isolados (que utilizam `mock_open`) e testes
de round-trip (que operam sobre arquivos de mock em disco em `tests/mocks/`)
garante que não há condições de corrida entre os workers.

### 6.3 Filtragem de avisos de descontinuação nos testes

O `pyproject.toml` configura o pytest para suprimir `DeprecationWarning`
originados em `inewave.nwlistop`, evitando que os avisos das classes
`ValoresSerie` e `ValoresSeriePatamar` poluam a saída dos testes:

```toml
[tool.pytest.ini_options]
filterwarnings = [
    "ignore::DeprecationWarning:inewave.nwlistop",
]
```

Testes que precisam verificar a emissão dos avisos devem usar
`warnings.catch_warnings()` com `simplefilter("always")` explicitamente.
