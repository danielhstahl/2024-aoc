from typing import List


def check_increasing(levels: List[int]) -> bool:
    for item1, item2 in zip(levels[:-1], levels[1:]):
        if item1 >= item2:
            return False
    return True


def check_decreasing(levels: List[int]) -> bool:
    for item1, item2 in zip(levels[:-1], levels[1:]):
        if item1 <= item2:
            return False
    return True


def check_range(levels: List[int]) -> bool:
    for item1, item2 in zip(levels[:-1], levels[1:]):
        if abs(item1 - item2) > 3:
            return False

    return True


def check_safe(levels: List[int]) -> bool:
    if check_increasing(levels):
        if check_range(levels):
            return True
    elif check_decreasing(levels):
        if check_range(levels):
            return True
    return False


def check_safe_remove_item(levels: List[int], end: bool = False) -> bool:
    if check_safe(levels):
        return True
    elif not end:
        for index in range(len(levels)):
            new_level = levels[:index] + levels[index + 1 :]
            if check_safe_remove_item(new_level, True):
                return True
    return False


def get_number_that_are_safe(levels: List[List[int]]) -> int:
    number_safe = 0
    for level in levels:
        if check_safe(level):
            number_safe += 1

    return number_safe


if __name__ == "__main__":
    levels = [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9],
    ]

    print(get_number_that_are_safe(levels))  ## should be 2
    import csv

    number_safe = 0
    with open("day2_input.txt", newline="\n") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in spamreader:
            row_int = [int(elem) for elem in row]
            if check_safe(row_int):
                number_safe += 1
    print(number_safe)

    ## Part 2
    for level in levels:
        print(check_safe_remove_item(level))

    number_safe = 0
    with open("day2_input.txt", newline="\n") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in spamreader:
            row_int = [int(elem) for elem in row]
            if check_safe_remove_item(row_int):
                number_safe += 1
    print(number_safe)
