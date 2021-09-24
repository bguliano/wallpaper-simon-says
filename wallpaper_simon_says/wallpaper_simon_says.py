import ctypes
from time import sleep
import os
import mouse
from random import randint

GREEN = 'green'
BLUE = 'blue'
YELLOW = 'yellow'
RED = 'red'
BLANK = 'blank'

CHEATS = False

all_colors = [GREEN, RED, YELLOW, BLUE]
all_colors_counterclockwise = [RED, GREEN, YELLOW, BLUE]
all_colors_clockwise = reversed(all_colors_counterclockwise)

delay = 0.3

ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(), BLANK + '.jpg'), 0)


class Square:
    def __init__(self, name: str, tl: tuple, tr: tuple, bl: tuple, br: tuple):
        self.tl = tl
        self.tr = tr
        self.bl = bl
        self.br = br
        self.top_slope = (self.tl[1] - self.tr[1]) / (self.tl[0] - self.tr[0])
        self.bottom_slope = (self.br[1] - self.bl[1]) / (self.br[0] - self.bl[0])
        self.name = name

    def is_inside(self, point: tuple, log: bool = False) -> bool:
        if log:
            print(f'Point testing: {point}')
        in_x_bounds = self.tl[0] <= point[0] <= self.tr[0]
        if log:
            print(f'In x bounds of {self.name}? {in_x_bounds}')
        if in_x_bounds:
            if log:
                print(f'top slope: {self.top_slope}')
                print(f'bottom slope: {self.bottom_slope}')
            if self.top_slope:
                b = self.tl[1] - (self.top_slope * self.tl[0])
                if log:
                    print(f'y coord {point[1]} must be greater than {self.top_slope * point[0] + b}')
                return (self.top_slope * point[0] + b) <= point[1] <= self.bl[1]
            else:
                b = self.bl[1] - (self.bottom_slope * self.bl[0])
                if log:
                    print(f'y coord {point[1]} must be less than {self.bottom_slope * point[0] + b}')
                return (self.bottom_slope * point[0] + b) >= point[1] >= self.tl[1]
        else:
            return False


def draw_wallpaper(color: str, quick: bool = False):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(), color + '.jpg'), 0)
    if quick:
        sleep(0.2)
    else:
        sleep(delay)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(), BLANK + '.jpg'), 0)


TL = Square(GREEN, (1196, 413), (1339, 393), (1196, 534), (1339, 534))
TR = Square(RED, (1351, 392), (1538, 365), (1351, 534), (1538, 534))
BL = Square(YELLOW, (1195, 546), (1340, 546), (1195, 667), (1340, 688))
BR = Square(BLUE, (1351, 546), (1538, 546), (1351, 688), (1538, 715))


def wait_for_click() -> str:
    clicked = None
    while not clicked:
        mouse.wait(target_types=mouse.UP)
        coords = mouse.get_position()
        for square in [TL, TR, BL, BR]:
            if square.is_inside(coords):
                clicked = square.name
                break
    return clicked


def show_pattern(pattern: list):
    for item in pattern:
        draw_wallpaper(item)
        sleep(delay)


def celebrate():
    sleep(delay)
    for _ in range(2):
        for color in all_colors_counterclockwise:
            draw_wallpaper(color, True)
    draw_wallpaper(BLANK)
    sleep(1)


def fail(color: str):
    for _ in range(4):
        draw_wallpaper(color)
        sleep(delay)


while True:
    failed = False

    squares = [wait_for_click()]
    draw_wallpaper(squares[0])
    if CHEATS:
        print(squares)
    celebrate()

    while not failed:
        squares.append(all_colors[randint(0, 3)])
        if CHEATS:
            print(squares)
        show_pattern(squares)
        selected = ""
        for item in squares:
            selected = wait_for_click()
            draw_wallpaper(selected)
            if selected != item:
                failed = True
                break
        if not failed:
            celebrate()
        else:
            fail(selected)
    print(
        "-------------GAME OVER-------------",
        f"Your score was: {len(squares)}",
        "-----------------------------------",
        sep='\n'
    )
