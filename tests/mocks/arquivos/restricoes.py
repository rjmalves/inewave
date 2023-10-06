MockRE = "RE  ;    1; 1.0ger_usit(13) + ger_usih(66)\n"
MockREHorizPer = "RE-HORIZ-PER ; 1; 2021/01; 2021/01\n"
MockRELimFormPer = (
    "RE-LIM-FORM-PER ;        1; 2021/01;  2021/03;     1;   -1.1e30;  5000\n"
)

MockRestricaoEletrica = [
    "&RE; cod_rest;  formula\n",
    "RE  ;    1; 1.0ger_usit(13) + ger_usih(66)\n",
    "RE  ;    2; 0.5ener_interc(3,4)\n",
    "\n",
    "&RE-HORIZ-PER; cod_rest; PerIni; PerFin\n",
    "RE-HORIZ-PER ;        1;2021/01;2021/03\n",
    "RE-HORIZ-PER ;        2;2021/01;2021/03\n",
    "\n",
    "&RE-LIM-FORM-PER; cod_rest;  PerIni;  PerFin;   Pat;    LimInf;  LimSup\n",
    "RE-LIM-FORM-PER ;        1; 2021/01; 2021/03;     1;   -1.1e30;  5000\n",
    "RE-LIM-FORM-PER ;        1; 2021/01; 2021/03;     2;   -1.1e30;  5000\n",
    "RE-LIM-FORM-PER ;        1; 2021/01; 2021/03;     3;   -1.1e30;  5000\n",
    "RE-LIM-FORM-PER ;        2; 2021/01; 2021/03;     1;   -1.1e30;  1000\n",
    "RE-LIM-FORM-PER ;        2; 2021/01; 2021/03;     2;   -1.1e30;  1000\n",
    "RE-LIM-FORM-PER ;        2; 2021/01; 2021/03;     3;   -1.1e30;  1000",
]

MockRHE = "RRHE;       1 ; ger_ree(1) + ener_ver_ree(1)   \n"
MockRHEHorizPer = "RHE-HORIZ-PER;        2;      2021/01;      2025/12\n"
MockRHELsLPPEarmi = "RHE-LS-LPP-EARMI;        2;    2;     -0.3;     4000.0\n"

MockRestricaoEnergia = [
    "&RHE; cod_rest;  formula\n",
    "RHE;       1 ; ger_ree(1) + ener_ver_ree(1)   \n",
    "RHE;       2 ; ger_ree(3)\n",
    "\n",
    "&RHE-HORIZ-PER; cod_rest; data_inicial; data_final\n",
    "RHE-HORIZ-PER;        1;      2021/01;      2025/12\n",
    "RHE-HORIZ-PER;        2;      2021/01;      2025/12\n",
    "\n",
    "&RHE-LS-LPP-EARMI; cod_rest; reta; coef_ang; coef_lin\n",
    "RHE-LS-LPP-EARMI;        1;    1;      0.2;    -1000.0\n",
    "RHE-LS-LPP-EARMI;        1;    2;     -0.5;    20000.0\n",
    "RHE-LS-LPP-EARMI;        2;    1;      0.5;    -1000.0\n",
    "RHE-LS-LPP-EARMI;        2;    2;     -0.3;     4000.0\n",
]

MockRHQ = "RHQ;       1 ; qtur(66)  \n"
MockRHQHorizPer = "RHQ-HORIZ-PER;        1;      2021/01;      2022/12\n"
MockRHQLsLPPVoli = "RHQ-LS-LPP-VOLI;        1;    1; 0.30; 3000.00\n"
MockRHQLimFormPerPat = " RHQ-LIM-FORM-PER-PAT;      7; 2023/03; 2023/06;   1;   1000.00;   1500.00"

MockRestricaoVazao = [
    "&RHQ; cod_rest;  formula\n",
    "RHQ;       1 ; qtur(66)  \n",
    "RHQ;       2 ; qtur(1) + qver(1) \n",
    "\n",
    "&RHQ-HORIZ-PER; cod_rest; data_inicial; data_final\n",
    "RHQ-HORIZ-PER;        1;      2021/01;      2022/12\n",
    "RHQ-HORIZ-PER;        2;      2021/01;      2022/12\n",
    "\n",
    "&RHQ-LS-LPP-VOLI; cod_rest; reta; coef_ang; coef_lin\n",
    "RHQ-LS-LPP-VOLI;        1;    1; 0.30; 3000.00\n",
    "RHQ-LS-LPP-VOLI;        1;    2; 0.20; 4000.00\n",
    "RHQ-LS-LPP-VOLI;        2;    1; 0.30; 1000.00\n",
    "RHQ-LS-LPP-VOLI;        2;    2; 0.20; 2000.00\n",
    "\n",
    "&RHQ-LIM-FORM-PER-PAT; CodRvz; PerIni ; PerFin ; Pat;    LimInf;    LimSup\,",
    " RHQ-LIM-FORM-PER-PAT;      7; 2023/03; 2023/06;   1;   1000.00;   1500.00\,",
    " RHQ-LIM-FORM-PER-PAT;      7; 2023/03; 2023/06;   2;   1000.00;   1500.00\,",
    " RHQ-LIM-FORM-PER-PAT;      7; 2023/03; 2023/06;   3;   1000.00;   1500.00\,",
    " RHQ-LIM-FORM-PER-PAT;      5; 2023/05; 2023/08;   1;    350.00;    500.00\,",
    " RHQ-LIM-FORM-PER-PAT;      5; 2023/05; 2023/08;   2;    350.00;    500.00\,",
    " RHQ-LIM-FORM-PER-PAT;      5; 2023/05; 2023/08;   3;    350.00;    500.00\,",
]


MockRHV = " RHV;      1; 1*vtur(18) + 2*vver(17) + 2*varm(18)"
MockRHVHorizPer = " RHV-HORIZ-PER;      1; 2023/03; 2023/06"
MockRHVLimFormPer = (
    " RHV-LIM-FORM-PER;      1; 2023/03; 2023/06;    100.00;    100.00"
)

MockRHV = [
    "&RHV;CodRVol; Formula\n",
    " RHV;      1; 1*vtur(18) + 2*vver(17) + 2*varm(18)\n",
    " RHV;      2; 3*vtur(122) + 1*vver(121) + 4*varm(122)\n",
    "\n",
    "&RHV-HORIZ-PER;CodRVol; PerIni ; PerFin\n",
    " RHV-HORIZ-PER;      1; 2023/03; 2023/06\n",
    " RHV-HORIZ-PER;      2; 2023/03; 2023/06\n",
    "\n",
    "&RHV-LIM-FORM-PER;CodRVol; PerIni ; PerFin ;    LimInf;    LimSup\n",
    " RHV-LIM-FORM-PER;      1; 2023/03; 2023/06;    100.00;    100.00\n",
    " RHV-LIM-FORM-PER;      2; 2023/03; 2023/06;     80.00;    100.00\n",
]

MockRestricoes = (
    MockRestricaoEletrica + MockRestricaoEnergia + MockRestricaoVazao
)
