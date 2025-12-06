from hashi.modelo import (
    Ilha,
    Tabuleiro,
    criar_tabuleiro_a_partir_de_linhas,
    carregar_tabuleiro_de_arquivo,
    gerar_grade_ascii,
    representar_tabuleiro_ascii,
)


def test_criar_ilha():
    ilha = Ilha(2, 3, 2)
    assert ilha.linha == 2
    assert ilha.coluna == 3
    assert ilha.qtd_ponte_necessaria == 2

def test_adicionar_ilhas_no_tabuleiro():
    tab = Tabuleiro(5, 5)
    i1 = Ilha(0, 0, 1)
    i2 = Ilha(0, 3, 2)

    tab.adicionar_ilha(i1)
    tab.adicionar_ilha(i2)

    assert len(tab.ilhas) == 2
    assert i1.id == 0
    assert i2.id == 1

def test_adicionar_ponte():
    tab = Tabuleiro(5, 5)
    i1 = Ilha(0, 0, 1)
    i2 = Ilha(0, 3, 2)

    tab.adicionar_ilha(i1)
    tab.adicionar_ilha(i2)

    tab.adicionar_ponte(i1, i2, quantidade=1)

    assert len(tab.pontes) == 1
    a, b, q = tab.pontes[0]
    assert a == i1.id
    assert b == i2.id
    assert q == 1

def test_criar_tabuleiro_a_partir_de_linhas():
    linhas = [
        ". . 2 .",
        ". . . .",
        "1 . . 3",
        ". . . .",
    ]

    tab = criar_tabuleiro_a_partir_de_linhas(linhas)

    # verifica dimensões
    assert tab.linhas == 4
    assert tab.colunas == 4

    # devem existir 3 ilhas: (0,2)=2 ; (2,0)=1 ; (2,3)=3
    assert len(tab.ilhas) == 3

    coordenadas = {(ilha.linha, ilha.coluna): ilha.qtd_ponte_necessaria for ilha in tab.ilhas}

    assert coordenadas[(0, 2)] == 2
    assert coordenadas[(2, 0)] == 1
    assert coordenadas[(2, 3)] == 3

def test_carregar_tabuleiro_de_arquivo(tmp_path):
    # cria um arquivo temporário com um puzzle simples
    conteudo = "\n".join([
        ". . 2 .",
        ". . . .",
        "1 . . 3",
        ". . . .",
    ])
    arquivo = tmp_path / "puzzle.txt"
    arquivo.write_text(conteudo, encoding="utf-8")

    tab = carregar_tabuleiro_de_arquivo(str(arquivo))

    assert tab.linhas == 4
    assert tab.colunas == 4
    assert len(tab.ilhas) == 3

def test_representar_tabuleiro_ascii_com_pontes():
    # Tabuleiro: 1 . 2 . 1  (1x5)
    tab = Tabuleiro(1, 5)
    i1 = Ilha(0, 0, 1)
    i2 = Ilha(0, 2, 2)
    i3 = Ilha(0, 4, 1)

    tab.adicionar_ilha(i1)
    tab.adicionar_ilha(i2)
    tab.adicionar_ilha(i3)

    tab.adicionar_ponte(i1, i2, quantidade=1)
    tab.adicionar_ponte(i2, i3, quantidade=1)

    linhas = gerar_grade_ascii(tab)

    # grade expandida, continua 1 linha
    assert len(linhas) == 1

    # queremos algo com duas ilhas "1", uma ilha "2" e alguns '-' no meio
    primeira_linha = linhas[0]
    sem_espacos = primeira_linha.replace(" ", "")

    # deve ter exatamente dois '1' e um '2'
    assert sem_espacos.count("1") == 2
    assert sem_espacos.count("2") == 1

    # deve ter pelo menos um '-' (ponte) entre eles
    assert "-" in sem_espacos
