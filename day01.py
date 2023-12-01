from sys import stdin
from typing import Iterable, NewType, TypeVar, Type


def main() -> None:
    data: str = stdin.read()
    calibration_document = CalibrationDocument.from_string(data)
    correct_calibration_document = CorrectedCalibrationDocument.from_string(data)
    print("Part 1:", calibration_document.calibration_value())
    print("Part 2:", correct_calibration_document.calibration_value())


DigitTranslationTable = dict[str, int]
CalibrationLine = NewType("CalibrationLine", list[int])
T = TypeVar("T", bound="CalibrationDocument")


class CalibrationDocument:
    translation_table: DigitTranslationTable = {str(num): num for num in range(1, 10)}

    def __init__(self, lines: list[CalibrationLine]):
        self.lines: list[CalibrationLine] = lines

    @classmethod
    def from_string(cls: Type[T], data: str) -> T:
        return cls(
            list(
                CalibrationLine(
                    list(digit_generator(line, table=cls.translation_table))
                )
                for line in data.split("\n")
                if line
            )
        )

    def calibration_value(self) -> int:
        return sum(10 * line[0] + line[-1] for line in self.lines)


class CorrectedCalibrationDocument(CalibrationDocument):
    translation_table: DigitTranslationTable = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        **CalibrationDocument.translation_table,
    }


def digit_generator(calibration_line: str, *, table: dict) -> Iterable[int]:
    while calibration_line:
        for name, value in table.items():
            if calibration_line.startswith(name):
                yield value
                break

        calibration_line = calibration_line[1:]


if __name__ == "__main__":
    main()
