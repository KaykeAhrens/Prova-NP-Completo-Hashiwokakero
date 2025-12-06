from hashi.modelo import Tabuleiro, Ilha

def ha_ilha_entre(tabuleiro: Tabuleiro, ilha_a: Ilha, ilha_b: Ilha) -> bool:
    """Verifica se existe alguma outra ilha entre ilha_a e ilha_b
    na mesma linha ou coluna.
    """
    if ilha_a.linha == ilha_b.linha:
        linha = ilha_a.linha
        min_col = min(ilha_a.coluna, ilha_b.coluna)
        max_col = max(ilha_a.coluna, ilha_b.coluna)
        for ilha in tabuleiro.ilhas:
            if ilha is ilha_a or ilha is ilha_b:
                continue
            if ilha.linha == linha and min_col < ilha.coluna < max_col:
                return True
        return False

    if ilha_a.coluna == ilha_b.coluna:
        coluna = ilha_a.coluna
        min_lin = min(ilha_a.linha, ilha_b.linha)
        max_lin = max(ilha_a.linha, ilha_b.linha)
        for ilha in tabuleiro.ilhas:
            if ilha is ilha_a or ilha is ilha_b:
                continue
            if ilha.coluna == coluna and min_lin < ilha.linha < max_lin:
                return True
        return False

    # se não estão na mesma linha nem coluna, nem faz sentido checar "entre"
    return False


def quantidade_pontes_entre(tabuleiro: Tabuleiro, ilha_a: Ilha, ilha_b: Ilha) -> int:
    """Retorna quantas pontes já existem entre duas ilhas (somando 1 ou 2)."""
    id_a = ilha_a.id
    id_b = ilha_b.id
    total = 0
    for a, b, qtd in tabuleiro.pontes:
        if (a == id_a and b == id_b) or (a == id_b and b == id_a):
            total += qtd
    return total


def pode_colocar_ponte(tabuleiro: Tabuleiro, ilha_a: Ilha, ilha_b: Ilha) -> bool:
    """Verifica se é permitido colocar MAIS UMA ponte entre duas ilhas."""
    # não pode ser a mesma ilha
    if ilha_a is ilha_b:
        return False

    # tem que estar na mesma linha ou coluna
    mesma_linha = ilha_a.linha == ilha_b.linha
    mesma_coluna = ilha_a.coluna == ilha_b.coluna
    if not (mesma_linha or mesma_coluna):
        return False

    # não pode ter ilha no meio do caminho
    if ha_ilha_entre(tabuleiro, ilha_a, ilha_b):
        return False

    # no máximo 2 pontes entre o mesmo par de ilhas
    qtd_atual = quantidade_pontes_entre(tabuleiro, ilha_a, ilha_b)
    if qtd_atual >= 2:
        return False
    
    # não pode cruzar com nenhuma ponte já existente
    if ponte_cruza_outra(tabuleiro, ilha_a, ilha_b):
        return False

    return True

def contar_pontes_da_ilha(tabuleiro: Tabuleiro, ilha: Ilha) -> int:
    """Conta quantas pontes estão ligadas a uma ilha."""
    total = 0
    for a, b, qtd in tabuleiro.pontes:
        if a == ilha.id or b == ilha.id:
            total += qtd
    return total


def ilha_estourou_limite(tabuleiro: Tabuleiro, ilha: Ilha) -> bool:
    """Retorna True se a ilha já possui mais pontes do que deveria."""
    return contar_pontes_da_ilha(tabuleiro, ilha) > ilha.qtd_ponte_necessaria


def ilha_completa(tabuleiro: Tabuleiro, ilha: Ilha) -> bool:
    """Retorna True se a ilha já atingiu exatamente seu limite."""
    return contar_pontes_da_ilha(tabuleiro, ilha) == ilha.qtd_ponte_necessaria


def obter_adjacencias(tabuleiro: Tabuleiro):
    """Retorna um dicionário onde cada ilha tem uma lista de ilhas vizinhas
       conectadas por pelo menos 1 ponte.
    """
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
    inicio = tabuleiro.ilhas[0].id  # escolhe a primeira ilha como origem
    visitados = dfs_iniciar(adj, inicio)

    return len(visitados) == len(tabuleiro.ilhas)

def todas_ilhas_completas(tabuleiro: Tabuleiro) -> bool:
    """Verifica se todas as ilhas do tabuleiro já atingiram seu número de pontes."""
    for ilha in tabuleiro.ilhas:
        if not ilha_completa(tabuleiro, ilha):
            return False
    return True


