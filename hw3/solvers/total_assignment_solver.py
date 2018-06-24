import math
from pprint import pprint
from typing import Tuple, List, Dict

from graph.max_flow_solver import Flow
from graph.min_cost_solver import MinCostFlowSolver
from graph.min_cost_graph import MinCostFlowGraph, MinCostEdge as Edge, MinCostNode as Node
from .position_config import Position, PositionConfig

def distance(a: Position, b: Position):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

class TotalAssignmentSolution:
    def __init__(self, position_edges: Dict[Position, List[Edge]], flow: Flow):
        self.permutation = [0] * len(position_edges)

        for position, edges in position_edges.items():
            for j, edge in enumerate(edges, 1):
                if flow[edge] == 1:
                    self.permutation[position.i] = j
                    continue

    def __iter__(self):
        return iter(self.permutation)

    def __str__(self):
        return str(self.permutation)

class TotalAssignmentProblem:
    def __init__(self):
        self.solver = MinCostFlowSolver()

    def solve(self, position: PositionConfig, next_position: PositionConfig) -> TotalAssignmentSolution:
        graph, position_edges = self.construct_graph(position, next_position)
        flow = self.solver.solve(graph)
        return TotalAssignmentSolution(position_edges, flow)

    @staticmethod
    def construct_graph(positions: PositionConfig, next_positions: PositionConfig) \
            -> Tuple[MinCostFlowGraph, Dict[Position, List[Edge]]]:
        position_edges = {position: [] for position in positions}

        primary_nodes = {position: Node("P%d" % i, 0) for i, position in enumerate(positions, 1)}
        secondary_nodes = {next_position: Node("S%d" % i, 0) for i, next_position in enumerate(next_positions, 1)}

        graph = MinCostFlowGraph()

        for position in positions:
            source = primary_nodes[position]
            for next_position in next_positions:
                target = secondary_nodes[next_position]
                cost = distance(position, next_position)
                edge = graph.create_edge(source, target, 0, 1, cost)
                position_edges[position].append(edge)

        main_source = Node("main-source", len(positions))
        main_target = Node("main-target", - len(positions))

        for node in primary_nodes.values():
            graph.create_edge(main_source, node, 1, 1, 0)

        for node in secondary_nodes.values():
            graph.create_edge(node, main_target, 1, 1, 0)

        return graph, position_edges
