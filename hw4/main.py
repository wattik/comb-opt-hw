#!/usr/bin/env python3
import sys

from bratley.bratley import Solution, Solver, ProblemDefinition
from bratley.entities import Task
from parser import Reader, Writer

def solve(task_lines) -> Solution:
    tasks = set()
    for i, task in enumerate(task_lines, 1):
        tasks.add(Task(i, task[1], task[0], task[2]))

    problem_definition = ProblemDefinition(tasks)

    solver = Solver()
    return solver.solve(problem_definition)

def main():
    input_filename, output_filename = sys.argv[1], sys.argv[2]

    input_file = open(input_filename)
    output_file = open(output_filename, "w")

    # Inputs
    n = Reader.single_integer(input_file)

    tasks = []
    for i in range(1, n + 1):
        task = Reader.integer_list_line(input_file)
        tasks.append(task)

    # Solver
    solution = solve(tasks)

    # Outputs
    if not solution.is_feasible():
        Writer.integer(output_file, -1)
    else:
        for i in range(1, n + 1):
            print(solution[i])
            Writer.integer(output_file, solution[i])

    input_file.close()
    output_file.close()

if __name__ == '__main__':
    main()
