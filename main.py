import time

from hashi.modelo import carregar_tabuleiro_de_arquivo, representar_tabuleiro_ascii
from hashi.solver import resolver
from hashi.regras import tabuleiro_eh_solucao
from hashi.visual import mostrar_interface_hashi


def mostrar_resumo_tabuleiro(tabuleiro):
    print("\nIlhas:")
    for ilha in tabuleiro.ilhas:
        print(f"  Ilha {ilha.id} em ({ilha.linha}, {ilha.coluna}) precisa de {ilha.qtd_ponte_necessaria}")

    print("\nPontes:")
    if not tabuleiro.pontes:
        print("  (nenhuma ponte ainda)")
    else:
        for a, b, qtd in tabuleiro.pontes:
            print(f"  {qtd} ponte(s) entre ilha {a} e ilha {b}")


def main():
    caminho = input("Digite o caminho do arquivo do puzzle (puzzles/puzzle.txt por ex): ").strip()

    tab = carregar_tabuleiro_de_arquivo(caminho)

    # caminho do arquivo de solução (ex: puzzles/puzzle4_solucao.txt)
    if "." in caminho:
        prefixo = caminho.rsplit(".", 1)[0]
    else:
        prefixo = caminho
    caminho_solucao = prefixo + "_solucao.txt"

    print("\nTabuleiro carregado (resumo):")
    mostrar_resumo_tabuleiro(tab)
    print("\nAbrindo interface gráfica. Clique em 'Resolver' para ver a solução.\n")
    
    def resolver_callback(tabuleiro):
        print("Resolvendo...")
        inicio = time.perf_counter()
        encontrou = resolver(tabuleiro)
        fim = time.perf_counter()
        duracao = fim - inicio
        print(f"Tempo de resolução: {duracao:.4f} segundos")

        if not encontrou:
            print("Não foi encontrada solução para esse tabuleiro.")
            return False, duracao

        print("Solução encontrada (resumo):")
        mostrar_resumo_tabuleiro(tabuleiro)

        if tabuleiro_eh_solucao(tabuleiro):
            print("O tabuleiro é uma solução válida de Hashiwokakero!")

            # salvar solução em arquivo
            try:
                with open(caminho_solucao, "w", encoding="utf-8") as f:
                    f.write(representar_tabuleiro_ascii(tabuleiro))
                print(f"Solução salva em: {caminho_solucao}\n")
            except Exception as e:
                print(f"Erro ao salvar a solução em arquivo: {e}")

            return True, duracao
        else:
            print("Erro: o tabuleiro não é uma solução válida.")
            return False, duracao


    # abre a janela interativa com botão 'Resolver'
    mostrar_interface_hashi(tab, resolver_callback)


if __name__ == "__main__":
    main()