def tabuleiro_eh_solucao(tabuleiro: Tabuleiro) -> bool:
    """
    Um tabuleiro é solução válida se:
    - todas as ilhas têm exatamente a quantidade de pontes necessária
    - o tabuleiro é completamente conectado
    """
    if not todas_ilhas_completas(tabuleiro):
        return False
    if not tabuleiro_conectado(tabuleiro):
        return False
    return True

def ilhas_vizinhas(tabuleiro: Tabuleiro, ilha: Ilha):
    """
    Retorna as ilhas que podem ser ligadas diretamente a 'ilha':
    - estão na mesma linha ou coluna
    - não há outra ilha no caminho
    """
    vizinhas = []

    for outra in tabuleiro.ilhas:
        if outra is ilha:
            continue

        mesma_linha = ilha.linha == outra.linha
        mesma_coluna = ilha.coluna == outra.coluna

        if not (mesma_linha or mesma_coluna):
            continue

        # não pode ter ilha "no meio"
        if ha_ilha_entre(tabuleiro, ilha, outra):
            continue

        vizinhas.append(outra)

    return vizinhas

def test_ilhas_vizinhas():
    # Tabuleiro:
    # A . B . C  (mesma linha)
    tab = Tabuleiro(1, 5)

    A = Ilha(0, 0, 1)
    B = Ilha(0, 2, 1)
    C = Ilha(0, 4, 1)

    tab.adicionar_ilha(A)
    tab.adicionar_ilha(B)
    tab.adicionar_ilha(C)

    # A consegue ver apenas B
    assert ilhas_vizinhas(tab, A) == [B]

    # B consegue ver A e C
    assert ilhas_vizinhas(tab, B) == [A, C]

    # C consegue ver apenas B
    assert ilhas_vizinhas(tab, C) == [B]


def _segmento_ponte(tabuleiro: Tabuleiro, id_a: int, id_b: int):
    """
    Retorna o segmento da ponte em coordenadas de grade (linha, coluna).
    """
    ilha_a = tabuleiro.ilhas[id_a]
    ilha_b = tabuleiro.ilhas[id_b]
    return ilha_a.linha, ilha_a.coluna, ilha_b.linha, ilha_b.coluna


def _segmentos_cruzam(tabuleiro: Tabuleiro,
                      a1: int, b1: int,
                      a2: int, b2: int) -> bool:
    """
    Verifica se a ponte (a1,b1) cruza a ponte (a2,b2) em um ponto que NÃO é ilha.
    Consideramos apenas cruzamento de um segmento horizontal com um vertical.
    """
    r1a, c1a, r1b, c1b = _segmento_ponte(tabuleiro, a1, b1)
    r2a, c2a, r2b, c2b = _segmento_ponte(tabuleiro, a2, b2)

    # Segmento 1
    horiz1 = (r1a == r1b)
    vert1 = (c1a == c1b)
    # Segmento 2
    horiz2 = (r2a == r2b)
    vert2 = (c2a == c2b)

    # Só há cruzamento se um for horizontal e o outro vertical
    if horiz1 and vert2:
        row_h = r1a
        col_v = c2a

        c_min = min(c1a, c1b)
        c_max = max(c1a, c1b)
        r_min = min(r2a, r2b)
        r_max = max(r2a, r2b)

        # ponto de interseção está estritamente entre os extremos dos dois segmentos
        if c_min < col_v < c_max and r_min < row_h < r_max:
            # se existir ilha exatamente nesse ponto, não é "cruzar", é encontrar a ilha
            for ilha in tabuleiro.ilhas:
                if ilha.linha == row_h and ilha.coluna == col_v:
                    return False
            return True

    if vert1 and horiz2:
        # simétrico ao caso anterior
        row_h = r2a
        col_v = c1a

        c_min = min(c2a, c2b)
        c_max = max(c2a, c2b)
        r_min = min(r1a, r1b)
        r_max = max(r1a, r1b)

        if c_min < col_v < c_max and r_min < row_h < r_max:
            for ilha in tabuleiro.ilhas:
                if ilha.linha == row_h and ilha.coluna == col_v:
                    return False
            return True

    # paralelos ou colineares não contam como "cruzar" (no máx. sobrepor, o que já é tratado por outras regras)
    return False


def ponte_cruza_outra(tabuleiro: Tabuleiro, ilha_a: Ilha, ilha_b: Ilha) -> bool:
    """
    Verifica se a ponte entre ilha_a e ilha_b cruzaria alguma ponte já existente no tabuleiro.
    """
    nova_a = ilha_a.id
    nova_b = ilha_b.id

    for x, y, qtd in tabuleiro.pontes:
        # ignora mesmas ilhas (mesmo par de ponte, paralela)
        if {x, y} == {nova_a, nova_b}:
            continue

        if _segmentos_cruzam(tabuleiro, nova_a, nova_b, x, y):
            return True

    return False

