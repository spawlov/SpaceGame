import curses
import os
import time
from random import choice, randint
from typing import Any, Coroutine

from animations import animate_spaceship, blink, fire, fly_garbage

TIC_TIMEOUT = 0.1


def get_frames(path: str, repeat: int = 1) -> list[str]:
    frames = []
    for filename in os.listdir(path):
        with open(f"{path}/{filename}") as file:
            frame = file.read()
        for _ in range(repeat):
            frames.append(frame)
    return frames


def get_stars(canvas: Any, height: int, width: int, stars: list[str], quantity: int) -> list[Coroutine[Any, Any, None]]:
    return [
        blink(
            canvas,
            randint(2, height - 2),
            randint(2, width - 2),
            choice(stars),
            randint(0, 3),
        )
        for _ in range(quantity)
    ]


def get_garbage(canvas: Any, quantity: int) -> list[Coroutine[Any, Any, None]]:
    return [fly_garbage(canvas, randint(1, 150), choice(get_frames("animations/garbage"))) for _ in range(quantity)]


def begin_even_loop(canvas: Any, coroutines: list[Coroutine[Any, Any, None]]) -> None:
    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def main(canvas: Any) -> None:
    # canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)
    height, width = curses.window.getmaxyx(canvas)
    stars = ["*", "+", ".", "'", "`"]
    coroutines = get_stars(canvas, height, width, stars, 300)
    coroutines.append(fire(canvas, height // 2, width // 2))
    coroutines.append(animate_spaceship(canvas, height // 2, width // 2, get_frames("animations/rocket", 2)))
    coroutines += get_garbage(canvas, 10)

    begin_even_loop(canvas, coroutines)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(main)
