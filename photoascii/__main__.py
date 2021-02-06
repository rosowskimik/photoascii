import argparse
import sys
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
    parser.add_argument("-o", "--outfile", type=argparse.FileType(mode="w"),
                        dest="outfile", default=sys.stdout, help="write output to file")
    parser.add_argument("-i", "--inverted", action="store_true",
                        dest="inverted", default=False, help="invert light & dark colors")

    args = parser.parse_args()

    for file in args.images:
        output_text = convert_image(
            file, args.map_type, args.scale, args.inverted)
        args.outfile.write(output_text)

    args.outfile.close()


if __name__ == "__main__":
    main()
