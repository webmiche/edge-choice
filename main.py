from dataclasses import dataclass
from networkx import DiGraph, contracted_edge, weakly_connected_components, subgraph, draw_networkx, nx_agraph, relabel_nodes, tree
import matplotlib.pyplot as plt
from random import randint
from networkx.drawing.nx_pydot import graphviz_layout
from matplotlib.backend_bases import MouseButton
import math

from matplotlib.widgets import TextBox

recursion_tree = DiGraph()

node_size = 300

count = 0


def read_and_inc():
    global count
    count += 1
    return count


@dataclass
class Node:
    graph: DiGraph
    hash: int
    is_component_node: bool

    def __init__(self, G: DiGraph, is_component: bool):
        self.hash = read_and_inc()
        self.graph = G
        self.is_component_node = is_component

    def __hash__(self) -> int:
        return self.hash


pos = {}


def enumerate_disconnected_graph(G: DiGraph) -> int:
    sum = 0

    full_graph_node = Node(G, True)

    recursion_tree.add_node(full_graph_node)

    for comp in weakly_connected_components(G):
        curr_graph = subgraph(G, comp)
        sum += enumerate_graph(curr_graph, full_graph_node)

    return sum


def enumerate_graph(G: DiGraph, parent_node: Node) -> int:
    curr_rec_tree_node = Node(G, False)
    recursion_tree.add_node(curr_rec_tree_node)
    recursion_tree.add_edge(parent_node, curr_rec_tree_node)

    # Recursion end
    if G.number_of_edges() == 0:
        return 1

    # Choose an edge
    edges = [(u, v) for u, v in G.edges]
    edge = edges[0]

    # Inline decision
    if G.in_degree(edge[1]) <= 1:
        lhs = enumerate_graph(
            contracted_edge(G, edge, self_loops=False, copy=True),
            curr_rec_tree_node)
    else:
        # If someone else calls this node, it needs to be duplicated before
        # inlining. This corresponds to a new graph with this edge removed and
        # edges from the fused not to all children of the node to be fused.
        new_graph = DiGraph()
        new_graph.add_nodes_from(G.nodes())
        new_graph.add_edges_from([e for e in edges if e != edge])
        new_graph.add_edges_from([(edge[0], e[1]) for e in edges
                                  if e[0] == edges[1]])
        lhs = enumerate_graph(new_graph, curr_rec_tree_node)

    # No Inline decision, this edge can be removed from the graph
    new_graph = DiGraph()
    new_graph.add_nodes_from(G.nodes())
    new_graph.add_edges_from([e for e in edges if e != edge])

    rhs = 0

    comps = weakly_connected_components(new_graph)
    comps = [c for c in comps]
    if len(comps) == 1:
        # If there is still one connected component, recurse into it
        rhs += enumerate_graph(subgraph(new_graph, comps[0]),
                               curr_rec_tree_node)

    else:
        # If there are multiple now (always exactly 2), created an inner node
        # and recurse
        inner_node = Node(new_graph, True)
        recursion_tree.add_node(inner_node)
        recursion_tree.add_edge(curr_rec_tree_node, inner_node)

        for comp in weakly_connected_components(new_graph):
            rhs += enumerate_graph(subgraph(new_graph, comp), inner_node)

    # This step needs all the computations from its children and one to evaluate
    # this choice
    return lhs + rhs + 1


def show_graph(G: DiGraph):

    #pos = graphviz_layout(G, prog="dot")
    draw_networkx(G, node_color="#a6cee3", font_size=10)
    plt.show()


def submit(index):
    i = int(index)
    plt.figure().clear()
    for n in recursion_tree.nodes:
        if n.hash == i:
            show_graph(n.graph)


fig, ax = plt.subplots()

if __name__ == "__main__":
    G = DiGraph(nx_agraph.read_dot("ex.ll.callgraph.dot"))

    labels = {}
    for i, n in enumerate(G.nodes):
        labels[n] = "N" + str(i)

    relabel_nodes(G, labels, copy=False)

    print(enumerate_disconnected_graph(G))

    rec_labels = {}
    for n in recursion_tree.nodes:
        rec_labels[n] = "N" + str(n.__hash__())

    node_colors = []
    for n in recursion_tree.nodes:
        node_colors.append("#b2df8a" if n.is_component_node else "#a6cee3")

    pos = graphviz_layout(recursion_tree, prog="dot")
    draw_networkx(recursion_tree,
                  ax=ax,
                  pos=pos,
                  labels=rec_labels,
                  node_color=node_colors,
                  font_size=10,
                  node_size=node_size)

    axbox = fig.add_axes([0.1, 0.05, 0.8, 0.075])
    text_box = TextBox(axbox, "Choose Node", textalignment="center")
    text_box.on_submit(submit)

    #d = ax.collections[0]

    plt.show()
