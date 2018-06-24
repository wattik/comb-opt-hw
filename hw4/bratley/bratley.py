from queue import LifoQueue as Stack
from typing import Set

from bratley.entities import Task, TaskAssignment, Node

class ProblemDefinition:
    def __init__(self, tasks: Set[Task]):
        self.tasks = tasks

class Solution:
    def __init__(self, optimalAssignment: TaskAssignment):
        self.optimalAssignment = optimalAssignment

    def is_feasible(self):
        return self.optimalAssignment is not None

    def __getitem__(self, item):
        return self.optimalAssignment.task_assignment[item]

class Solver:
    def solve(self, problem: ProblemDefinition) -> Solution:
        root_node = Node(TaskAssignment.empty_assignment(), problem.tasks, 0)

        stack = [root_node]

        best_solution = max(task.deadline for task in problem.tasks) + 1 # estimate
        optimal_solution = None

        while len(stack) > 0:
            node = stack.pop()

            if node.is_leaf():
                if node.time <= best_solution:
                    optimal_solution = node.partial_assignment
                    best_solution = node.time
            else:
                if self.exceeds_deadline(node):
                    continue

                if self.is_suboptimal(node, best_solution):
                    continue

                if self.partial_solution_optimal(node):
                    stack = []

            for task in node.remaining_tasks:
                task_start_time = max(node.time, task.release_time)
                new_assignment = node.partial_assignment.assign_task(task, task_start_time)
                new_node = Node(new_assignment, node.remaining_tasks - {task}, task_start_time + task.processing_time)
                stack.append(new_node)

        return Solution(optimal_solution)

    @staticmethod
    def computer_lower_bound(node: Node):
        min_release_time = min(task.release_time for task in node.remaining_tasks)
        sum_processing_times = sum(task.processing_time for task in node.remaining_tasks)
        return max(node.time, min_release_time) + sum_processing_times

    @staticmethod
    def exceeds_deadline(node: Node):
        return any(
            task.deadline < max(node.time, task.release_time) + task.processing_time
            for task in node.remaining_tasks
        )

    def is_suboptimal(self, node, best_solution):
        lower_bound = self.computer_lower_bound(node)
        return lower_bound >= best_solution

    @staticmethod
    def partial_solution_optimal(node):
        return node.time <= min(task.release_time for task in node.remaining_tasks)
