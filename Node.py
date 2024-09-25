class Node:
    def __init__(self, data):
        self.data = data
        self.neighbords = []

    def add_neighbord(self, node):
        self.neighbords.append(node)

    def __str__(self) -> str:
        return self.data
