## Part two is my first failure
## I went down a wrong lane and will have to
## refactor a ton of code to get this working
## there may be a recursive solution, but
## nothing about this is elegant and the edge
## cases are highly irritating.

from typing import List, Tuple, Optional


def load_from_file(file_name: str) -> Tuple[List[str], str]:
    values = []
    first_part = True
    directions = ""
    with open(file_name, newline="\n") as file:
        for row in file.readlines():
            cleaned = row.strip()
            if first_part and cleaned != "":
                values.append(list(cleaned))
            else:
                directions += cleaned
            if cleaned == "":
                first_part = False

    return values, directions


def find_robot_start(warehouse: List[List[str]]) -> Tuple[int, int]:
    for row_index, row in enumerate(warehouse):
        for col_index, value in enumerate(row):
            if value == "@":
                return row_index, col_index


def logic_for_relevant_slice(relevant_slice: List[str]):
    # begin from robot

    for index, element in enumerate(relevant_slice):
        if element == "#":
            break  # can't move
        if element == ".":  # if room to move, move everything
            relevant_slice.pop(
                index
            )  # wow, is this really all the logic needed?  thats awesome if so
            break


def logic_for_larger_slice(
    warehouse: List[List[str]], row_index: int, col_index: int, direction: str
) -> Optional[
    List[Tuple[int, Tuple[int, int]]]
]:  # only up or down, left and right follows previous logic
    # begin from robot
    if direction == "^":
        width_left = 0
        width_right = 1
        hold_all_element_indeces = []
        for index in range(row_index):
            hold_all_element_indeces.append(
                (row_index - index, (col_index - width_left, col_index + width_right))
            )
            elements = warehouse[row_index - index][
                col_index - width_left : col_index + width_right
            ]

            if elements[0] == "]":
                width_left += 1

            if elements[-1] == "[":
                width_right += 1
            # print(
            ##    "index",
            ##   index,
            #  "hold_all_element",
            #  hold_all_element_indeces,
            #  "elements",
            #  elements,
            # )

            # if "".join(elements) == "]":
            #    width_left += 1
            # if "".join(elements) == "[":
            #    width_right += 1
            # if "".join(elements) == "[]":
            # do nothing
            #    pass

            # add more if exist

            # take away if dont exist
            j = 0
            while j < len(elements) and elements[j] == ".":
                j += 1
                width_left -= 1
            j = len(elements) - 1
            while j >= 0 and elements[j] == ".":
                j -= 1
                width_right -= 1

            for element in elements:
                # this logic doesnt work; can have pounds in between "valid" blocks
                if element == "#":
                    return None  # can't move

            do_all_equal_period = True
            for element in elements:
                if element != ".":
                    do_all_equal_period = False
            if do_all_equal_period:
                return hold_all_element_indeces
    else:  ## direction is down
        width_left = 0
        width_right = 1
        hold_all_element_indeces = []
        for index in range(len(warehouse) - row_index):
            hold_all_element_indeces.append(
                (row_index + index, (col_index - width_left, col_index + width_right))
            )
            elements = warehouse[row_index + index][
                col_index - width_left : col_index + width_right
            ]
            if elements[0] == "]":
                width_left += 1
            if elements[-1] == "[":
                width_right += 1

            j = 0
            while j < len(elements) and elements[j] == ".":
                j += 1
                width_left -= 1
            j = len(elements) - 1
            while j >= 0 and elements[j] == ".":
                j -= 1
                width_right -= 1
            for element in elements:
                if element == "#":
                    return None  # can't move...this is actually false, sometimes boxes can wrap "around" barriers.
            do_all_equal_period = True
            for element in elements:
                if element != ".":
                    do_all_equal_period = False
            if do_all_equal_period:
                return hold_all_element_indeces


