# Suguru

Suguru is a Sudoku-like game. The player has to fill a board's cells with numbers, following the following restrictions:

* The cells of each group must be filled with the numbers 1...(group size) - one of each.
* Neighboring cells cannot contain the same number. Diagonally adjacent cells are considered neighbors.

The board dimentions is usually 7-by-7, and max group size is usually 5.

It is similar to [Nonomino](https://en.wikipedia.org/wiki/Nonomino).

# Playing with pygame

```bash
pip install suguru[pygame]
suguru
```

#  Development

* Download source
* Install development dependencies: `flit install -s --deps develop`
* Format code: `black .`
* Run tests: `pytest`
* Bump version in `src/suguru/__init__.py`
* Build package: `flit build`
* Deploy: `flit publish`
