from typing import List, Tuple, Optional


def load_from_file(file_name: str) -> List[List[str]]:
    values = []
    with open(file_name, newline="\n") as file:
        for row in file.readlines():
            cleaned = row.strip()
            values.append([int(v) for v in cleaned])
    return values


def find_trailheads(map: List[List[int]]) -> List[Tuple[int, int]]:
    trail_head = []
    for row_index, row in enumerate(map):
        for col_index, value in enumerate(row):
            if value == 0:
                trail_head.append((row_index, col_index))
    return trail_head


def if_in_range_get_value(map: List[List[int]], spot: Tuple[int, int]) -> Optional[int]:
    num_rows = len(map)
    num_cols = len(map[0])
    row_index, col_index = spot
    if row_index < 0:
        return None
    if col_index < 0:
        return None
    if row_index >= num_rows:
        return None
    if col_index >= num_cols:
        return None
    return map[row_index][col_index]


def find_in_radii(
    map: List[List[int]], spot: Tuple[int, int], next_number: int
) -> List[Tuple[int, int]]:
    row_index, col_index = spot
    radii = {
        "up": (row_index - 1, col_index),
        "left": (row_index, col_index - 1),
        "right": (row_index, col_index + 1),
        "down": (row_index + 1, col_index),
    }
    return [
        v[1]
        for v in (
            (if_in_range_get_value(map, value), value) for value in radii.values()
        )
        if v[0] is not None and v[0] == next_number
    ]


def iterate_path(
    map: List[List[int]],
    hold_end: List[Tuple[int, int]],
    next_step: Tuple[int, int],
    next_number: int,
) -> int:
    next_iter = find_in_radii(map, next_step, next_number)
    if next_number == 9:
        hold_end.extend(
            [f"{row_index}_{col_index}" for row_index, col_index in next_iter]
        )
    else:
        for step in next_iter:
            iterate_path(map, hold_end, step, next_number + 1)


def get_paths_per_trailhead(
    map: List[List[int]], trail_head: Tuple[int, int]
) -> List[List[int]]:
    steps = []
    iterate_path(map, steps, trail_head, 1)
    return steps


def get_unique_trail_heads(trail_ends: List[str]) -> List[str]:
    return list(set(trail_ends))


def get_sum_of_trail_heads(
    map: List[List[int]], trail_heads: List[Tuple[int, int]]
) -> int:

    return sum(
        len(get_unique_trail_heads(get_paths_per_trailhead(map, trail_head)))
        for trail_head in trail_heads
    )


def get_sum_of_all_paths(
    map: List[List[int]], trail_heads: List[Tuple[int, int]]
) -> int:
    return sum(
        len(get_paths_per_trailhead(map, trail_head)) for trail_head in trail_heads
    )


if __name__ == "__main__":
    test_map = load_from_file("day10_input_example.txt")
    test_trail_heads = find_trailheads(test_map)
    print(get_sum_of_trail_heads(test_map, test_trail_heads))  # should be 36

    map = load_from_file("day10_input.txt")
    trail_heads = find_trailheads(map)
    print(get_sum_of_trail_heads(map, trail_heads))  #

    # part 2
    print(get_sum_of_all_paths(test_map, test_trail_heads))  # should be 81
    print(get_sum_of_all_paths(map, trail_heads))
