import copy
import time
from typing import Iterable, Optional

from . import suguru

try:
    import z3
except ImportError:
    pass


Options = dict[suguru.Point, set[int]]


def solve(board: suguru.Suguru) -> Optional[suguru.Board]:
    try:
        return next(all_solutions(board))
    except StopIteration:
        return None


def all_solutions(board: suguru.Suguru) -> Iterable[suguru.Board]:
    options = {
        (x, y): _get_options(board, x, y)
        for x, y in board.cells()
        if board.at(x, y) == 0
    }
    yield from _all_solutions(board, options)


def _all_solutions(board: suguru.Suguru, options: Options) -> Iterable[suguru.Board]:
    if len(options) == 0:
        yield copy.deepcopy(board.board)
        return

    (x, y), opts = min(options.items(), key=lambda item: len(item[1]))
    assert board.at(x, y) == 0
    for opt in opts:
        board.insert(x, y, opt)
        neighbors = set(board.neighbors_at(x, y))
        new_options = {}
        for key, value in options.items():
            if key == (x, y):
                pass
            elif key in neighbors and opt in value:
                new_options[key] = value - {opt}
            else:
                new_options[key] = value
        yield from _all_solutions(board, new_options)
    board.insert(x, y, 0)


def _get_options(board: suguru.Suguru, x: int, y: int) -> set[int]:
    options = set(range(1, board.group_size_at(x, y) + 1))
    used_nearby = {board.at(nx, ny) for nx, ny in board.neighbors_at(x, y)}
    return options - used_nearby


def solve_z3(board: suguru.Suguru) -> Optional[suguru.Board]:
    # encode
    xy_to_var = {(x, y): z3.Int(f"{x}_{y}") for x, y in board.cells()}
    constraints = []
    for (x, y), var in xy_to_var.items():
        if board.at(x, y) != 0:
            constraints.append(var == board.at(x, y))
        else:
            constraints += [var >= 1, var <= board.group_size_at(x, y)]
            constraints += [
                var != xy_to_var[n] for n in board.neighbors_at(x, y) if n < (x, y)
            ]

    # solve
    solver = z3.Solver()
    solver.add(*constraints)
    res = solver.check()
    if res in (z3.unsat, z3.unknown):
        return None
    model = solver.model()

    # decode
    solution = [
        [model[xy_to_var[(x, y)]] for x in range(board.width)]
        for y in range(board.height)
    ]
    return solution


def main():
    board = [
        [3, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [2, 5, 0, 0, 0, 1],
    ]
    group = [
        [1, 1, 2, 3, 3, 4],
        [1, 2, 2, 2, 3, 4],
        [1, 2, 5, 6, 3, 7],
        [5, 5, 5, 6, 3, 7],
        [5, 8, 6, 6, 6, 7],
        [8, 8, 9, 9, 9, 10],
        [8, 8, 9, 9, 10, 10],
    ]

    print("Running...")
    start_time = time.perf_counter()
    suguru_board = suguru.Suguru(board, group, 5)
    result = solve(suguru_board)
    # result = solve_z3(suguru_board)
    elapsed_time = time.perf_counter() - start_time
    print(f"Done! success: {result != None}, time: {elapsed_time:0.3f}s")
    print(suguru_board)


if __name__ == "__main__":
    main()
