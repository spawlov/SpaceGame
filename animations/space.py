import asyncio
import curses
from typing import Any


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
            for _ in range(20):
                await asyncio.sleep(0)
            offset_tics += 3

        if offset_tics == 1:
            canvas.addstr(row, column, symbol)
            for _ in range(3):
                await asyncio.sleep(0)
            offset_tics += 1

        if offset_tics == 2:
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            for _ in range(5):
                await asyncio.sleep(0)
            offset_tics = 0

        if offset_tics == 3:
            canvas.addstr(row, column, symbol)
            for _ in range(3):
                await asyncio.sleep(0)
            offset_tics -= 2
