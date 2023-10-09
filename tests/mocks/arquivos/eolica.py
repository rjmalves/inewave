MockRegistroPEECadastro = "PEE-CAD  ; 1         ; NEInterior\n"

MockRegistroPEEPotenciaInstaladaPeriodo = (
    "PEE-POT-INST-PER  ;  1        ; 2021/01; 2030/12; 6058.890\n"
)

MockEolicaCadastro = [
    "& PEE-CAD ; Codigo ; Nome ; Identificador ; QuantidadeIConjunto\n",
    "PEE-CAD ; 1 ; NEInterior ;  ; 1\n",
    "PEE-CAD ; 2 ; NELitoral ;  ;  1\n",
    "PEE-CAD ; 3 ; NEPE ;  ;  1\n",
    "PEE-CAD ; 4 ; SULInterior ; ; 1\n",
    "PEE-CAD ; 5 ; SULLitoral ; ; 1\n",
    "\n",
]


MockRegistroPEEConfiguracaoPeriodo = (
    "PEE-CONFIG-PER  ; 1         ; 2021/01; 2030/12; centralizado\n"
)

MockEolicaConfig = [
    "&PEE-CONFIG-PER; CodigoEolica; PeriodoInicial; PeriodoFinal  ; EstadoEolica (centralizado = 1, fixo = 2, nãoexistente = 3)\n",
    "PEE-CONFIG-PER ; 1 ; 2021/01; 2030/12; centralizado\n",
    "PEE-CONFIG-PER ; 2 ; 2021/01; 2030/12; centralizado\n",
    "PEE-CONFIG-PER ; 3 ; 2021/01; 2030/12; centralizado\n",
    "PEE-CONFIG-PER ; 4 ; 2021/01; 2030/12; centralizado\n",
    "PEE-CONFIG-PER ; 5 ; 2021/01; 2030/12; centralizado\n",
]

MockRegistroPEEFTE = "PEE-FPVP-LIN-PU-PER	  ; 1         ; 2021/01; 2030/12; -0.14454132687670500 ; 0.10904637648150100\n"

MockEolicaFTE = [
    "& PEE-FPVP-LIN-PU-PER ; CodEolica;PerIni ;PerFin ; CoeficienteLinear; CoeficienteAngular\n",
    "\n",
    "PEE-FPVP-LIN-PU-PER ; 1; 2021/01; 2030/12;  -0.14454132; 0.10904637\n",
    "PEE-FPVP-LIN-PU-PER ; 2; 2021/01; 2030/12;  -0.34282825; 0.09599283\n",
    "PEE-FPVP-LIN-PU-PER ; 3; 2021/01; 2030/12;  -0.31163518; 0.14003760\n",
    "PEE-FPVP-LIN-PU-PER ; 4; 2021/01; 2030/12;  -0.08251197; 0.07183436\n",
    "PEE-FPVP-LIN-PU-PER ; 5; 2021/01; 2030/12;  -0.24408456; 0.09996426",
]


MockRegistroPEEGeracaoPatamar = (
    "PEE-GER-PROF-PER-PAT  ; 1         ; 2021/01; 2021/01; 1   ; 0.8800\n"
)

MockEolicaGeracao = [
    "& PEE-GER-PROF-PER-PAT; CodEolica;PerIni ;PerFin ;Pat   ;PROFUNDIDADE\n",
    "PEE-GER-PROF-PER-PAT; 1 ; 2021/01; 2021/01; 1 ; 0.8800\n",
    "PEE-GER-PROF-PER-PAT; 1 ; 2021/01; 2021/01; 2 ; 1.0496\n",
    "PEE-GER-PROF-PER-PAT; 1 ; 2021/01; 2021/01; 3 ; 1.0421\n",
    "PEE-GER-PROF-PER-PAT; 1 ; 2021/02; 2021/02; 1 ; 0.8800\n",
    "PEE-GER-PROF-PER-PAT; 1 ; 2021/02; 2021/02; 2 ; 1.0496\n",
    "PEE-GER-PROF-PER-PAT; 1 ; 2021/02; 2021/02; 3 ; 1.0421\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t \n",
]

MockRegistroHistoricoVentoHorizonte = (
    "VENTO-HIST-HORIZ  ; 1979/01     ; 2016/01\n"
)

MockRegistroHistoricoVento = "VENTO-HIST  ; 1           ; 1979/01     ; 1979/02   ;      4.05       ; 1.0\n"


MockRegistroPostoCadastro = ("POSTO-VENTO-CAD  ; 1           ; NEInterior\n",)

MockRegistroPEEPosto = "PEE-POSTO  ; 1         ; 1\n"

MockEolicaPosto = [
    "&POSTO-VENTO-CAD ; CodigoPosto ; NomePosto\n",
    "POSTO-VENTO-CAD  ; 1           ; NEInterior\n",
    "POSTO-VENTO-CAD  ; 2           ; NELitoral\n",
    "POSTO-VENTO-CAD  ; 3           ; NEPE\n",
    "POSTO-VENTO-CAD  ; 4           ; SULInterior\n",
    "POSTO-VENTO-CAD  ; 5           ; SULLitoral\n",
    "\n",
    "&PEE-POSTO ; CodigoPEE ; CodigoPosto\n",
    "PEE-POSTO  ; 1         ; 1\n",
    "PEE-POSTO  ; 2         ; 2\n",
    "PEE-POSTO  ; 3         ; 3\n",
    "PEE-POSTO  ; 4         ; 4\n",
    "PEE-POSTO  ; 5         ; 5\n",
]


MockRegistroPEESubmercado = "PEE-SUBM   ; 1         ; 3\n"

MockPEESubmercado = [
    "& PEE-SUBM; CodigoEolica; CodigoSubmercado\n",
    "PEE-SUBM ; 1 ; 3\n",
    "PEE-SUBM ; 2 ; 3\n",
    "PEE-SUBM ; 3 ; 3\n",
    "PEE-SUBM ; 4 ; 2\n",
    "PEE-SUBM ; 5 ; 2\n",
    "",
]

MockEolica = (
    MockEolicaCadastro
    + MockEolicaConfig
    + MockEolicaFTE
    + MockEolicaGeracao
    + MockEolicaPosto
    + MockPEESubmercado
)
