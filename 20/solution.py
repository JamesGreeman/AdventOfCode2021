from __future__ import annotations

from typing import List


def read_raw_input() -> ImageProcessor:
    lines = [line.strip() for line in open("input.txt")]
    processing_key = [True if char == '#' else False for char in lines[0]]

    image = [[True if char == '#' else False for char in line] for line in lines[1:] if line]

    return ImageProcessor(processing_key, image)


class ImageProcessor:

    def __init__(self, processing_key: List[bool], initial_image: List[List[bool]]):
        self.processing_key = processing_key
        self.image = initial_image
        self.outer_pixels_lit = False

    def process_image(self):
        processed_image = []
        for y in range(0, len(self.image) + 2):
            row = []
            for x in range(0, len(self.image[0]) + 2):
                processed_decimal = self.to_decimal(self.get_surrounding_pixels(x - 1, y - 1))
                row.append(self.processing_key[processed_decimal])
            processed_image.append(row)

        self.image = processed_image
        self.outer_pixels_lit = self.processing_key[511] if self.outer_pixels_lit else self.processing_key[0]

    def get_surrounding_pixels(self, x: int, y: int) -> List[bool]:
        pixels = []
        coords = []
        for y_iter in range(y-1, y+2):
            for x_iter in range(x-1, x+2):
                coords.append(f"{x_iter},{y_iter}")
                if x_iter < 0 or y_iter < 0 or x_iter >= len(self.image[0]) or y_iter >= len(self.image):
                    pixels.append(self.outer_pixels_lit)
                else:
                    pixels.append(self.image[y_iter][x_iter])
        return pixels

    def get_number_lit(self) -> int:
        if self.outer_pixels_lit:
            raise ValueError("There are infinite lit pixels.")
        else:
            return sum([1 if val else 0 for row in self.image for val in row])

    @staticmethod
    def to_decimal(bools: List[bool]) -> int:
        bitstring = "".join(["1" if val else "0" for val in bools])
        return int(bitstring, 2)

    def __repr__(self) -> str:
        return "\n".join(["".join(["#" if val else "." for val in line]) for line in self.image])


def main():
    image = read_raw_input()

    print(image)
    for _ in range(0, 50):
        image.process_image()
        print()
        print(image)

    print(image.get_number_lit())


main()
