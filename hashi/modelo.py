class Ilha:
    def __init__(self, linha, coluna, qtd_ponte_necessaria):
        self.linha = linha
        self.coluna = coluna
        self.qtd_ponte_necessaria = qtd_ponte_necessaria
        self.id = None  # será atribuído ao adicionar no tabuleiro

    def __repr__(self):
        return f"Ilha({self.linha}, {self.coluna}, precisa={self.qtd_ponte_necessaria})"


class Tabuleiro:
    def __init__(self, linhas, colunas, ilhas=None):
        self.linhas = linhas
        self.colunas = colunas
        self.ilhas = ilhas if ilhas else []
        # pontes são tuplas: (id_ilha_a, id_ilha_b, quantidade)
        self.pontes = []

    def adicionar_ilha(self, ilha):
        ilha.id = len(self.ilhas)
        self.ilhas.append(ilha)

    def adicionar_ponte(self, ilha_a, ilha_b, quantidade=1):
        self.pontes.append((ilha_a.id, ilha_b.id, quantidade))


def criar_tabuleiro_a_partir_de_linhas(linhas_texto):
    """
    Recebe uma lista de strings, onde cada string representa uma linha do tabuleiro.
    Formato esperado (separado por espaços):
    ". . 2 ."
    "1 . . 3"
    etc.

    '.' significa vazio.
    Um número inteiro significa uma ilha com aquela quantidade de pontes necessárias.
    """
    qtd_linhas = len(linhas_texto)
    if qtd_linhas == 0:
        raise ValueError("Lista de linhas vazia para criar tabuleiro.")

    # assumimos que todas as linhas têm a mesma quantidade de colunas
    colunas_primeira_linha = linhas_texto[0].split()
    qtd_colunas = len(colunas_primeira_linha)

    tabuleiro = Tabuleiro(qtd_linhas, qtd_colunas)

    for i, linha_str in enumerate(linhas_texto):
        tokens = linha_str.split()
        if len(tokens) != qtd_colunas:
            raise ValueError("Todas as linhas devem ter o mesmo número de colunas.")

        for j, token in enumerate(tokens):
            if token == ".":
                continue  # célula vazia, sem ilha
            # se não for ponto, esperamos um número inteiro
            qtd_ponte = int(token)
            ilha = Ilha(i, j, qtd_ponte)
            tabuleiro.adicionar_ilha(ilha)

    return tabuleiro

def carregar_tabuleiro_de_arquivo(caminho_arquivo: str) -> Tabuleiro:
    """
    Lê um arquivo de texto e monta um Tabuleiro.
    Cada linha do arquivo representa uma linha do tabuleiro.
    Exemplo de conteúdo:

    . . 2 .
    . . . .
    1 . . 3
    . . . .

    """
    linhas = []
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha == "":
                continue  # ignora linhas vazias
            linhas.append(linha)

    return criar_tabuleiro_a_partir_de_linhas(linhas)

def gerar_grade_ascii(tabuleiro: Tabuleiro) -> list[str]:
    """
    Gera uma grade com representação textual do tabuleiro,
    incluindo ilhas (números) e pontes:
    - '-' para ponte horizontal simples
    - '=' para ponte horizontal dupla
    - '|' para ponte vertical simples
    - '║' para ponte vertical dupla

    A grade é expandida para permitir desenhar pontes entre ilhas.
    """
    linhas_grade = tabuleiro.linhas * 2 - 1
    colunas_grade = tabuleiro.colunas * 2 - 1

    # começa com tudo vazio (espaço)
    grade = [
        [' ' for _ in range(colunas_grade)]
        for _ in range(linhas_grade)
    ]

    # coloca as ilhas (número da ilha) nas posições pares
    for ilha in tabuleiro.ilhas:
        r = ilha.linha * 2
        c = ilha.coluna * 2
        grade[r][c] = str(ilha.qtd_ponte_necessaria)

    # desenha as pontes
    for a, b, qtd in tabuleiro.pontes:
        ilha_a = tabuleiro.ilhas[a]
        ilha_b = tabuleiro.ilhas[b]

        if ilha_a.linha == ilha_b.linha:
            # ponte horizontal
            r = ilha_a.linha * 2
            c1 = ilha_a.coluna * 2
            c2 = ilha_b.coluna * 2
            c_min, c_max = sorted([c1, c2])
            char = '-' if qtd == 1 else '='
            for c in range(c_min + 1, c_max):
                grade[r][c] = char

        elif ilha_a.coluna == ilha_b.coluna:
            # ponte vertical
            c = ilha_a.coluna * 2
            r1 = ilha_a.linha * 2
            r2 = ilha_b.linha * 2
            r_min, r_max = sorted([r1, r2])
            char = '|' if qtd == 1 else '║'
            for r in range(r_min + 1, r_max):
                grade[r][c] = char

    # transforma cada linha em string
    return ["".join(linha) for linha in grade]


def representar_tabuleiro_ascii(tabuleiro: Tabuleiro) -> str:
    """
    Retorna uma string pronta para printar no terminal,
    com o tabuleiro linha por linha.
    """
    linhas = gerar_grade_ascii(tabuleiro)
    return "\n".join(linhas)
