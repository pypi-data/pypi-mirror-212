import itertools
import random
from functools import cache
from typing import Iterable, Optional

import pygame

from . import solver, suguru

SIZE = (800, 600)
FPS = 30

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


CELL_W = 60
CELL_H = 60
FONT_SIZE = 48

GROUP_COLORS = [
    pygame.color.Color(r, g, b)
    for r, g, b in itertools.product(
        range(0xC0, 0x100, 0x10),
        range(0xC0, 0x100, 0x10),
        range(0xC0, 0x100, 0x10),
    )
]
random.shuffle(GROUP_COLORS)

KEY_TO_NUMBER = {
    pygame.K_0: 0,
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
}


Point = tuple[int, int]


def get_color(group: int) -> pygame.color.Color:
    return GROUP_COLORS[group % len(GROUP_COLORS)]


def get_points(width: int, height: int) -> Iterable[Point]:
    yield from itertools.product(range(width), range(height))


@cache
def get_font(name: str, size: int) -> pygame.font.Font:
    return pygame.font.Font(name, size)


@cache
def get_text(
    text, color: pygame.Color = BLACK, background: Optional[pygame.Color] = None
) -> pygame.Surface:
    font = get_font("freesansbold.ttf", FONT_SIZE)
    return font.render(text, True, color, background)


def generate_random_board():
    for _ in itertools.count():
        board = suguru.Suguru.random()
        solution = solver.solve(board)
        if solution:
            board.clear()
            return board


class SuguruGame:
    def __init__(self):
        self.run = True
        self.should_draw = True
        self.board = generate_random_board()
        self.number = 0

    def handle(self, surface: pygame.Surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.board = generate_random_board()
                self.should_draw = True
            elif event.type == pygame.KEYDOWN:
                self.number = KEY_TO_NUMBER.get(event.key, self.number)
                self.should_draw = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x = (x - self._get_left(surface)) // CELL_W
                y = (y - self._get_top(surface)) // CELL_H
                if 0 <= x < self.board.width and 0 <= y < self.board.height:
                    self.board.insert(x, y, self.number)
                    self.should_draw = True

    def logic(self):
        pass

    def _get_left(self, surface: pygame.Surface) -> int:
        w = CELL_W * self.board.width
        return (surface.get_width() - w) // 2

    def _get_top(self, surface: pygame.Surface) -> int:
        h = CELL_H * self.board.height
        return (surface.get_height() - h) // 2

    def draw(self, surface: pygame.Surface):
        if not self.should_draw:
            return
        # self.should_draw = False

        w = CELL_W * self.board.width
        h = CELL_H * self.board.height
        left = self._get_left(surface)
        top = self._get_top(surface)

        # clear:
        surface.fill(WHITE)

        # current number:
        surface.blit(get_text(str(self.number)), (0, 0))

        # cells:
        for x, y in self.board.cells():
            group_color = get_color(self.board.group_at(x, y))
            rect = pygame.Rect(left + (x * CELL_W), top + (y * CELL_H), CELL_W, CELL_H)
            # background
            pygame.draw.rect(surface, group_color, rect)
            # text
            if self.board.at(x, y) != 0:
                text_color = BLACK if self.board.is_valid_at(x, y) else RED
                text = get_text(str(self.board.at(x, y)), text_color)
                text_rect = text.get_rect()
                text_rect.center = rect.center
                surface.blit(text, text_rect)
            # left boundary
            if x > 0:
                line_width = 1 if self.board.is_same_group(x - 1, y, x, y) else 5
                pygame.draw.line(
                    surface, BLACK, rect.topleft, rect.bottomleft, width=line_width
                )
            # top boundary
            if y > 0:
                line_width = 1 if self.board.is_same_group(x, y - 1, x, y) else 5
                pygame.draw.line(
                    surface, BLACK, rect.topleft, rect.topright, width=line_width
                )

        # external boundary:
        pygame.draw.rect(surface, BLACK, (left - 5, top - 5, w + 10, h + 10), width=5)


def main():
    game = SuguruGame()

    pygame.init()

    screen = pygame.display.set_mode(SIZE)

    clock = pygame.time.Clock()
    while game.run:
        game.handle(screen)

        game.logic()

        game.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
