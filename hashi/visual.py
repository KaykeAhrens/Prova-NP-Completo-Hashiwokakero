import tkinter as tk
from hashi.modelo import Tabuleiro, Ilha


TAMANHO_CELULA = 60
MARGEM = 20
RAIO_ILHA = 18


def _coordenadas_centro(linha, coluna):
    """Converte (linha, coluna) do tabuleiro lógico para coordenadas em pixels."""
    x = MARGEM + coluna * TAMANHO_CELULA
    y = MARGEM + linha * TAMANHO_CELULA
    return x, y


def desenhar_tabuleiro(canvas: tk.Canvas, tabuleiro: Tabuleiro):
    canvas.delete("all")

    # desenha uma grade leve ao fundo
    largura = tabuleiro.colunas * TAMANHO_CELULA + 2 * MARGEM
    altura = tabuleiro.linhas * TAMANHO_CELULA + 2 * MARGEM

    for i in range(tabuleiro.linhas + 1):
        y = MARGEM + i * TAMANHO_CELULA
        canvas.create_line(
            MARGEM, y, largura - MARGEM, y,
            fill="#dddddd"
        )

    for j in range(tabuleiro.colunas + 1):
        x = MARGEM + j * TAMANHO_CELULA
        canvas.create_line(
            x, MARGEM, x, altura - MARGEM,
            fill="#dddddd"
        )

    # desenhar pontes primeiro (por baixo das ilhas)
    # agregando todas as pontes entre o mesmo par de ilhas
    pontes_por_par = {}
    for a, b, qtd in tabuleiro.pontes:
        chave = tuple(sorted((a, b)))
        pontes_por_par[chave] = pontes_por_par.get(chave, 0) + qtd

    for (a, b), total in pontes_por_par.items():
        ilha_a = tabuleiro.ilhas[a]
        ilha_b = tabuleiro.ilhas[b]
        x1, y1 = _coordenadas_centro(ilha_a.linha, ilha_a.coluna)
        x2, y2 = _coordenadas_centro(ilha_b.linha, ilha_b.coluna)

        if total == 1:
            canvas.create_line(x1, y1, x2, y2, width=4, fill="#444444")
        elif total == 2:
            # duas linhas paralelas levemente deslocadas
            if x1 == x2:
                # vertical: desloca no eixo x
                canvas.create_line(x1 - 5, y1, x2 - 5, y2, width=3, fill="#444444")
                canvas.create_line(x1 + 5, y1, x2 + 5, y2, width=3, fill="#444444")
            elif y1 == y2:
                # horizontal: desloca no eixo y
                canvas.create_line(x1, y1 - 5, x2, y2 - 5, width=3, fill="#444444")
                canvas.create_line(x1, y1 + 5, x2, y2 + 5, width=3, fill="#444444")


    # desenhar ilhas por cima
    for ilha in tabuleiro.ilhas:
        x, y = _coordenadas_centro(ilha.linha, ilha.coluna)
        canvas.create_oval(
            x - RAIO_ILHA,
            y - RAIO_ILHA,
            x + RAIO_ILHA,
            y + RAIO_ILHA,
            fill="#ffffff",
            outline="#000000",
            width=2
        )
        canvas.create_text(
            x,
            y,
            text=str(ilha.qtd_ponte_necessaria),
            font=("Arial", 14, "bold")
        )

def mostrar_interface_hashi(tabuleiro: Tabuleiro, resolver_callback):
    """
    Abre uma janela Tkinter interativa com:
    - canvas mostrando o tabuleiro
    - botão 'Resolver' que chama resolver_callback(tabuleiro)
      e redesenha o canvas com a solução.
    - botão 'Reiniciar' que limpa as pontes e volta ao estado inicial.

    resolver_callback deve ser uma função que recebe o tabuleiro
    e retorna (sucesso: bool, duracao: float).
    """
    largura = tabuleiro.colunas * TAMANHO_CELULA + 2 * MARGEM
    altura = tabuleiro.linhas * TAMANHO_CELULA + 2 * MARGEM

    janela = tk.Tk()
    janela.title("Hashiwokakero")

    canvas = tk.Canvas(janela, width=largura, height=altura, bg="white")
    canvas.pack(padx=10, pady=10)

    label_status = tk.Label(janela, text="Puzzle inicial.", font=("Arial", 11))
    label_status.pack(pady=5)

    def ao_clicar_resolver():
        sucesso, duracao = resolver_callback(tabuleiro)
        desenhar_tabuleiro(canvas, tabuleiro)

        if sucesso:
            label_status.config(
                text=f"Solução encontrada! Tempo: {duracao:.4f} s"
            )
            botao_resolver.config(state="disabled")
        else:
            label_status.config(
                text="Não foi encontrada solução para este tabuleiro."
            )

    def ao_clicar_reiniciar():
        # limpa todas as pontes do tabuleiro
        tabuleiro.pontes.clear()
        desenhar_tabuleiro(canvas, tabuleiro)
        label_status.config(text="Puzzle reiniciado.")
        botao_resolver.config(state="normal")

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    botao_resolver = tk.Button(frame_botoes, text="Resolver", command=ao_clicar_resolver)
    botao_resolver.grid(row=0, column=0, padx=5)

    botao_reiniciar = tk.Button(frame_botoes, text="Reiniciar", command=ao_clicar_reiniciar)
    botao_reiniciar.grid(row=0, column=1, padx=5)

    # desenha estado inicial
    desenhar_tabuleiro(canvas, tabuleiro)

    janela.mainloop()


