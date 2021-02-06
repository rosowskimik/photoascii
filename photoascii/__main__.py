import argparse
from photoascii import convert_image


def size_type(string: str):
    if string == "fit":
        return True
    if string == "none":
        return False

    if "x" not in string:
        raise ValueError

    width, height = string.split("x")
    return (int(width), int(height))


def main():
    parser = argparse.ArgumentParser(
        prog="photoascii", description="Convert images to ascii art")

    parser.add_argument("images", type=argparse.FileType(mode="rb"), nargs="+")
    parser.add_argument("-m", "--map", choices=("average", "lightness",
                                                "luminosity"), dest="map_type", default="average", help="(default: %(default)s)")
    parser.add_argument("-s", "--scale", dest="scale", default="fit", type=size_type,
                        help="resize image before converting, use 'none' to convert image 1:1 (default: scale to fit terminal)", metavar="[width]x[height]")

    args = parser.parse_args()

    for file in args.images:
        output_text = convert_image(file, args.map_type, args.scale)
        with open('output.txt', 'w') as nf:
            nf.write(output_text)
        # print(output_text)


if __name__ == "__main__":
    main()
