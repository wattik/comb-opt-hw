from graph.base_graph import Edge, Node

class FlowEdge(Edge):
    def __init__(self, name, lower, upper):
        super().__init__(name)
        self.upper = upper
        self.lower = lower

    def __str__(self):
        return "%s >> l=%s, u=%s" % (self.name, str(self.lower), str(self.upper))

    def __repr__(self):
        return self.name

class FlowGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def create_edge(self, source: Node, target: Node, lower: int, upper: int):
        edge = FlowEdge(source.name + "->" + target.name, lower, upper)

        self.nodes.add(source)
        self.nodes.add(target)
        self.edges.add(edge)

        source.add_successor(edge, target)
        target.add_predecessor(edge, source)

        return edge

    def remove_edge(self, source: Node, edge: FlowEdge, target: Node):
        source.outbound.remove((edge, target))
        target.inbound.remove((source, edge))
        self.edges.remove(edge)

        if len(source.inbound) == 0 and len(source.outbound) == 0:
            self.nodes.remove(source)

        if len(target.inbound) == 0 and len(target.outbound) == 0:
            self.nodes.remove(target)