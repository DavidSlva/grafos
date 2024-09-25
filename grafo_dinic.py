from queue import Queue
# graph es una lista de adyacencia 
# [[1, 2], [0, 3], [0, 4, 5], [1], [2, 6], [2], [4]]
def search_by_bfs(graph, source, target):
    visited = set()
    cola = Queue()
    cola.put(source)
    visited.add(source)
    while not cola.empty():
        actual = cola.get()
        for vecino, peso in graph[actual]:
            if vecino not in visited:
                cola.put(vecino)
                visited.add(vecino)
                if(vecino == target):
                    return True
    
    return False

def levels_bfs(graph, source, target):
    visited = set()
    levels = [[source]]

    queue = Queue()
    queue.put(source)
    visited.add(source)
    current_level = 0
    while not queue.empty():
        actual = queue.get()
        if actual not in levels[current_level]:
            levels[current_level].append(actual)
        for vecino, peso in graph[actual]:
            if vecino not in visited and peso > 0:
                visited.add(vecino)
                queue.put(vecino)
                if target == vecino:
                    levels.append([vecino])
                    break
        current_level +=1
        levels.append([])
    return levels

def find_levels_bfs(graph, source, sink):
    visited = set()
    levels = []
    queue = Queue()
    queue.put(source)
    visited.add(source)
    levels.append([source])

    while not queue.empty():
        next_level = []

        for _ in range(queue.qsize()):
            actual = queue.get()

            for vecino, peso in graph[actual]:
                if vecino not in visited and peso > 0:
                    visited.add(vecino)
                    queue.put(vecino)
                    next_level.append(vecino)
                    if vecino == sink:
                        levels.append(next_level)
                        return levels
        if next_level:
            levels.append(next_level)
    return levels
        


# adj = [[1, 2], [0, 3], [0, 4, 5], [1], [2, 6], [2], [4]]
adj = [
    [(1, 10), (2, 5)],      # Nodo 0 conectado a Nodo 1 (capacidad 10), Nodo 2 (capacidad 5)
    [(0, 10), (3, 15)],     # Nodo 1 conectado a Nodo 0 (capacidad 10), Nodo 3 (capacidad 15)
    [(0, 5), (4, 10), (5, 7)], # Nodo 2 conectado a Nodo 0 (capacidad 5), Nodo 4 (capacidad 10), Nodo 5 (capacidad 7)
    [(1, 15)],              # Nodo 3 conectado a Nodo 1 (capacidad 15)
    [(2, 10), (6, 20)],     # Nodo 4 conectado a Nodo 2 (capacidad 10), Nodo 6 (capacidad 20)
    [(2, 7)],               # Nodo 5 conectado a Nodo 2 (capacidad 7)
    [(4, 20)]               # Nodo 6 conectado a Nodo 4 (capacidad 20)
]
print(adj)
print(search_by_bfs(adj, 1, 4))
print(find_levels_bfs(adj, 0, 4))
