# 1.10.4

- Correção na escrita do arquivo `ghmin.dat` em linhas relativas aos anos "POS" [#106](https://github.com/rjmalves/inewave/issues/106) (@joaoCalmon).
- Melhor processamento de variáveis ausentes ao caso no arquivo MEDIAS-USIH.CSV (@rdlobato)
- Suporte a processar um número variável de etapas no arquivo newave.tim (@rdlobato)
- Correção de tipagem estática para mypy

# 1.10.3

- Correção na leitura do arquivo `sistema.dat` em arquivos gerados com espaços adicionais nas linhas dos blocos [#104](https://github.com/rjmalves/inewave/issues/106).

# 1.10.2

- Correção na escrita do arquivo `nwlistop.dat` para suportar o numero de variaveis totais da opção 2 do programa NWLISTOP [#104](https://github.com/rjmalves/inewave/issues/104).

# 1.10.1

- Correção na leitura dos arquivos `c_adic.dat` e `sistema.dat` para considerar nomes completos de submercados [#101](https://github.com/rjmalves/inewave/issues/101).
- Correção no nome da coluna `codigo_usina` para `codigo_posto` no arquivo `vazpast.dat`

# 1.10.0

- Gestão do projeto através de arquivo `pyproject.toml` em substituição ao par `setup.py` + `requirements.txt`
- Correção no processamento da energia armazenada inicial por subsistema do `dger.dat` [#97](https://github.com/rjmalves/inewave/issues/97).
- Suporte aos campos de restrições elétricas especiais existentes na versão 30 do modelo NEWAVE
- Melhorias na documentação, incluindo exemplos de arquivos das LIBS [#94](https://github.com/rjmalves/inewave/issues/94)
- Suporte a obter a versão do modelo NEWAVE utilizada a partir do arquivo newave.tim (@eduardomdc)
- Requisito de versão de Python atualizado para `>=3.10`

# 1.9.2

- Versionamento dos arquivos `cmargXXX.out` e `cmargXXX-med.out` do NWLISTOP devido o aumento de dígitos impressos.

# 1.9.1

- Correção nos tamanhos dos campos de vazão desviada do arquivo `dsvagua.dat`

# 1.9.0

- Suporte ao arquivo do NWLISTOP com informação do Custo Futuro por cenário (`custo_futuro.out`)
- Suporte a arquivos do NWLISTOP renomeados: `viol_eletrica.out`, `cviol_eletrica.out`, `viol_pos_vretiruh.out`, `viol_neg_vretiruh.out`.
- Descontinuado o uso do `pylama` como linter para garantir padrões PEP de código devido à falta de suporte em Python >= 3.12. Adoção do [ruff](https://github.com/astral-sh/ruff) em substituição.

# 1.8.1

- Correção da leitura dos arquivos `pivarm.out` e `pivarmincr.out` do NWLISTOP [#87](https://github.com/rjmalves/inewave/issues/87).

# 1.8.0

- Nomes de arquivos e formatos atualizados para compatibilidade com a versão 29.3 do modelo NEWAVE. Classes que implementam os arquivos antigos foram marcadas como `deprecated`, mas ainda existem no módulo.
- Suporte à obtenção da versão do modelo utilizada, impressa no arquivo `pmo.dat`.
- Arquivos do modelo NEWAVE renomeados: `nwv_avl_evap.csv` (`evap_avl_desv.csv`), `nwv_cortes_evap.csv` (`evap_cortes.csv`), `nwv_eco_evap.csv` (`evap_eco.csv`), `avl_cortesfpha_nwv.csv` (`fpha_cortes.csv`), `eco_fpha.csv` (`fpha_eco_.csv`), `avl_desvfpha_v_q.csv` (`fpha_avl_desv_v_q.csv`) e `avl_desvfpha_s.csv` (`fpha_avl_desv_s.csv`)
- Arquivos do NWLISTOP renomeados: `dlpptbmax.out` (`viol_lpp_tbmax.out`), `dlpptbmaxm.out` (`viol_lpp_tbmaxm.out`), `dlpptbmaxsin.out` (`viol_lpp_tbmaxsin.out`), `dlppdfmax.out` (`viol_lpp_dfmax.out`), `dlppdfmaxm.out` (`viol_lpp_dfmaxm.out`), `dlppdfmaxsin.out` (`viol_lpp_dfmaxsin.out`), `vevmin.out` (`viol_evmin.out`), `vevminm.out` (`viol_evminm.out`), `vevminsin.out` (`viol_evminsin.out`), `deletricasin.out` (`viol_eletricasin.out`), `celetricasin.out` (`cviol_eletricasin.out`), `c_v_rhq.out` (`cviol_rhq.out`), `c_v_rhq_s.out` (`cviol_rhq_sin.out`), `c_v_rhv.out` (`cviol_rhv.out`), `c_v_rhv_s.out` (`cviol_rhv_sin.out`), `vghmin.out` (`viol_ghmin.out`), `vghminm.out` (`viol_ghminm.out`), `vghminsin.out` (`viol_ghminsin.out`), `vghminuh.out` (`viol_ghminuh.out`), `vagua.out` (`valor_agua.out`), `depminuh.out` (`viol_vazmin.out`), `dvazmax.out` (`viol_vazmax.out`), `desvuh.out` (`vretiradauh.out`), `vturuh.out` (`qturuh.out`), `vertuh.out` (`qvertuh.out`), `vdesviouh.out` (`qdesviouh.out`), `dfphauh.out` (`viol_fpha.out`), `dtbmax.out` (`viol_turbmax.out`), `dtbmin.out` (`viol_turbmin.out`), `dpos_evap.out` (`viol_pos_evap.out`), `dneg_evap.out` (`viol_neg_evap.out`).

# 1.7.5

- Dependência da cfinterface atualizada para [v1.6.0](https://github.com/rjmalves/cfi/releases/tag/v1.6.0)
- Uso de `__slots__` nas definições de componentes

# 1.7.4

- Fix na leitura dos blocos de geração mínima e máxima de usinas térmicas do `pmo.dat` [#83](https://github.com/rjmalves/inewave/issues/83)
- Fix na leitura do arquivo `energias.dat` [#82](https://github.com/rjmalves/inewave/issues/82)

# 1.7.3

- Atualização do formato da leitura do arquivo `vevapuhXXX.out` do nwlistop para maior precisão.

# 1.7.2

- Fix na leitura dos blocos de valores de penalidades do `pmo.dat` em casos com períodos pós-estudo
- Atualização do formato da leitura dos arquivos `dpos_evapXXX.out` e `dneg_evapXXX.out` do nwlistop para notação científica.

# 1.7.1

- Fix na leitura do bloco de configurações por estágio do `pmo.dat` no caso do relatório conter apenas um bloco [#79](https://github.com/rjmalves/inewave/issues/79)

# 1.7.0

- Suporte aos blocos de energia armazenada máxima por REE, geração térmica mínima e máxima por UTE no `pmo.dat` [#77](https://github.com/rjmalves/inewave/issues/77), [#76](https://github.com/rjmalves/inewave/issues/76)
- Suporte ao arquivo `vazinat.dat` [#74](https://github.com/rjmalves/inewave/issues/74)
- Refactor da leitura dos arquivos `MEDIAS-*` do NWLISTOP, com novo suporte aos `MEDIAS-REE`, `MEDIAS-USIH`, `MEDIAS-USIT`, `MEDIAS-USIE`, `MEDIAS-REP`, `MEDIAS-RHQ` e `MEDIAS-RHV` [#78](https://github.com/rjmalves/inewave/issues/78)
- Atualizaçao da documentação das propriedades do modelo do `sistema.dat` [#70](https://github.com/rjmalves/inewave/issues/70)

# v1.6.0

- Suporte aos blocos com valores de penalidades por tipo de violação no arquivo `pmo.dat`
- Suporte aos novos arquivos do `NWLISTOP` associados à evaporação: `vevapuhXXX.out`, `dpos_evapXXX.out`, `dneg_evapXXX.out` e ao arquivo `gh_fphexatXXX.out`.

# v1.5.7

- Suporte à leitura do arquivo `avl_cortesfpha_nwv.csv`, que mudou de sintaxe na versão `28.16` do NEWAVE

# v1.5.6

- Fix na modelagem do arquivo `dger.dat`, na posição do campo de agregação da simulação final.

# v1.5.5

- Fix na construção dos registros específicos do `modif.dat`, que não permitiam atribuir valores a propriedades de registros criados fora do contexto de leitura.

# v1.5.4

- Fix na modelagem do arquivo `modif.dat` para modelar de maneira "exata" os demais registros suportados, exceto o registro USINA, devido ao campo de comentário com nome da usina permitir espaços.

# v1.5.3

- Fix na modelagem do arquivo `modif.dat` para modelar de maneira "exata" os registros VOLMIN e VOLMAX, que possuem posição livre dos campos de dados, separados por espaços.

# v1.5.2

- Fix na modelagem do arquivo `modif.dat` para listar as modificações de uma usina

# v1.5.1

- Fix nas colunas do DataFrame das restrições do arquivo `re.dat`

# v1.5.0

- Refactor da modelagem utilizada para dados provenientes das LIBS: criado o submódulo `libs`, de forma que o usuário possa realizar a importação com `from inewave.libs import ...`.
- Modelagem de entidades das LIBS não é feita baseada nos arquivos fornecidos nos casos de exemplo das versões do modelo, mas sim baseado nas entidades envolvidas na informação, semelhante à divisão feita no site da documentação oficial [LIBS](https://see.cepel.br/manual/libs/latest/index.html)
- Suporte aos arquivos e mnemônicos faltantes para ter suporte total à versão `28.16.1` do modelo NEWAVE
- Novo arquivo de entrada suportados: `volref_saz.dat`
- Novos dados das LIBS: restrições RHV e RHQ, produtibilidade e perdas variáveis, FPHA, polinjus.
- Novos arquivos do NWLISTOP suportados: `c_v_rhqXXX.out`, `c_v_rhvXXX.out`, `cbombXXX.out`, `cbombsin.out`, `celetricas.out`, `deletricas.out`, `form_rhqXXX.out`, `form_rhvXXX.out`, `ghmax_fphaXXX.out`, `ghmax_fphcXXX.out`, `pivarmincrXXX.out`, `vbombXXX.out`, `viol_rhqXXX.out`, `viol_rhvXXX.out`.

# v1.4.0

- Suporte a arquivos do NWLISTOP necessários para fechamento de balanço hídrico de REE: `ghidrXXX.out`, `ghidrmXXX.out`, `ghidrsin.out`, `edesvcXXX.out`, `edesvcmXXX.out`, `edesvcsin.out`, `evapoXXX.out`, `evapomXXX.out`, `evaporsin.out`, `vmortXXX.out`, `vmortmXXX.out`, `vmortsin.out`, `mevminXXX.out`, `mevminmXXX.out`, `mevminsin.out`.

# v1.3.0

- Suporte a novos arquivos do NWLISTOP presentes da versão 28.15.3 do NEWAVE: cotas de montante e jusante por UHE e altura de queda líquida por UHE.
- Suporte aos arquivos de retirada de água e desvio de água por UHE do NWLISTOP

# v1.2.2

- Fix no processamento de arquivos por patamar do NWLISTOP: alguns arquivos possuíam desalinhamento nos campos das séries.
- Otimizada a formatação do dataframes do NWLISTOP.

# v1.2.1

- Fix na leitura do bloco de energia armazenada do `pmo.dat`: remoção de caracteres especiais do nome do último REE.

# v1.2.0

- Fix na leitura do `dger.dat`: o modelo esperava a linha de "COMP. CORR. CRUZ.", que não está presente em todas as versões do modelo. Foi compatibilizado para esperar o formato das versões oficiais.
- Campos do `dger.dat` atualizados para versão 28.15.2 do NEWAVE.
- Suporte à leitura do arquivo `eco_fpha.dat`
- Suporte à leitura do arquivo `pivarmXXX.out` do NWLISTOP
- Suporte à leitura dos campos de energia armazenada inicial e volume armazenado inicial do `pmo.dat`

# v1.1.2

- Hotfix na leitura do `pmo.dat`: o bloco de configurações para cada estágio não suportava casos com mais de 100 configurações devido a um erro no modelo da linha.

# v1.1.1

- Hotfix na leitura do `pmo.dat`: o bloco de custos passou a ter mais de 30 linhas, que era o limite do array alocado. Passado para 100.

# v1.1.0

- Conversão dos campos dos arquivos de entrada que representavam informações de datas como `int` para `datetime`
- Padronização de todos os arquivos de entrada que possuíam informações como `DataFrame` para formato normal
- Padronização de blocos do `pmo.dat`, `parp.dat`, `parpeol.dat` e `parpvaz.dat` para serem modelados como `DataFrame` em formatos normais.

# v1.0.0

- Primeira major release
- Suporte à leitura e escrita todos os arquivos de entrada utilizados oficialmente no modelo NEWAVE
- Suporte à leitura da maioria dos arquivos de saída do modelo NEWAVE, NWLISTCF e NWLISTOP
- Métodos le_arquivo e escreve_arquivo deprecados

# v0.0.98 (v1.0.0-rc0)

- rc0 da primeira major release (v1.0.0)
- Suporte à leitura e escrita todos os arquivos de entrada utilizados oficialmente no modelo NEWAVE
- Suporte à leitura da vasta maioria dos arquivos de saída do modelo NEWAVE, NWLISTCF e NWLISTOP
- Métodos le_arquivo e escreve_arquivo ainda não deprecados
- Nomes das colunas dos dataframes padronizados para `snake_case`
- Nomes das classes padronizados para `PascalCase`
- Arquivos do NWLISTOP processados para formato normal de séries temporais
- Dependência da cfinterface atualizada para [v1.5.2](https://github.com/rjmalves/cfi/releases/tag/v1.5.2)
