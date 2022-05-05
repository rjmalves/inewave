MockBlockTipoPenalizacao = [
    " XXX XXX XXX      (TIPO DE PENALIZACAO: 0-FIXA 1-MAXPEN; MES PENALIZACAO: 1 A 12;  VMINOP SAZONAL NO PRE/POS: 0-NAO CONSIDERA 1-CONSIDERA)\n",
    " 001 011 001\n",
]

MockBlocoCustoPorSistema = [
    " SISTEMA   CUSTO\n",
    " XXX       XXXX.XX\n",
    " 001       1745.08\n",
    " 002       1745.08\n",
    " 010       1745.08\n",
    " 011       1745.08\n",
    " 012       1745.08\n",
    " 999\n",
]

MockBlocoCurvaSeguranca = [
    " CURVA DE SEGURANCA (EM % DE EARMX)\n",
    " XXX\n",
    "      JAN.X FEV.X MAR.X ABR.X MAI.X JUN.X JUL.X AGO.X SET.X OUT.X NOV.X DEZ.X\n",
    "   1\n",
    "2021   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2022   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2023   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2024   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2025   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "   2\n",
    "2021   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "2022   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "2023   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "2024   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "2025   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "  10\n",
    "2021   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2022   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2023   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2024   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2025   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "  11\n",
    "2021   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "2022   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "2023   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "2024   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "2025   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30.   30. \n",
    "  12\n",
    "2021   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2022   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2023   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2024   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "2025   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10.   10. \n",
    "9999\n",
]

MockMaximoIteracoesProcessoIterativoEtapa2 = [
    "PROCESSO ITERATIVO DA ETAPA 2 DO MECANISMO DE AVERSAO AO RISCO\n",
    "NUM. MAXIMO DE ITERACOES         0     (SE = 0 -> NAO USA PROC. ITERATIVO DA ETAPA 2)\n",
]

MockIteracaoAPartirProcessoIterativoEtapa2 = [
    "ITERACAO A PARTIR               10\n",
]

MockToleranciaProcessoIterativoEtapa2 = [
    "TOLERANCIA P/ PROCESSO       0.010     (EM % DA PENALIDADE DE REFERENCIA)\n",
]

MockImpressaoRelatorioProcessoIterativoEtapa2 = [
    "IMPRESSAO DE RELATORIO           0     (=0 NAO IMPRIME; =1 IMPRIME)\n",
]


MockCurva = (
    MockBlockTipoPenalizacao
    + MockBlocoCustoPorSistema
    + MockBlocoCurvaSeguranca
    + MockMaximoIteracoesProcessoIterativoEtapa2
    + MockIteracaoAPartirProcessoIterativoEtapa2
    + MockToleranciaProcessoIterativoEtapa2
    + MockImpressaoRelatorioProcessoIterativoEtapa2
)
