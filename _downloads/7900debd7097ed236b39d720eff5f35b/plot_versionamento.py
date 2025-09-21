"""
========================================
Versionamento de Arquivos
========================================
"""

# %%
# Para exemplificar a leitura de arquivos que mudaram de formato
# com o versionamento do modelo NEWAVE, será utilizada a leitura
# do pmo.dat para obtenção da versão da rodada
from inewave.newave import Pmo

arq_pmo = Pmo.read("./newave/pmo.dat")

# %%
# A versão utilizada na execução do modelo pode ser obtida com
versao = arq_pmo.versao_modelo
versao

# %%
# Exemplos de arquivos que sofreram alteração de formato
# com o versionamento do modelo são os `cmargXXX.out` e `cmargXXX-med.out`
# do NWLISTOP, com as informações do custo marginal de operação. A partir da
# versão 29.4.1, houve uma mudança na formatação do arquivo. Desta forma, ao se realizar
# a leitura diretamente da classe :ref:`Cmargmed <cmargmed>`, espera-se que o arquivo esteja no formato
# da última versão do modelo. Caso não esteja, os valores não são lidos corretamente
from inewave.nwlistop import Cmargmed

cmarg = Cmargmed.read("./nwlistop/cmarg001-med.out")
cmarg.valores

# %%

cmarg_v28_erro = Cmargmed.read("./nwlistop/cmarg001-med_v28.out")
cmarg_v28_erro.valores

# %%
# Todavia, se é atribuída a versão correta, os valores são lidos correamente
Cmargmed.set_version(versao)
cmarg_v28 = Cmargmed.read("./nwlistop/cmarg001-med_v28.out")
cmarg_v28.valores
