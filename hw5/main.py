#!/usr/bin/env python3
import sys
from itertools import product
from math import inf
from typing import Iterable, Tuple

from parser import Reader, Writer
from shp import ShortestHamiltonianPath, Matrix, SSHPPSolver

class Solution:
    def __init__(self, shp: ShortestHamiltonianPath):
        self.path = [i + 1 for i in shp.path]

class Stripe:
    def __init__(self, i: int, height: int, width: int, image: Tuple[int, ...]):
        self.i = i

        indices = tuple(product(range(height), range(3)))
        self.right_edge = [image[k] for k in (3 * i * width + 3 * (width - 1) + c for i, c in indices)]
        self.left_edge = [image[k] for k in (3 * i * width + c for i, c in indices)]


class Stripes:
    def __init__(self, cardinality: int):
        self.cardinality = cardinality
        self.stripes = [None] * cardinality

    def add(self, stripe: Stripe):
        self.stripes[stripe.i - 1] = stripe

    def __iter__(self) -> Iterable[Stripe]:
        return iter(self.stripes)

class ProblemSolver:
    def solve(self, stripes: Stripes) -> Solution:
        distances = self.create_distances(stripes)
        solver = SSHPPSolver()
        solution = solver.solve(stripes.cardinality, distances)
        return Solution(solution)

    @staticmethod
    def create_distances(stripes: Stripes) -> Matrix:
        def d(stripe_i: Stripe, stripe_j: Stripe) -> float:
            return sum(abs(x_i - x_j) for x_i, x_j in zip(stripe_i.right_edge, stripe_j.left_edge))

        matrix = Matrix()
        for stripe_i, stripe_j in product(stripes, stripes):
            if stripe_i == stripe_j:
                distance = 300 * stripes.cardinality
            else:
                distance = d(stripe_i, stripe_j)

            matrix.add(stripe_i.i, stripe_j.i, distance)

        return matrix

def main():
    input_filename, output_filename = sys.argv[1], sys.argv[2]

    input_file = open(input_filename)
    output_file = open(output_filename, "w")

    # Inputs
    cardinality, width, height = Reader.integer_list_line(input_file)
    stripes = Stripes(cardinality)

    for i in range(1, cardinality + 1):
        image = Reader.integer_list_line(input_file)
        stripes.add(Stripe(i - 1, height, width, image))

    # Solver
    solver = ProblemSolver()
    solution = solver.solve(stripes)

    # Outputs
    print("*" * 100)
    print(solution.path)
    Writer.integer_list_line(output_file, solution.path)

    input_file.close()
    output_file.close()

if __name__ == '__main__':
    main()
