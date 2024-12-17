from typing import List, Tuple, Dict


def load_from_file(file_name: str) -> List[List[str]]:
    values = []
    with open(file_name, newline="\n") as file:
        for row in file.readlines():
            cleaned = row.strip()
            values.append(list(cleaned))
    return values


def get_map_by_character(
    locations: List[List[str]],
) -> Dict[str, List[Tuple[int, int]]]:
    map_of_antenna: Dict[str, List[Tuple[int, int]]] = {}
    for row_index, row in enumerate(locations):
        for col_index, value in enumerate(row):
            if value != ".":
                if value in map_of_antenna:
                    map_of_antenna[value].append((row_index, col_index))
                else:
                    map_of_antenna[value] = [(row_index, col_index)]
    return map_of_antenna


def out_of_bounds(bounds: Tuple[int, int], row_index: int, col_index: int) -> bool:
    if row_index < 0:
        return True
    if col_index < 0:
        return True
    if row_index >= bounds[0]:
        return True
    if col_index >= bounds[1]:
        return True
    return False


def get_antinode_part_1(
    antenna1: Tuple[int, int], antenna2: Tuple[int, int], matrix_bounds: Tuple[int, int]
) -> List[Tuple[int, int]]:
    row_index_1, col_index_1 = antenna1
    row_index_2, col_index_2 = antenna2
    vertical_dist = row_index_1 - row_index_2
    horizontal_dist = col_index_1 - col_index_2

    before_row_index_1 = row_index_1 + vertical_dist
    after_row_index_2 = row_index_2 - vertical_dist

    before_col_index_1 = col_index_1 + horizontal_dist
    after_col_index_2 = col_index_2 - horizontal_dist

    result = []
    if not out_of_bounds(matrix_bounds, before_row_index_1, before_col_index_1):
        result.append((before_row_index_1, before_col_index_1))

    if not out_of_bounds(matrix_bounds, after_row_index_2, after_col_index_2):
        result.append((after_row_index_2, after_col_index_2))
    return result


def get_antinodes_part_2(
    antenna1: Tuple[int, int], antenna2: Tuple[int, int], matrix_bounds: Tuple[int, int]
) -> List[Tuple[int, int]]:
    direction_1_row_index, direction_1_col_index = antenna1
    direction_2_row_index, direction_2_col_index = antenna2
    vertical_dist = direction_1_row_index - direction_2_row_index
    horizontal_dist = direction_1_col_index - direction_2_col_index

    result = []
    while not out_of_bounds(
        matrix_bounds, direction_1_row_index, direction_1_col_index
    ):
        result.append((direction_1_row_index, direction_1_col_index))
        direction_1_row_index = direction_1_row_index + vertical_dist
        direction_1_col_index = direction_1_col_index + horizontal_dist

    while not out_of_bounds(
        matrix_bounds, direction_2_row_index, direction_2_col_index
    ):
        result.append((direction_2_row_index, direction_2_col_index))
        direction_2_row_index = direction_2_row_index - vertical_dist
        direction_2_col_index = direction_2_col_index - horizontal_dist

    return result


def find_all_anti_nodes(
    antenna_of_type: List[Tuple[int, int]], get_antinode: callable
) -> List[Tuple[int, int]]:
    anti_nodes = []
    for index, antenna in enumerate(antenna_of_type):
        for other_antenna in antenna_of_type[index + 1 :]:
            for anti_node in get_antinode(antenna, other_antenna):
                anti_nodes.append(anti_node)
    return anti_nodes


def get_all_anti_nodes_for_each_key(
    all_antennas: Dict[str, List[Tuple[int, int]]],
    get_antinode: callable,
) -> Dict[str, List[str]]:
    unique_set: Dict[str, List[str]] = {}
    for antenna_key, antenna_set in all_antennas.items():
        all_anti_nodes = find_all_anti_nodes(antenna_set, get_antinode)
        keys = [f"{anti_node[0]}_{anti_node[1]}" for anti_node in all_anti_nodes]
        for key in keys:
            if key in unique_set:
                unique_set[key].append(antenna_key)
            else:
                unique_set[key] = [antenna_key]
    return unique_set


if __name__ == "__main__":
    test_inputs = load_from_file("day8_input_example.txt")
    test_map_of_antenna = get_map_by_character(test_inputs)
    test_results = get_all_anti_nodes_for_each_key(
        test_map_of_antenna,
        lambda antenna1, antenna2: get_antinode_part_1(
            antenna1, antenna2, (len(test_inputs), len(test_inputs[0]))
        ),
    )
    print(len(list(test_results.keys())))

    inputs = load_from_file("day8_input.txt")
    map_of_antenna = get_map_by_character(inputs)
    results = get_all_anti_nodes_for_each_key(
        map_of_antenna,
        lambda antenna1, antenna2: get_antinode_part_1(
            antenna1, antenna2, (len(inputs), len(inputs[0]))
        ),
    )
    print(len(list(results.keys())))
    # print(get_all_answers(inputs))  #

    ## Step 2
    test_results_part_2 = get_all_anti_nodes_for_each_key(
        test_map_of_antenna,
        lambda antenna1, antenna2: get_antinodes_part_2(
            antenna1, antenna2, (len(test_inputs), len(test_inputs[0]))
        ),
    )
    print(len(list(test_results_part_2.keys())))  # should be 34

    results_part_2 = get_all_anti_nodes_for_each_key(
        map_of_antenna,
        lambda antenna1, antenna2: get_antinodes_part_2(
            antenna1, antenna2, (len(inputs), len(inputs[0]))
        ),
    )
    print(len(list(results_part_2.keys())))
