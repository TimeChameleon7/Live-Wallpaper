from ctypes import windll
from PIL import Image
import colorsys
import math
import time

user32 = windll.user32

img_location = 'image.jpg'
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)


def color_generator(size: int):
    for i in range(size):
        r, g, b = colorsys.hsv_to_rgb(i / float(size), 1, 1)
        yield int(r * 255), int(g * 255), int(b * 255)


def rectangle_generator(edges: tuple):
    x1, y1, x2, y2 = edges
    for y in range(y1, y2):
        for x in range(x1, x2):
            yield x, y


def get_corners(center: tuple, radius: int) -> tuple:
    x, y = center
    return x - radius, y - radius, x + radius, y + radius


def try_pass(target):
    try:
        return target()
    except IndexError:
        pass


def draw_circle(img: Image, radius: int, center: tuple) -> None:
    rad2 = radius ** 2
    for xy in rectangle_generator(get_corners(center, radius)):
        if rad2 > (xy[0] - center[0]) ** 2 + (xy[1] - center[1]) ** 2:
            try_pass(lambda: img.putpixel(xy, (255, 255, 255)))


def draw_square(img: Image, radius: int, center: tuple) -> None:
    for xy in rectangle_generator(get_corners(center, radius)):
        try_pass(lambda: img.putpixel(xy, (255, 255, 255)))


radius = 25
amplitude = 100
start_time = time.time()
for n in range(1000):
    i = amplitude * math.sin((n / amplitude) * math.pi / 4)
    img = Image.new('RGB', (width, height))
    draw_circle(img, radius, (int(n + radius), int(i + height / 2)))
    img.save(img_location, 'JPEG', quality=100)
    user32.SystemParametersInfoW(20, 0, img_location, 0)

elapsed_time = time.time() - start_time
print(1 / (elapsed_time / 1000))
