Tutorial
============

O *inewave* provê uma interface semelhante para todos os arquivos do modelo NEWAVE e para os
programas auxiliares NWLISTCF e NWLISTOP. Para os arquivos de entrada, são implementadas as capacidades
de leitura e escrita, permitindo uma geração automática de arquivos. Para os arquivos de saída, é implementada
somente a capacidade de leitura, de modo a permitir análise facilitada de resultados.

A leitura dos arquivos é sempre implementada a partir do método `read` da respectiva classe, enquanto que a escrita
dos arquivos é implementada pelo método `write` da instância em questão, quando for suportada.

Um exemplo é o processamento do arquivo de vazões históricas :ref:`vazoes.dat <vazoes>`. Sendo um arquivo de entrada,
é permitido realizar a leitura e a escrita deste arquivo, modificando alguma informação de entrada caso
seja desejado pelo usuário. Por exemplo, pode-se fazer uma sensibilidade de elevar em 10% todos os valores
de vazões históricas, afetando o ajuste do modelo PAR(p):


.. code-block:: python

    from inewave.newave import Vazoes
    arq_vazoes = Vazoes.read("./vazoes.dat")
    arq_vazoes.vazoes

          1    2    3    4    5     6     7     8    ...  313   314  315  316  317  318  319  320
    0     178  178    0    0    0  1476  1690  1737  ...  311   890  176  176    0   62   58   28
    1     371  371    0    0    0  2964  3318  3385  ...  464  2025  195  190   10   82   76   35
    2     326  326    0    0    0  2167  2471  2532  ...  538  1529  183  183    3   89   80   50
    3     479  479    0    0    0  1585  1827  1879  ...  383   910  185  185    4   43   39   20
    4     332  332    0    0    0  1254  1428  1463  ...  291   517  173  173    0   33   30   17
    ...   ...  ...  ...  ...  ...   ...   ...   ...  ...  ...   ...  ...  ...  ...  ...  ...  ...
    1075    0    0    0    0    0     0     0     0  ...    0     0    0    0    0    0    0    0
    1076    0    0    0    0    0     0     0     0  ...    0     0    0    0    0    0    0    0
    1077    0    0    0    0    0     0     0     0  ...    0     0    0    0    0    0    0    0
    1078    0    0    0    0    0     0     0     0  ...    0     0    0    0    0    0    0    0
    1079    0    0    0    0    0     0     0     0  ...    0     0    0    0    0    0    0    0

    [1080 rows x 320 columns]

    arq_vazoes.vazoes *= 1.1
    arq_vazoes.vazoes

            1      2    3    4    5       6       7    ...     314    315    316   317   318   319   320
    0     195.8  195.8  0.0  0.0  0.0  1623.6  1859.0  ...   979.0  193.6  193.6   0.0  68.2  63.8  30.8
    1     408.1  408.1  0.0  0.0  0.0  3260.4  3649.8  ...  2227.5  214.5  209.0  11.0  90.2  83.6  38.5
    2     358.6  358.6  0.0  0.0  0.0  2383.7  2718.1  ...  1681.9  201.3  201.3   3.3  97.9  88.0  55.0
    3     526.9  526.9  0.0  0.0  0.0  1743.5  2009.7  ...  1001.0  203.5  203.5   4.4  47.3  42.9  22.0
    4     365.2  365.2  0.0  0.0  0.0  1379.4  1570.8  ...   568.7  190.3  190.3   0.0  36.3  33.0  18.7
    ...     ...    ...  ...  ...  ...     ...     ...  ...     ...    ...    ...   ...   ...   ...   ...
    1075    0.0    0.0  0.0  0.0  0.0     0.0     0.0  ...     0.0    0.0    0.0   0.0   0.0   0.0   0.0
    1076    0.0    0.0  0.0  0.0  0.0     0.0     0.0  ...     0.0    0.0    0.0   0.0   0.0   0.0   0.0
    1077    0.0    0.0  0.0  0.0  0.0     0.0     0.0  ...     0.0    0.0    0.0   0.0   0.0   0.0   0.0
    1078    0.0    0.0  0.0  0.0  0.0     0.0     0.0  ...     0.0    0.0    0.0   0.0   0.0   0.0   0.0
    1079    0.0    0.0  0.0  0.0  0.0     0.0     0.0  ...     0.0    0.0    0.0   0.0   0.0   0.0   0.0

    [1080 rows x 320 columns]

    arq_vazoes.write("./vazoes.dat")


