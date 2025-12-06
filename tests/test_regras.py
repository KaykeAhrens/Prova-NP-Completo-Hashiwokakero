from hashi.modelo import Tabuleiro, Ilha
from hashi.regras import contar_pontes_da_ilha, ha_ilha_entre, ilha_completa, ilha_estourou_limite, quantidade_pontes_entre, pode_colocar_ponte


def montar_tabuleiro_simples():
    """
    Cria um tabuleiro assim (1 linha, 4 colunas):

    I . I I

    Posições:
    (0,0) ilha_esquerda
    (0,2) ilha_meio
    (0,3) ilha_direita
    """
    tab = Tabuleiro(1, 4)

    ilha_esquerda = Ilha(0, 0, 1)
    ilha_meio = Ilha(0, 2, 1)
    ilha_direita = Ilha(0, 3, 1)

    tab.adicionar_ilha(ilha_esquerda)
    tab.adicionar_ilha(ilha_meio)
    tab.adicionar_ilha(ilha_direita)

    return tab, ilha_esquerda, ilha_meio, ilha_direita


def test_ha_ilha_entre_mesma_linha():
    tab, esquerda, meio, direita = montar_tabuleiro_simples()

    # entre esquerda (0,0) e direita (0,3) existe a ilha do meio (0,2)
    assert ha_ilha_entre(tab, esquerda, direita) is True

    # entre esquerda (0,0) e meio (0,2) não existe nenhuma ilha no meio
    assert ha_ilha_entre(tab, esquerda, meio) is False


def test_quantidade_pontes_entre():
    tab, esquerda, meio, direita = montar_tabuleiro_simples()

    # inicialmente, não há pontes
    assert quantidade_pontes_entre(tab, esquerda, direita) == 0

    # adiciona 1 ponte
    tab.adicionar_ponte(esquerda, direita, quantidade=1)
    assert quantidade_pontes_entre(tab, esquerda, direita) == 1

    # adiciona mais 1 ponte
    tab.adicionar_ponte(esquerda, direita, quantidade=1)
    assert quantidade_pontes_entre(tab, esquerda, direita) == 2


def test_pode_colocar_ponte_regras_basicas():
    tab, esquerda, meio, direita = montar_tabuleiro_simples()

    # Não pode colocar ponte entre esquerda e direita, porque tem ilha no meio
    assert pode_colocar_ponte(tab, esquerda, direita) is False

    # Pode colocar ponte entre esquerda e meio (mesma linha, sem ilha no meio)
    assert pode_colocar_ponte(tab, esquerda, meio) is True

    # Colocamos 2 pontes entre esquerda e meio -> depois disso, não pode mais
    tab.adicionar_ponte(esquerda, meio, quantidade=1)
    tab.adicionar_ponte(esquerda, meio, quantidade=1)
    assert quantidade_pontes_entre(tab, esquerda, meio) == 2

    # Terceira ponte entre o mesmo par não é permitida
    assert pode_colocar_ponte(tab, esquerda, meio) is False


def test_contagem_e_limites():
    tab = Tabuleiro(1, 3)
    ilha1 = Ilha(0, 0, 2)  # precisa de 2 pontes
    ilha2 = Ilha(0, 2, 2)

    tab.adicionar_ilha(ilha1)
    tab.adicionar_ilha(ilha2)

    # inicialmente não há pontes
    assert contar_pontes_da_ilha(tab, ilha1) == 0
    assert ilha_completa(tab, ilha1) is False
    assert ilha_estourou_limite(tab, ilha1) is False

    # adiciona 1 ponte
    tab.adicionar_ponte(ilha1, ilha2, quantidade=1)
    assert contar_pontes_da_ilha(tab, ilha1) == 1
    assert ilha_completa(tab, ilha1) is False

    # adiciona outra ponte — agora completa
    tab.adicionar_ponte(ilha1, ilha2, quantidade=1)
    assert contar_pontes_da_ilha(tab, ilha1) == 2
    assert ilha_completa(tab, ilha1) is True

    # se tentássemos uma terceira ponte, estouraria o limite
    tab.pontes.append((ilha1.id, ilha2.id, 1))  # forçamos para simular erro
    assert ilha_estourou_limite(tab, ilha1) is True

def obter_adjacencias(tabuleiro: Tabuleiro):
    """Retorna um dicionário onde cada ilha tem uma lista de ilhas vizinhas
       conectadas por pelo menos 1 ponte."""
    adj = {ilha.id: [] for ilha in tabuleiro.ilhas}

    for a, b, qtd in tabuleiro.pontes:
        if qtd > 0:
            adj[a].append(b)
            adj[b].append(a)

    return adj


def dfs_iniciar(adj, inicio):
    """Executa uma DFS a partir de uma ilha e retorna todas as alcançáveis."""
    visitados = set()
    pilha = [inicio]

    while pilha:
        atual = pilha.pop()
        if atual not in visitados:
            visitados.add(atual)
            for viz in adj[atual]:
                if viz not in visitados:
                    pilha.append(viz)

    return visitados


def tabuleiro_conectado(tabuleiro: Tabuleiro) -> bool:
    """Verifica se todas as ilhas formam um único componente conectado."""
    if not tabuleiro.ilhas:
        return True  # tabuleiro vazio é tecnicamente conectado

    adj = obter_adjacencias(tabuleiro)
    inicio = tabuleiro.ilhas[0].id  # escolhe a primeira ilha
    visitados = dfs_iniciar(adj, inicio)

    return len(visitados) == len(tabuleiro.ilhas)

