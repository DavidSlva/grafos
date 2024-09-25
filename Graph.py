from Node import Node
from typing import List
from queue import Queue
class Graph:

    def __init__(self):
        self.nodes: List[Node] = []

    def add_edge(self, start_node: Node, end_node: Node):
        start_node.add_neighbord(end_node)

    def add_node(self, node: Node):
        self.nodes.append(node)
        return node

    def __repr__(self) -> str:
        result = ""
        for node in self.nodes:
            result += f"[{str(node)}] -> {[str(n) for n in node.neighbords]} \n"
        return result

    def bfs(self, node: Node):
        visited = set()
        cola = Queue()
        cola.put(node)
        visited.add(node)
        while not cola.empty():
            actual = cola.get()
            for neighbord in actual.neighbords:
                if neighbord not in visited:
                    visited.add(neighbord)
                    cola.put(neighbord)

    def dfs(self, node: Node):
        visited = set()
        def DFS(actual: Node):
            for neighbord in actual.neighbords:
                if neighbord not in visited:
                    visited.add(neighbord)
                    DFS(neighbord)
        DFS(node)

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

print(g)

