# -*- coding: utf-8
import networkx as nx
import matplotlib.pyplot as plt
import operator
import sys


def prim_mst(grafo, r):
    # Definição dos atributos utilizados nos vértices
    nx.set_node_attributes(grafo, 'lam', float('inf'))
    nx.set_node_attributes(grafo, 'pred', None)

    grafo.node[r]['lam'] = 0

    # Criação da fila de prioridades
    fila_q = sorted(grafo.node.items(),
                    key=lambda k: operator.itemgetter('lam')(
                        operator.itemgetter(1)(k)))  # Ordena lista de acordo com o valor de lambda
    fila_q = [x[0] for x in fila_q]  # Lista possui os nomes dos vértices

    # Algoritmo de Prim
    while len(fila_q) > 0:
        u = fila_q.pop(0)

        for v in nx.all_neighbors(grafo, u):
            if v in fila_q and grafo.node[v]['lam'] > grafo.edge[u][v]['weight']:
                grafo.node[v]['lam'] = grafo.edge[u][v]['weight']
                grafo.node[v]['pred'] = u

        fila_q = sorted(grafo.node.items(),
                        key=lambda k: operator.itemgetter('lam')(
                            operator.itemgetter(1)(k)))
        fila_q = [x[0] for x in fila_q]

    # Criação do grafo da árvore
    g_out = nx.Graph()
    lista_arestas = [(grafo.node[v]['pred'], v, grafo.node[v]['lam'])
                     for v in grafo.node if grafo.node[v]['pred'] != None]
    g_out.add_weighted_edges_from(lista_arestas)

    return g_out


def main():
    print('Lendo dados...')
    g_in = nx.read_weighted_edgelist(sys.argv[1], nodetype=int)

    print('Criando MST...')
    g_out = prim_mst(g_in, 0)

    print('Desenhando árvore...')
    pos = nx.spring_layout(g_out, k=0.15, iterations=50)
    nx.draw_networkx_nodes(g_out, pos, cmap=plt.get_cmap('jet'), node_size=150)
    nx.draw_networkx_edges(g_out, pos, edgelist=g_out.edges(), arrows=True)
    nx.draw_networkx_labels(g_out, pos, font_size=5)
    labels = nx.get_edge_attributes(g_out, 'weight')
    nx.draw_networkx_edge_labels(g_out, pos, edge_labels=labels, font_size=5)
    plt.axis('off')

    plt.savefig('mst_prim.pdf')


if __name__ == "__main__":
    main()
