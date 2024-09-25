import queue
from typing import List, Dict

class Node:
    def __init__(self, data):
        self.data = data
        self.neighbors: List[Node] = []
    def add_neighbor(self, node):
        self.neighbors.append(node)
    def __repr__(self):
        return f'Node({self.data})'
class Graph:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
    def add_node(self, data):
        if data not in self.nodes:
            self.nodes[data] = Node(data)
        return self.nodes[data]
    def add_edge(self, node1:Node, node2:Node): 
        node1.add_neighbor(node2)
    def __repr__(self) -> str:
        result = ""
        for node in self.nodes.values():
            result += f"{str(node)} to {[str(n) for n in node.neighbors]} \n" 
        return result

    def is_directed(self) -> bool:
        nodes = self.nodes.values()
        for node in nodes:
            for neighbor in node.neighbors:
                if(node not in neighbor.neighbors):
                    return True
        return False

    
    def bfs_layers(self, start_node: Node) -> Dict[int, List[Node]]:
        visited = set()
        cola = queue.Queue()
        cola.put((start_node, 0))
        visited.add(start_node)
        layers = {}
        while not cola.empty():
            actual, layer = cola.get()
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(actual)
            for neighbor in actual.neighbors:
                if neighbor not in visited:
                    cola.put((neighbor, layer + 1))
                    visited.add(neighbor)
        return layers

    
    def bfs(self, start_node: Node) -> List[Node]:
        visited = set()
        layer = [start_node]
        cola = queue.Queue()
        cola.put(start_node)
        visited.add(actual)
        while not cola.empty():
            actual = cola.get()
            layer.append(actual)
            for neighbor in actual.neighbors:
                if neighbor not in visited:
                    cola.put(neighbor)
                    visited.add(neighbor)
        return layer

    def is_conected(self, node: Node) -> bool:
        if not self.nodes:
            return True # Un grafo vacío se considera conectado
        visited = set(self.bfs(node))
        return len(visited) == len(self.nodes)
        
    def dfs(self, start_node: Node):
        visited = set()
        def recursive(actual: Node):
            visited.add(actual)
            for neighbord in actual.neighbors:
                if neighbord not in visited:
                    recursive(neighbord)
        recursive(start_node)
        return visited
    
    def dfs_iterative(self, node: Node):
        visited = set()
        stack = [node]
        while stack:
            actual = stack.pop()
            if actual not in visited:
                visited.add(actual)
                for neighbor in actual.neighbors:
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited


g = Graph()
n1 = g.add_node("A")
n2 = g.add_node("B")
n3 = g.add_node("C")
n4 = g.add_node("D")
n5 = g.add_node("E")
n6 = g.add_node("F")

g.add_edge(n1, n2)
g.add_edge(n1, n3)
g.add_edge(n1, n4)
g.add_edge(n2, n5)
g.add_edge(n3, n6)
g.add_edge(n4, n6)
g.add_edge(n5, n6)
bfs_ton1 = g.bfs_layers(n1)
print(g)
print(bfs_ton1)
