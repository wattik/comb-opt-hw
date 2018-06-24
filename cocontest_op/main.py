#!/usr/bin/env python3
from itertools import product
from typing import List, Tuple

import gurobipy as g
import sys
from parser import Reader, Writer


class Solution:
    def __init__(self, cost: int, plan: Tuple[str, ...]):
        self.cost = cost
        self.plan = plan


class Cost:
    def __init__(self, c):
        self.c = c

    def __getitem__(self, item):
        if item in self.c:
            return self.c[item]
        else:
            return g.GRB.INFINITY


class AirTicketSolver:
    def solve(self, hometown: str, flights: List[Tuple[str, str, int, int]]) -> Solution:
        cities, days, cost = self.init_parameters(flights)

        model = g.Model()
        x = {}
        s = {}
        a = {}
        p = {}
        l = {}

        M = max(cost.c.values()) * (len(days) + 1)

        for i in cities:
            for j in cities:
                for d in days:
                    x[i, j, d] = model.addVar(vtype=g.GRB.BINARY)

                    if cost[i, j, d] == g.GRB.INFINITY:
                        model.addConstr(x[i, j, d] == 0)

        for i in cities:
            for j in cities:
                p[i, j] = sum(x[i, j, d] * cost[i, j, d] for d in days)
                l[i, j] = sum(x[i, j, d] for d in days)

        for i in cities:
            for d in days:
                a[i, d] = sum(x[i, j, d] for j in cities)

        for i in cities:
            s[i] = model.addVar(vtype=g.GRB.INTEGER)

        for i in cities:
            model.addConstr(
                sum(x[i, j, d] for j in cities for d in days) == 1
            )

        for j in cities:
            model.addConstr(
                sum(x[i, j, d] for i in cities for d in days) == 1
            )

        for d in days:
            model.addConstr(
                sum(x[i, j, d] for i in cities for j in cities) == 1
            )

        # initial conditions
        model.addConstr(
            g.quicksum(x[hometown, j, 0] for j in cities) == 1
        )

        model.addConstr(
            g.quicksum(x[i, hometown, len(days) - 1] for i in cities) == 1
        )

        other_cities = cities - {hometown}
        for i in cities:
            for j in other_cities:
                model.addConstr(
                    s[i] + p[i, j] <= s[j] + (1 - l[i, j]) * M
                )

        for i in cities:
            for j in cities:
                for d in days:
                    tomorrow = (d + 1) % len(days)
                    model.addConstr(
                        (1 - x[i, j, d]) + a[j, tomorrow] >= 1
                    )

        model.setObjective(
            sum(x[i, j, d] * cost[i, j, d] for d in days for i in cities for j in cities),
            sense=g.GRB.MINIMIZE
        )
        model.optimize()

        optimum = model.objVal
        plan = tuple()

        for d in days:
            for i, j in product(cities, cities):
                if x[i, j, d].x == 1:
                    plan += (i,)

        return Solution(optimum, plan)

    @staticmethod
    def init_parameters(flights):
        costs = {}
        cities = set()
        for flight in flights:
            costs[flight[0], flight[1], flight[2]] = flight[3]
            cities.add(flight[0])

        n = len(cities)
        return cities, list(range(n)), Cost(costs)

def main():
    print(sys.argv)
    input_filename, output_filename = sys.argv[1], sys.argv[2]

    input_file = open(input_filename)
    output_file = open(output_filename, "w")

    # Inputs
    hometown = Reader.string_line(input_file)

    types = (str, str, int, int)
    flights = Reader.multi_types_multi_lines(input_file, types)

    # Solver
    solver = AirTicketSolver()
    solution = solver.solve(hometown, flights)

    # Outputs
    Writer.integer(output_file, solution.cost)
    Writer.list_line(output_file, solution.plan)

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    main()
