from dataclasses import dataclass
from networkx import DiGraph, contracted_edge, weakly_connected_components, subgraph, draw_networkx, nx_agraph, relabel_nodes, tree
import matplotlib.pyplot as plt
from random import randint
from networkx.drawing.nx_pydot import graphviz_layout
from matplotlib.backend_bases import MouseButton
import math

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

    def __init__(self, G: DiGraph):
        self.hash = read_and_inc()
        self.graph = G

    def __hash__(self) -> int:
        return self.hash


pos = {}


def enumerate_disconnected_graph(G: DiGraph) -> int:
    sum = 0

    for comp in weakly_connected_components(G):
        curr_graph = subgraph(G, comp)
        rec_tree_node = Node(curr_graph)
        recursion_tree.add_node(rec_tree_node)
        sum += enumerate_graph(curr_graph, rec_tree_node)

    return sum


def enumerate_graph(G: DiGraph, parent_node: Node) -> int:
    curr_rec_tree_node = Node(G)
    recursion_tree.add_node(curr_rec_tree_node)
    recursion_tree.add_edge(parent_node, curr_rec_tree_node)

    if G.number_of_edges() == 0:
        return 0

    edges = [(u, v) for u, v in G.edges]
    edge = edges[0]

    if G.in_degree(edge[1]) <= 1:
        lhs = enumerate_graph(
            contracted_edge(G, edge, self_loops=False, copy=True),
            curr_rec_tree_node)
    else:
        new_graph = DiGraph()
        new_graph.add_nodes_from(G.nodes())
        new_graph.add_edges_from([e for e in edges if e != edge])
        new_graph.add_edges_from([(edge[0], e[1]) for e in edges
                                  if e[0] == edges[1]])
        lhs = enumerate_graph(new_graph, curr_rec_tree_node)

    new_graph = DiGraph()
    new_graph.add_nodes_from(G.nodes())
    new_graph.add_edges_from([e for e in edges if e != edge])

    rhs = 0

    for comp in weakly_connected_components(G):
        rhs += enumerate_graph(subgraph(new_graph, comp), curr_rec_tree_node)

    return lhs + rhs + 1


def show_graph(G: DiGraph):

    #pos = graphviz_layout(G, prog="t")
    draw_networkx(G, node_color="#a6cee3", font_size=10)
    plt.show()


def is_in_circle(click_x: int, click_y: int, coord_x: int, coord_y: int):
    dist = pow((coord_x - click_x), 2) + pow((coord_y - click_y), 2)
    r_squared = node_size / 4
    return r_squared >= dist


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

    pos = graphviz_layout(recursion_tree, prog="dot")
    draw_networkx(recursion_tree,
                  pos=pos,
                  labels=rec_labels,
                  node_color="#a6cee3",
                  font_size=10,
                  node_size=node_size)

    pos_inv = dict(zip(pos.values(), pos.keys()))
    print(pos_inv)

    def on_click(event):
        if event.button is MouseButton.LEFT:
            print(event.xdata)
            print(event.ydata)
            for n in recursion_tree.nodes:
                position = pos[n]
                if is_in_circle(event.xdata, event.ydata, position[0],
                                position[1]):
                    print(n)
                    plt.figure().clear()
                    show_graph(n.graph)

    binding_id = plt.connect('button_press_event', on_click)

    plt.show()
