import shutil
from io import BufferedReader
from typing import Union

from PIL import Image

LETTER_MATRIX = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def get_term_size():
    size = shutil.get_terminal_size()
    return (size.columns // 3, size.lines)


def get_pixel_matrix(file: BufferedReader, scale):
    with Image.open(file) as img:
        if scale:
            size = get_term_size() if scale is True else scale
            img.thumbnail(size=size)
        img.show()
        width = img.width
        pixels = list(img.getdata())

        pixel_matrix = [pixels[i:i+width]
                        for i in range(0, len(pixels), width)]

    return pixel_matrix


def get_intensity_matrix(pixel_matrix, map_type) -> int:
    if map_type == "average":
        intensity_matrix = [[(r + g + b) / 3 for r, g, b in row]
                            for row in pixel_matrix]
    elif map_type == "lightness":
        intensity_matrix = [
            [(max(r, g, b) + min(r, g, b)) / 2 for r, g, b in row] for row in pixel_matrix]
    else:
        intensity_matrix = [[(0.21*r + 0.72*g + 0.07*b) / 3 for r, g, b in row]
                            for row in pixel_matrix]

    return intensity_matrix


def get_char_from_intensity(intensity: int) -> str:
    scale = intensity / 255
    char = LETTER_MATRIX[round(scale * 64)] * 3

    return char


def convert_image(file: BufferedReader, map_type: str, scale: Union[bool, tuple[int, int]]) -> str:
    color_matrix = get_pixel_matrix(file, scale)
    intensity_matrix = get_intensity_matrix(color_matrix, map_type)

    output = str()
    for row in intensity_matrix:
        chars = [get_char_from_intensity(i) for i in row]
        output += ''.join(chars) + '\n'

    return output
