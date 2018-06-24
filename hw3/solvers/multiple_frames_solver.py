from typing import Iterable, Tuple

from .total_assignment_solver import TotalAssignmentSolution, TotalAssignmentProblem
from .position_config import PositionConfig

def diff_pairs(iterable):
    first = iter(iterable)
    second = iter(iterable)
    next(second)
    for item in second:
        yield next(first), item

class MultipleFramesSolution:
    def __init__(self, solutions: Iterable[TotalAssignmentSolution]):
        self.assignments = solutions

class MultipleFramesProblem:
    @staticmethod
    def solve(frames: Iterable[Tuple[int]]) -> MultipleFramesSolution:
        total_assignment_problem = TotalAssignmentProblem()

        solutions = []
        for frame, next_frame in diff_pairs(frames):
            position, next_position = PositionConfig.from_frame(frame), PositionConfig.from_frame(next_frame)
            solution = total_assignment_problem.solve(position, next_position)
            solutions += [solution]

        return MultipleFramesSolution(solutions)