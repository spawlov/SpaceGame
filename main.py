import curses
import os
import random
import time

from animations import animate_spaceship, blink, fire

TIC_TIMEOUT = 0.1


def get_frames(path: str) -> list:
    frames = []
    for filename in os.listdir(path):
        with open(f"{path}/{filename}") as file:
            frames.append(file.read())
    return frames


def get_stars(canvas, height: int, width: int, stars: list, quantity: int) -> list:
    return [
        blink(
            canvas,
            random.randint(2, height - 2),
            random.randint(2, width - 2),
            random.choice(stars),
        )
        for i in range(quantity)
    ]


def begin_even_loop(canvas, coroutines: list) -> None:
    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def main(canvas) -> None:
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)
    height, width = curses.window.getmaxyx(canvas)
    stars = ["*", "+", ".", "'", "`"]
    coroutines = get_stars(canvas, height, width, stars, 300)
    coroutines.append(fire(canvas, height // 2, width // 2))
    coroutines.append(animate_spaceship(canvas, height // 2, width // 2, get_frames("animations/rocket")))

    begin_even_loop(canvas, coroutines)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(main)
