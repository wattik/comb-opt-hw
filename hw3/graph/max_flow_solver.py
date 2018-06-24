from math import inf
from typing import Tuple, Iterable

from graph.base_graph import Edge, Node
from graph.max_flow_graph import FlowEdge, FlowGraph

class Flow:
    def __init__(self):
        self._flow = {}

    def __setitem__(self, key: Edge, value: int):
        self._flow[key] = value

    def __getitem__(self, key):
        return self._flow.setdefault(key, 0)

    def remove(self, edge):
        self._flow.pop(edge, None)

    def remove_all(self, edges: Iterable[Edge]):
        for edge in edges:
            self.remove(edge)

    def __repr__(self):
        l = []
        for k, v in self._flow.items():
            l.append("%s, f=%d" % (str(k), v))
        return "\n".join(l)

class FlowInfeasible(Exception):
    pass

class MaxFlowSolver:
    def solve(self, graph: FlowGraph, source: Node, sink: Node) -> Flow:
        flow = self._init_flow(graph, source, sink)

        delta, path = self._label(source, sink, flow)
        while delta > 0:
            for forward, edge in path:
                if forward:
                    flow[edge] += delta
                else:
                    flow[edge] -= delta

            delta, path = self._label(source, sink, flow)

        return flow

    def _init_flow(self, graph: FlowGraph, source: Node, sink: Node) -> Flow:
        """
        :raises FlowInfeasible
        """
        if all(0 == edge.lower for edge in graph.edges):
            return Flow()

        # Transform the problem
        new_source = Node("new source")
        new_sink = Node("new sink")

        source_edges = set()
        sink_edges = set()

        for node in frozenset(graph.nodes):
            b = sum(e.lower for n, e in node.inbound) - sum(e.lower for e, n in node.outbound)
            if b > 0:
                edge = graph.create_edge(new_source, node, 0, b)
                source_edges.add((edge, node))
            elif b < 0:
                edge = graph.create_edge(node, new_sink, 0, -b)
                sink_edges.add((edge, node))

        for edge in graph.edges:
            edge._previous_lower = edge.lower
            edge.lower = 0
            edge.upper -= edge._previous_lower

        backward_edge = graph.create_edge(sink, source, 0, inf)

        # Solve
        flow = self.solve(graph, new_source, new_sink)

        # Check if feasible
        if any(edge.upper != flow[edge] for edge, _ in source_edges) or any(edge.upper != flow[edge] for edge, _ in sink_edges):
            raise FlowInfeasible()

        # Transform the problem back
        graph.remove_edge(sink, backward_edge, source)
        flow.remove(backward_edge)

        for edge, node in source_edges:
            graph.remove_edge(new_source, edge, node)
            flow.remove(edge)

        for edge, node in sink_edges:
            graph.remove_edge(node, edge, new_sink)
            flow.remove(edge)

        for edge in graph.edges:
            edge.lower = edge._previous_lower
            edge.upper += edge._previous_lower
            flow[edge] += edge._previous_lower
            delattr(edge, "_previous_lower")

        return flow

    @staticmethod
    def _label(source, sink, flow) -> Tuple[int, Iterable[Tuple[bool, FlowEdge]]]:
        visited = set()

        def dfs(node):
            visited.add(node)
            if node == sink:
                return []

            for edge, successor in node.successors:
                if flow[edge] < edge.upper and successor not in visited:
                    path = dfs(successor)
                    if path is not None:
                        return [(True, edge)] + path

            for predecessor, edge in node.predecessors:
                if flow[edge] > edge.lower and predecessor not in visited:
                    path = dfs(predecessor)
                    if path is not None:
                        return [(False, edge)] + path
            # no admissible edge leading from 'node' to sink
            return None

        path = dfs(source)
        if path is not None:
            delta = min((edge.upper - flow[edge]) if forward else (flow[edge] - edge.lower) for forward, edge in path)
        else:
            delta = 0

        # print(delta)
        return delta, path
