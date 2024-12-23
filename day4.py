from typing import List, Callable

PATTERN_TO_MATCH = "XMAS"


def back(pattern: List[str], i: int, j: int) -> int:
    length_pattern = len(PATTERN_TO_MATCH)
    if i >= length_pattern - 1:
        pattern = "".join([pattern[j][i - k] for k in range(length_pattern)])
        return 1 if pattern == PATTERN_TO_MATCH else 0
    return 0


def back_up_diag(pattern: List[str], i: int, j: int) -> bool:
    length_pattern = len(PATTERN_TO_MATCH)
    if i >= length_pattern - 1 and j >= length_pattern - 1:
        pattern = "".join([pattern[j - k][i - k] for k in range(length_pattern)])
        return 1 if pattern == PATTERN_TO_MATCH else 0
    return 0


def up(pattern: List[str], i: int, j: int) -> bool:
    length_pattern = len(PATTERN_TO_MATCH)
    if j >= length_pattern - 1:
        pattern = "".join([pattern[j - k][i] for k in range(length_pattern)])
        return 1 if pattern == PATTERN_TO_MATCH else 0
    return 0


def forward_up_diag(pattern: List[str], i: int, j: int) -> bool:
    length_pattern = len(PATTERN_TO_MATCH)
    length_text = len(pattern[0])
    if i <= length_text - length_pattern and j >= length_pattern - 1:
        pattern = "".join([pattern[j - k][i + k] for k in range(length_pattern)])
        return 1 if pattern == PATTERN_TO_MATCH else 0
    return 0


def forward(pattern: List[str], i: int, j: int) -> bool:
    length_pattern = len(PATTERN_TO_MATCH)
    length_text = len(pattern[0])
    if i <= length_text - length_pattern:
        return 1 if pattern[j][i : i + length_pattern] == PATTERN_TO_MATCH else 0
    return 0


def forward_down_diag(pattern: List[str], i: int, j: int) -> bool:
    length_pattern = len(PATTERN_TO_MATCH)
    length_text = len(pattern[0])
    if i <= length_text - length_pattern and j <= len(pattern) - length_pattern:
        pattern = "".join([pattern[j + k][i + k] for k in range(length_pattern)])
        return 1 if pattern == PATTERN_TO_MATCH else 0
    return 0


def down(pattern: List[str], i: int, j: int) -> bool:
    length_pattern = len(PATTERN_TO_MATCH)
    if j <= len(pattern) - length_pattern:
        pattern = "".join([pattern[j + k][i] for k in range(length_pattern)])
        return 1 if pattern == PATTERN_TO_MATCH else 0
    return 0


def back_down_diag(pattern: List[str], i: int, j: int) -> bool:
    length_pattern = len(PATTERN_TO_MATCH)
    if i >= length_pattern - 1 and j <= len(pattern) - length_pattern:
        pattern = "".join([pattern[j + k][i - k] for k in range(length_pattern)])
        return 1 if pattern == PATTERN_TO_MATCH else 0
    return 0


def find_match(pattern: List[str]) -> int:
    total_match = 0
    for j, row in enumerate(pattern):
        for i, _ in enumerate(row):
            total_match += (
                back(pattern, i, j)
                + back_up_diag(pattern, i, j)
                + up(pattern, i, j)
                + forward_up_diag(pattern, i, j)
                + forward(pattern, i, j)
                + forward_down_diag(pattern, i, j)
                + down(pattern, i, j)
                + back_down_diag(pattern, i, j)
            )
    return total_match


def return_element_if_in_bounds(pattern: List[str], i: int, j: int) -> str:
    if i >= len(pattern):
        return None
    if i < 0:
        return None
    if j >= len(pattern[i]):
        return None
    if j < 0:
        return None
    return pattern[i][j]


def _plus(a: int, b: int) -> int:
    return a + b


def _minus(a: int, b: int) -> int:
    return a - b


def _nothing(a: int, b: int) -> int:
    return a


def generic_match(
    pattern: List[str],
    i: int,
    j: int,
    operator1: Callable[[int, int], int],
    operator2: Callable[[int, int], int],
) -> bool:
    length_pattern = len(PATTERN_TO_MATCH)
    pattern = "".join(
        element
        for element in [
            return_element_if_in_bounds(pattern, operator1(i, k), operator2(j, k))
            for k in range(length_pattern)
        ]
        if element is not None
    )
    return 1 if pattern == PATTERN_TO_MATCH else 0


def find_match_generic(pattern: List[str]) -> int:
    total_match = 0
    total_indeces = 0
    for i, row in enumerate(pattern):
        for j, _ in enumerate(row):
            total_indeces += 1
            total_match += (
                generic_match(pattern, i, j, _minus, _minus)  # down left diagonal
                + generic_match(pattern, i, j, _minus, _plus)  # down right diagnoal
                + generic_match(pattern, i, j, _plus, _minus)  # up left diagonal
                + generic_match(pattern, i, j, _plus, _plus)  # up right diagonal
                + generic_match(pattern, i, j, _minus, _nothing)  # down
                + generic_match(pattern, i, j, _nothing, _minus)  # left
                + generic_match(pattern, i, j, _plus, _nothing)  # up
                + generic_match(pattern, i, j, _nothing, _plus)  # right
            )
    print(total_indeces)
    return total_match


def find_x(pattern: List[str], i: int, j: int) -> int:
    slash1 = pattern[i - 1][j - 1] + pattern[i][j] + pattern[i + 1][j + 1]
    slash2 = pattern[i + 1][j - 1] + pattern[i][j] + pattern[i - 1][j + 1]
    if slash1 == "MAS" or slash1 == "SAM":
        if slash2 == "MAS" or slash2 == "SAM":
            return 1
    return 0


def part_2(pattern: List[str]) -> int:
    num_row = len(pattern)
    total = 0
    for i in range(1, num_row - 1):
        num_col = len(pattern[i])
        for j in range(1, num_col - 1):
            total += find_x(pattern, i, j)

    return total


if __name__ == "__main__":
    init_pattern = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX",
    ]
    print(find_match_generic(init_pattern))  # should be 18

    pattern = []
    with open("day4_input.txt", newline="\n") as file:
        for row in file.readlines():
            pattern.append(row.strip())
    print(find_match_generic(pattern))

    ## Part 2
    print(part_2(init_pattern))
    print(part_2(pattern))
