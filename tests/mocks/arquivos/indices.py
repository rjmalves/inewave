MockIndices = [
    "&**************************************************;;\n",
    "& Descricao colunas:;;\n",
    "&**************************************************;;\n",
    "& ID: Id dos cards de indice;;\n",
    "& Descricao: Descricao do card Índice;;\n",
    "& Caminho: Caminho do arquivo com os dados dos cards para o indice;;\n",
    "&    ID                                                ;Descricao                                                   ;Caminho                                                                         \n",
    "     HIDRELETRICA-CADASTRO-RESERVATORIO-CURVAJUSANTE   ;pol                                                         ;polinjus.csv              \n",
    " PARQUE-EOLICO-EQUIVALENTE-CADASTRO                    ;Dados de usinas renovaveis                                     ;renovaveis.csv\n",
    " PARQUE-EOLICO-EQUIVALENTE-CONFIGURACAO                ;Dados de usinas renovaveis                                     ;renovaveis.csv\n",
    " PARQUE-EOLICO-EQUIVALENTE-SUBMERCADO                  ;Dados de usinas renovaveis                                     ;renovaveis.csv\n",
    " RESTRICAO-ELETRICA-ESPECIAL                       ;Dados da funcionalidade restricao-eletrica-especial         ;lib_restricao-eletrica-especial.csv                                             \n",
    "HIDRELETRICA-CADASTRO-RESERVATORIO ; ; volumes-referencia.csv\n",
    "&HIDRELETRICA-FPHA-METODO-REDUCAO-CORTES; ; tratamento-fpha.csv\n",
]

MockIndicesRepetidos = [
    "& Identificadores repetidos;;\n",
    "RESTRICAO-ELETRICA-ESPECIAL;;restricao-eletrica.csv\n",
    "restricao-eletrica-especial;;restricao-eletrica-2.csv\n",
    "RESTRICAO-ELETRICA-ESPECIAL;;restricao-eletrica-3.csv\n",
]

MockRegistroIndice = " RESTRICAO-ELETRICA-ESPECIAL                       ;Dados da funcionalidade restricao-eletrica-especial         ;lib_restricao-eletrica-especial.csv                                             \n"

MockRegistroIndiceCampoVazio = (
    "RESTRICAO-ELETRICA-ESPECIAL; ; restricao-eletrica.csv\n"
)

# Conteúdo de um indices.csv real de um caso do NEWAVE, com quebras de
# linha CRLF e um card comentado
MockIndicesNewave = [
    "RESTRICAO-ELETRICA-ESPECIAL; ; restricao-eletrica.csv\r\n",
    "HIDRELETRICA-CADASTRO-RESERVATORIO-CURVAJUSANTE ; ; polinjus.csv\r\n",
    "HIDRELETRICA-CADASTRO-RESERVATORIO ; ; volumes-referencia.csv\r\n",
    "&HIDRELETRICA-FPHA-METODO-REDUCAO-CORTES; ; tratamento-fpha.csv\r\n",
]
