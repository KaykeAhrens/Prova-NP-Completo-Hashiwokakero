from hashi.modelo import Tabuleiro, Ilha
from hashi.solver import resolver
from hashi.regras import tabuleiro_eh_solucao


def test_solver_simples_uma_ponte():
    # Tabuleiro:
    # 1 1
    tab = Tabuleiro(1, 2)

    ilha1 = Ilha(0, 0, 1)
    ilha2 = Ilha(0, 1, 1)

    tab.adicionar_ilha(ilha1)
    tab.adicionar_ilha(ilha2)

    resultado = resolver(tab)

    assert resultado is True
    assert tabuleiro_eh_solucao(tab) is True

    # deve haver exatamente 1 ponte entre as duas ilhas
    assert len(tab.pontes) == 1

def test_solver_tres_ilhas_em_linha():
    # Tabuleiro:
    # 1 2 1
    tab = Tabuleiro(1, 3)

    i1 = Ilha(0, 0, 1)
    i2 = Ilha(0, 1, 2)
    i3 = Ilha(0, 2, 1)

    tab.adicionar_ilha(i1)
    tab.adicionar_ilha(i2)
    tab.adicionar_ilha(i3)

    resultado = resolver(tab)

    assert resultado is True, "O solver deveria resolver 1-2-1"

    # verificar que é solução válida
    assert tabuleiro_eh_solucao(tab) is True

    # contar pontes finais
    num_pontes_1_2 = 0
    num_pontes_2_3 = 0

    for a, b, qtd in tab.pontes:
        if (a == i1.id and b == i2.id) or (a == i2.id and b == i1.id):
            num_pontes_1_2 += qtd
        if (a == i2.id and b == i3.id) or (a == i3.id and b == i2.id):
            num_pontes_2_3 += qtd

    assert num_pontes_1_2 == 1
    assert num_pontes_2_3 == 1
