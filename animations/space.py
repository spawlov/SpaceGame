import curses
from typing import Any

from .curses_tools import sleep


async def blink(
    canvas: Any,
    row: int,
    column: int,
    symbol: str,
    offset_tics: int,
) -> None:
    while True:
        if offset_tics == 0:
            canvas.addstr(row, column, symbol, curses.A_DIM)
            await sleep(20)
            offset_tics += 3

        if offset_tics == 1:
            canvas.addstr(row, column, symbol)
            await sleep(3)
            offset_tics += 1

        if offset_tics == 2:
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await sleep(5)
            offset_tics = 0

        if offset_tics == 3:
            canvas.addstr(row, column, symbol)
            await sleep(3)
            offset_tics -= 2
