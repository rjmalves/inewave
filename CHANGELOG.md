# Changelog

Todas as mudancas notaveis neste projeto serao documentadas neste arquivo.

O formato e baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semantico](https://semver.org/lang/pt-BR/).

## [1.14.1] - 2026-07-01

### Corrigido

- Correção na leitura da geração térmica por submercado e patamar de carga na classe `Forward` (propriedade `geracao_termica`): os rótulos de usina e patamar agora respeitam o agrupamento das classes térmicas por submercado, corrigindo o desalinhamento que ocorria quando os submercados possuíam quantidades diferentes de classes térmicas [#121](https://github.com/rjmalves/inewave/pull/121) (@beralbdom).

### Modificado

- Detecção do formato do arquivo `hidr.dat` na classe `Hidr` por correspondência exata do tamanho do arquivo (320 ou 600 registros de 792 ou 832 bytes), em vez de divisibilidade pelo tamanho do registro. A mudança elimina a ambiguidade entre os formatos e passa a sinalizar com aviso os arquivos truncados ou de tamanho não padronizado, antes lidos silenciosamente com um número incorreto de registros.

## [1.14.0] - 2026-06-09

### Adicionado

- Suporte ao formato estendido do arquivo `hidr.dat`, com os coeficientes dos polinômios cota-volume e cota-área em precisão dupla (registros de 832 bytes), através do novo registro `RegistroUHEHidrF64`. A classe `Hidr` detecta o formato automaticamente pelo tamanho do arquivo (792 ou 832 bytes), com possibilidade de forçar via `version="f32"` ou `version="f64"`.
- Propriedade `tamanho_registro` e método `converte_tamanho_registro` na classe `Hidr`, permitindo inspecionar e converter entre os formatos de precisão simples e dupla.
- Coluna `fonte` na propriedade `usinas_nao_simuladas` da classe `Patamar`, preservando o rótulo textual do bloco de usinas não simuladas (consistente com `Sistema.geracao_usinas_nao_simuladas`).

### Corrigido

- Correção na leitura da classe `Patamar` para decks de PDE, em que os cabeçalhos do bloco de usinas não simuladas contêm um rótulo textual da fonte (p.ex. `1 1 SUDESTE BIO`), antes interpretados incorretamente como linhas de dados [#119](https://github.com/rjmalves/inewave/issues/119) (@saulo1305).

### Modificado

- Identificação de linhas de cabeçalho de subsistema/bloco por conteúdo (ausência de valores nas colunas mensais) em vez de tamanho da linha, nos blocos das classes `Patamar` e `Sistema`, tornando a leitura robusta a rótulos textuais opcionais nos cabeçalhos.
- Escrita determinística (ordenada pelas chaves de agrupamento) e comparação de blocos (`__eq__`) independente da ordem das linhas nas classes `Patamar` e `Sistema`.

## [1.13.2] - 2026-04-10

### Modificado

- Escrita explícita dos períodos na opção 4 do arquivo nwlistop.dat [#117](https://github.com/rjmalves/inewave/pull/117) (@saulo1305).

### Corrigido

- Correção na modelagem da classe `Modif` para processar corretamente campos livres com número de espaços variáveis [#116](https://github.com/rjmalves/inewave/issues/116)

## [1.13.1] - 2026-03-08

### Modificado

- Requisito mínimo de Python atualizado de `>= 3.10` para `>= 3.11`, acompanhando o fim de suporte do pandas para Python 3.10.
- Requisito mínimo de pandas atualizado de `>= 2.2.3` para `>= 3.0.0`.

## [1.13.0] - 2026-03-08

### Adicionado

- Suporte ao argumento `version=` no método `read` das classes com múltiplos formatos (`Cmarg`, `Cmargmed`, `Pivarm`, `Pivarmincr`, `AvlCortesFpha`), eliminando a necessidade de chamar `set_version` separadamente.
- Novo método `validate(version=...)` para verificar se os blocos encontrados em um arquivo correspondem ao conjunto esperado para uma dada versão, retornando um `VersionMatchResult` com diagnóstico de tipos ausentes e inesperados.
- Introdução das classes base `TabelaSerieAnual` e `TabelaSeriePatamarAnual` para blocos de dados tabulares do NWLISTOP, substituindo a implementação manual linha a linha com uso de `TabularParser` do `cfinterface`.
- Introdução das classes base `_ArquivoSerieBase` e `_ArquivoSeriePatamarBase` para centralizar a lógica de montagem da propriedade `valores` em todos os arquivos de série do NWLISTOP.
- Ativação de `mypy --strict` para todos os submódulos do pacote (`inewave.newave`, `inewave.nwlistop`, `inewave.nwlistcf`, `inewave._utils`, `inewave.libs`).
- Suíte de benchmarks em `benchmarks/` para medição de tempo de importação e leitura de arquivos representativos, com resultados registrados em `benchmarks/benchmark_results.md`.
- Suporte à execução paralela de testes com `pytest-xdist` (`pytest -n auto`).
- Total de 1140 testes cobrindo leitura, escrita, round-trip e validação de versão para todos os arquivos suportados.

### Modificado

- Adoção de importações lazy via `__getattr__` e `importlib` em `inewave.newave` e `inewave.nwlistop`, reduzindo o custo de importação inicial dos submódulos.
- Atualização das dependências mínimas: `cfinterface >= 1.9.0`, `numpy >= 2.2.1`, `pandas >= 2.2.3`.

### Descontinuado

- Classes `ValoresSerie` e `ValoresSeriePatamar` marcadas como descontinuadas com emissão de `DeprecationWarning` na instanciação.

## [1.12.1] - 2026-03-05

### Modificado

- Restrição da dependência `cfinterface` para versões `<=1.8.3`

### Corrigido

- Correção na leitura do arquivo `hidr.dat` com campos vazios (@beralbdom)

## [1.12.0] - 2026-02-02

### Modificado

- Atualização no processamento dos `parp.dat`, `parpeol.dat`, `parpvaz.dat` e `penalid.dat` para compatibilização com pandas `>=3.0.0`.

## [1.11.2] - 2025-12-03

### Corrigido

- Correção no arquivo `dger.dat` em relação aos campos adicionados recentemente ao final do arquivo

## [1.11.1] - 2025-11-10

### Corrigido

- Correção no arquivo `dger.dat` em relação ao número de aberturas variável por estágio

## [1.11.0] - 2025-11-05

### Adicionado

- Suporte ao processamento do arquivo `eliminacao_cortes.dat`
- Adicionados mais exemplos para a documentação

### Modificado

- Atualização do arquivo `arquivos.dat` com as linhas adicionais relativas ao `volref_saz.dat` e `eliminacao_cortes.dat`

### Corrigido

- Correção de tipagem estática para mypy

## [1.10.4] - 2025-09-20

### Adicionado

- Suporte a processar um número variável de etapas no arquivo newave.tim (@rdlobato)

### Modificado

- Melhor processamento de variáveis ausentes ao caso no arquivo MEDIAS-USIH.CSV (@rdlobato)

### Corrigido

- Correção na escrita do arquivo `ghmin.dat` em linhas relativas aos anos "POS" [#106](https://github.com/rjmalves/inewave/issues/106) (@joaoCalmon).
- Correção de tipagem estática para mypy

## [1.10.3] - 2025-08-04

### Corrigido

- Correção na leitura do arquivo `sistema.dat` em arquivos gerados com espaços adicionais nas linhas dos blocos [#104](https://github.com/rjmalves/inewave/issues/106).

## [1.10.2] - 2025-07-14

### Corrigido

- Correção na escrita do arquivo `nwlistop.dat` para suportar o numero de variaveis totais da opção 2 do programa NWLISTOP [#104](https://github.com/rjmalves/inewave/issues/104).

## [1.10.1] - 2025-07-09

### Corrigido

- Correção na leitura dos arquivos `c_adic.dat` e `sistema.dat` para considerar nomes completos de submercados [#101](https://github.com/rjmalves/inewave/issues/101).
- Correção no nome da coluna `codigo_usina` para `codigo_posto` no arquivo `vazpast.dat`

## [1.10.0] - 2025-01-02

### Adicionado

- Suporte aos campos de restrições elétricas especiais existentes na versão 30 do modelo NEWAVE
- Suporte a obter a versão do modelo NEWAVE utilizada a partir do arquivo newave.tim (@eduardomdc)

### Modificado

- Gestão do projeto através de arquivo `pyproject.toml` em substituição ao par `setup.py` + `requirements.txt`
- Melhorias na documentação, incluindo exemplos de arquivos das LIBS [#94](https://github.com/rjmalves/inewave/issues/94)
- Requisito de versão de Python atualizado para `>=3.10`

### Corrigido

- Correção no processamento da energia armazenada inicial por subsistema do `dger.dat` [#97](https://github.com/rjmalves/inewave/issues/97).

## [1.9.2] - 2024-09-19

### Adicionado

- Versionamento dos arquivos `cmargXXX.out` e `cmargXXX-med.out` do NWLISTOP devido o aumento de dígitos impressos.

## [1.9.1] - 2024-07-18

### Corrigido

- Correção nos tamanhos dos campos de vazão desviada do arquivo `dsvagua.dat`

## [1.9.0] - 2024-07-18

### Adicionado

- Suporte ao arquivo do NWLISTOP com informação do Custo Futuro por cenário (`custo_futuro.out`)
- Suporte a arquivos do NWLISTOP renomeados: `viol_eletrica.out`, `cviol_eletrica.out`, `viol_pos_vretiruh.out`, `viol_neg_vretiruh.out`.

### Modificado

- Descontinuado o uso do `pylama` como linter para garantir padrões PEP de código devido à falta de suporte em Python >= 3.12. Adoção do [ruff](https://github.com/astral-sh/ruff) em substituição.

## [1.8.1] - 2024-05-08

### Corrigido

- Correção da leitura dos arquivos `pivarm.out` e `pivarmincr.out` do NWLISTOP [#87](https://github.com/rjmalves/inewave/issues/87).

## [1.8.0] - 2024-04-24

### Adicionado

- Suporte à obtenção da versão do modelo utilizada, impressa no arquivo `pmo.dat`.

### Modificado

- Arquivos do modelo NEWAVE renomeados: `nwv_avl_evap.csv` (`evap_avl_desv.csv`), `nwv_cortes_evap.csv` (`evap_cortes.csv`), `nwv_eco_evap.csv` (`evap_eco.csv`), `avl_cortesfpha_nwv.csv` (`fpha_cortes.csv`), `eco_fpha.csv` (`fpha_eco_.csv`), `avl_desvfpha_v_q.csv` (`fpha_avl_desv_v_q.csv`) e `avl_desvfpha_s.csv` (`fpha_avl_desv_s.csv`)
- Arquivos do NWLISTOP renomeados: `dlpptbmax.out` (`viol_lpp_tbmax.out`), `dlpptbmaxm.out` (`viol_lpp_tbmaxm.out`), `dlpptbmaxsin.out` (`viol_lpp_tbmaxsin.out`), `dlppdfmax.out` (`viol_lpp_dfmax.out`), `dlppdfmaxm.out` (`viol_lpp_dfmaxm.out`), `dlppdfmaxsin.out` (`viol_lpp_dfmaxsin.out`), `vevmin.out` (`viol_evmin.out`), `vevminm.out` (`viol_evminm.out`), `vevminsin.out` (`viol_evminsin.out`), `deletricasin.out` (`viol_eletricasin.out`), `celetricasin.out` (`cviol_eletricasin.out`), `c_v_rhq.out` (`cviol_rhq.out`), `c_v_rhq_s.out` (`cviol_rhq_sin.out`), `c_v_rhv.out` (`cviol_rhv.out`), `c_v_rhv_s.out` (`cviol_rhv_sin.out`), `vghmin.out` (`viol_ghmin.out`), `vghminm.out` (`viol_ghminm.out`), `vghminsin.out` (`viol_ghminsin.out`), `vghminuh.out` (`viol_ghminuh.out`), `vagua.out` (`valor_agua.out`), `depminuh.out` (`viol_vazmin.out`), `dvazmax.out` (`viol_vazmax.out`), `desvuh.out` (`vretiradauh.out`), `vturuh.out` (`qturuh.out`), `vertuh.out` (`qvertuh.out`), `vdesviouh.out` (`qdesviouh.out`), `dfphauh.out` (`viol_fpha.out`), `dtbmax.out` (`viol_turbmax.out`), `dtbmin.out` (`viol_turbmin.out`), `dpos_evap.out` (`viol_pos_evap.out`), `dneg_evap.out` (`viol_neg_evap.out`).

### Descontinuado

- Nomes de arquivos e formatos atualizados para compatibilidade com a versão 29.3 do modelo NEWAVE. Classes que implementam os arquivos antigos foram marcadas como `deprecated`, mas ainda existem no módulo.

## [1.7.5] - 2024-04-12

### Modificado

- Dependência da cfinterface atualizada para [v1.6.0](https://github.com/rjmalves/cfi/releases/tag/v1.6.0)
- Uso de `__slots__` nas definições de componentes

## [1.7.4] - 2024-04-12

### Corrigido

- Fix na leitura dos blocos de geração mínima e máxima de usinas térmicas do `pmo.dat` [#83](https://github.com/rjmalves/inewave/issues/83)
- Fix na leitura do arquivo `energias.dat` [#82](https://github.com/rjmalves/inewave/issues/82)

## [1.7.3] - 2024-03-01

### Modificado

- Atualização do formato da leitura do arquivo `vevapuhXXX.out` do nwlistop para maior precisão.

## [1.7.2] - 2024-03-01

### Modificado

- Atualização do formato da leitura dos arquivos `dpos_evapXXX.out` e `dneg_evapXXX.out` do nwlistop para notação científica.

### Corrigido

- Fix na leitura dos blocos de valores de penalidades do `pmo.dat` em casos com períodos pós-estudo

## [1.7.1] - 2024-02-26

### Corrigido

- Fix na leitura do bloco de configurações por estágio do `pmo.dat` no caso do relatório conter apenas um bloco [#79](https://github.com/rjmalves/inewave/issues/79)

## [1.7.0] - 2024-02-23

### Adicionado

- Suporte aos blocos de energia armazenada máxima por REE, geração térmica mínima e máxima por UTE no `pmo.dat` [#77](https://github.com/rjmalves/inewave/issues/77), [#76](https://github.com/rjmalves/inewave/issues/76)
- Suporte ao arquivo `vazinat.dat` [#74](https://github.com/rjmalves/inewave/issues/74)

### Modificado

- Refactor da leitura dos arquivos `MEDIAS-*` do NWLISTOP, com novo suporte aos `MEDIAS-REE`, `MEDIAS-USIH`, `MEDIAS-USIT`, `MEDIAS-USIE`, `MEDIAS-REP`, `MEDIAS-RHQ` e `MEDIAS-RHV` [#78](https://github.com/rjmalves/inewave/issues/78)
- Atualizaçao da documentação das propriedades do modelo do `sistema.dat` [#70](https://github.com/rjmalves/inewave/issues/70)

## [1.6.0] - 2024-02-19

### Adicionado

- Suporte aos blocos com valores de penalidades por tipo de violação no arquivo `pmo.dat`
- Suporte aos novos arquivos do `NWLISTOP` associados à evaporação: `vevapuhXXX.out`, `dpos_evapXXX.out`, `dneg_evapXXX.out` e ao arquivo `gh_fphexatXXX.out`.

## [1.5.7] - 2024-01-17

### Adicionado

- Suporte à leitura do arquivo `avl_cortesfpha_nwv.csv`, que mudou de sintaxe na versão `28.16` do NEWAVE

## [1.5.6] - 2024-01-05

### Corrigido

- Fix na modelagem do arquivo `dger.dat`, na posição do campo de agregação da simulação final.

## [1.5.5] - 2024-01-04

### Corrigido

- Fix na construção dos registros específicos do `modif.dat`, que não permitiam atribuir valores a propriedades de registros criados fora do contexto de leitura.

## [1.5.4] - 2024-01-04

### Corrigido

- Fix na modelagem do arquivo `modif.dat` para modelar de maneira "exata" os demais registros suportados, exceto o registro USINA, devido ao campo de comentário com nome da usina permitir espaços.

## [1.5.3] - 2024-01-02

### Corrigido

- Fix na modelagem do arquivo `modif.dat` para modelar de maneira "exata" os registros VOLMIN e VOLMAX, que possuem posição livre dos campos de dados, separados por espaços.

## [1.5.2] - 2024-01-02

### Corrigido

- Fix na modelagem do arquivo `modif.dat` para listar as modificações de uma usina

## [1.5.1] - 2023-12-22

### Corrigido

- Fix nas colunas do DataFrame das restrições do arquivo `re.dat`

## [1.5.0] - 2023-10-11

### Adicionado

- Suporte aos arquivos e mnemônicos faltantes para ter suporte total à versão `28.16.1` do modelo NEWAVE
- Novo arquivo de entrada suportados: `volref_saz.dat`
- Novos dados das LIBS: restrições RHV e RHQ, produtibilidade e perdas variáveis, FPHA, polinjus.
- Novos arquivos do NWLISTOP suportados: `c_v_rhqXXX.out`, `c_v_rhvXXX.out`, `cbombXXX.out`, `cbombsin.out`, `celetricas.out`, `deletricas.out`, `form_rhqXXX.out`, `form_rhvXXX.out`, `ghmax_fphaXXX.out`, `ghmax_fphcXXX.out`, `pivarmincrXXX.out`, `vbombXXX.out`, `viol_rhqXXX.out`, `viol_rhvXXX.out`.

### Modificado

- Refactor da modelagem utilizada para dados provenientes das LIBS: criado o submódulo `libs`, de forma que o usuário possa realizar a importação com `from inewave.libs import ...`.
- Modelagem de entidades das LIBS não é feita baseada nos arquivos fornecidos nos casos de exemplo das versões do modelo, mas sim baseado nas entidades envolvidas na informação, semelhante à divisão feita no site da documentação oficial [LIBS](https://see.cepel.br/manual/libs/latest/index.html)

## [1.4.0] - 2023-09-29

### Adicionado

- Suporte a arquivos do NWLISTOP necessários para fechamento de balanço hídrico de REE: `ghidrXXX.out`, `ghidrmXXX.out`, `ghidrsin.out`, `edesvcXXX.out`, `edesvcmXXX.out`, `edesvcsin.out`, `evapoXXX.out`, `evapomXXX.out`, `evaporsin.out`, `vmortXXX.out`, `vmortmXXX.out`, `vmortsin.out`, `mevminXXX.out`, `mevminmXXX.out`, `mevminsin.out`.

## [1.3.0] - 2023-09-15

### Adicionado

- Suporte a novos arquivos do NWLISTOP presentes da versão 28.15.3 do NEWAVE: cotas de montante e jusante por UHE e altura de queda líquida por UHE.
- Suporte aos arquivos de retirada de água e desvio de água por UHE do NWLISTOP

## [1.2.2] - 2023-09-15

### Modificado

- Otimizada a formatação do dataframes do NWLISTOP.

### Corrigido

- Fix no processamento de arquivos por patamar do NWLISTOP: alguns arquivos possuíam desalinhamento nos campos das séries.

## [1.2.1] - 2023-09-14

### Corrigido

- Fix na leitura do bloco de energia armazenada do `pmo.dat`: remoção de caracteres especiais do nome do último REE.

## [1.2.0] - 2023-09-14

### Adicionado

- Suporte à leitura do arquivo `eco_fpha.dat`
- Suporte à leitura do arquivo `pivarmXXX.out` do NWLISTOP
- Suporte à leitura dos campos de energia armazenada inicial e volume armazenado inicial do `pmo.dat`

### Modificado

- Campos do `dger.dat` atualizados para versão 28.15.2 do NEWAVE.

### Corrigido

- Fix na leitura do `dger.dat`: o modelo esperava a linha de "COMP. CORR. CRUZ.", que não está presente em todas as versões do modelo. Foi compatibilizado para esperar o formato das versões oficiais.

## [1.1.2] - 2023-08-28

### Corrigido

- Hotfix na leitura do `pmo.dat`: o bloco de configurações para cada estágio não suportava casos com mais de 100 configurações devido a um erro no modelo da linha.

## [1.1.1] - 2023-08-25

### Corrigido

- Hotfix na leitura do `pmo.dat`: o bloco de custos passou a ter mais de 30 linhas, que era o limite do array alocado. Passado para 100.

## [1.1.0] - 2023-08-24

### Modificado

- Conversão dos campos dos arquivos de entrada que representavam informações de datas como `int` para `datetime`
- Padronização de todos os arquivos de entrada que possuíam informações como `DataFrame` para formato normal
- Padronização de blocos do `pmo.dat`, `parp.dat`, `parpeol.dat` e `parpvaz.dat` para serem modelados como `DataFrame` em formatos normais.

## [1.0.0] - 2023-08-02

### Adicionado

- Primeira major release
- Suporte à leitura e escrita todos os arquivos de entrada utilizados oficialmente no modelo NEWAVE
- Suporte à leitura da maioria dos arquivos de saída do modelo NEWAVE, NWLISTCF e NWLISTOP

### Descontinuado

- Métodos le_arquivo e escreve_arquivo deprecados

## [0.0.98] - 2023-08-01

### Adicionado

- rc0 da primeira major release (v1.0.0)
- Suporte à leitura e escrita todos os arquivos de entrada utilizados oficialmente no modelo NEWAVE
- Suporte à leitura da vasta maioria dos arquivos de saída do modelo NEWAVE, NWLISTCF e NWLISTOP
- Métodos le_arquivo e escreve_arquivo ainda não deprecados

### Modificado

- Nomes das colunas dos dataframes padronizados para `snake_case`
- Nomes das classes padronizados para `PascalCase`
- Arquivos do NWLISTOP processados para formato normal de séries temporais
- Dependência da cfinterface atualizada para [v1.5.2](https://github.com/rjmalves/cfi/releases/tag/v1.5.2)

[1.13.1]: https://github.com/rjmalves/inewave/compare/v1.13.0...v1.13.1
[1.13.0]: https://github.com/rjmalves/inewave/compare/v1.12.1...v1.13.0
[1.12.1]: https://github.com/rjmalves/inewave/compare/v1.12.0...v1.12.1
[1.12.0]: https://github.com/rjmalves/inewave/compare/v1.11.2...v1.12.0
[1.11.2]: https://github.com/rjmalves/inewave/compare/v1.11.1...v1.11.2
[1.11.1]: https://github.com/rjmalves/inewave/compare/v1.11.0...v1.11.1
[1.11.0]: https://github.com/rjmalves/inewave/compare/v1.10.4...v1.11.0
[1.10.4]: https://github.com/rjmalves/inewave/compare/v1.10.3...v1.10.4
[1.10.3]: https://github.com/rjmalves/inewave/compare/v1.10.2...v1.10.3
[1.10.2]: https://github.com/rjmalves/inewave/compare/v1.10.1...v1.10.2
[1.10.1]: https://github.com/rjmalves/inewave/compare/v1.10.0...v1.10.1
[1.10.0]: https://github.com/rjmalves/inewave/compare/v1.9.2...v1.10.0
[1.9.2]: https://github.com/rjmalves/inewave/compare/v1.9.1...v1.9.2
[1.9.1]: https://github.com/rjmalves/inewave/compare/v1.9.0...v1.9.1
[1.9.0]: https://github.com/rjmalves/inewave/compare/v1.8.1...v1.9.0
[1.8.1]: https://github.com/rjmalves/inewave/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.com/rjmalves/inewave/compare/v1.7.5...v1.8.0
[1.7.5]: https://github.com/rjmalves/inewave/compare/v1.7.4...v1.7.5
[1.7.4]: https://github.com/rjmalves/inewave/compare/v1.7.3...v1.7.4
[1.7.3]: https://github.com/rjmalves/inewave/compare/v1.7.2...v1.7.3
[1.7.2]: https://github.com/rjmalves/inewave/compare/v1.7.1...v1.7.2
[1.7.1]: https://github.com/rjmalves/inewave/compare/v1.7.0...v1.7.1
[1.7.0]: https://github.com/rjmalves/inewave/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/rjmalves/inewave/compare/v1.5.7...v1.6.0
[1.5.7]: https://github.com/rjmalves/inewave/compare/v1.5.6...v1.5.7
[1.5.6]: https://github.com/rjmalves/inewave/compare/v1.5.5...v1.5.6
[1.5.5]: https://github.com/rjmalves/inewave/compare/v1.5.4...v1.5.5
[1.5.4]: https://github.com/rjmalves/inewave/compare/v1.5.3...v1.5.4
[1.5.3]: https://github.com/rjmalves/inewave/compare/v1.5.2...v1.5.3
[1.5.2]: https://github.com/rjmalves/inewave/compare/v1.5.1...v1.5.2
[1.5.1]: https://github.com/rjmalves/inewave/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/rjmalves/inewave/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/rjmalves/inewave/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/rjmalves/inewave/compare/v1.2.2...v1.3.0
[1.2.2]: https://github.com/rjmalves/inewave/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/rjmalves/inewave/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/rjmalves/inewave/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/rjmalves/inewave/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/rjmalves/inewave/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/rjmalves/inewave/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/rjmalves/inewave/compare/v0.0.98...v1.0.0
[0.0.98]: https://github.com/rjmalves/inewave/releases/tag/v0.0.98
