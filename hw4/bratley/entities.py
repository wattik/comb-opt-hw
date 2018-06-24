from typing import Dict, NewType, Set

class Task:
    def __init__(self, i: int, release_time: int, processing_time: int, deadline: int):
        self.id = i
        self.deadline = deadline
        self.processing_time = processing_time
        self.release_time = release_time

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "T%d" % self.id

StartTime = NewType("StartTime", int)

class TaskAssignment:
    def __init__(self, task_assignment: Dict[int, StartTime]):
        self.task_assignment = task_assignment

    @classmethod
    def empty_assignment(cls) -> "TaskAssignment":
        return TaskAssignment({})

    def assign_task(self, task: Task, start_time: StartTime) -> "TaskAssignment":
        new_assignment = self.task_assignment.copy()
        new_assignment[task.id] = start_time
        return TaskAssignment(new_assignment)

    def __str__(self):
        return str(self.task_assignment)

class Node:
    def __init__(self, partial_assignment: TaskAssignment, remaining_tasks: Set[Task], time: int):
        self.time = time
        self.partial_assignment = partial_assignment
        self.remaining_tasks = remaining_tasks
        self.__is_leaf = len(self.remaining_tasks) == 0

    def is_leaf(self):
        return self.__is_leaf

    def __str__(self):
        return "c = %d \n" % self.time + \
               "partial_assignment = %s \n" % str(self.partial_assignment) + \
               "remaining_tasks = %s " % str(self.remaining_tasks)
