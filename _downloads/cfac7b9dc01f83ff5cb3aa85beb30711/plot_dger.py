"""
========================================
Alteração no dger.dat
========================================
"""


# %%
# O dger.dat é um dos principais arquivos de entrada do modelo NEWAVE. É
# comum desejar realizar alterações automáticas neste arquivo, para fins de
# estudos periódicos. Isto pode ser feito utilizando a classe `Dger`:
from inewave.newave import Dger

arq_dger = Dger.read("./newave/dger.dat")

# %%
# Uma alteração muito comum é o nome do caso:
arq_dger.nome_caso

# %%
# Para alterá-lo, basta fazer:
arq_dger.nome_caso = "Caso de teste - inewave"
arq_dger.nome_caso

# %%
# Todos os campos do arquivo são editáveis seguindo esta mesma lógica. Os nomes das propriedades
# que foram escolhidas para implementação buscam refletir o sentido da configuração. Por exemplo,
# para as opções do gerenciamento externo de PLs, existem as propriedades separadas:

print(
    arq_dger.utiliza_gerenciamento_pls,
    arq_dger.comunicacao_dois_niveis,
    arq_dger.armazenamento_local_arquivos_temporarios,
)


# %%
# Para exportar o arquivo modificado, basta utilizar o método `write` a partir do objeto que foi
# alterado. Todavia, não é obrigatório fornecer um caminho para um arquivo no disco. A exportação
# também pode ser feita para um buffer em memória, se o objetivo
# for enviar o conteúdo do arquivo através de uma requisição HTTP, por exemplo, ou armazenar em um
# banco de dados para documentos:
from io import StringIO

conteudo_dger = StringIO()
arq_dger.write(conteudo_dger)
print(conteudo_dger.getvalue())
