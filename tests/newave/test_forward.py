from inewave.newave.forward import Forward
import pandas as pd

ARQ_FORWARD = "./tests/mocks/arquivos/forward.dat"

TAMANHO_REGISTRO = 41264
NUMERO_CLASSES_TERMICAS_SUBMERCADOS = [34, 19, 43, 24]


def test_atributos_encontrados_forward():
    f = Forward.read(
        ARQ_FORWARD,
        tamanho_registro=TAMANHO_REGISTRO,
        numero_estagios=1,
        numero_forwards=2,
        numero_rees=12,
        numero_submercados=4,
        numero_total_submercados=5,
        numero_patamares_carga=3,
        numero_patamares_deficit=1,
        numero_agrupamentos_intercambio=6,
        numero_classes_termicas_submercados=NUMERO_CLASSES_TERMICAS_SUBMERCADOS,
        numero_usinas_hidreletricas=162,
        lag_maximo_usinas_gnl=2,
        numero_parques_eolicos_equivalentes=0,
        numero_estacoes_bombeamento=0,
        nomes_classes_termicas=[
            "ANGRA 1",
            "ANGRA 2",
            "BAIXADA FLU",
            "CUBATAO",
            "CUIABA G CC",
            "DAIA",
            "DO ATLAN_CSA",
            "DO ATLANTICO",
            "GNA I",
            "GNA P. ACU 3",
            "GOIANIA II",
            "IBIRITE",
            "JUIZ DE FORA",
            "LINHARES",
            "MARLIM AZUL",
            "N.PIRATINING",
            "NORTEFLU-1",
            "NORTEFLU-2",
            "NORTEFLU-3",
            "NORTEFLU-4",
            "ONCA PINTADA",
            "PALMEIRAS GO",
            "PIRAT.12 G",
            "R.SILVEIRA",
            "SEROPEDICA",
            "ST.CRUZ 34",
            "ST.CRUZ NOVA",
            "STA VITORIA",
            "T.NORTE 2",
            "TERMOMACAE",
            "TERMORIO",
            "TRES LAGOAS",
            "VIANA",
            "XAVANTES",
            "ARAUCARIA",
            "ARGENTINA 1",
            "ARGENTINA 1B",
            "ARGENTINA 2A",
            "ARGENTINA 2B",
            "ARGENTINA 2C",
            "ARGENTINA 2D",
            "CAMBARA",
            "CANDIOTA 3",
            "CANOAS",
            "CISFRAMA",
            "FIGUEIRA",
            "J.LACERDA A1",
            "J.LACERDA A2",
            "J.LACERDA B",
            "J.LACERDA C",
            "PAMPA SUL",
            "SAO SEPE",
            "URUGUAIANA",
            "ALTOS",
            "ARACATI",
            "BAHIA I",
            "BATURITE",
            "CAMACARI MII",
            "CAMACARI PI",
            "CAMPINA GDE",
            "CAMPO MAIOR",
            "CAUCAIA",
            "CRATO",
            "ENGUIA PECEM",
            "ERB CANDEIAS",
            "FORTALEZA",
            "GLOBAL I",
            "GLOBAL II",
            "IGUATU",
            "JUAZEIRO N",
            "MARACANAU I",
            "MARAMBAIA",
            "MURICY",
            "NAZARIA",
            "P. PECEM I",
            "P. PECEM II",
            "P. SERGIPE I",
            "PAU FERRO I",
            "PECEM II",
            "PERNAMBU_III",
            "PETROLINA",
            "POTIGUAR",
            "POTIGUAR III",
            "PROSPERI III",
            "PROSPERID II",
            "PROSPERIDADE",
            "SUAPE II",
            "SYKUE I",
            "TERMOBAHIA",
            "TERMOCABO",
            "TERMOCEARA",
            "TERMOMANAUS",
            "TERMONE",
            "TERMOPB",
            "TERMOPE",
            "VALE DO ACU",
            "APARECIDA",
            "C. ROCHA",
            "GERAMAR I",
            "GERAMAR II",
            "JARAQUI",
            "MANAUARA",
            "MARAN IV L22",
            "MARAN IV L7",
            "MARAN V L22",
            "MARAN V L7",
            "MARANHAO III",
            "MARANHAO IV",
            "MARANHAO V",
            "MAUA 3",
            "N.VEN 2 L22",
            "N.VEN 2 L7",
            "N.VENECIA 2",
            "NT BARCARENA",
            "O. CANOAS 1",
            "PARNAIBA IV",
            "PARNAIBA V",
            "PONTA NEGRA",
            "PORTO ITAQUI",
            "TAMBAQUI",
        ],
        nomes_usinas_hidreletricas=[
            "FUNIL-GRANDE",
            "BATALHA",
            "SERRA FACAO",
            "CAPIM BRANC1",
            "CAPIM BRANC2",
            "CORUMBA IV",
            "PIRAJU",
            "ITAIPU",
            "NILO PECANHA",
            "FONTES",
            "BAGUARI",
            "SAO DOMINGOS",
            "RETIRO BAIXO",
            "TRES MARIAS",
            "QUEIMADO",
            "JAURU",
            "GUAPORE",
            "CORUMBA III",
            "SINOP",
            "COLIDER",
            "TELES PIRES",
            "SAO MANOEL",
            "SLT VERDINHO",
            "OURINHOS",
            "SERRA MESA",
            "CANA BRAVA",
            "SAO SALVADOR",
            "PEIXE ANGIC",
            "LAJEADO",
            "SALTO",
            "RONDON II",
            "PONTE PEDRA",
            "JIRAU",
            "STO ANTONIO",
            "ESPORA",
            "ITIQUIRA I",
            "ITIQUIRA II",
            "DARDANELOS",
            "CACU",
            "B. COQUEIROS",
            "FOZ R. CLARO",
            "FICT.MAUA",
            "GUARAPIRANGA",
            "BILLINGS",
            "HENRY BORDEN",
            "JAGUARI",
            "PARAIBUNA",
            "SANTA BRANCA",
            "FUNIL",
            "LAJES",
            "PICADA",
            "SOBRAGI",
            "SIMPLICIO",
            "ILHA POMBOS",
            "P. PASSOS",
            "SALTO GRANDE",
            "P. ESTRELA",
            "CANDONGA",
            "AIMORES",
            "MASCARENHAS",
            "GUILMAN-AMOR",
            "SA CARVALHO",
            "ROSAL",
            "SAMUEL",
            "IRAPE",
            "STA CLARA MG",
            "CAMARGOS",
            "ITUTINGA",
            "FURNAS",
            "M. DE MORAES",
            "ESTREITO",
            "JAGUARA",
            "IGARAPAVA",
            "VOLTA GRANDE",
            "P. COLOMBIA",
            "CACONDE",
            "E. DA CUNHA",
            "A.S.OLIVEIRA",
            "MARIMBONDO",
            "A. VERMELHA",
            "I. SOLTEIRA",
            "EMBORCACAO",
            "NOVA PONTE",
            "MIRANDA",
            "CORUMBA I",
            "ITUMBIARA",
            "CACH.DOURADA",
            "SAO SIMAO",
            "BARRA BONITA",
            "A.S. LIMA",
            "IBITINGA",
            "PROMISSAO",
            "NAVANHANDAVA",
            "TRES IRMAOS",
            "JUPIA",
            "P. PRIMAVERA",
            "MANSO",
            "A.A. LAYDNER",
            "CHAVANTES",
            "L.N. GARCEZ",
            "CANOAS II",
            "CANOAS I",
            "CAPIVARA",
            "TAQUARUCU",
            "ROSANA",
            "MAUA",
            "STA CLARA PR",
            "FUNDAO",
            "G.B. MUNHOZ",
            "BAIXO IGUACU",
            "BARRA GRANDE",
            "GARIBALDI",
            "CAMPOS NOVOS",
            "MACHADINHO",
            "ITA",
            "PASSO FUNDO",
            "MONJOLINHO",
            "QUEBRA QUEIX",
            "SAO JOSE",
            "PASSO S JOAO",
            "FOZ CHAPECO",
            "CASTRO ALVES",
            "MONTE CLARO",
            "14 DE JULHO",
            "ERNESTINA",
            "PASSO REAL",
            "JACUI",
            "ITAUBA",
            "D. FRANCISCA",
            "G.P. SOUZA",
            "SALTO PILAO",
            "JORDAO",
            "SEGREDO",
            "SLT.SANTIAGO",
            "SALTO OSORIO",
            "SALTO CAXIAS",
            "SOBRADINHO",
            "ITAPARICA",
            "COMP PAF-MOX",
            "XINGO",
            "FICT.QUEIMAD",
            "FICT.TRES MA",
            "FICT.RETIRO",
            "ITAPEBI",
            "FICT.IRAPE",
            "P. CAVALO",
            "B. ESPERANCA",
            "CACH.CALDEIR",
            "ESTREITO TOC",
            "TUCURUI",
            "BALBINA",
            "COARACY NUNE",
            "FERREIRA GOM",
            "STO ANT JARI",
            "FICT.SERRA M",
            "FICT.CANA BR",
            "FICT.LAJEADO",
            "FICT.PEIXE A",
            "FICT.SAO SAL",
            "PIMENTAL",
            "CURUA-UNA",
            "BELO MONTE",
        ],
    )
    assert isinstance(f.volume_armazenado_absoluto_final, pd.DataFrame)


