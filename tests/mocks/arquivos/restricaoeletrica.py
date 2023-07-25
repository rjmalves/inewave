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
