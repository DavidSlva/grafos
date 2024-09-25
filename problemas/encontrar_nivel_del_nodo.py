from Node import Node
from Graph import Graph


g = Graph()
g = Graph()
n1 = g.add_node(Node("A"))
n2 = g.add_node(Node("B"))
n3 = g.add_node(Node("C"))
n4 = g.add_node(Node("D"))
n5 = g.add_node(Node("E"))
n6 = g.add_node(Node("F"))

g.add_edge(n1, n2)
g.add_edge(n1, n3)
g.add_edge(n1, n4)
g.add_edge(n2, n5)
g.add_edge(n3, n6)
g.add_edge(n4, n6)
g.add_edge(n5, n6)
