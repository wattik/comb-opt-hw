#!/usr/bin/env python3
import sys
from typing import List

import gurobipy as g

from parser import Reader, Writer

class CallCenterSolver:
    optimum = None
    hour_schedule = None

    def __init__(self, demands: List[int]):
        self.d = demands
        self._solve()

    def _solve(self):
        model = g.Model()
        x = [model.addVar(vtype=g.GRB.INTEGER) for _ in range(24)]
        c = [model.addVar(vtype=g.GRB.INTEGER) for _ in range(24)]

        for i, c_i in enumerate(c):
            z_i = self.d[i] - sum([x[j % 24]for j in range(i-7, i + 1)])
            model.addConstr(c_i >= z_i)
            model.addConstr(c_i >= -z_i)

        model.setObjective(sum(c), sense=g.GRB.MINIMIZE)

        model.optimize()

        self.optimum = model.objVal
        self.hour_schedule = [x_i.x for x_i in x]


def main():
    input_filename, output_filename = sys.argv[1], sys.argv[2]

    input_file = open(input_filename)
    output_file = open(output_filename, "w")

    demands = Reader.integer_list_line(input_file)

    solver = CallCenterSolver(demands)

    Writer.integer(output_file, solver.optimum)
    Writer.integer_list_line(output_file, solver.hour_schedule)


if __name__ == '__main__':
    main()
