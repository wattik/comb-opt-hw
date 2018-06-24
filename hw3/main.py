#!/usr/bin/env python3
import sys

from solvers.multiple_frames_solver import MultipleFramesProblem
from parser import Writer, Reader

def main():
    # Input
    input_filename, output_filename = sys.argv[1], sys.argv[2]

    input_file = open(input_filename)
    output_file = open(output_filename, "w")

    num_of_objects, num_of_frames = Reader.integer_list_line(input_file)

    frames = []
    for _ in range(num_of_frames):
        frame = Reader.integer_list_line(input_file)
        frames.append(frame)

    # Problem Solution
    problem = MultipleFramesProblem()
    solution = problem.solve(frames)

    # Output
    for assignment in solution.assignments:
        Writer.integer_list_line(output_file, assignment)

    input_file.close()
    output_file.close()

if __name__ == '__main__':
    main()
