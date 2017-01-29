import networkx as nx
import numpy as np


def distribuicao_teorica(grafo):
    w = np.ones(grafo.number_of_nodes())
    w = w * grafo.in_degree().values()
    w = w / (2 * grafo.number_of_edges())

    return w


def probabilidades(grafo):
    dimensao = grafo.number_of_nodes()
    matriz_p = nx.convert_matrix.to_numpy_matrix(grafo)

    diagonal = grafo.out_degree().values()
    delta = np.identity(dimensao)
    for i in range(dimensao):
        if diagonal[i] != 0:
            diagonal[i] = 1. / diagonal[i]
    delta = delta * diagonal

    return delta * matriz_p


def power_method(estado_anterior, grafo):
    matriz_p = np.matrix(probabilidades(grafo)).transpose()

    return np.matrix(estado_anterior) * matriz_p


def caminhada(estado_inicial, grafo, k):
    estado_atual = estado_inicial

    for i in range(k):
        estado_atual = power_method(estado_atual, grafo)

    return np.squeeze(np.asarray(estado_atual))#

def caminhada_d(estado_inicial, grafo, k):
    p = np.matrix(probabilidades(grafo))
    aux = p.copy()

    for i in range(k):
        aux = np.dot(aux,p)

    return estado_inicial * aux


def main():
    G = nx.DiGraph()
    G.add_nodes_from([x for x in range(1, 37)])
    arestas = [(1, 15), (1, 3), (3, 4), (3, 7), (4, 7), (4, 6),
               (6, 7), (6, 8), (7, 8), (7, 27), (8, 27), (8, 10), (10, 11),
               (10, 12), (11, 12), (11, 13), (12, 13), (12, 14), (13, 14), (13, 15),
               (14, 15), (14, 16), (15, 16), (15, 4), (16, 4), (16, 29),
               (19, 6), (19, 21), (21, 22), (21, 23), (22, 23),
               (22, 16), (23, 16), (23, 35), (26, 27), (26, 28),
               (27, 28), (27, 29), (28, 29), (28, 30), (29, 30), (29, 31), (30, 31),
               (31, 30), (31, 33), (33, 12), (33, 35), (34, 34), (35, 36)]
    G.add_edges_from(arestas)

    estado_inicial = np.array([0. for i in range(36)])
    estado_inicial[0] = 1.0

    print(distribuicao_teorica(G))

if __name__ == "__main__":
    main()