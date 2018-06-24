from typing import Tuple, Type, Iterable, TextIO

IO = TextIO


class Reader:
    @staticmethod
    def integer_list_line(file: IO) -> Tuple[int, ...]:
        line = file.readline()
        return tuple(int(i) for i in line.split(" "))

    @staticmethod
    def string_line(file: IO):
        line = file.readline()
        return str(line).strip()

    @staticmethod
    def single_integer(file: IO):
        return int(Reader.string_line(file))

    @staticmethod
    def multi_types_multi_lines(file: IO, types: Tuple[Type, ...], separator=" "):
        lines = []

        for line in file:
            typed_data = []
            lines.append(typed_data)

            for t, data in zip(types, line.split(separator)):
                typed_data.append(t(data))

        return lines


class Writer:
    @staticmethod
    def integer_list_line(file: IO, integers: Iterable[int], separator=" ") -> None:
        file.write(separator.join(str(int(round(i))) for i in integers) + "\n")

    @staticmethod
    def integer(file: IO, integer: int) -> None:
        file.write(str(int(round(integer))) + "\n")

    @staticmethod
    def list_line(file: IO, str_list: Iterable, separator=" "):
        file.write(separator.join(str(item) for item in str_list) + "\n")
