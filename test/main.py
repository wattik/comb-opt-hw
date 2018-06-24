#!/usr/bin/env python3
import sys
from itertools import product
from typing import Tuple, Dict

import gurobipy as g

from parser import Reader, Writer

machines = list(range(1, 11))
products = list(range(1, 12))

class Solution:
    pass

class SolutionFound(Solution):
    def __init__(self, cost: int, x):
        self.cost = cost
        self.X = []
        for i in machines:
            row_solutions = []
            for j in products:
                row_solutions.append(x[i, j].x)
            self.X.append(row_solutions)

class SolutionNotFound(Solution):
    pass

class ProductionProblem(object):
    def solve(self,
              F: Tuple[int, ...],
              T: Tuple[int, ...],
              p: Tuple[int, ...],
              c: Dict[Tuple[int, int], int],
              t: Dict[Tuple[int, int], int]
              ) -> Solution:
        model = g.Model()

        x = {}
        for i in machines:
            for j in products:
                x[i, j] = model.addVar(vtype=g.GRB.INTEGER, lb=0)

        y = {}
        for i in machines:
            y[i] = model.addVar(vtype=g.GRB.BINARY)

        f = {}
        for i in machines:
            f[i] = g.quicksum(x[i, j] for j in products)

        k = model.addVar(lb=0, vtype=g.GRB.INTEGER)

        # Constraint: tie y_i and sum_j(x_i_j)
        M = 10 ** 3  # could be chosen more wisely
        for i in machines:
            model.addConstr(f[i] <= M * y[i])
            model.addConstr(f[i] >= y[i])

        # Constraint (a)
        for j in products:
            model.addConstr(p[j - 1] <= g.quicksum(x[i, j] for i in machines))

        # Constraint (b)
        model.addConstr(g.quicksum(x[i, 6] for i in machines) == 5 * k)

        # Constraint (c)
        for i in machines:
            model.addConstr(T[i - 1] >= g.quicksum(t[i, j] * x[i, j] for j in products))

        # Constraint (d)
        model.addConstr(y[1] + y[3] <= 1)

        # Optimization
        model.setObjective(
            g.quicksum(
                c[i, j] * x[i, j] for i, j in product(machines, products)
            ) + g.quicksum(
                F[i - 1] * y[i] for i in machines
            ), sense=g.GRB.MINIMIZE)
        model.optimize()

        if model.status == g.GRB.INFEASIBLE:
            return SolutionNotFound()
        else:
            return SolutionFound(model.objVal, x)

def main():
    input_filename, output_filename = sys.argv[1], sys.argv[2]

    input_file = open(input_filename)
    output_file = open(output_filename, "w")

    F = Reader.integer_list_line(input_file)
    T = Reader.integer_list_line(input_file)
    p = Reader.integer_list_line(input_file)

    c = {}
    for i in machines:
        c_line = Reader.integer_list_line(input_file)
        for j in products:
            c[i, j] = c_line[j - 1]

    t = {}
    for i in machines:
        t_line = Reader.integer_list_line(input_file)
        for j in products:
            t[i, j] = t_line[j - 1]

    solver = ProductionProblem()

    solution = solver.solve(F, T, p, c, t)

    if isinstance(solution, SolutionNotFound):
        Writer.integer(output_file, -1)
    elif isinstance(solution, SolutionFound):
        Writer.integer(output_file, solution.cost)
        for i in machines:
            Writer.integer_list_line(output_file, solution.X[i - 1])

if __name__ == '__main__':
    main()
