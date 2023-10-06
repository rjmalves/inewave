MockRegistroEolicaCadastro = "EOLICA-CADASTRO ; 1 ; NEInterior ;  ; 1"

MockRegistroEolicaCadastroAerogerador = (
    "EOLICA-CADASTRO-AEROGERADOR ; 1 ; 1 ; 0 ; 0 ; 0 ; 0 ; 6058.890 ; 0 ; 0\n"
)

MockRegistroEolicaCadastroConjuntoAerogeradores = (
    "EOLICA-CADASTRO-CONJUNTO-AEROGERADORES ; 1 ; 1 ; NEInterior_cj ; 1\n"
)

MockRegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo = "EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO; 1 ; 1 ;2021/01; 2030/12; 1\n"

MockRegistroEolicaConjuntoAerogeradoresPotenciaEfetiva = "EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO; 1 ; 1 ;2021/01; 2030/12; 6058.890\n"

MockRegistroPEECadastro = "PEE-CAD  ; 1         ; NEInterior\n"

MockRegistroPEEPotenciaInstaladaPeriodo = (
    "PEE-POT-INST-PER  ;  1        ; 2021/01; 2030/12; 6058.890\n"
)

MockEolicaCadastro = [
    "& EOLICA-CADASTRO ; Codigo ; Nome ; Identificador ; QuantidadeIConjunto\n",
    "EOLICA-CADASTRO ; 1 ; NEInterior ;  ; 1\n",
    "EOLICA-CADASTRO ; 2 ; NELitoral ;  ;  1\n",
    "EOLICA-CADASTRO ; 3 ; NEPE ;  ;  1\n",
    "EOLICA-CADASTRO ; 4 ; SULInterior ; ; 1\n",
    "EOLICA-CADASTRO ; 5 ; SULLitoral ; ; 1\n",
    "\n",
    "& EOLICA-CADASTRO-CONJUNTO-AEROGERADORES ; CodigoEolica ; IConjunto ; NomeConjunto ; QuantidadeIAerogerador\n",
    "EOLICA-CADASTRO-CONJUNTO-AEROGERADORES ; 1 ; 1 ; NEInterior_cj ; 1\n",
    "EOLICA-CADASTRO-CONJUNTO-AEROGERADORES ; 2 ; 1 ; NELitoral_cj ; 1\n",
    "EOLICA-CADASTRO-CONJUNTO-AEROGERADORES ; 3 ; 1 ; NEPE_cj ; 1\n",
    "EOLICA-CADASTRO-CONJUNTO-AEROGERADORES ; 4 ; 1 ; SULInterior_cj ; 1\n",
    "EOLICA-CADASTRO-CONJUNTO-AEROGERADORES ; 5 ; 1 ; SULLitoral_cj  ; 1\n",
    "\n",
    "& EOLICA-CADASTRO-AEROGERADOR ; CodigoEolica ; IConjunto ; VelocidadeCutIn ; VelocidadeNominal ; VelocidadeCutOut ; PotenciaVelocidadeCutIn ; PotenciaVelocidadeNominal ; PotenciaVelocidadeCutOut ; AlturaTorre\n",
    "EOLICA-CADASTRO-AEROGERADOR ; 1 ; 1 ; 0 ; 0 ; 0 ; 0 ; 6058.890 ; 0 ; 0\n",
    "EOLICA-CADASTRO-AEROGERADOR ; 2 ; 1 ; 0 ; 0 ; 0 ; 0 ; 7359.195 ; 0 ; 0\n",
    "EOLICA-CADASTRO-AEROGERADOR ; 3 ; 1 ; 0 ; 0 ; 0 ; 0 ;  635.615 ; 0 ; 0\n",
    "EOLICA-CADASTRO-AEROGERADOR ; 4 ; 1 ; 0 ; 0 ; 0 ; 0 ;  292.200 ; 0 ; 0\n",
    "EOLICA-CADASTRO-AEROGERADOR ; 5 ; 1 ; 0 ; 0 ; 0 ; 0 ; 1651.190 ; 0 ; 0\n",
    "\n",
    "& EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO; CodEolica; IConjAero  ;PerIni ;PerFin ;NumAeroConj\n",
    "EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO; 1 ; 1 ;2021/01; 2030/12; 1\n",
    "EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO; 2 ; 1 ;2021/01; 2030/12; 1\n",
    "EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO; 3 ; 1 ;2021/01; 2030/12; 1\n",
    "EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO; 4 ; 1 ;2021/01; 2030/12; 1\n",
    "EOLICA-CONJUNTO-AEROGERADORES-QUANTIDADE-OPERANDO-PERIODO; 5 ; 1 ;2021/01; 2030/12; 1\n",
    "\n",
    "& EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO; CodEolica; IConjAero  ;PerIni ;PerFin ;PotEfet \n",
    "EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO; 1 ; 1 ;2021/01; 2030/12; 6058.890\n",
    "EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO; 2 ; 1 ;2021/01; 2030/12; 7359.195\n",
    "EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO; 3 ; 1 ;2021/01; 2030/12;  635.615\n",
    "EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO; 4 ; 1 ;2021/01; 2030/12;  292.200\n",
    "EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO; 5 ; 1 ;2021/01; 2030/12; 1651.190\n",
    "\n",
]

MockRegistroEolicaConfiguracaoPeriodo = (
    "EOLICA-CONFIGURACAO-PERIODO ; 1 ; 2021/01; 2030/12; centralizado\n"
)

MockRegistroPEEConfiguracaoPeriodo = (
    "PEE-CONFIG-PER  ; 1         ; 2021/01; 2030/12; centralizado\n"
)

