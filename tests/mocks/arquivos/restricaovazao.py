MockRHQ = "RHQ;       1 ; qtur(66)  \n"
MockRHQHorizPer = "RHQ-HORIZ-PER;        1;      2021/01;      2022/12\n"
MockRHQLsLPPVoli = "RHQ-LS-LPP-VOLI;        1;    1; 0.30; 3000.00\n"

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
]
