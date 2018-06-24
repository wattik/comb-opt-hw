class Edge:
    ID = 1

    def __init__(self, name: str):
        self.name = name
        self.id = Edge.ID
        Edge.ID += 1

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return hash(self) == hash(other)

class Node:
    ID = 1

    def __init__(self, name):
        self.name = name
        self.id = Node.ID
        Node.ID += 1
        self.outbound = set()
        self.inbound = set()

    def add_successor(self, edge: Edge, successor: "Node"):
        self.outbound.add((edge, successor))

    def add_predecessor(self, edge: Edge, predecessor: "Node"):
        self.inbound.add((predecessor, edge))

    @property
    def successors(self):
        return iter(self.outbound)

    @property
    def predecessors(self):
        return iter(self.inbound)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)