def splice_back_into_warehouse(
    warehouse: List[List[str]],
    spot: Tuple[int, int],
    direction: str,
    mutated_slice: List[str],
) -> Tuple[int, int]:
    row_index, col_index = spot
    num_rows = len(warehouse)
    num_cols = len(warehouse[0])
    n = len(mutated_slice)
    if direction == "<":

        for i in range(n):
            warehouse[row_index][n - i - 1] = mutated_slice[i]

        col_index_of_robot = n - 1
        if col_index_of_robot != col_index:
            warehouse[row_index][col_index] = "."  # if vacated by bot
        return row_index, col_index_of_robot
    elif direction == ">":
        for i in range(n):
            warehouse[row_index][num_cols - n + i] = mutated_slice[i]
        col_index_of_robot = num_cols - n
        if col_index_of_robot != col_index:
            warehouse[row_index][col_index] = "."  # if vacated by bot
        return row_index, col_index_of_robot
    elif direction == "^":
        for i in range(n):
            warehouse[n - i - 1][col_index] = mutated_slice[i]
        row_index_of_robot = n - 1
        if row_index_of_robot != row_index:
            warehouse[row_index][col_index] = "."  # if vacated by bot
        return row_index_of_robot, col_index

    elif direction == "v":
        for i in range(n):
            warehouse[num_rows - n + i][col_index] = mutated_slice[i]
        row_index_of_robot = num_rows - n
        if row_index_of_robot != row_index:
            warehouse[row_index][col_index] = "."  # if vacated by bot
        return row_index_of_robot, col_index


def pretty_print_warehouse(warehouse: List[List[str]]):

    for row in warehouse:
        col_str = ""
        for col in row:
            col_str += col
        print(col_str)


# warehouse will be mutated
def go_in_direction(
    warehouse: List[List[str]],
    spot: Tuple[int, int],
    direction: str,
) -> Tuple[int, int]:
    row_index, col_index = spot
    if direction == "<":
        relevant_slice = list(
            reversed(warehouse[row_index][0 : col_index + 1])
        )  # include robot

    elif direction == ">":
        relevant_slice = warehouse[row_index][col_index:]  # include robot

    elif direction == "^":
        relevant_slice = list(
            reversed([elem[col_index] for elem in warehouse[0 : row_index + 1]])
        )  # include robot

    else:  # v
        relevant_slice = [
            elem[col_index] for elem in warehouse[row_index:]
        ]  # include robot

    logic_for_relevant_slice(relevant_slice)
    # print("slice", relevant_slice, "spot", spot, "direction", direction)
    return splice_back_into_warehouse(warehouse, spot, direction, relevant_slice)


def follow_instructions(
    warehouse: List[List[str]],
    directions: str,
    start_spot: Tuple[int, int],
):
    spot = start_spot
    for direction in directions:
        spot = go_in_direction(warehouse, spot, direction)
        # pretty_print_warehouse(warehouse)


def check_is_valid(warehouse: List[List[str]]) -> bool:
    for row in warehouse:
        for v1, v2 in zip(row[:-1], row[1:]):
            if v1 == "[" and v2 != "]" or v2 == "]" and v1 != "[":
                return False
    return True


def follow_instructions_part_2(
    warehouse: List[List[str]],
    directions: str,
    start_spot: Tuple[int, int],
):
    spot = start_spot
    for direction in directions:
        spot = go_in_direction_part_2(warehouse, spot, direction)
        # print("direction", direction)
        # pretty_print_warehouse(warehouse)
        # if not check_is_valid(warehouse):
        #    print("NOT VALID")
        #    break


def go_in_direction_part_2(
    warehouse: List[List[str]], spot: Tuple[int, int], direction: str
):
    row_index, col_index = spot
    if direction == "<":
        relevant_slice = list(
            reversed(warehouse[row_index][0 : col_index + 1])
        )  # include robot
        logic_for_relevant_slice(relevant_slice)
        return splice_back_into_warehouse(warehouse, spot, direction, relevant_slice)
    elif direction == ">":
        relevant_slice = warehouse[row_index][col_index:]  # include robot
        logic_for_relevant_slice(relevant_slice)
        return splice_back_into_warehouse(warehouse, spot, direction, relevant_slice)
    elif direction == "^":
        result = logic_for_larger_slice(warehouse, row_index, col_index, direction)
        if (
            result is not None
        ):  # if it is None, then can't move; do nothing, move on to next direction
            for row_index, (col_index_left, col_index_right) in reversed(result[1:]):
                for i in range(col_index_left, col_index_right):
                    # print(
                    #    "setting warehouse at ",
                    #    row_index,
                    #    i,
                    #    "to value at ",
                    #    row_index + 1,
                    #    i,
                    #    "which is ",
                    #    warehouse[row_index + 1][i],
                    # )
                    warehouse[row_index][i] = warehouse[row_index + 1][i]
                    warehouse[row_index + 1][i] = "."
            return row_index, col_index
        return spot
    else:  # v
        result = logic_for_larger_slice(warehouse, row_index, col_index, direction)
        if (
            result is not None
        ):  # if it is None, then can't move; do nothing, move on to next direction
            for row_index, (col_index_left, col_index_right) in reversed(result[1:]):
                for i in range(col_index_left, col_index_right):

                    warehouse[row_index][i] = warehouse[row_index - 1][i]
                    warehouse[row_index - 1][i] = "."
            return row_index, col_index
        return spot


