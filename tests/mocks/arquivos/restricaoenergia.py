MockRHE = "RRHE;       1 ; ger_ree(1) + ener_ver_ree(1)   \n"
MockRHEHorizPer = "RHE-HORIZ-PER;        2;      2021/01;      2025/12\n"
MockRHQLsLPPEarmi = "RHE-LS-LPP-EARMI;        2;    2;     -0.3;     4000.0\n"

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
