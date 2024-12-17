from typing import List, Tuple, Optional, Dict


def load_from_file(file_name: str) -> List[List[str]]:
    values = []
    with open(file_name, newline="\n") as file:
        for row in file.readlines():
            cleaned = row.strip()
            values.append(list(cleaned))
    return values


def extract_unique_regions_and_area(
    garden: List[List[str]],
) -> Dict[str, int]:
    keys = {}
    for row in garden:
        for item in row:
            if item in keys:
                keys[item] += 1
            else:
                keys[item] = 1
    return keys


def check_bounds(garden: List[List[str]], spot: Tuple[int, int]) -> bool:
    row_index, col_index = spot
    if row_index < 0:
        return False
    if col_index < 0:
        return False
    if row_index >= len(garden):
        return False
    if col_index >= len(garden[0]):
        return False

    return True


def element_has_border(
    garden: List[List[str]], region: str, spot: Tuple[int, int]
) -> int:
    row_index, col_index = spot
    up = (row_index - 1, col_index)
    right = (row_index, col_index + 1)
    down = (row_index + 1, col_index)
    left = (row_index, col_index - 1)
    total_border = 0
    if not check_bounds(garden, up) or garden[up[0]][up[1]] != region:
        total_border += 1
    if not check_bounds(garden, down) or garden[down[0]][down[1]] != region:
        total_border += 1
    if not check_bounds(garden, left) or garden[left[0]][left[1]] != region:
        total_border += 1
    if not check_bounds(garden, right) or garden[right[0]][right[1]] != region:
        total_border += 1
    return total_border


## this gets "nodes" rather than "spots".
## a "node" is a point on the spot.  So a spot of [1, 3] may have nodes of [1, 3], [1, 4], [2, 3], [2, 4]
def get_element_borders(
    garden: List[List[str]],
    region: str,
    spot: Tuple[int, int],
    border: List[Tuple[str, str, Tuple[int, int], Tuple[int, int]]],
) -> int:
    row_index, col_index = spot
    up = (row_index - 1, col_index)
    right = (row_index, col_index + 1)
    down = (row_index + 1, col_index)
    left = (row_index, col_index - 1)
    total_border = 0
    if not check_bounds(garden, up) or garden[up[0]][up[1]] != region:
        ul = (row_index, col_index)  # upper left
        ur = (row_index, col_index + 1)  # upper right
        border.append((get_key(ul), get_key(ur), ul, ur))

    if not check_bounds(garden, down) or garden[down[0]][down[1]] != region:
        br = (row_index + 1, col_index + 1)  # bottom right
        bl = (row_index + 1, col_index)  # bottom left
        border.append((get_key(br), get_key(bl), br, bl))

    if not check_bounds(garden, left) or garden[left[0]][left[1]] != region:
        bl = (row_index + 1, col_index)  # bottom left
        ul = (row_index, col_index)  # upper left
        border.append((get_key(bl), get_key(ul), bl, ul))

    if not check_bounds(garden, right) or garden[right[0]][right[1]] != region:
        ur = (row_index, col_index + 1)  # upper right
        br = (row_index + 1, col_index + 1)  # bottom right
        border.append((get_key(ur), get_key(br), ur, br))


def get_key(spot: Tuple[int, int]) -> str:
    row_index, col_index = spot
    return f"{row_index}_{col_index}"


def has_up(
    garden: List[List[str]], spot: Tuple[int, int], region: str, cache: dict
) -> Optional[Tuple[int, int]]:
    row_index, col_index = spot
    up = (row_index - 1, col_index)
    key = get_key(up)
    return (
        up
        if check_bounds(garden, up)
        and garden[up[0]][up[1]] == region
        and key not in cache
        else None
    )


def has_down(
    garden: List[List[str]], spot: Tuple[int, int], region: str, cache: dict
) -> Optional[Tuple[int, int]]:
    row_index, col_index = spot
    down = (row_index + 1, col_index)
    key = get_key(down)
    return (
        down
        if check_bounds(garden, down)
        and garden[down[0]][down[1]] == region
        and key not in cache
        else None
    )


def has_left(
    garden: List[List[str]], spot: Tuple[int, int], region: str, cache: dict
) -> Optional[Tuple[int, int]]:
    row_index, col_index = spot
    left = (row_index, col_index - 1)
    key = get_key(left)
    return (
        left
        if check_bounds(garden, left)
        and garden[left[0]][left[1]] == region
        and key not in cache
        else None
    )


