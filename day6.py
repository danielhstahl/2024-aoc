## This is the first one to give me some trouble.
## if I had to redo this I would have made a more
## generic "move" function to encapsolate the logic

from typing import List, Tuple, Optional


def load_from_file(file_name: str) -> List[List[str]]:
    values = []
    with open(file_name, newline="\n") as file:
        for row in file.readlines():
            cleaned = row.strip()
            values.append(list(cleaned))
    return values


def find_init_carrot(map: List[List[str]]) -> Tuple[int, int]:
    for row_index, row in enumerate(map):
        for col_index, value in enumerate(row):
            if value == "^":
                return row_index, col_index


def up(map: List[List[str]], row_index: int, col_index: int) -> Tuple[bool, int, int]:
    new_index = row_index - 1
    if new_index >= 0:
        if map[new_index][col_index] == "#":
            if (
                map[row_index][col_index + 1] == "#"
            ):  # hit another corner rahter than advancing
                return False, row_index, col_index
            return False, row_index, col_index + 1
        else:
            return True, new_index, col_index
    return True, new_index, col_index


def down(map: List[List[str]], row_index: int, col_index: int) -> Tuple[bool, int, int]:
    new_index = row_index + 1
    if new_index < len(map):
        if map[new_index][col_index] == "#":
            if (
                map[row_index][col_index - 1] == "#"
            ):  # hit another corner rahter than advancing
                return False, row_index, col_index
            return False, row_index, col_index - 1
        else:
            return True, new_index, col_index
    return True, new_index, col_index


def left(map: List[List[str]], row_index: int, col_index: int) -> Tuple[bool, int, int]:
    new_index = col_index - 1
    if new_index >= 0:
        if map[row_index][new_index] == "#":
            if (
                map[row_index - 1][col_index] == "#"
            ):  # hit another corner rahter than advancing
                return False, row_index, col_index
            return False, row_index - 1, col_index
        else:
            return True, row_index, new_index

    return True, row_index, new_index


def right(
    map: List[List[str]], row_index: int, col_index: int
) -> Tuple[bool, int, int]:
    new_index = col_index + 1
    if new_index < len(map[0]):
        if map[row_index][new_index] == "#":
            if (
                map[row_index + 1][col_index] == "#"
            ):  # hit another corner rahter than advancing
                return False, row_index, col_index
            return False, row_index + 1, col_index
        else:
            return True, row_index, new_index
    return False, row_index, new_index


class Move:
    location = "up"
    map_fn = {"up": up, "right": right, "left": left, "down": down}

    def rotate(self):
        if self.location == "up":
            self.location = "right"
        elif self.location == "right":
            self.location = "down"
        elif self.location == "down":
            self.location = "left"
        elif self.location == "left":
            self.location = "up"

    def move(
        self, map: List[List[str]], row_index: int, col_index: int
    ) -> Tuple[bool, int, int]:
        return self.map_fn[self.location](map, row_index, col_index)


def _location_key(row_index: int, col_index: int) -> str:
    return str(row_index) + "_" + str(col_index)


def iterate_map(map: List[List[str]], start: Tuple[int, int]) -> Optional[List[str]]:
    row_index, col_index = start
    move = Move()
    locations = {}
    direction_and_location = {}
    location_key = _location_key(row_index, col_index)
    direction_key = "first"
    while (
        row_index >= 0
        and row_index < len(map)
        and col_index >= 0
        and col_index < len(map[0])
    ):
        location_key = _location_key(row_index, col_index)
        locations[location_key] = True
        full_key = location_key + direction_key

        if (
            location_key != direction_key
        ):  # can, in some cases, have duplicate keys if hit a multiple blocks and rotate in place
            if full_key in direction_and_location:
                direction_and_location[full_key] += 1
            else:
                direction_and_location[full_key] = 1
            if direction_and_location[full_key] > 1:
                return None  # loop
        direction_key = location_key  # previous "direction"
        no_obstacle, new_row_index, new_col_index = move.move(map, row_index, col_index)
        if not no_obstacle:
            move.rotate()
        row_index = new_row_index
        col_index = new_col_index

    return list(locations.keys())


def exhaustive_and_expensive_search(
    map: List[List[str]], start: Tuple[int, int]
) -> int:
    total_num = 0
    for row_index, row in enumerate(map):
        for col_index, value in enumerate(row):
            if value != "#" and value != "^":
                map[row_index][col_index] = "#"
                if iterate_map(map, start) == -1:
                    total_num += 1
                map[row_index][col_index] = value
    return total_num


def exhaustive_and_expensive_search_but_only_on_locations_can_hit(
    map: List[List[str]],
    start: Tuple[int, int],
    locations_to_try: List[Tuple[int, int]],
) -> int:
    total_num = 0
    for value in locations_to_try:
        row_index, col_index = value
        map[row_index][col_index] = "#"
        if not iterate_map(map, start):
            total_num += 1
        map[row_index][col_index] = value
    return total_num


def _unwrap_strings(path: List[str]) -> List[Tuple[int, int]]:
    locations = []
    for value in path:
        row, col = value.split("_")
        locations.append((int(row), int(col)))
    return locations


if __name__ == "__main__":
    map = load_from_file("day6_input_example.txt")
    results_test = iterate_map(map, find_init_carrot(map))
    print(len(results_test))  # should be 41

    actual_map = load_from_file("day6_input.txt")
    start = find_init_carrot(actual_map)
    results = iterate_map(actual_map, start)
    print(len(results))  #  5153
    # Part 2

    print(
        exhaustive_and_expensive_search_but_only_on_locations_can_hit(
            map, find_init_carrot(map), _unwrap_strings(results_test)
        )
    )  # should be 6

    print(
        exhaustive_and_expensive_search_but_only_on_locations_can_hit(
            actual_map, start, _unwrap_strings(results)
        )
    )  # should not be 1709...1709 is too small :(  It is 1711, good grief
