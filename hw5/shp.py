from itertools import product
from numbers import Number
from typing import Dict, Tuple, List, NewType

import gurobipy as g

class Matrix:
    def __init__(self):
        self.values = {}  # type: Dict[Tuple[int, int], Number]

    def add(self, i: int, j: int, value: Number):
        self.values[(i, j)] = value

    def get(self, i: int, j: int) -> Number:
        return self.values[(i, j)]

    @classmethod
    def from_dict(cls, values: Dict[Tuple[int, int], Number]):
        matrix = cls()
        matrix.values = values
        return matrix

class ShortestHamiltonianPath:
    def __init__(self, dummy, vars_assignment, nodes):
        shortest_cycle = Cycle.find(dummy, Matrix.from_dict(vars_assignment), nodes)
        self.path = shortest_cycle[:-1]

def diff_pairs(iterable):
    first = iter(iterable)
    second = iter(iterable)
    next(second)
    for item in second:
        yield next(first), item

Edge = NewType("Edge", Tuple[int, int])

class Cycle:
    @staticmethod
    def find(start: int, incidence_matrix: Matrix, nodes) -> List[int]:
        cycle = []
        i = start
        j = None
        while j != start:
            for j in nodes:
                if incidence_matrix.get(i, j) == 1:
                    cycle.append(j)
                    i = j
                    break
        return cycle

class ConstraintCallback:
    def __init__(self, dummy, variables: Dict[Edge, g.Var], nodes: Tuple[int]):
        self.nodes = nodes
        self.vars = variables
        self.dummy = dummy
        self.num_of_nodes = len(nodes)

    def get_vars_assignment(self, model) -> Dict[Edge, int]:
        return {
            (i, j): int(round(model.cbGetSolution(self.vars[Edge((i, j))])))
            for i, j in product(self.nodes, self.nodes)
        }

    def __call__(self, model, where):
        if where != g.GRB.Callback.MIPSOL:
            return

        vars_assignment = self.get_vars_assignment(model)
        cycle = Cycle.find(self.dummy, Matrix.from_dict(vars_assignment), self.nodes)

        if len(cycle) < self.num_of_nodes:
            s = g.quicksum(self.vars[(i, j)] for i, j in product(cycle, cycle))
            model.cbLazy(s <= len(cycle) - 1)

class SSHPPSolver:
    def solve(self, num_of_nodes: int, distances: Matrix) -> ShortestHamiltonianPath:
        model = g.Model()
        model.Params.lazyConstraints = 1

        nodes = tuple(range(num_of_nodes + 1))
        node_pairs = tuple(product(nodes, nodes))
        dummy = num_of_nodes

        # constants
        d = distances.values.copy()
        d[(dummy, dummy)] = 300 * num_of_nodes
        for i in nodes[:-1]:
            d[(dummy, i)] = 0
            d[(i, dummy)] = 0

        # variables
        x = {}
        for i, j in node_pairs:
            x[(i, j)] = model.addVar(vtype=g.GRB.BINARY, name="(%d, %d)" % (i, j))

        # constraints
        for i in nodes:
            s = g.quicksum(x[(i, j)] for j in nodes)
            model.addConstr(s == 1)

            s = g.quicksum(x[(j, i)] for j in nodes)
            model.addConstr(s == 1)

        # optimization
        model.setObjective(
            g.quicksum(x[(i, j)] * d[(i, j)] for i, j in node_pairs)
        )
        callback = ConstraintCallback(dummy, x, nodes)

        def wrapper(*args):
            return callback(*args)

        # noinspection PyArgumentList
        model.optimize(wrapper)

        # solution extraction
        x_solution = self.extract_solution(x, node_pairs)
        return ShortestHamiltonianPath(dummy, x_solution, nodes)

    @staticmethod
    def extract_solution(x, node_pairs):
        return {(i, j): int(round(x[(i, j)].x)) for i, j in node_pairs}