def test_eq_forward():
    f1 = Forward.read(
        ARQ_FORWARD,
        tamanho_registro=TAMANHO_REGISTRO,
        numero_estagios=1,
        numero_forwards=2,
        numero_rees=12,
        numero_submercados=4,
        numero_total_submercados=5,
        numero_patamares_carga=3,
        numero_patamares_deficit=1,
        numero_agrupamentos_intercambio=6,
        numero_classes_termicas_submercados=NUMERO_CLASSES_TERMICAS_SUBMERCADOS,
        numero_usinas_hidreletricas=162,
        lag_maximo_usinas_gnl=2,
        numero_parques_eolicos_equivalentes=0,
        numero_estacoes_bombeamento=0,
        nomes_classes_termicas=[
            "ANGRA 1",
            "ANGRA 2",
            "BAIXADA FLU",
            "CUBATAO",
            "CUIABA G CC",
            "DAIA",
            "DO ATLAN_CSA",
            "DO ATLANTICO",
            "GNA I",
            "GNA P. ACU 3",
            "GOIANIA II",
            "IBIRITE",
            "JUIZ DE FORA",
            "LINHARES",
            "MARLIM AZUL",
            "N.PIRATINING",
            "NORTEFLU-1",
            "NORTEFLU-2",
            "NORTEFLU-3",
            "NORTEFLU-4",
            "ONCA PINTADA",
            "PALMEIRAS GO",
            "PIRAT.12 G",
            "R.SILVEIRA",
            "SEROPEDICA",
            "ST.CRUZ 34",
            "ST.CRUZ NOVA",
            "STA VITORIA",
            "T.NORTE 2",
            "TERMOMACAE",
            "TERMORIO",
            "TRES LAGOAS",
            "VIANA",
            "XAVANTES",
            "ARAUCARIA",
            "ARGENTINA 1",
            "ARGENTINA 1B",
            "ARGENTINA 2A",
            "ARGENTINA 2B",
            "ARGENTINA 2C",
            "ARGENTINA 2D",
            "CAMBARA",
            "CANDIOTA 3",
            "CANOAS",
            "CISFRAMA",
            "FIGUEIRA",
            "J.LACERDA A1",
            "J.LACERDA A2",
            "J.LACERDA B",
            "J.LACERDA C",
            "PAMPA SUL",
            "SAO SEPE",
            "URUGUAIANA",
            "ALTOS",
            "ARACATI",
            "BAHIA I",
            "BATURITE",
            "CAMACARI MII",
            "CAMACARI PI",
            "CAMPINA GDE",
            "CAMPO MAIOR",
            "CAUCAIA",
            "CRATO",
            "ENGUIA PECEM",
            "ERB CANDEIAS",
            "FORTALEZA",
            "GLOBAL I",
            "GLOBAL II",
            "IGUATU",
            "JUAZEIRO N",
            "MARACANAU I",
            "MARAMBAIA",
            "MURICY",
            "NAZARIA",
            "P. PECEM I",
            "P. PECEM II",
            "P. SERGIPE I",
            "PAU FERRO I",
            "PECEM II",
            "PERNAMBU_III",
            "PETROLINA",
            "POTIGUAR",
            "POTIGUAR III",
            "PROSPERI III",
            "PROSPERID II",
            "PROSPERIDADE",
            "SUAPE II",
            "SYKUE I",
            "TERMOBAHIA",
            "TERMOCABO",
            "TERMOCEARA",
            "TERMOMANAUS",
            "TERMONE",
            "TERMOPB",
            "TERMOPE",
            "VALE DO ACU",
            "APARECIDA",
            "C. ROCHA",
            "GERAMAR I",
            "GERAMAR II",
            "JARAQUI",
            "MANAUARA",
            "MARAN IV L22",
            "MARAN IV L7",
            "MARAN V L22",
            "MARAN V L7",
            "MARANHAO III",
            "MARANHAO IV",
            "MARANHAO V",
            "MAUA 3",
            "N.VEN 2 L22",
            "N.VEN 2 L7",
            "N.VENECIA 2",
            "NT BARCARENA",
            "O. CANOAS 1",
            "PARNAIBA IV",
            "PARNAIBA V",
            "PONTA NEGRA",
            "PORTO ITAQUI",
            "TAMBAQUI",
        ],
        nomes_usinas_hidreletricas=[
            "FUNIL-GRANDE",
            "BATALHA",
            "SERRA FACAO",
            "CAPIM BRANC1",
            "CAPIM BRANC2",
            "CORUMBA IV",
            "PIRAJU",
            "ITAIPU",
            "NILO PECANHA",
            "FONTES",
            "BAGUARI",
            "SAO DOMINGOS",
            "RETIRO BAIXO",
            "TRES MARIAS",
            "QUEIMADO",
            "JAURU",
            "GUAPORE",
            "CORUMBA III",
            "SINOP",
            "COLIDER",
            "TELES PIRES",
            "SAO MANOEL",
            "SLT VERDINHO",
            "OURINHOS",
            "SERRA MESA",
            "CANA BRAVA",
            "SAO SALVADOR",
            "PEIXE ANGIC",
            "LAJEADO",
            "SALTO",
            "RONDON II",
            "PONTE PEDRA",
            "JIRAU",
            "STO ANTONIO",
            "ESPORA",
            "ITIQUIRA I",
            "ITIQUIRA II",
            "DARDANELOS",
            "CACU",
            "B. COQUEIROS",
            "FOZ R. CLARO",
            "FICT.MAUA",
            "GUARAPIRANGA",
            "BILLINGS",
            "HENRY BORDEN",
            "JAGUARI",
            "PARAIBUNA",
            "SANTA BRANCA",
            "FUNIL",
            "LAJES",
            "PICADA",
            "SOBRAGI",
            "SIMPLICIO",
            "ILHA POMBOS",
            "P. PASSOS",
            "SALTO GRANDE",
            "P. ESTRELA",
            "CANDONGA",
            "AIMORES",
            "MASCARENHAS",
            "GUILMAN-AMOR",
            "SA CARVALHO",
            "ROSAL",
            "SAMUEL",
            "IRAPE",
            "STA CLARA MG",
            "CAMARGOS",
            "ITUTINGA",
            "FURNAS",
            "M. DE MORAES",
            "ESTREITO",
            "JAGUARA",
            "IGARAPAVA",
            "VOLTA GRANDE",
            "P. COLOMBIA",
            "CACONDE",
            "E. DA CUNHA",
            "A.S.OLIVEIRA",
            "MARIMBONDO",
            "A. VERMELHA",
            "I. SOLTEIRA",
            "EMBORCACAO",
            "NOVA PONTE",
            "MIRANDA",
            "CORUMBA I",
            "ITUMBIARA",
            "CACH.DOURADA",
            "SAO SIMAO",
            "BARRA BONITA",
            "A.S. LIMA",
            "IBITINGA",
            "PROMISSAO",
            "NAVANHANDAVA",
            "TRES IRMAOS",
            "JUPIA",
            "P. PRIMAVERA",
            "MANSO",
            "A.A. LAYDNER",
            "CHAVANTES",
            "L.N. GARCEZ",
            "CANOAS II",
            "CANOAS I",
            "CAPIVARA",
            "TAQUARUCU",
            "ROSANA",
            "MAUA",
            "STA CLARA PR",
            "FUNDAO",
            "G.B. MUNHOZ",
            "BAIXO IGUACU",
            "BARRA GRANDE",
            "GARIBALDI",
            "CAMPOS NOVOS",
            "MACHADINHO",
            "ITA",
            "PASSO FUNDO",
            "MONJOLINHO",
            "QUEBRA QUEIX",
            "SAO JOSE",
            "PASSO S JOAO",
            "FOZ CHAPECO",
            "CASTRO ALVES",
            "MONTE CLARO",
            "14 DE JULHO",
            "ERNESTINA",
            "PASSO REAL",
            "JACUI",
            "ITAUBA",
            "D. FRANCISCA",
            "G.P. SOUZA",
            "SALTO PILAO",
            "JORDAO",
            "SEGREDO",
            "SLT.SANTIAGO",
            "SALTO OSORIO",
            "SALTO CAXIAS",
            "SOBRADINHO",
            "ITAPARICA",
            "COMP PAF-MOX",
            "XINGO",
            "FICT.QUEIMAD",
            "FICT.TRES MA",
            "FICT.RETIRO",
            "ITAPEBI",
            "FICT.IRAPE",
            "P. CAVALO",
            "B. ESPERANCA",
            "CACH.CALDEIR",
            "ESTREITO TOC",
            "TUCURUI",
            "BALBINA",
            "COARACY NUNE",
            "FERREIRA GOM",
            "STO ANT JARI",
            "FICT.SERRA M",
            "FICT.CANA BR",
            "FICT.LAJEADO",
            "FICT.PEIXE A",
            "FICT.SAO SAL",
            "PIMENTAL",
            "CURUA-UNA",
            "BELO MONTE",
        ],
    )
    f2 = Forward.read(
        ARQ_FORWARD,
        tamanho_registro=TAMANHO_REGISTRO,
        numero_estagios=1,
        numero_forwards=2,
        numero_rees=12,
        numero_submercados=4,
        numero_total_submercados=5,
        numero_patamares_carga=3,
        numero_patamares_deficit=1,
        numero_agrupamentos_intercambio=6,
        numero_classes_termicas_submercados=NUMERO_CLASSES_TERMICAS_SUBMERCADOS,
        numero_usinas_hidreletricas=162,
        lag_maximo_usinas_gnl=2,
        numero_parques_eolicos_equivalentes=0,
        numero_estacoes_bombeamento=0,
        nomes_classes_termicas=[
            "ANGRA 1",
            "ANGRA 2",
            "BAIXADA FLU",
            "CUBATAO",
            "CUIABA G CC",
            "DAIA",
            "DO ATLAN_CSA",
            "DO ATLANTICO",
            "GNA I",
            "GNA P. ACU 3",
            "GOIANIA II",
            "IBIRITE",
            "JUIZ DE FORA",
            "LINHARES",
            "MARLIM AZUL",
            "N.PIRATINING",
            "NORTEFLU-1",
            "NORTEFLU-2",
            "NORTEFLU-3",
            "NORTEFLU-4",
            "ONCA PINTADA",
            "PALMEIRAS GO",
            "PIRAT.12 G",
            "R.SILVEIRA",
            "SEROPEDICA",
            "ST.CRUZ 34",
            "ST.CRUZ NOVA",
            "STA VITORIA",
            "T.NORTE 2",
            "TERMOMACAE",
            "TERMORIO",
            "TRES LAGOAS",
            "VIANA",
            "XAVANTES",
            "ARAUCARIA",
            "ARGENTINA 1",
            "ARGENTINA 1B",
            "ARGENTINA 2A",
            "ARGENTINA 2B",
            "ARGENTINA 2C",
            "ARGENTINA 2D",
            "CAMBARA",
            "CANDIOTA 3",
            "CANOAS",
            "CISFRAMA",
            "FIGUEIRA",
            "J.LACERDA A1",
            "J.LACERDA A2",
            "J.LACERDA B",
            "J.LACERDA C",
            "PAMPA SUL",
            "SAO SEPE",
            "URUGUAIANA",
            "ALTOS",
            "ARACATI",
            "BAHIA I",
            "BATURITE",
            "CAMACARI MII",
            "CAMACARI PI",
            "CAMPINA GDE",
            "CAMPO MAIOR",
            "CAUCAIA",
            "CRATO",
            "ENGUIA PECEM",
            "ERB CANDEIAS",
            "FORTALEZA",
            "GLOBAL I",
            "GLOBAL II",
            "IGUATU",
            "JUAZEIRO N",
            "MARACANAU I",
            "MARAMBAIA",
            "MURICY",
            "NAZARIA",
            "P. PECEM I",
            "P. PECEM II",
            "P. SERGIPE I",
            "PAU FERRO I",
            "PECEM II",
            "PERNAMBU_III",
            "PETROLINA",
            "POTIGUAR",
            "POTIGUAR III",
            "PROSPERI III",
            "PROSPERID II",
            "PROSPERIDADE",
            "SUAPE II",
            "SYKUE I",
            "TERMOBAHIA",
            "TERMOCABO",
            "TERMOCEARA",
            "TERMOMANAUS",
            "TERMONE",
            "TERMOPB",
            "TERMOPE",
            "VALE DO ACU",
            "APARECIDA",
            "C. ROCHA",
            "GERAMAR I",
            "GERAMAR II",
            "JARAQUI",
            "MANAUARA",
            "MARAN IV L22",
            "MARAN IV L7",
            "MARAN V L22",
            "MARAN V L7",
            "MARANHAO III",
            "MARANHAO IV",
            "MARANHAO V",
            "MAUA 3",
            "N.VEN 2 L22",
            "N.VEN 2 L7",
            "N.VENECIA 2",
            "NT BARCARENA",
            "O. CANOAS 1",
            "PARNAIBA IV",
            "PARNAIBA V",
            "PONTA NEGRA",
            "PORTO ITAQUI",
            "TAMBAQUI",
        ],
        nomes_usinas_hidreletricas=[
            "FUNIL-GRANDE",
            "BATALHA",
            "SERRA FACAO",
            "CAPIM BRANC1",
            "CAPIM BRANC2",
            "CORUMBA IV",
            "PIRAJU",
            "ITAIPU",
            "NILO PECANHA",
            "FONTES",
            "BAGUARI",
            "SAO DOMINGOS",
            "RETIRO BAIXO",
            "TRES MARIAS",
            "QUEIMADO",
            "JAURU",
            "GUAPORE",
            "CORUMBA III",
            "SINOP",
            "COLIDER",
            "TELES PIRES",
            "SAO MANOEL",
            "SLT VERDINHO",
            "OURINHOS",
            "SERRA MESA",
            "CANA BRAVA",
            "SAO SALVADOR",
            "PEIXE ANGIC",
            "LAJEADO",
            "SALTO",
            "RONDON II",
            "PONTE PEDRA",
            "JIRAU",
            "STO ANTONIO",
            "ESPORA",
            "ITIQUIRA I",
            "ITIQUIRA II",
            "DARDANELOS",
            "CACU",
            "B. COQUEIROS",
            "FOZ R. CLARO",
            "FICT.MAUA",
            "GUARAPIRANGA",
            "BILLINGS",
            "HENRY BORDEN",
            "JAGUARI",
            "PARAIBUNA",
            "SANTA BRANCA",
            "FUNIL",
            "LAJES",
            "PICADA",
            "SOBRAGI",
            "SIMPLICIO",
            "ILHA POMBOS",
            "P. PASSOS",
            "SALTO GRANDE",
            "P. ESTRELA",
            "CANDONGA",
            "AIMORES",
            "MASCARENHAS",
            "GUILMAN-AMOR",
            "SA CARVALHO",
            "ROSAL",
            "SAMUEL",
            "IRAPE",
            "STA CLARA MG",
            "CAMARGOS",
            "ITUTINGA",
            "FURNAS",
            "M. DE MORAES",
            "ESTREITO",
            "JAGUARA",
            "IGARAPAVA",
            "VOLTA GRANDE",
            "P. COLOMBIA",
            "CACONDE",
            "E. DA CUNHA",
            "A.S.OLIVEIRA",
            "MARIMBONDO",
            "A. VERMELHA",
            "I. SOLTEIRA",
            "EMBORCACAO",
            "NOVA PONTE",
            "MIRANDA",
            "CORUMBA I",
            "ITUMBIARA",
            "CACH.DOURADA",
            "SAO SIMAO",
            "BARRA BONITA",
            "A.S. LIMA",
            "IBITINGA",
            "PROMISSAO",
            "NAVANHANDAVA",
            "TRES IRMAOS",
            "JUPIA",
            "P. PRIMAVERA",
            "MANSO",
            "A.A. LAYDNER",
            "CHAVANTES",
            "L.N. GARCEZ",
            "CANOAS II",
            "CANOAS I",
            "CAPIVARA",
            "TAQUARUCU",
            "ROSANA",
            "MAUA",
            "STA CLARA PR",
            "FUNDAO",
            "G.B. MUNHOZ",
            "BAIXO IGUACU",
            "BARRA GRANDE",
            "GARIBALDI",
            "CAMPOS NOVOS",
            "MACHADINHO",
            "ITA",
            "PASSO FUNDO",
            "MONJOLINHO",
            "QUEBRA QUEIX",
            "SAO JOSE",
            "PASSO S JOAO",
            "FOZ CHAPECO",
            "CASTRO ALVES",
            "MONTE CLARO",
            "14 DE JULHO",
            "ERNESTINA",
            "PASSO REAL",
            "JACUI",
            "ITAUBA",
            "D. FRANCISCA",
            "G.P. SOUZA",
            "SALTO PILAO",
            "JORDAO",
            "SEGREDO",
            "SLT.SANTIAGO",
            "SALTO OSORIO",
            "SALTO CAXIAS",
            "SOBRADINHO",
            "ITAPARICA",
            "COMP PAF-MOX",
            "XINGO",
            "FICT.QUEIMAD",
            "FICT.TRES MA",
            "FICT.RETIRO",
            "ITAPEBI",
            "FICT.IRAPE",
            "P. CAVALO",
            "B. ESPERANCA",
            "CACH.CALDEIR",
            "ESTREITO TOC",
            "TUCURUI",
            "BALBINA",
            "COARACY NUNE",
            "FERREIRA GOM",
            "STO ANT JARI",
            "FICT.SERRA M",
            "FICT.CANA BR",
            "FICT.LAJEADO",
            "FICT.PEIXE A",
            "FICT.SAO SAL",
            "PIMENTAL",
            "CURUA-UNA",
            "BELO MONTE",
        ],
    )
    assert f1 == f2