MockEolicaConfig = [
    "&EOLICA-CONFIGURACAO-PERIODO; CodigoEolica; PeriodoInicial; PeriodoFinal  ; EstadoEolica (centralizado = 1, fixo = 2, nãoexistente = 3)\n",
    "EOLICA-CONFIGURACAO-PERIODO ; 1 ; 2021/01; 2030/12; centralizado\n",
    "EOLICA-CONFIGURACAO-PERIODO ; 2 ; 2021/01; 2030/12; centralizado\n",
    "EOLICA-CONFIGURACAO-PERIODO ; 3 ; 2021/01; 2030/12; centralizado\n",
    "EOLICA-CONFIGURACAO-PERIODO ; 4 ; 2021/01; 2030/12; centralizado\n",
    "EOLICA-CONFIGURACAO-PERIODO ; 5 ; 2021/01; 2030/12; centralizado\n",
]

MockRegistroFuncaoProducao = "EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO ; 1; 2021/01; 2030/12;  -0.14454132; 0.109046370\n"

MockRegistroPEEFTE = "PEE-FPVP-LIN-PU-PER	  ; 1         ; 2021/01; 2030/12; -0.14454132687670500 ; 0.10904637648150100\n"

MockEolicaFTE = [
    "& EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO ; CodEolica;PerIni ;PerFin ; CoeficienteLinear; CoeficienteAngular\n",
    "\n",
    "EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO ; 1; 2021/01; 2030/12;  -0.14454132; 0.10904637\n",
    "EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO ; 2; 2021/01; 2030/12;  -0.34282825; 0.09599283\n",
    "EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO ; 3; 2021/01; 2030/12;  -0.31163518; 0.14003760\n",
    "EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO ; 4; 2021/01; 2030/12;  -0.08251197; 0.07183436\n",
    "EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO ; 5; 2021/01; 2030/12;  -0.24408456; 0.09996426",
]

MockRegistroEolicaGeracaoPatamar = "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR; 1 ; 2021/01; 2021/01; 2 ; 1.0496\n"

MockRegistroPEEGeracaoPatamar = (
    "PEE-GER-PROF-PER-PAT  ; 1         ; 2021/01; 2021/01; 1   ; 0.8800\n"
)

MockEolicaGeracao = [
    "& EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR; CodEolica;PerIni ;PerFin ;Pat   ;PROFUNDIDADE\n",
    "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR; 1 ; 2021/01; 2021/01; 1 ; 0.8800\n",
    "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR; 1 ; 2021/01; 2021/01; 2 ; 1.0496\n",
    "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR; 1 ; 2021/01; 2021/01; 3 ; 1.0421\n",
    "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR; 1 ; 2021/02; 2021/02; 1 ; 0.8800\n",
    "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR; 1 ; 2021/02; 2021/02; 2 ; 1.0496\n",
    "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR; 1 ; 2021/02; 2021/02; 3 ; 1.0421\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t \n",
]

MockRegistroEolicaHistoricoHorizonte = (
    "EOLICA-HISTORICO-VENTO-HORIZONTE ; 1979/01 ; 2016/01\n"
)

MockRegistroEolicaHistorico = (
    "EOLICA-HISTORICO-VENTO; 1; 1979/01; 1979/02;    3.43; 1.0\n"
)

MockRegistroHistoricoVentoHorizonte = (
    "VENTO-HIST-HORIZ  ; 1979/01     ; 2016/01\n"
)

MockRegistroHistoricoVento = "VENTO-HIST  ; 1           ; 1979/01     ; 1979/02   ;      4.05       ; 1.0\n"

MockEolicaHistorico = [
    "& EOLICA-HISTORICO-VENTO-HORIZONTE ; DataInicial ; DataFinal\n",
    "EOLICA-HISTORICO-VENTO-HORIZONTE ; 1979/01 ; 2016/01\n",
    "\n",
    "\n",
    "& EOLICA-HISTORICO-VENTO ; CodigoEolica ; DataInicial ; DataFinal ; MagnitudeVelocidadeVento ; DirecaoVento \n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/01; 1979/02;    3.43; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/02; 1979/03;    4.28; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/03; 1979/04;    4.67; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/04; 1979/05;    4.50; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/05; 1979/06;    4.77; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/06; 1979/07;    6.09; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/07; 1979/08;    5.66; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/08; 1979/09;    6.21; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/09; 1979/10;    6.75; 1.0\n",
    "EOLICA-HISTORICO-VENTO; 1; 1979/10; 1979/11;    5.64; 1.0\n",
]

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

MockRegistroEolicaSubmercado = "EOLICA-SUBMERCADO ; 5 ; 2\n"

MockRegistroPEESubmercado = "PEE-SUBM   ; 1         ; 3\n"

MockEolicaSubmercado = [
    "& EOLICA-SUBMERCADO; CodigoEolica; CodigoSubmercado\n",
    "EOLICA-SUBMERCADO ; 1 ; 3\n",
    "EOLICA-SUBMERCADO ; 2 ; 3\n",
    "EOLICA-SUBMERCADO ; 3 ; 3\n",
    "EOLICA-SUBMERCADO ; 4 ; 2\n",
    "EOLICA-SUBMERCADO ; 5 ; 2\n",
    "",
]

MockEolica = (
    MockEolicaCadastro
    + MockEolicaConfig
    + MockEolicaFTE
    + MockEolicaGeracao
    + MockEolicaHistorico
    + MockEolicaPosto
    + MockEolicaSubmercado
)
