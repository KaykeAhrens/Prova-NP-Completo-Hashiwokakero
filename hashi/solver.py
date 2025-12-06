from hashi.modelo import Tabuleiro, Ilha
from hashi.regras import (
    pode_colocar_ponte,
    ilha_completa,
    ilha_estourou_limite,
    tabuleiro_eh_solucao,
    contar_pontes_da_ilha,
    ilhas_vizinhas,
    quantidade_pontes_entre,
)


def _pontes_restantes(tabuleiro: Tabuleiro, ilha: Ilha) -> int:
    """
    Quantas pontes ainda faltam para esta ilha atingir o valor desejado.
    Pode ser negativo se já estourou (o que indica erro).
    """
    usadas = contar_pontes_da_ilha(tabuleiro, ilha)
    return ilha.qtd_ponte_necessaria - usadas


def _capacidade_maxima(ilha: Ilha, tabuleiro: Tabuleiro) -> int:
    """
    Retorna o máximo de pontes que ainda poderiam ser adicionadas a partir desta ilha,
    considerando os vizinhos e o limite de 2 pontes por par.
    """
    capacidade = 0
    for viz in ilhas_vizinhas(tabuleiro, ilha):
        atual = quantidade_pontes_entre(tabuleiro, ilha, viz)
        capacidade += max(0, 2 - atual)
    return capacidade


def _poda(tabuleiro: Tabuleiro) -> bool:
    """
    Retorna True se este estado deve ser podado (sem chance de solução),
    False se ainda pode haver solução.
    """
    for ilha in tabuleiro.ilhas:
        restante = _pontes_restantes(tabuleiro, ilha)

        # já estourei o limite, impossível
        if restante < 0 or ilha_estourou_limite(tabuleiro, ilha):
            return True

        # se já está completa, não precisa checar capacidade
        if restante == 0:
            continue

        # calcula capacidade restante para esta ilha
        capacidade = _capacidade_maxima(ilha, tabuleiro)

        # se a capacidade máxima dos vizinhos é menor que o que falta,
        # nunca irá conseguir completar essa ilha
        if capacidade < restante:
            return True

        # se preciso de pontes (>0) mas não tenho nenhuma capacidade, também é impossível
        if capacidade == 0 and restante > 0:
            return True

    return False


def _adicionar_ponte(tabuleiro: Tabuleiro, ilha_a: Ilha, ilha_b: Ilha, quantidade: int) -> None:
    """
    Adiciona 'quantidade' pontes entre ilha_a e ilha_b.
    Usa a API do próprio Tabuleiro.
    """

    # Delegamos para o método do Tabuleiro, uma vez por quantidade
    for _ in range(quantidade):
        tabuleiro.adicionar_ponte(ilha_a, ilha_b, quantidade=1)


def _remover_ponte(tabuleiro: Tabuleiro, ilha_a: Ilha, ilha_b: Ilha, quantidade: int) -> None:
    """
    Remove 'quantidade' pontes entre ilha_a e ilha_b.
    Remove da lista de pontes do tabuleiro.
    """
    a_id = ilha_a.id
    b_id = ilha_b.id

    for _ in range(quantidade):
        removida = False
        # procura um registro (a,b,1) ou (b,a,1) e remove
        for idx, (x, y, qtd) in enumerate(tabuleiro.pontes):
            if qtd != 1:
                continue
            if (x == a_id and y == b_id) or (x == b_id and y == a_id):
                tabuleiro.pontes.pop(idx)
                removida = True
                break
        if not removida:
            # não encontrou a ponte esperada; em um estado consistente isso não deveria acontecer
            break


def _todas_ilhas_completas(tabuleiro: Tabuleiro) -> bool:
    """
    Verifica se todas as ilhas já atingiram exatamente o número de pontes desejado.
    """
    for ilha in tabuleiro.ilhas:
        if not ilha_completa(tabuleiro, ilha):
            return False
    return True


def _gerar_pares_possiveis(tabuleiro: Tabuleiro):
    """
    Gera todos os pares de ilhas que podem, em princípio, receber pontes (vizinhas em linha/coluna).
    Usa apenas pares (i, j) com i.id < j.id para não repetir.
    """
    pares = []
    for ilha in tabuleiro.ilhas:
        for viz in ilhas_vizinhas(tabuleiro, ilha):
            if ilha.id < viz.id:
                pares.append((ilha, viz))
    return pares


def _backtracking(tabuleiro: Tabuleiro, pares, indice: int) -> bool:
    """
    Backtracking sobre a lista de pares de ilhas.
    Para cada par, decide quantas novas pontes (0, 1 ou 2) serão adicionadas,
    respeitando as regras e aplicando podas.
    """
    # Se todas as ilhas estão completas, verifico conectividade e termino
    if _todas_ilhas_completas(tabuleiro):
        return tabuleiro_eh_solucao(tabuleiro)

    # Se já considerei todos os pares e ainda não completei, não há solução neste ramo
    if indice >= len(pares):
        return False

    ilha_a, ilha_b = pares[indice]

    # quantas pontes já existem entre este par?
    atual = quantidade_pontes_entre(tabuleiro, ilha_a, ilha_b)
    max_adicional = max(0, 2 - atual)

    # Heurística: tentar primeiro adicionar mais pontes (2, depois 1, depois 0)
    # Isso tende a completar ilhas mais rápido e pode levar a podas mais cedo.
    for adicionar in range(max_adicional, -1, -1):
        if adicionar > 0:
            # verifica se não vai estourar o limite de 2 pontes entre o par
            atual = quantidade_pontes_entre(tabuleiro, ilha_a, ilha_b)
            if atual + adicionar > 2:
                continue

            # verifica se é permitido colocar pelo menos mais uma ponte
            # (visibilidade, não cruzar, etc.)
            if not pode_colocar_ponte(tabuleiro, ilha_a, ilha_b):
                continue

            _adicionar_ponte(tabuleiro, ilha_a, ilha_b, adicionar)

        # aplica poda: se o estado ficou claramente impossível, não continua
        if not _poda(tabuleiro):
            if _backtracking(tabuleiro, pares, indice + 1):
                return True

        # desfaz as pontes adicionadas neste passo
        if adicionar > 0:
            _remover_ponte(tabuleiro, ilha_a, ilha_b, adicionar)


    return False


def resolver(tabuleiro: Tabuleiro) -> bool:
    """
    Função pública chamada pelo restante do código.
    Prepara a lista de pares de ilhas e chama o backtracking.
    """
    pares = _gerar_pares_possiveis(tabuleiro)

    # pequena heurística: ordenar pares colocando primeiro os que envolvem
    # ilhas de maior demanda (mais pontes faltando).
    def peso_par(par):
        ilha_a, ilha_b = par
        return -(_pontes_restantes(tabuleiro, ilha_a) + _pontes_restantes(tabuleiro, ilha_b))

    pares.sort(key=peso_par)

    return _backtracking(tabuleiro, pares, 0)
