import argparse
import pathlib
from photoascii import convert_image


def main():
    parser = argparse.ArgumentParser(
        prog="photoascii", description="Convert images to ascii art")

    parser.add_argument("images", type=argparse.FileType(mode="rb"), nargs="+")

    args = parser.parse_args()

    for file in args.images:
        output_text = convert_image(file)
        with open('output.txt', 'w') as nf:
            nf.write(output_text)


if __name__ == "__main__":
    main()
