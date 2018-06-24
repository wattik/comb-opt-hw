from math import inf
from pprint import pprint
from typing import NewType, Tuple, Dict, List

from .base_graph import Node
from .max_flow_solver import Flow, MaxFlowSolver
from .min_cost_graph import MinCostFlowGraph, GraphExtension, ResidualGraph, MinCostEdge, MinCostNode

Cycle = NewType("Cycle", List[MinCostEdge])

class CycleNotFound(Exception):
    pass

class CycleCancelling:
    def find_cycle(self, graph: ResidualGraph) -> Tuple[Cycle, float]:
        dummy_source = Node("dummy-cycle-cancelling-source")

        cycle_graph = GraphExtension(graph)
        for node in frozenset(cycle_graph.nodes):
            cycle_graph.create_edge(dummy_source, node, inf, inf, 0)

        shortest_path = {node: inf for node in cycle_graph.nodes}
        shortest_path[dummy_source] = 0
        previous_node = {}

        # Bellman-Ford
        for i in range(1, len(cycle_graph.nodes)):
            for source, edge, target in cycle_graph.triplets():
                if edge.upper > 0 and shortest_path[target] > shortest_path[source] + edge.cost:
                    shortest_path[target] = shortest_path[source] + edge.cost
                    previous_node[target] = (source, edge)

        # Cost-Negative Cycle Detection
        cycle_graph.flush()
        for source, edge, target in graph.triplets():
            if edge.upper > 0 and shortest_path[target] > shortest_path[source] + edge.cost:
                return self.construct_negative_cycle(target, previous_node)

        raise CycleNotFound()

    @staticmethod
    def construct_negative_cycle(start_node: MinCostNode, previous_node: Dict[Node, Tuple[Node, MinCostEdge]]) -> Tuple[Cycle, float]:
        visited = set()
        # Let's walk the reverse path to find a node that certainly is in C
        node, _ = previous_node[start_node]
        while node not in visited:
            visited.add(node)
            node, _ = previous_node[node]

        # Now, we know node is in C. Bravo!
        cycle = Cycle([])
        start_node = node

        node, edge = previous_node[start_node]
        cycle.append(edge)

        while node != start_node:
            node, edge = previous_node[node]
            cycle.append(edge)

        return cycle, min(edge.upper for edge in cycle)

        # raise Exception("Cycle not found in construct_negative_cycle() - which is an incorrect behaviour.")

class MinCostFlowSolver:
    def solve(self, graph: MinCostFlowGraph):
        flow = self._init_flow(graph)
        residual_graph = ResidualGraph(graph, flow)
        cycle_cancelling = CycleCancelling()

        try:
            cycle, delta = cycle_cancelling.find_cycle(residual_graph)
            while delta > 0:
                for edge in cycle:
                    if edge._is_original_edge:
                        flow[edge] += delta
                    else:
                        flow[edge._counter_edge] -= delta

                    edge.upper -= delta
                    edge._counter_edge.upper += delta

                cycle, delta = cycle_cancelling.find_cycle(residual_graph)

        except CycleNotFound as e:
            pass

        residual_graph.flush()
        return flow

    @staticmethod
    def _init_flow(graph: MinCostFlowGraph) -> Flow:
        source = Node("initial_flow_source")
        target = Node("initial_flow_target")

        max_flow_graph = GraphExtension(graph)

        for node in tuple(max_flow_graph.nodes):
            if node.balance > 0:
                max_flow_graph.create_edge(source, node, 0, node.balance, inf)
            if node.balance < 0:
                max_flow_graph.create_edge(node, target, 0, -node.balance, inf)

        max_flow_solver = MaxFlowSolver()
        flow = max_flow_solver.solve(max_flow_graph, source, target)

        flow.remove_all(max_flow_graph.added_edges)

        max_flow_graph.flush()
        return flow
