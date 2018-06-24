from typing import Tuple, Iterable

class Position:
    ID = 100

    def __init__(self, i, position):
        self.i = i
        self.position = position
        self.id = Position.ID
        Position.ID += 1

    def __getitem__(self, item):
        return self.position[item]

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self) -> str:
        return str(self.position)

    def __repr__(self):
        return str(self)

def pairwise(iterable):
    iterator = iter(iterable)
    for item in iterator:
        yield item, next(iterator)

class PositionConfig:
    def __init__(self, positions: Tuple[Position, ...]):
        self.positions = positions

    @classmethod
    def from_frame(cls, frame: Iterable[int]):
        positions = []
        for i, (f1, f2) in enumerate(pairwise(frame)):
            position = Position(i, (f1, f2))
            positions.append(position)
        return cls(tuple(positions))

    def __iter__(self):
        return iter(self.positions)

    def __len__(self):
        return len(self.positions)

    def __str__(self):
        return str(self.positions)
