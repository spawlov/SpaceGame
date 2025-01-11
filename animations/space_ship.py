import asyncio
import itertools
import statistics

from .curses_tools import draw_frame, get_frame_size, read_controls


async def animate_spaceship(canvas, start_height, start_width, frames):
    rocket_frames = itertools.cycle(frames)
    height, width = canvas.getmaxyx()
    border_width = 1

    frame = next(rocket_frames)
    frame_height, frame_width = get_frame_size(frame)
    frame_position_x = start_width - frame_width // 2
    frame_position_y = start_height - frame_height // 2
    while True:
        y_direction, x_direction, space_pressed = read_controls(canvas)

        new_frame_position_x = frame_position_x + x_direction
        new_frame_position_y = frame_position_y + y_direction

        frame_position_x = int(
            statistics.median(
                [
                    border_width,
                    new_frame_position_x,
                    width - frame_width - border_width,
                ]
            )
        )

        frame_position_y = int(
            statistics.median(
                [
                    border_width,
                    new_frame_position_y,
                    height - frame_height - border_width,
                ]
            )
        )

        draw_frame(canvas, frame_position_y, frame_position_x, frame)
        for _ in range(1):
            await asyncio.sleep(0)
        draw_frame(canvas, frame_position_y, frame_position_x, frame, negative=True)
        frame = next(rocket_frames)
