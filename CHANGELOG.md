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