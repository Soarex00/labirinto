from collections import deque  # a bfs usa deque como fila.
import heapq  # a busca gulosa usa heapq como fila de prioridade.


# i = início, f = saída, # = parede e . = caminho livre.
# o labirinto tem 10 linhas e 10 colunas.
labirinto = [
    "I.........",
    ".########.",
    ".########.",
    ".########.",
    "..........",
    ".....##.##",
    "####.#####",
    "####.#####",
    "####.#####",
    "####.....F",
]

# cada par diz como mudar de posição: cima, direita, baixo e esquerda.
DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def achar(lab, simbolo):
    # procura o símbolo e devolve sua posição (linha, coluna).
    for numero_linha, linha in enumerate(lab):
        if simbolo in linha:
            numero_coluna = linha.index(simbolo)
            return numero_linha, numero_coluna
    raise ValueError("Símbolo não encontrado no labirinto")


def livre(lab, numero_linha, numero_coluna):
    # a posição precisa estar dentro da grade e não pode ser uma parede.
    dentro = (
        0 <= numero_linha < len(lab)
        and 0 <= numero_coluna < len(lab[0])
    )
    return dentro and lab[numero_linha][numero_coluna] != "#"


def montar_grafo(lab):
    # cada posição livre vira uma chave com uma lista de vizinhos.
    grafo = {}
    # percorre cada linha e, dentro dela, cada coluna do labirinto.
    for numero_linha, linha in enumerate(lab):
        for numero_coluna, simbolo in enumerate(linha):
            if simbolo == "#":
                continue

            casa = (numero_linha, numero_coluna)
            grafo[casa] = []

            # confere se cada uma das quatro casas ao redor está livre.
            for mudanca_linha, mudanca_coluna in DIRECOES:
                linha_vizinha = numero_linha + mudanca_linha
                coluna_vizinha = numero_coluna + mudanca_coluna

                if livre(lab, linha_vizinha, coluna_vizinha):
                    vizinha = (linha_vizinha, coluna_vizinha)
                    grafo[casa].append(vizinha)
    return grafo


def desenhar(lab, caminho):
    # usa uma cópia para não alterar o labirinto original.
    grade = [list(linha) for linha in lab]
    for numero_linha, numero_coluna in caminho:
        if grade[numero_linha][numero_coluna] == ".":
            grade[numero_linha][numero_coluna] = "*"

    for linha in grade:
        print("".join(linha))


def montar_caminho(anterior, inicio, saida):
    # se a saída não foi alcançada, não existe caminho para reconstruir.
    if saida not in anterior:
        return []

    # volta da saída até o início seguindo os registros em anterior.
    caminho = []
    casa = saida
    while casa != inicio:
        caminho.append(casa)
        casa = anterior[casa]

    caminho.append(inicio)
    caminho.reverse()  # a lista estava de trás para frente.
    return caminho


def dfs(grafo, inicio, saida):
    # a pilha faz a última casa adicionada ser explorada primeiro.
    pilha = [inicio]
    descobertos = [inicio]
    anterior = {inicio: None}
    casas_visitadas = 0

    while pilha:
        casa = pilha.pop()
        casas_visitadas += 1

        if casa == saida:
            break

        # a pilha é o contrário da fila: inverte para explorar primeiro
        # na ordem cima, direita, baixo e esquerda.
        for vizinha in reversed(grafo[casa]):
            if vizinha not in descobertos:
                descobertos.append(vizinha)
                anterior[vizinha] = casa
                pilha.append(vizinha)

    caminho = montar_caminho(anterior, inicio, saida)
    return caminho, casas_visitadas


def bfs(grafo, inicio, saida):
    # a fila atende primeiro a casa que está esperando há mais tempo.
    fila = deque([inicio])
    descobertos = [inicio]
    anterior = {inicio: None}
    casas_visitadas = 0

    while fila:
        casa = fila.popleft()
        casas_visitadas += 1

        if casa == saida:
            break

        for vizinha in grafo[casa]:
            if vizinha not in descobertos:
                descobertos.append(vizinha)
                anterior[vizinha] = casa
                fila.append(vizinha)

    caminho = montar_caminho(anterior, inicio, saida)
    return caminho, casas_visitadas


def distancia(casa, saida):
    # distância de manhattan: conta linhas e colunas, ignorando paredes.
    return abs(casa[0] - saida[0]) + abs(casa[1] - saida[1])


def gulosa(grafo, inicio, saida):
    # a fila de prioridade escolhe a casa com menor distância estimada.
    fila = [(distancia(inicio, saida), inicio)]
    descobertos = [inicio]
    anterior = {inicio: None}
    casas_visitadas = 0

    while fila:
        estimativa, casa = heapq.heappop(fila)
        casas_visitadas += 1

        if casa == saida:
            break

        for vizinha in grafo[casa]:
            if vizinha not in descobertos:
                descobertos.append(vizinha)
                anterior[vizinha] = casa
                heapq.heappush(fila, (distancia(vizinha, saida), vizinha))

    caminho = montar_caminho(anterior, inicio, saida)
    return caminho, casas_visitadas


def mostrar_resultado(nome, lab, caminho, visitadas):
    print("\n" + nome)
    desenhar(lab, caminho)
    if caminho:
        passos = len(caminho) - 1
    else:
        passos = 0
    print("Tamanho do caminho:", passos, "passos")
    print("Casas visitadas:", visitadas)


if __name__ == "__main__":
    inicio = achar(labirinto, "I")
    saida = achar(labirinto, "F")
    grafo = montar_grafo(labirinto)

    caminho_dfs, visitadas_dfs = dfs(grafo, inicio, saida)
    caminho_bfs, visitadas_bfs = bfs(grafo, inicio, saida)
    caminho_gulosa, visitadas_gulosa = gulosa(grafo, inicio, saida)

    mostrar_resultado("DFS", labirinto, caminho_dfs, visitadas_dfs)
    mostrar_resultado("BFS", labirinto, caminho_bfs, visitadas_bfs)
    mostrar_resultado("Busca gulosa", labirinto, caminho_gulosa, visitadas_gulosa)

    print("\nComparação")
    print("Algoritmo       Tamanho do caminho    Casas visitadas")
    print("DFS             ", len(caminho_dfs) - 1, "                 ", visitadas_dfs)
    print("BFS             ", len(caminho_bfs) - 1, "                 ", visitadas_bfs)
    print("Busca gulosa    ", len(caminho_gulosa) - 1, "                 ", visitadas_gulosa)