def get_gps_from_warehouse(
    warehouse: List[List[str]], value_to_check: str = "O"  # "[" for part 2
) -> int:
    total_result = 0
    for row_index, row in enumerate(warehouse):
        for col_index, value in enumerate(row):
            if value == value_to_check:
                total_result += row_index * 100 + col_index
    return total_result


# def get_gps_from_warehouse_part_2(warehouse: List[List[str]]) -> int:
#    total_result = 0
#    for row_index, row in enumerate(warehouse):
#        for col_index, value in enumerate(row):
#            if value == "[":  # will always make a full box
#                total_result += row_index * 100 + col_index
#    return total_result


def scale_map(warehouse: List[List[str]]) -> List[List[str]]:
    new_map = []
    for row in warehouse:
        new_row = []
        for value in row:
            if value == "#":
                new_row.append(value)
                new_row.append(value)
            elif value == "O":
                new_row.append("[")
                new_row.append("]")
            elif value == "@":
                new_row.append("@")
                new_row.append(".")
            else:
                new_row.append(".")
                new_row.append(".")
        new_map.append(new_row)
    return new_map


def not_me_solution(warehouse: List[List[str]]):
    # x_bound = len(warehouse[0]) * 2
    warehouse_map = dict()
    robot = tuple()
    for y, row in enumerate(warehouse):
        for x, this_char in enumerate(row):
            if this_char == "@":
                robot = (x * 2, y)
                warehouse_map[(x * 2, y)] = "@"
                warehouse_map[(x * 2 + 1, y)] = "."
            elif this_char == "O":
                warehouse_map[(x * 2, y)] = "["
                warehouse_map[(x * 2 + 1, y)] = "]"
            else:
                warehouse_map[(x * 2, y)] = this_char
                warehouse_map[(x * 2 + 1, y)] = this_char
    m = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}
    return m, robot, warehouse_map


def not_me_solution_iterate(warehouse_map, move, m, robot):

    dx, dy = m[move]  # Get the direction we're moving in
    move_possible = True  # If we hit a wall, this will turn False
    movers = {
        robot: warehouse_map[robot]
    }  # Things that will move if move_possible is still True at the end
    rx, ry = robot
    to_check = [(rx, ry)]
    # Since we could potentially be moving lots of stuff at once, we'll keep a queue of things we're going to move
    # that we need to check we have room for. When moving horizontally, we'll only add the far side of a box to this
    # queue, since that's the side that could potentially hit a wall. Whe moving vertically, we'll add both sides of
    # each box to the queue since either side could hit a wall (or a new box).
    while to_check:
        cx, cy = to_check.pop()  # My actual location
        mx, my = cx + dx, cy + dy  # The location I want to move to
        if move in "<>":
            if warehouse_map[(mx, my)] in "[]":
                # We are moving horizontally and we found the side of the box. Add it and the other side to the movers
                # dictionary and then add the far side of the box to the queue to make sure it has room to move
                movers[(mx, my)] = warehouse_map[(mx, my)]
                movers[(mx + dx, my)] = warehouse_map[(mx + dx, my)]
                to_check.append((mx + dx, my))
            elif warehouse_map[(mx, my)] == "#":
                # We found a wall. No move is possible. Stop checking.
                move_possible = False
                break
        elif move in "^v":
            if warehouse_map[(mx, my)] == "[":
                # We are moving vertically and we found the left side of a box. Add it and the right side to the
                # movers dictionary and then add both sides to the queue to make sure it has room to move
                movers[(mx, my)] = warehouse_map[(mx, my)]
                movers[(mx + 1, my)] = warehouse_map[(mx + 1, my)]
                to_check.extend([(mx, my), (mx + 1, my)])
            elif warehouse_map[(mx, my)] == "]":
                # We are moving vertically and we found the right side of a box. Add it and the left side to the movers
                # dictionary and then add both sides tot he queue to make sure it has room to move
                movers[(mx, my)] = warehouse_map[(mx, my)]
                movers[(mx - 1, my)] = warehouse_map[(mx - 1, my)]
                to_check.extend([(mx, my), (mx - 1, my)])
            elif warehouse_map[(mx, my)] == "#":
                # We found a wall. No move is possible. Stop checking.
                move_possible = False
                break

    if move_possible:
        # Set all the original locations to '.' in the warehouse_map
        for this_loc in movers:
            warehouse_map[this_loc] = "."
        # Move everyone to their new location
        for this_mover in movers:
            mx, my = this_mover
            warehouse_map[(mx + dx, my + dy)] = movers[this_mover]
        robot = (rx + dx, ry + dy)
        warehouse_map[robot] = "@"

    return robot
    # gps_sum = 0
    # for coord in warehouse_map:
    #    cx, cy = coord
    #    if warehouse_map[coord] == "[":
    #        gps_sum += cx + 100 * cy
    # return gps_sum


