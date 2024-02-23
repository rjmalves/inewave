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
- Suporte a arquivos do NWLISTOP necessários para fechamento de balanço hídrico de REE: `ghidrXXX.out`, `ghidrmXXX.out`, `ghidrsin.out`, `edesvcXXX.out`, `edesvcmXXX.out`, `edesvcsin.out`,   `evapoXXX.out`, `evapomXXX.out`, `evaporsin.out`, `vmortXXX.out`, `vmortmXXX.out`, `vmortsin.out`, `mevminXXX.out`, `mevminmXXX.out`, `mevminsin.out`.

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