from networkx import DiGraph, contracted_edge, weakly_connected_components, subgraph


def enumerate_disconnected_graph(G: DiGraph) -> int:
    sum = 0

    for comp in weakly_connected_components(G):
        print(subgraph(G, comp))

        sum += enumerate_graph(subgraph(G, comp))

    return sum


def enumerate_graph(G: DiGraph) -> int:

    if G.number_of_edges() == 0:
        return 0

    edges = [(u, v) for u, v in G.edges]
    edge = edges[0]

    lhs = enumerate_graph(contracted_edge(G, edge, self_loops=False,
                                          copy=True))

    new_graph = DiGraph()
    new_graph.add_nodes_from(G.nodes())
    new_graph.add_edges_from([e for e in edges if e != edge])

    rhs = 0

    for comp in weakly_connected_components(G):
        rhs += enumerate_graph(subgraph(new_graph, comp))

    return lhs + rhs + 1