def compare_solution_warehouses(warehouse: List[List[str]], warehouse_map) -> bool:
    for row_index, row in enumerate(warehouse):
        for col_index, value in enumerate(row):
            if value != warehouse_map[(col_index, row_index)]:
                return False, row_index, col_index
    return True, -1, -1


def pretty_print_warehouse_not_mine(warehouse, warehouse_map):
    n = len(warehouse)
    m = len(warehouse[0])
    for i in range(n):
        line = ""
        for j in range(m):
            line += warehouse_map[(j, i)]
        print(line)


if __name__ == "__main__":
    # print(load_from_file("day15_input_example.txt"))
    test_warehouse, test_directions = load_from_file("day15_input_example2.txt")
    test_start = find_robot_start(test_warehouse)
    # pretty_print_warehouse(test_warehouse)
    follow_instructions(test_warehouse, test_directions, test_start)

    print(get_gps_from_warehouse(test_warehouse))  # should be 2028

    test_warehouse, test_directions = load_from_file("day15_input_example.txt")
    test_start = find_robot_start(test_warehouse)
    # pretty_print_warehouse(test_warehouse)
    follow_instructions(test_warehouse, test_directions, test_start)

    print(get_gps_from_warehouse(test_warehouse))  # should be 10092

    warehouse, directions = load_from_file("day15_input.txt")
    start = find_robot_start(warehouse)
    # pretty_print_warehouse(test_warehouse)
    follow_instructions(warehouse, directions, start)

    print(get_gps_from_warehouse(warehouse))  #

    ## PART 2
    test_warehouse, test_directions = load_from_file("day15_input_example3.txt")
    test_warehouse = scale_map(test_warehouse)
    test_start = find_robot_start(test_warehouse)
    # follow_instructions_part_2(test_warehouse, test_directions, test_start)
    # print(get_gps_from_warehouse(test_warehouse, "["))  #

    test_warehouse, test_directions = load_from_file("day15_input_example.txt")
    test_warehouse = scale_map(test_warehouse)
    test_start = find_robot_start(test_warehouse)
    # pretty_print_warehouse(test_warehouse)
    follow_instructions_part_2(test_warehouse, test_directions, test_start)
    pretty_print_warehouse(test_warehouse)
    print(get_gps_from_warehouse(test_warehouse, "["))  # should be 9021

    warehouse, directions = load_from_file("day15_input.txt")
    warehouse = scale_map(warehouse)
    start = find_robot_start(warehouse)
    follow_instructions_part_2(warehouse, directions, start)
    pretty_print_warehouse(warehouse)
    print(
        get_gps_from_warehouse(warehouse, "[")
    )  ### 1439968 TOO HIGH I think 1437468 is correct but I didn't get it
    print(find_robot_start(warehouse))

    warehouse, directions = load_from_file("day15_input.txt")
    # print(not_me_solution(warehouse, directions))

    ## Compare solutions
    spot = start
    m, robot, warehouse_map = not_me_solution(warehouse)
    warehouse = scale_map(warehouse)
    for index, direction in enumerate(directions):
        spot = go_in_direction_part_2(warehouse, spot, direction)
        robot = not_me_solution_iterate(warehouse_map, direction, m, robot)
        is_same, diff_row, diff_col = compare_solution_warehouses(
            warehouse, warehouse_map
        )
        if not is_same:
            print(index)
            print(diff_row)
            print(diff_col)
            pretty_print_warehouse(warehouse)
            pretty_print_warehouse_not_mine(warehouse, warehouse_map)
            break
