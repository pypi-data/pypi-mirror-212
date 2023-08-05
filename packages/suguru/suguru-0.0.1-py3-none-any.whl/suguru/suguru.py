import itertools
import random
from dataclasses import dataclass, field
from typing import Iterable

NEIGHBORS_DX_DY = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


Point = tuple[int, int]
Board = list[list[int]]


def get_points(width: int, height: int) -> Iterable[Point]:
    yield from itertools.product(range(width), range(height))


@dataclass
class Suguru:
    board: Board
    group: Board
    group_size: int
    group_members: dict[int, list[Point]] = field(init=False, repr=False)

    def __post_init__(self):
        self.group_members = {}
        for x, y in self.cells():
            group = self.group[y][x]
            self.group_members.setdefault(group, []).append((x, y))

    @classmethod
    def random(cls, width: int = 7, height: int = 7, group_size: int = 5) -> "Suguru":
        return _generate_random_suguru_board(width, height, group_size)

    @property
    def width(self) -> int:
        return len(self.board[0])

    @property
    def height(self) -> int:
        return len(self.board)

    @property
    def size(self) -> int:
        return self.width * self.height

    def cells(self) -> Iterable[Point]:
        yield from get_points(self.width, self.height)

    def at(self, x: int, y: int) -> int:
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.board[y][x]
        return 0

    def insert(self, x: int, y: int, value: int):
        self.board[y][x] = value

    def clear(self):
        for x, y in self.cells():
            self.insert(x, y, 0)

    def is_valid_at(self, x: int, y: int) -> bool:
        value = self.at(x, y)
        neighbors = [(x + dx, y + dy) for dx, dy in NEIGHBORS_DX_DY]
        group_members = set(self.group_members_at(x, y)) - {(x, y)}
        return (
            value <= self.group_size_at(x, y)
            and all(value != self.at(nx, ny) for nx, ny in neighbors)
            and all(value != self.at(gx, gy) for gx, gy in group_members)
        )

    def group_at(self, x: int, y: int) -> int:
        return self.group[y][x]

    def group_members_at(self, x: int, y: int) -> list[Point]:
        return self.group_members[self.group_at(x, y)]

    def group_size_at(self, x: int, y: int) -> int:
        return len(self.group_members_at(x, y))

    def is_same_group(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        return self.group_at(x1, y1) == self.group_at(x2, y2)

    def is_adjacent(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

    def is_neighbor(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        return self.is_same_group(x1, y1, x2, y2) or self.is_adjacent(x1, y1, x2, y2)

    def adjacent_at(self, x: int, y: int) -> Iterable[Point]:
        for dx, dy in NEIGHBORS_DX_DY:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                yield (nx, ny)

    def neighbors_at(self, x: int, y: int) -> set[Point]:
        all_neighbors = set(self.group_members_at(x, y)) | set(self.adjacent_at(x, y))
        return all_neighbors - {(x, y)}

    def __str__(self) -> str:
        width_chars = self.width * 2 + 1
        height_chars = self.height * 2 + 1
        res = [[" " for _ in range(width_chars)] for _ in range(height_chars)]
        for x in range(width_chars):
            res[0][x] = res[-1][x] = "-"
        for y in range(height_chars):
            res[y][0] = res[y][-1] = "|"
        for x in range(0, width_chars, 2):
            for y in range(0, height_chars, 2):
                res[y][x] = "+"
        for x, y in self.cells():
            if self.at(x, y) != 0:
                res[y * 2 + 1][x * 2 + 1] = str(self.at(x, y))
            if x > 0 and not self.is_same_group(x - 1, y, x, y):
                res[y * 2 + 1][x * 2] = "|"
            if y > 0 and not self.is_same_group(x, y - 1, x, y):
                res[y * 2][x * 2 + 1] = "-"
        return "\n".join(["".join(line) for line in res])


def _generate_random_suguru_board(width: int, height: int, group_size: int) -> Suguru:
    groups = _partition_into_groups(width, height, group_size)
    board = [[0 for _ in range(width)] for _ in range(height)]
    return Suguru(board, groups, group_size)


def _partition_into_groups(width: int, height: int, group_size: int) -> Board:
    groups = [[0 for _ in range(width)] for _ in range(height)]
    points = list(get_points(width, height))
    random.shuffle(points)

    group_index = 1
    for x, y in points:
        if groups[y][x] == 0:
            _create_group_at(groups, x, y, group_index, group_size)
            group_index += 1
    return groups


def _create_group_at(groups, x0, y0, group_index, group_size):
    size = 0
    options = [(x0, y0)]
    while len(options) > 0 and size < group_size:
        random.shuffle(options)
        x, y = options.pop()
        if groups[y][x] == 0:
            groups[y][x] = group_index
            size += 1
            options += list(_get_available_adjacent(groups, x, y))


def _get_available_adjacent(groups: Board, x: int, y: int) -> Iterable[Point]:
    if x > 0 and groups[y][x - 1] == 0:
        yield (x - 1, y)
    if x + 1 < len(groups[y]) and groups[y][x + 1] == 0:
        yield (x + 1, y)
    if y > 0 and groups[y - 1][x] == 0:
        yield (x, y - 1)
    if y + 1 < len(groups) and groups[y + 1][x] == 0:
        yield (x, y + 1)
