#!/usr/bin/env python3

import sys
from math import inf
from typing import Mapping, Tuple, Dict, Union

from graph import FlowGraph, Node, MaxFlowSolver, FlowInfeasible
from parser import Reader, Writer

class CustomerDemand:
    def __init__(self, i, low, upper, products):
        self.i = i
        self.products = products
        self.upper = upper
        self.low = low

    def __repr__(self) -> str:
        return "Demand: l=%d, u=%d, products=%s" % (self.low, self.upper, str(self.products))

class CustomerAssignment:
    def __init__(self, i):
        self.products = []
        self.i = i

    def add(self, other):
        self.products.append(other)

class Solution:
    def __init__(self, flow, assignment_edges, num_of_customers):
        self.assignments = dict((i, CustomerAssignment(i)) for i in range(1, 1 + num_of_customers))
        for customer, product in assignment_edges:
            edge = assignment_edges[(customer, product)]
            if flow[edge] == 1:
                self.assignments[customer].add(product)

class SolutionNotFound:
    pass

class Problem:
    def solve(self, customers: Mapping[int, CustomerDemand], review_demands: Dict[int, int], num_of_products: int, num_of_customers: int) -> Union[
        SolutionNotFound, Solution]:
        graph, source, sink, assignment_edges = self._construct_graph(customers, review_demands, num_of_products)
        try:
            solver = MaxFlowSolver()
            flow = solver.solve(graph, source, sink)
        except FlowInfeasible:
            return SolutionNotFound()

        # print(flow)
        return Solution(flow, assignment_edges, num_of_customers)

    @staticmethod
    def _construct_graph(customers: Mapping[int, CustomerDemand], review_demands: Dict[int, int], num_of_products: int) -> Tuple[FlowGraph, Node, Node, dict]:
        source = Node("source")
        sink = Node("sink")
        graph = FlowGraph()

        product_nodes = {}
        for product in range(1, num_of_products + 1):
            product_node = Node("P" + str(product))
            product_nodes[product] = product_node
            graph.create_edge(product_node, sink, review_demands[product], inf)

        assignment_edges = {}
        for customer in customers.values():
            customer_node = Node("C" + str(customer.i))
            graph.create_edge(source, customer_node, customer.low, customer.upper)
            for product in customer.products:
                edge = graph.create_edge(customer_node, product_nodes[product], 0, 1)
                assignment_edges[(customer.i, product)] = edge

        return graph, source, sink, assignment_edges

def main():
    # Input
    input_filename, output_filename = sys.argv[1], sys.argv[2]

    input_file = open(input_filename)
    output_file = open(output_filename, "w")

    num_of_customers, num_of_products = Reader.integer_list_line(input_file)
    customers = {}

    for i in range(1, num_of_customers + 1):
        numbers = Reader.integer_list_line(input_file)
        customer = CustomerDemand(i, numbers[0], numbers[1], numbers[2:])
        customers[i] = customer

    review_demands = Reader.integer_list_line(input_file)
    review_demands_dict = {i + 1: demand for i, demand in enumerate(review_demands)}
    # Solver
    solver = Problem()
    solution = solver.solve(customers, review_demands_dict, num_of_products, num_of_customers)

    # Output
    if isinstance(solution, SolutionNotFound):
        Writer.integer(output_file, -1)
    else:
        for i in range(1, 1 + num_of_customers):
            customer_assignment = solution.assignments[i]
            Writer.integer_list_line(output_file, customer_assignment.products)

    input_file.close()
    output_file.close()

if __name__ == '__main__':
    main()
