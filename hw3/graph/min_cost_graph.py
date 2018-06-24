from typing import Iterable, Tuple

from math import inf

from graph.max_flow_solver import Flow
from graph.max_flow_graph import FlowEdge
from graph.base_graph import Node

class MinCostNode(Node):
    def __init__(self, name, balance):
        super().__init__(name)
        self.balance = balance

    def __str__(self):
        return super().__str__() + ", b=%s" % str(self.balance)

class MinCostEdge(FlowEdge):
    def __init__(self, name, lower, upper, cost):
        super().__init__(name, lower, upper)
        self.cost = cost

    def __str__(self):
        return super().__str__() + ", c=%s" % str(self.cost)

class MinCostFlowGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def create_edge(self, source: MinCostNode, target: MinCostNode, lower: int, upper: int, cost: float) -> MinCostEdge:
        edge = MinCostEdge(source.name + "->" + target.name, lower, upper, cost)

        self.nodes.add(source)
        self.nodes.add(target)
        self.edges.add(edge)

        source.add_successor(edge, target)
        target.add_predecessor(edge, source)

        return edge

    def remove_edge(self, source: MinCostNode, edge: MinCostEdge, target: MinCostNode):
        source.outbound.remove((edge, target))
        target.inbound.remove((source, edge))
        self.edges.remove(edge)

        if len(source.inbound) == 0 and len(source.outbound) == 0:
            self.nodes.remove(source)

        if len(target.inbound) == 0 and len(target.outbound) == 0:
            self.nodes.remove(target)

    def triplets(self) -> Iterable[Tuple[MinCostNode, MinCostEdge, MinCostNode]]:
        return list((node, edge, successor) for node in self.nodes for edge, successor in node.outbound)

class GraphExtension:
    def __init__(self, graph: MinCostFlowGraph):
        self.graph = graph
        self.added_entities = set()
        self.added_edges = set()

    def create_edge(self, source: MinCostNode, target: MinCostNode, lower: int, upper: int, cost: int = inf):
        edge = self.graph.create_edge(source, target, lower, upper, cost)
        self.added_entities.add((source, edge, target))
        self.added_edges.add(edge)

        return edge

    def remove_edge(self, source: MinCostNode, edge: MinCostEdge, target: MinCostNode):
        self.graph.remove_edge(source, edge, target)
        self.added_entities.remove((source, edge, target))
        self.added_edges.remove(edge)

    @property
    def nodes(self):
        return self.graph.nodes

    @property
    def edges(self):
        return self.graph.edges

    def flush(self):
        for source, edge, target in frozenset(self.added_entities):
            self.remove_edge(source, edge, target)

    def triplets(self):
        return self.graph.triplets()

class ResidualGraph(GraphExtension):
    def __init__(self, graph: MinCostFlowGraph, flow: Flow):
        super().__init__(graph)
        self.flow = flow
        self._init()

    def flush(self):
        self.flow.remove_all(self.added_edges)
        super().flush()

        # convert edges back
        for edge in self.edges:
            edge.upper = edge._old_upper
            delattr(edge, "_old_upper")
            delattr(edge, "_counter_edge")
            delattr(edge, "_is_original_edge")

    def _init(self):
        for source, edge, target in self.graph.triplets():
            new_lower = 0
            new_upper = self.flow[edge] - edge.lower
            new_cost = - edge.cost

            counter_edge = self.create_edge(target, source, new_lower, new_upper, new_cost)
            counter_edge._is_original_edge = False
            counter_edge._counter_edge = edge

            edge._counter_edge = counter_edge
            edge._is_original_edge = True
            edge._old_upper = edge.upper
            edge.upper -= self.flow[edge]
            # edge.cost remains unchanged