def test_atributos_forward():
    f = Forward.read(
        ARQ_FORWARD,
        tamanho_registro=TAMANHO_REGISTRO,
        numero_estagios=1,
        numero_forwards=2,
        numero_rees=12,
        numero_submercados=4,
        numero_total_submercados=5,
        numero_patamares_carga=3,
        numero_patamares_deficit=1,
        numero_agrupamentos_intercambio=6,
        numero_classes_termicas_submercados=NUMERO_CLASSES_TERMICAS_SUBMERCADOS,
        numero_usinas_hidreletricas=162,
        lag_maximo_usinas_gnl=2,
        numero_parques_eolicos_equivalentes=0,
        numero_estacoes_bombeamento=0,
        nomes_classes_termicas=[
            "ANGRA 1",
            "ANGRA 2",
            "BAIXADA FLU",
            "CUBATAO",
            "CUIABA G CC",
            "DAIA",
            "DO ATLAN_CSA",
            "DO ATLANTICO",
            "GNA I",
            "GNA P. ACU 3",
            "GOIANIA II",
            "IBIRITE",
            "JUIZ DE FORA",
            "LINHARES",
            "MARLIM AZUL",
            "N.PIRATINING",
            "NORTEFLU-1",
            "NORTEFLU-2",
            "NORTEFLU-3",
            "NORTEFLU-4",
            "ONCA PINTADA",
            "PALMEIRAS GO",
            "PIRAT.12 G",
            "R.SILVEIRA",
            "SEROPEDICA",
            "ST.CRUZ 34",
            "ST.CRUZ NOVA",
            "STA VITORIA",
            "T.NORTE 2",
            "TERMOMACAE",
            "TERMORIO",
            "TRES LAGOAS",
            "VIANA",
            "XAVANTES",
            "ARAUCARIA",
            "ARGENTINA 1",
            "ARGENTINA 1B",
            "ARGENTINA 2A",
            "ARGENTINA 2B",
            "ARGENTINA 2C",
            "ARGENTINA 2D",
            "CAMBARA",
            "CANDIOTA 3",
            "CANOAS",
            "CISFRAMA",
            "FIGUEIRA",
            "J.LACERDA A1",
            "J.LACERDA A2",
            "J.LACERDA B",
            "J.LACERDA C",
            "PAMPA SUL",
            "SAO SEPE",
            "URUGUAIANA",
            "ALTOS",
            "ARACATI",
            "BAHIA I",
            "BATURITE",
            "CAMACARI MII",
            "CAMACARI PI",
            "CAMPINA GDE",
            "CAMPO MAIOR",
            "CAUCAIA",
            "CRATO",
            "ENGUIA PECEM",
            "ERB CANDEIAS",
            "FORTALEZA",
            "GLOBAL I",
            "GLOBAL II",
            "IGUATU",
            "JUAZEIRO N",
            "MARACANAU I",
            "MARAMBAIA",
            "MURICY",
            "NAZARIA",
            "P. PECEM I",
            "P. PECEM II",
            "P. SERGIPE I",
            "PAU FERRO I",
            "PECEM II",
            "PERNAMBU_III",
            "PETROLINA",
            "POTIGUAR",
            "POTIGUAR III",
            "PROSPERI III",
            "PROSPERID II",
            "PROSPERIDADE",
            "SUAPE II",
            "SYKUE I",
            "TERMOBAHIA",
            "TERMOCABO",
            "TERMOCEARA",
            "TERMOMANAUS",
            "TERMONE",
            "TERMOPB",
            "TERMOPE",
            "VALE DO ACU",
            "APARECIDA",
            "C. ROCHA",
            "GERAMAR I",
            "GERAMAR II",
            "JARAQUI",
            "MANAUARA",
            "MARAN IV L22",
            "MARAN IV L7",
            "MARAN V L22",
            "MARAN V L7",
            "MARANHAO III",
            "MARANHAO IV",
            "MARANHAO V",
            "MAUA 3",
            "N.VEN 2 L22",
            "N.VEN 2 L7",
            "N.VENECIA 2",
            "NT BARCARENA",
            "O. CANOAS 1",
            "PARNAIBA IV",
            "PARNAIBA V",
            "PONTA NEGRA",
            "PORTO ITAQUI",
            "TAMBAQUI",
        ],
        nomes_usinas_hidreletricas=[
            "FUNIL-GRANDE",
            "BATALHA",
            "SERRA FACAO",
            "CAPIM BRANC1",
            "CAPIM BRANC2",
            "CORUMBA IV",
            "PIRAJU",
            "ITAIPU",
            "NILO PECANHA",
            "FONTES",
            "BAGUARI",
            "SAO DOMINGOS",
            "RETIRO BAIXO",
            "TRES MARIAS",
            "QUEIMADO",
            "JAURU",
            "GUAPORE",
            "CORUMBA III",
            "SINOP",
            "COLIDER",
            "TELES PIRES",
            "SAO MANOEL",
            "SLT VERDINHO",
            "OURINHOS",
            "SERRA MESA",
            "CANA BRAVA",
            "SAO SALVADOR",
            "PEIXE ANGIC",
            "LAJEADO",
            "SALTO",
            "RONDON II",
            "PONTE PEDRA",
            "JIRAU",
            "STO ANTONIO",
            "ESPORA",
            "ITIQUIRA I",
            "ITIQUIRA II",
            "DARDANELOS",
            "CACU",
            "B. COQUEIROS",
            "FOZ R. CLARO",
            "FICT.MAUA",
            "GUARAPIRANGA",
            "BILLINGS",
            "HENRY BORDEN",
            "JAGUARI",
            "PARAIBUNA",
            "SANTA BRANCA",
            "FUNIL",
            "LAJES",
            "PICADA",
            "SOBRAGI",
            "SIMPLICIO",
            "ILHA POMBOS",
            "P. PASSOS",
            "SALTO GRANDE",
            "P. ESTRELA",
            "CANDONGA",
            "AIMORES",
            "MASCARENHAS",
            "GUILMAN-AMOR",
            "SA CARVALHO",
            "ROSAL",
            "SAMUEL",
            "IRAPE",
            "STA CLARA MG",
            "CAMARGOS",
            "ITUTINGA",
            "FURNAS",
            "M. DE MORAES",
            "ESTREITO",
            "JAGUARA",
            "IGARAPAVA",
            "VOLTA GRANDE",
            "P. COLOMBIA",
            "CACONDE",
            "E. DA CUNHA",
            "A.S.OLIVEIRA",
            "MARIMBONDO",
            "A. VERMELHA",
            "I. SOLTEIRA",
            "EMBORCACAO",
            "NOVA PONTE",
            "MIRANDA",
            "CORUMBA I",
            "ITUMBIARA",
            "CACH.DOURADA",
            "SAO SIMAO",
            "BARRA BONITA",
            "A.S. LIMA",
            "IBITINGA",
            "PROMISSAO",
            "NAVANHANDAVA",
            "TRES IRMAOS",
            "JUPIA",
            "P. PRIMAVERA",
            "MANSO",
            "A.A. LAYDNER",
            "CHAVANTES",
            "L.N. GARCEZ",
            "CANOAS II",
            "CANOAS I",
            "CAPIVARA",
            "TAQUARUCU",
            "ROSANA",
            "MAUA",
            "STA CLARA PR",
            "FUNDAO",
            "G.B. MUNHOZ",
            "BAIXO IGUACU",
            "BARRA GRANDE",
            "GARIBALDI",
            "CAMPOS NOVOS",
            "MACHADINHO",
            "ITA",
            "PASSO FUNDO",
            "MONJOLINHO",
            "QUEBRA QUEIX",
            "SAO JOSE",
            "PASSO S JOAO",
            "FOZ CHAPECO",
            "CASTRO ALVES",
            "MONTE CLARO",
            "14 DE JULHO",
            "ERNESTINA",
            "PASSO REAL",
            "JACUI",
            "ITAUBA",
            "D. FRANCISCA",
            "G.P. SOUZA",
            "SALTO PILAO",
            "JORDAO",
            "SEGREDO",
            "SLT.SANTIAGO",
            "SALTO OSORIO",
            "SALTO CAXIAS",
            "SOBRADINHO",
            "ITAPARICA",
            "COMP PAF-MOX",
            "XINGO",
            "FICT.QUEIMAD",
            "FICT.TRES MA",
            "FICT.RETIRO",
            "ITAPEBI",
            "FICT.IRAPE",
            "P. CAVALO",
            "B. ESPERANCA",
            "CACH.CALDEIR",
            "ESTREITO TOC",
            "TUCURUI",
            "BALBINA",
            "COARACY NUNE",
            "FERREIRA GOM",
            "STO ANT JARI",
            "FICT.SERRA M",
            "FICT.CANA BR",
            "FICT.LAJEADO",
            "FICT.PEIXE A",
            "FICT.SAO SAL",
            "PIMENTAL",
            "CURUA-UNA",
            "BELO MONTE",
        ],
    )

    assert f.mercado_liquido.shape == (8, 4)
    assert f.energia_armazenada_absoluta_inicial.shape == (24, 4)
    assert f.energia_natural_afluente.shape == (24, 4)
    assert f.geracao_hidraulica_controlavel.shape == (72, 5)
    assert f.energia_vertida.shape == (24, 4)
    assert f.energia_armazenada_absoluta_final.shape == (24, 4)
    assert f.energia_natural_afluente_fio_bruta.shape == (24, 4)
    assert f.energia_evaporada.shape == (24, 4)
    assert f.energia_enchimento_volume_morto.shape == (24, 4)
    assert f.geracao_termica.shape == (720, 5)
    assert f.deficit.shape == (24, 6)
    assert f.valor_agua.shape == (24, 4)
    assert f.custo_marginal_operacao.shape == (24, 5)
    assert f.geracao_hidraulica_fio_liquida.shape == (24, 4)
    assert f.perdas_geracao_hidraulica_fio.shape == (24, 4)
    assert f.intercambio.shape == (120, 6)
    assert f.excesso.shape == (24, 5)
    assert f.energia_natural_afluente_bruta.shape == (24, 4)
    assert f.energia_natural_afluente_controlavel_corrigida.shape == (24, 4)
    assert f.geracao_hidraulica_maxima.shape == (72, 5)
    assert f.energia_afluente_controlavel_desvio.shape == (24, 4)
    assert f.energia_afluente_fio_desvio.shape == (24, 4)
    assert f.beneficio_intercambio.shape == (120, 6)
    assert f.fator_correcao_energia_natural_afluente_controlavel.shape == (
        24,
        4,
    )
    assert f.violacao_curva_aversao.shape == (24, 4)
    assert f.acionamento_curva_aversao.shape == (24, 4)
    assert f.penalidade_curva_aversao.shape == (24, 4)
    assert f.custo_operacao.shape == (2, 3)
    assert f.custo_geracao_termica.shape == (8, 4)
    assert f.beneficio_agrupamento_intercambio.shape == (36, 5)
    assert f.energia_natural_afluente_fio.shape == (24, 4)
    assert f.beneficio_despacho_gnl.shape == (48, 6)
    assert f.violacao_geracao_hidraulica_minima.shape == (72, 5)
    assert f.violacao_energia_vazao_minima.shape == (24, 4)
    assert (
        f.geracao_hidraulica_maxima_considerando_restricoes_eletricas.shape
        == (72, 5)
    )
    assert f.volume_armazenado_absoluto_final.shape == (324, 4)
    assert f.geracao_hidraulica_usina.shape == (972, 5)
    assert f.volume_turbinado.shape == (972, 5)
    assert f.volume_vertido.shape == (972, 5)
    assert f.violacao_geracao_hidraulica_minima_usina.shape == (972, 5)
    assert f.enchimento_volume_morto_usina.shape == (324, 4)
    assert f.violacao_defluencia_minima.shape == (972, 5)
    assert f.volume_desvio_usina.shape == (324, 4)
    assert f.volume_desvio_positivo_usina.shape == (324, 4)
    assert f.volume_desvio_negativo_usina.shape == (324, 4)
    assert f.violacao_fpha.shape == (972, 5)
    assert f.vazao_afluente.shape == (324, 4)
    assert f.vazao_incremental.shape == (324, 4)
    assert f.volume_armazenado_percentual_final.shape == (324, 4)
    assert f.custo_violacao_energia_vazao_minima.shape == (24, 4)
    assert f.custo_energia_afluente_controlavel_desvio.shape == (24, 4)
    assert f.custo_energia_afluente_fio_desvio.shape == (24, 4)
    assert f.custo_violacao_geracao_hidraulica_minima.shape == (72, 5)
    assert f.geracao_eolica.shape == (0, 5)
    assert f.velocidade_vento.shape == (0, 4)
    assert f.violacao_funcao_producao_eolica.shape == (0, 5)
    assert f.violacao_defluencia_maxima.shape == (972, 5)
    assert f.violacao_turbinamento_maximo.shape == (972, 5)
    assert f.violacao_turbinamento_minimo.shape == (972, 5)
    assert f.violacao_lpp_turbinamento_maximo.shape == (72, 5)
    assert f.violacao_lpp_defluencia_maxima.shape == (72, 5)
    assert f.violacao_lpp_turbinamento_maximo_usina.shape == (972, 5)
    assert f.violacao_lpp_defluencia_maxima_usina.shape == (972, 5)
    assert f.rhs_lpp_turbinamento_maximo.shape == (72, 5)
    assert f.rhs_lpp_defluencia_maxima.shape == (72, 5)
    assert f.rhs_lpp_turbinamento_maximo_usina.shape == (972, 5)
    assert f.rhs_lpp_defluencia_maxima_usina.shape == (972, 5)
    assert f.violacao_restricoes_eletricas_especiais.shape == (0, 5)
    assert f.custo_restricoes_eletricas_especiais.shape == (0, 5)
    assert f.volume_armazenado_absoluto_inicial.shape == (324, 4)
    assert f.valor_agua_usina.shape == (324, 4)
    assert f.volume_evaporado.shape == (324, 4)
    assert f.volume_bombeado.shape == (0, 5)
    assert f.consumo_energia_estacao_bombeamento.shape == (0, 5)
    assert f.volume_canal_desvio_usina.shape == (972, 5)