Se tratando dos arquivos de saída, não existe implementação para o método `write`, mas é possível realizar
a leitura normalmente, e acessar todas as propriedades encontradas. Para o :ref:`pmo.dat <pmo>`, por exemplo:

.. code-block:: python

    from inewave.newave import Pmo
    arq_pmo = Pmo.read("./pmo.dat")
    arq_pmo.convergencia

         iteracao  limite_inferior_zinf       zinf  ...  delta_zinf  zsup_iteracap           tempo
    0           1             138791.52  233699.67  ...         NaN            NaN 0 days 00:01:26
    1           1             136547.08  233699.67  ...         NaN            NaN             NaT
    2           1             124349.93  233699.67  ...         NaN      129974.34             NaT
    3           2             124900.33  237047.52  ...         NaN            NaN 0 days 00:01:37
    4           2             123012.91  237047.52  ...         NaN            NaN             NaT
    ..        ...                   ...        ...  ...         ...            ...             ...
    145        49             117421.66  268020.83  ...         NaN            NaN             NaT
    146        49             106305.07  268020.83  ...       0.136      115517.88             NaT
    147        50             118497.14  268378.30  ...         NaN            NaN 0 days 00:02:59
    148        50             117421.66  268378.30  ...         NaN            NaN             NaT
    149        50             106305.07  268378.30  ...       0.133      117230.85             NaT

    [150 rows x 8 columns]


Via de regra, a maioria dos arquivos modelados pelo *inewave* não necessita que nenhum argumento além do caminho para o caso
seja fornecido à função `read`. Todavia, ao se realizar o processamento de alguns dos arquivos binários, como o :ref:`forward.dat <forward>` e
o :ref:`cortes.dat <cortes>`, é necessário fornecer argumentos adicionais, visto que é necessária informação existente em outros arquivos
para que a leitura seja feita corretamente. Por exemplo, para o :ref:`energiaf.dat <energiaf>`:

.. code-block:: python

    from inewave.newave import Energiaf
    arq_energiaf = Energiaf.read(
            "./energiaf.dat",
            numero_forwards=2,
            numero_rees=1,
            numero_estagios=16,
            numero_estagios_th=12,
        )
    arq_energiaf.energias

        estagio  ree  serie         valor
    0       -11    1      1   7274.313246
    1       -11    1      2  11945.751618
    2       -10    1      1   7437.112877
    3       -10    1      2   7687.093101
    4        -9    1      1   7788.548023
    5        -9    1      2  11399.842496
    6        -8    1      1   5196.246300
    7        -8    1      2   7111.996327
    8        -7    1      1   5308.294925
    9        -7    1      2   4970.571844
    10       -6    1      1   5141.033372
    11       -6    1      2   4015.610566
    12       -5    1      1   3797.894460
    13       -5    1      2   3682.614472
    14       -4    1      1   3134.981601
    15       -4    1      2   3233.576467
    16       -3    1      1   3335.920508
    17       -3    1      2   3762.190756

    [56 rows x 4 columns]


Alguns arquivos do modelo NEWAVE podem sofrer alterações de sintaxe conforme são feitas atualizações no modelo.
Desta forma, poderia ser necessário criar mais de uma classe para dar suporte ao mesmo arquivo. Todavia, o framework
`cfinterface <https://github.com/rjmalves/cfi>`_ possui uma modelagem para dar suporte a mais de uma
versão do mesmo arquivo fazendo uso do método `set_version` de cada uma das classes.
Entretanto, até o momento o uso deste método não foi necessário para nenhum arquivo do modelo NEWAVE, visto
que as implementações feitas pelo desenvolvedor tendem a ser retrocompatíveis.
