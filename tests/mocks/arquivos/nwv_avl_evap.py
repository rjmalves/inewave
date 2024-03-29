MockNwvAvlEvap = [
    "***********************************************************************\n",
    "*                                                                     *\n",
    "*            CEPEL - CENTRO DE PESQUISAS DE ENERGIA ELETRICA          *\n",
    "*  CEPEL: NEWAVE     - Versao FPHA_NEWAVE                             *\n",
    "*                                                                     *\n",
    "***********************************************************************\n",
    "\n",
    "\n",
    "\n",
    "------------------------------------------------------------\n",
    "Avaliacao dos desvios da Representacao linear da evaporacao.                    \n",
    "------------------------------------------------------------\n",
    "-------------------------------------------------------------------------------\n",
    "IPER;         Indice do periodo                                                                                                                                                                         \n",
    "USIH;         Numero de cadastro da usina hidroeletrica                                                                                                                                                 \n",
    "NomeUsih;     Nome de cadastro da usina hidroeletrica                                                                                                                                                   \n",
    "Varm;         Volume Armazenado Total                                                                                                                                                                   \n",
    "Evap. Calc.;  Evaporacao caculada pelos polinomios AreaXCota e CotaXVolume                                                                                                                              \n",
    "Evap. Modelo; Evaporacao calculada pelo modelo linear construido pelo Decomp                                                                                                                            \n",
    "Desvio Abs.;  Desvio absoluto entre o valor exato e o obtido pelo modelo (hm3)                                                                                                                          \n",
    "Desvio (%);   Desvio percentual entre o valor exato e o obtido pelo modelo (MW)                                                                                                                         \n",
    "-------------------------------------------------------------------------------\n",
    "\n",
    "@Tabela\n",
    "-----;-----;--------------;----------;----------;----------;------------;-----------;\n",
    "IPER ;USIH ;   NomeUsih   ;   Varm   ;Evap. Calc;Evap. Mode;Desvio Abs. ;Desvio (%) ;\n",
    "  -  ;  -  ;      -       ;  (hm3)   ;  (hm3)   ;  (hm3)   ;   (hm3)    ;    (%)    ;\n",
    "-----;-----;--------------;----------;----------;----------;------------;-----------;\n",
    "   1 ; 004 ; FUNIL-GRANDE ;   265.86 ;     0.23 ;     0.23 ;      0.000 ;       0.00;\n",
    "   1 ; 020 ; BATALHA      ;   430.05 ;     0.00 ;     0.00 ;      0.000 ;       0.00;\n",
    "   1 ; 020 ; BATALHA      ;   700.36 ;     0.00 ;     0.00 ;      0.000 ;       0.00;\n",
    "   1 ; 020 ; BATALHA      ;   970.67 ;     0.00 ;     0.00 ;      0.000 ;       0.00;\n",
    "   1 ; 020 ; BATALHA      ;  1240.99 ;     0.00 ;     0.00 ;      0.000 ;       0.00;\n",
    "   1 ; 020 ; BATALHA      ;  1511.30 ;     0.00 ;     0.00 ;      0.000 ;       0.00;\n",
    "   1 ; 021 ; SERRA FACAO  ;  1752.00 ;     0.53 ;     0.62 ;      0.082 ;      15.26;\n",
    "   1 ; 021 ; SERRA FACAO  ;  2441.40 ;     0.73 ;     0.75 ;      0.013 ;       1.83;\n",
    "   1 ; 021 ; SERRA FACAO  ;  3130.80 ;     0.88 ;     0.88 ;      0.000 ;       0.03;\n",
    "   1 ; 021 ; SERRA FACAO  ;  3820.20 ;     1.01 ;     1.01 ;     -0.001 ;      -0.05;\n",
    "   1 ; 021 ; SERRA FACAO  ;  4509.60 ;     1.15 ;     1.14 ;     -0.006 ;      -0.57;\n",
    "   1 ; 027 ; CAPIM BRANC1 ;   228.27 ;     0.06 ;     0.06 ;      0.000 ;       0.02;\n",
    "   1 ; 027 ; CAPIM BRANC1 ;   230.84 ;     0.06 ;     0.06 ;      0.000 ;       0.01;\n",
    "   1 ; 027 ; CAPIM BRANC1 ;   233.41 ;     0.06 ;     0.06 ;      0.000 ;       0.00;\n",
    "   1 ; 027 ; CAPIM BRANC1 ;   235.99 ;     0.06 ;     0.06 ;      0.000 ;       0.00;\n",
    "   1 ; 027 ; CAPIM BRANC1 ;   238.56 ;     0.06 ;     0.06 ;      0.000 ;       0.01;\n",
    "   1 ; 028 ; CAPIM BRANC2 ;   867.55 ;     0.11 ;     0.11 ;      0.000 ;       0.00;\n",
    "   1 ; 029 ; CORUMBA IV   ;  2936.60 ;     2.61 ;     2.59 ;     -0.012 ;      -0.47;\n",
    "   1 ; 029 ; CORUMBA IV   ;  3090.88 ;     2.72 ;     2.72 ;     -0.005 ;      -0.17;\n",
    "   1 ; 029 ; CORUMBA IV   ;  3245.16 ;     2.84 ;     2.84 ;     -0.001 ;      -0.02;\n",
    "   1 ; 029 ; CORUMBA IV   ;  3399.44 ;     2.96 ;     2.96 ;     -0.001 ;      -0.02;\n",
    "   1 ; 029 ; CORUMBA IV   ;  3553.72 ;     3.09 ;     3.09 ;     -0.004 ;      -0.14;\n",
    "   1 ; 048 ; PIRAJU       ;   105.42 ;     0.38 ;     0.38 ;      0.000 ;       0.00;\n",
    "   1 ; 066 ; ITAIPU       ; 27914.01 ;    18.18 ;    18.18 ;      0.000 ;       0.00;\n",
    "   1 ; 131 ; NILO PECANHA ;     9.00 ;     0.00 ;     0.00 ;      0.000 ;       0.00;\n",
    "   1 ; 132 ; FONTES       ;   393.81 ;     0.00 ;     0.00 ;      0.000 ;       0.00;\n",
    "   1 ; 141 ; BAGUARI      ;    32.46 ;    -0.14 ;    -0.14 ;      0.000 ;       0.00;\n",
    "   1 ; 153 ; SAO DOMINGOS ;   131.30 ;     0.25 ;     0.25 ;      0.000 ;       0.00;\n",
    "   1 ; 155 ; RETIRO BAIXO ;   200.72 ;    -0.32 ;    -0.38 ;     -0.057 ;       0.00;\n",
    "   1 ; 155 ; RETIRO BAIXO ;   208.89 ;    -0.39 ;    -0.40 ;     -0.019 ;       0.00;\n",
    "   1 ; 155 ; RETIRO BAIXO ;   217.07 ;    -0.43 ;    -0.43 ;     -0.002 ;       0.00;\n",
    "   1 ; 155 ; RETIRO BAIXO ;   225.24 ;    -0.46 ;    -0.46 ;     -0.002 ;       0.00;\n",
    "   1 ; 155 ; RETIRO BAIXO ;   233.42 ;    -0.47 ;    -0.49 ;     -0.015 ;       0.00;\n",
    "   1 ; 156 ; TRES MARIAS  ;  4250.00 ;    -0.36 ;    -0.40 ;     -0.034 ;       0.00;\n",
    "   1 ; 156 ; TRES MARIAS  ;  7305.60 ;    -0.52 ;    -0.53 ;     -0.003 ;       0.00;\n",
    "   1 ; 156 ; TRES MARIAS  ; 10361.20 ;    -0.65 ;    -0.65 ;      0.001 ;       0.00;\n",
    "   1 ; 156 ; TRES MARIAS  ; 13416.80 ;    -0.78 ;    -0.78 ;      0.001 ;       0.00;\n",
    "   1 ; 156 ; TRES MARIAS  ; 16472.40 ;    -0.93 ;    -0.91 ;      0.015 ;       0.00;\n",
    "   1 ; 162 ; QUEIMADO     ;    95.25 ;     0.33 ;     0.27 ;     -0.061 ;     -18.31;\n",
    "   1 ; 162 ; QUEIMADO     ;   187.60 ;     0.50 ;     0.45 ;     -0.051 ;     -10.29;\n",
    "   1 ; 162 ; QUEIMADO     ;   279.95 ;     0.63 ;     0.62 ;     -0.005 ;      -0.82;\n",
    "   1 ; 162 ; QUEIMADO     ;   372.30 ;     0.80 ;     0.80 ;     -0.005 ;      -0.57;\n",
    "   1 ; 162 ; QUEIMADO     ;   464.65 ;     1.02 ;     0.97 ;     -0.047 ;      -4.61;\n",
    "   1 ; 195 ; JAURU        ;    16.92 ;     0.04 ;     0.04 ;      0.000 ;       0.00;\n",
    "   1 ; 196 ; GUAPORE      ;    22.46 ;     0.07 ;     0.07 ;      0.000 ;       0.00;\n",
    "   1 ; 203 ; CORUMBA III  ;   709.00 ;     0.70 ;     0.70 ;      0.002 ;       0.27;\n",
    "   1 ; 203 ; CORUMBA III  ;   761.60 ;     0.73 ;     0.73 ;      0.000 ;       0.04;\n",
    "   1 ; 203 ; CORUMBA III  ;   814.20 ;     0.77 ;     0.77 ;      0.000 ;       0.00;\n",
    "   1 ; 203 ; CORUMBA III  ;   866.80 ;     0.80 ;     0.80 ;      0.000 ;      -0.01;\n",
    "   1 ; 203 ; CORUMBA III  ;   919.40 ;     0.83 ;     0.83 ;     -0.001 ;      -0.15;\n",
    "   1 ; 227 ; SINOP        ;  1012.40 ;    11.38 ;    10.63 ;     -0.752 ;      -6.61;\n",
    "   1 ; 227 ; SINOP        ;  1424.16 ;    12.37 ;    11.70 ;     -0.668 ;      -5.41;\n",
    "   1 ; 227 ; SINOP        ;  1835.92 ;    12.84 ;    12.76 ;     -0.079 ;      -0.61;\n",
    "   1 ; 227 ; SINOP        ;  2247.68 ;    13.90 ;    13.83 ;     -0.069 ;      -0.50;\n",
    "   1 ; 227 ; SINOP        ;  2659.44 ;    15.40 ;    14.89 ;     -0.505 ;      -3.28;\n",
    "   1 ; 228 ; COLIDER      ;  1495.39 ;     3.27 ;     3.27 ;      0.000 ;       0.00;\n",
    "   1 ; 229 ; TELES PIRES  ;   961.11 ;     5.56 ;     5.56 ;      0.000 ;       0.00;\n",
    "   1 ; 230 ; SAO MANOEL   ;   566.12 ;     2.69 ;     2.69 ;      0.000 ;       0.00;\n",
    "   1 ; 241 ; SLT VERDINHO ;   392.58 ;     0.51 ;     0.51 ;      0.000 ;       0.00;\n",
    "   1 ; 249 ; OURINHOS     ;    20.86 ;     0.13 ;     0.13 ;      0.000 ;       0.00;\n",
    "   1 ; 251 ; SERRA MESA   ; 11150.00 ;    12.27 ;    13.89 ;      1.622 ;      13.23;\n",
    "   1 ; 251 ; SERRA MESA   ; 19800.00 ;    20.03 ;    21.19 ;      1.158 ;       5.78;\n",
    "   1 ; 251 ; SERRA MESA   ; 28450.00 ;    28.33 ;    28.48 ;      0.151 ;       0.53;\n",
    "   1 ; 251 ; SERRA MESA   ; 37100.00 ;    35.63 ;    35.78 ;      0.147 ;       0.41;\n",
    "   1 ; 251 ; SERRA MESA   ; 45750.00 ;    41.95 ;    43.08 ;      1.122 ;       2.67;\n",
    "   1 ; 252 ; CANA BRAVA   ;  2237.79 ;     4.30 ;     4.30 ;      0.000 ;       0.00;\n",
    "   1 ; 253 ; SAO SALVADOR ;   936.28 ;     3.33 ;     3.33 ;      0.000 ;       0.00;\n",
    "   1 ; 257 ; PEIXE ANGIC  ;  2212.70 ;     5.67 ;     5.63 ;     -0.035 ;      -0.61;\n",
    "\n",
]
