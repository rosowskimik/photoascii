from io import BufferedReader
from PIL import Image
import pathlib

LETTER_MATRIX = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def get_pixel_matrix(file: BufferedReader):
    with Image.open(file) as img:
        img.thumbnail(size=(250, 250))
        img.show()
        width = img.width
        pixels = list(img.getdata())

        pixel_matrix = [pixels[i:i+width]
                        for i in range(0, len(pixels), width)]

    return pixel_matrix


def get_intensity_matrix(pixel_matrix) -> int:
    intensity_matrix = [[(r + g + b) / 3 for r, g, b in row]
                        for row in pixel_matrix]

    return intensity_matrix


def get_char_from_intensity(intensity: int) -> str:
    scale = intensity / 255
    char = LETTER_MATRIX[round(scale * 64)] * 3

    return char


def convert_image(file: BufferedReader) -> str:
    color_matrix = get_pixel_matrix(file)
    intensity_matrix = get_intensity_matrix(color_matrix)

    output = str()
    for row in intensity_matrix:
        chars = [get_char_from_intensity(i) for i in row]
        output += ''.join(chars) + '\n'

    return output