def has_right(
    garden: List[List[str]], spot: Tuple[int, int], region: str, cache: dict
) -> Optional[Tuple[int, int]]:
    row_index, col_index = spot
    right = (row_index, col_index + 1)
    key = get_key(right)
    return (
        right
        if check_bounds(garden, right)
        and garden[right[0]][right[1]] == region
        and key not in cache
        else None
    )


def find_all_contiguous(
    garden: List[List[str]], spot: Tuple[int, int], region: str, cache: dict
) -> Dict[str, Tuple[int, int]]:
    up = has_up(garden, spot, region, cache)
    if up is not None:
        cache[get_key(up)] = up
        find_all_contiguous(garden, up, region, cache)

    down = has_down(garden, spot, region, cache)
    if down is not None:
        cache[get_key(down)] = down
        find_all_contiguous(garden, down, region, cache)

    left = has_left(garden, spot, region, cache)
    if left is not None:
        cache[get_key(left)] = left
        find_all_contiguous(garden, left, region, cache)

    right = has_right(garden, spot, region, cache)
    if right is not None:
        cache[get_key(right)] = right
        find_all_contiguous(garden, right, region, cache)


def get_all_of_region(
    garden: List[List[str]], region: str
) -> List[List[Tuple[int, int]]]:
    contiguous: Dict[str, int] = {}
    hold_region = []
    for row_index, row in enumerate(garden):
        for col_index, element in enumerate(row):
            spot = (row_index, col_index)
            key = get_key(spot)
            if element == region and not key in contiguous:
                local = {key: spot}
                find_all_contiguous(garden, spot, region, local)
                hold_region.append(list(local.values()))
                contiguous.update(local)
    return hold_region


def get_sum_of_price(garden: List[List[str]], regions: Dict[str, int]) -> int:
    total_sum = 0
    for key, value in regions.items():
        areas_of_region = get_all_of_region(garden, key)
        for area in areas_of_region:
            total_fence_area = 0
            for spot in area:
                total_fence_area += element_has_border(garden, key, spot)
            total_sum += total_fence_area * len(
                area
            )  # total number of spots is the acreage

    return total_sum


def is_corner(node1: Tuple[int, int], node2: Tuple[int, int]) -> int:
    row_index1, col_index1 = node1
    row_index2, col_index2 = node2

    if row_index1 != row_index2 and col_index1 != col_index2:
        return 1
    return 0


def get_linkages(
    border: List[Tuple[str, str, Tuple[int, int], Tuple[int, int]]]
) -> int:
    num_corner = 0
    ## naive for loop, but should be small enough to not matter
    for index, (key1, key2, node1, node2) in enumerate(border):
        next_key2 = ""
        upper = index + 1
        lower = index - 1
        while next_key2 != key1:  # get "closest" match
            upper_index = upper % len(border)
            lower_index = lower % len(border)
            next_key1, next_key2, next_node1, next_node2 = border[upper_index]

            if key1 == next_key2:
                num_corner += is_corner(next_node1, node2)
                break

            next_key1, next_key2, next_node1, next_node2 = border[lower_index]
            if key1 == next_key2:
                num_corner += is_corner(next_node1, node2)
                break

            upper += 1
            lower -= 1
    return num_corner


def get_sum_of_price_straight_lines(
    garden: List[List[str]], regions: Dict[str, int]
) -> int:
    total_sum = 0
    for key, value in regions.items():
        areas_of_region = get_all_of_region(garden, key)
        for area in areas_of_region:
            border = []
            for spot in area:
                get_element_borders(garden, key, spot, border)

            total_sum += get_linkages(border) * len(
                area
            )  # total number of spots is the acreage
    return total_sum


if __name__ == "__main__":
    test_garden = load_from_file("day12_input_example.txt")
    test_regions = extract_unique_regions_and_area(test_garden)
    print(get_sum_of_price(test_garden, test_regions))  # should be 1930

    garden = load_from_file("day12_input.txt")
    regions = extract_unique_regions_and_area(garden)
    print(get_sum_of_price(garden, regions))

    # part 2

    print(get_sum_of_price_straight_lines(test_garden, test_regions))  # should be 1206

    print(
        get_sum_of_price_straight_lines(garden, regions)
    )  # 812370 is too high,  802635 is too low 812370
