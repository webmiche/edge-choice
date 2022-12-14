import networkx as nx
import matplotlib.pyplot as plt
from enumerate_choices import enumerate_disconnected_graph

G = nx.DiGraph(nx.nx_agraph.read_dot("ex.ll.callgraph.dot"))
nx.draw_networkx(G)
plt.show()

print(enumerate_disconnected_graph(G))
