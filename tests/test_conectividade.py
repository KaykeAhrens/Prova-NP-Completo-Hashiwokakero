from hashi.modelo import Tabuleiro, Ilha

from hashi.regras import (
    obter_adjacencias,
    dfs_iniciar,
    tabuleiro_conectado,
    tabuleiro_eh_solucao,      
)


def montar_tabuleiro_conexo():
    """
    Tabuleiro:
    I -- I -- I
    """
    tab = Tabuleiro(1, 3)

    i1 = Ilha(0, 0, 1)
    i2 = Ilha(0, 1, 1)
    i3 = Ilha(0, 2, 1)

    tab.adicionar_ilha(i1)
    tab.adicionar_ilha(i2)
    tab.adicionar_ilha(i3)

    tab.adicionar_ponte(i1, i2, 1)
    tab.adicionar_ponte(i2, i3, 1)

    return tab


def montar_tabuleiro_desconexo():
    """
    Tabuleiro:
    I   I   I

    (nenhuma ponte)
    """
    tab = Tabuleiro(1, 3)

    i1 = Ilha(0, 0, 1)
    i2 = Ilha(0, 1, 1)
    i3 = Ilha(0, 2, 1)

    tab.adicionar_ilha(i1)
    tab.adicionar_ilha(i2)
    tab.adicionar_ilha(i3)

    return tab


def test_adj_e_dfs():
    tab = montar_tabuleiro_conexo()

    adj = obter_adjacencias(tab)
    assert adj[0] == [1]
    assert adj[1] == [0, 2]
    assert adj[2] == [1]

    visitados = dfs_iniciar(adj, 0)
    assert visitados == {0, 1, 2}


def test_tabuleiro_conectado():
    assert tabuleiro_conectado(montar_tabuleiro_conexo()) is True
    assert tabuleiro_conectado(montar_tabuleiro_desconexo()) is False

def test_tabuleiro_eh_solucao():
    # monta tabuleiro conexo com ilhas completas
    tab = montar_tabuleiro_conexo()

    # cada ilha precisa de 1, mas no nosso montar_tabuleiro_conexo
    # a gente criou as ilhas com qtd_ponte_necessaria = 1
    # e adicionou 1 ponte para cada extremidade (i1-i2, i2-i3).
    # porém, i2 acaba com 2 pontes, então não é solução ainda.

    assert tabuleiro_eh_solucao(tab) is False  # ilha do meio está com 2 pontes, mas só precisava de 1

    # vamos ajustar para uma situação que seja solução:
    # recria um tabuleiro com apenas 2 ilhas, cada uma precisando de 1 ponte
    tab2 = Tabuleiro(1, 2)
    i1 = Ilha(0, 0, 1)
    i2 = Ilha(0, 1, 1)
    tab2.adicionar_ilha(i1)
    tab2.adicionar_ilha(i2)
    tab2.adicionar_ponte(i1, i2, 1)

    # agora ambas têm exatamente 1 ponte, e o tabuleiro é conexo
    assert tabuleiro_eh_solucao(tab2) is True
