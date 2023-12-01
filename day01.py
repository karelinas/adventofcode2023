from sys import stdin
from typing import Iterable

DIGIT_NAMES = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
DIGITS = {str(num): num for num in range(1, 10)}
DIGITS_AND_NAMES = {**DIGITS, **DIGIT_NAMES}


def main() -> None:
    calibration_document: str = stdin.read()
    print("Part 1:", calibration_value(calibration_document))
    print("Part 2:", corrected_calibration_value(calibration_document))


def digit_generator(calibration_line: str, *, table: dict) -> Iterable[int]:
    while calibration_line:
        for name, value in table.items():
            if calibration_line.startswith(name):
                yield value
                break

        calibration_line = calibration_line[1:]


def line_value(calibration_digits: list[int]) -> int:
    return 10 * calibration_digits[0] + calibration_digits[-1]


def calibration_value(calibration_document: str, *, table=None) -> int:
    table = table or DIGITS
    return sum(
        line_value(list(digit_generator(line, table=table)))
        for line in calibration_document.split("\n")
        if line
    )


def corrected_calibration_value(calibration_document: str) -> int:
    return calibration_value(calibration_document, table=DIGITS_AND_NAMES)


if __name__ == "__main__":
    main()
