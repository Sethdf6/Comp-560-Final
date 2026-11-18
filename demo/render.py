# turns a recorded game into a short video
# needs pillow and ffmpeg
#
# python3 demo/render.py demo/game.json demo/demo.mp4 --seconds 45

import argparse
import json
import math
import subprocess

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
FPS = 30

BACKGROUND = (18, 22, 30)
PANEL_TEXT = (232, 236, 242)
MUTED = (140, 150, 165)
BOARD_COLOR = (36, 43, 56)
EMPTY_COLOR = (48, 57, 73)
ACCENT = (255, 196, 61)

# tile colors by power of two, from cool to warm
TILE_COLORS = [
    (70, 84, 105), (72, 104, 138), (56, 128, 160), (40, 150, 160),
    (46, 168, 132), (96, 180, 92), (170, 186, 66), (226, 176, 52),
    (238, 138, 52), (232, 96, 62), (214, 62, 92), (170, 60, 150),
    (110, 70, 190),
]

FONT_FILES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def load_font(size):
    for path in FONT_FILES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONTS = {size: load_font(size) for size in (20, 24, 30, 40, 52, 64)}


def tile_color(value):
    rank = int(math.log2(value)) - 1
    return TILE_COLORS[min(rank, len(TILE_COLORS) - 1)]


def centered(draw, box, text, font, fill):
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    x = (box[0] + box[2]) / 2 - (right + left) / 2
    y = (box[1] + box[3]) / 2 - (bottom + top) / 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_board(draw, grid):
    size = len(grid)
    origin, side, gap = 60, 600, 14
    cell = (side - gap * (size + 1)) / size

    draw.rounded_rectangle((origin, origin, origin + side, origin + side), 18, fill=BOARD_COLOR)

    for row in range(size):
        for col in range(size):
            x = origin + gap + col * (cell + gap)
            y = origin + gap + row * (cell + gap)
            box = (x, y, x + cell, y + cell)
            value = grid[row][col]

            if value == 0:
                draw.rounded_rectangle(box, 12, fill=EMPTY_COLOR)
                continue

            draw.rounded_rectangle(box, 12, fill=tile_color(value))
            digits = len(str(value))
            font = FONTS[64] if digits <= 2 else FONTS[52] if digits == 3 else FONTS[40]
            centered(draw, box, str(value), font, (255, 255, 255))


def draw_panel(draw, record, index, milestones, rate):
    steps = record["steps"]
    step = steps[index] if index >= 0 else None
    grid = step["board"] if step else record["start"]
    x = 720

    draw.text((x, 60), "2048 expectimax solver", font=FONTS[40], fill=PANEL_TEXT)
    draw.text((x, 112), f"search depth {record['depth']}, snake heuristic", font=FONTS[24], fill=MUTED)

    rows = [
        ("move", f"{index + 1} / {len(steps)}"),
        ("score", str(step["score"] if step else 0)),
        ("max tile", str(max(max(row) for row in grid))),
        ("last move", step["move"] if step else "-"),
    ]
    y = 180
    for label, value in rows:
        draw.text((x, y), label, font=FONTS[24], fill=MUTED)
        draw.text((x + 170, y - 8), value, font=FONTS[40], fill=PANEL_TEXT)
        y += 62

    # progress bar
    y += 6
    draw.rounded_rectangle((x, y, x + 480, y + 10), 5, fill=EMPTY_COLOR)
    done = 480 * (index + 1) / len(steps)
    if done >= 10:
        draw.rounded_rectangle((x, y, x + done, y + 10), 5, fill=ACCENT)
    if rate == 0:
        draw.text((x, y + 20), "game over", font=FONTS[24], fill=ACCENT)
    else:
        draw.text((x, y + 20), f"playback: {rate} moves per second", font=FONTS[20], fill=MUTED)

    y += 70
    for tile, move in milestones:
        if move <= index + 1:
            draw.text((x, y), f"reached {tile} at move {move}", font=FONTS[24], fill=ACCENT)
            y += 34

    draw.text((x, 668), f"seed {record['seed']}, recorded game, not live", font=FONTS[20], fill=MUTED)


def find_milestones(record):
    milestones = []
    goals = [1024, 2048, 4096, 8192]
    for number, step in enumerate(record["steps"], 1):
        top = max(max(row) for row in step["board"])
        while goals and top >= goals[0]:
            milestones.append((goals.pop(0), number))
    return milestones


def frame_plan(total_steps, seconds):
    # slow start and slow end, fast in the middle
    # returns (step index, moves per second) for every frame
    slow_rate = 5
    head = min(30, total_steps // 3)
    tail = min(25, total_steps // 3)
    middle = total_steps - head - tail

    hold = 3
    middle_seconds = max(1.0, seconds - hold - (head + tail) / slow_rate)
    fast_rate = max(slow_rate, middle / middle_seconds)

    plan = []
    position = 0.0
    while position < total_steps:
        in_middle = head <= position < total_steps - tail
        rate = fast_rate if in_middle else slow_rate
        plan.append((int(position), round(rate)))
        position += rate / FPS

    # make sure the last board is shown, then hold it
    plan.append((total_steps - 1, slow_rate))
    plan.extend([(total_steps - 1, 0)] * (hold * FPS))
    return plan


def render(record, out_path, seconds):
    steps = record["steps"]
    milestones = find_milestones(record)
    plan = frame_plan(len(steps), seconds)

    ffmpeg = subprocess.Popen(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
            "-i", "-",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart",
            out_path,
        ],
        stdin=subprocess.PIPE,
    )

    # one second of the start board before the first move
    for index, rate in [(-1, 5)] * FPS + plan:
        image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        draw = ImageDraw.Draw(image)
        grid = steps[index]["board"] if index >= 0 else record["start"]

        draw_board(draw, grid)
        draw_panel(draw, record, index, milestones, rate)

        ffmpeg.stdin.write(image.tobytes())

    ffmpeg.stdin.close()
    ffmpeg.wait()
    print("frames:", FPS + len(plan), "seconds:", round((FPS + len(plan)) / FPS, 1))
    print("saved to", out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("game")
    parser.add_argument("out")
    parser.add_argument("--seconds", type=float, default=45)
    args = parser.parse_args()

    with open(args.game) as file:
        record = json.load(file)

    render(record, args.out, args.seconds)


if __name__ == "__main__":
    main()
