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
        width = img.width
        pixels = list(img.getdata())

        pixel_matrix = [pixels[i:i+width]
                        for i in range(0, len(pixels), width)]

    return pixel_matrix


def get_intensity_matrix(pixel_matrix, map_type, inverted) -> int:
    to_subtract = 255 if inverted else 0
    if map_type == "average":
        intensity_matrix = [[abs(((rgb[0] + rgb[1] + rgb[3]) / 3) - to_subtract) for rgb in row]
                            for row in pixel_matrix]
    elif map_type == "lightness":
        intensity_matrix = [
            [abs(((max(rgb[0], rgb[1], rgb[2]) + min(rgb[0], rgb[1], rgb[2])) / 2) - to_subtract) for rgb in row] for row in pixel_matrix]
    else:
        intensity_matrix = [[abs(((0.21*rgb[0] + 0.72*rgb[1] + 0.07*rgb[2]) / 3) - to_subtract) for rgb in row]
                            for row in pixel_matrix]

    return intensity_matrix


def get_char_from_intensity(intensity: int) -> str:
    scale = intensity / 255
    char = LETTER_MATRIX[round(scale * 64)] * 3

    return char


def convert_image(file: BufferedReader, map_type: str, scale: Union[bool, tuple[int, int]], inverted: bool) -> str:
    color_matrix = get_pixel_matrix(file, scale)
    intensity_matrix = get_intensity_matrix(color_matrix, map_type, inverted)

    output = str()
    for row in intensity_matrix:
        chars = [get_char_from_intensity(i) for i in row]
        output += ''.join(chars) + '\n'

    return output
