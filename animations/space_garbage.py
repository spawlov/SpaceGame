import asyncio
from random import choice, randint
from typing import Any, Coroutine

from .curses_tools import draw_frame, get_frame_size, sleep


async def fly_garbage(canvas: Any, column: int, garbage_frame: str, speed: Any = 0.5) -> None:
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas: Any, frames: list[str], coroutines: list[Coroutine[Any, Any, None]]) -> None:
    border_width = 1
    rows, columns = canvas.getmaxyx()

    while True:
        frame = choice(frames)
        trash_height_size, trash_width_size = get_frame_size(frame)
        x_position = randint(border_width, columns - trash_width_size - border_width)
        garbage = fly_garbage(canvas, x_position, frame)
        coroutines.append(garbage)
        await sleep(randint(10, 30))
