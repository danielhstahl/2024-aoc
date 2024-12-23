from typing import List
from copy import deepcopy

TEST_INPUT = ["125", "17"]
ACTUAL_INPUT = ["0", "7", "6618216", "26481", "885", "42", "202642", "8791"]

# If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
# The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone.
# (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.


def apply_rules(stone: str) -> List[str]:
    if stone == "0":
        return ["1"]
    stone_length = len(stone)
    if stone_length % 2 == 0:
        mid_point = stone_length // 2
        return [stone[:mid_point], str(int(stone[mid_point:]))]
    return [str(int(stone) * 2024)]


def iterate_stone(stones: List[str]) -> List[str]:
    next_stones = deepcopy(stones)
    next_index = 0
    for stone in stones:
        new_stone_set = apply_rules(stone)
        split_next = next_stones[:next_index]
        split_next.extend(new_stone_set)
        next_stones = split_next + next_stones[next_index + 1 :]
        next_index += len(new_stone_set)

    return next_stones


## THIS IS WAY FASTER
def iterate_stone_mem_efficient(stones: List[str]):
    n = len(stones)
    for i in range(n):
        new_stone_set = apply_rules(stones[i])
        if len(new_stone_set) == 1:
            stones[i] = new_stone_set[0]
        else:
            stones[i] = new_stone_set[0]
            stones.append(new_stone_set[1])  # shouldn't matter where it lands
    # return next_stones


def keep_blinking(stones: List[str], num_blinks: int) -> List[str]:
    new_stones = deepcopy(stones)
    for i in range(num_blinks):
        iterate_stone_mem_efficient(new_stones)

    return new_stones


def do_one_stone_at_a_time(stone: str, cache: dict, limit: int) -> int:
    if stone in cache:
        return cache[stone]  # array
    stones = [stone]
    for i in range(limit):
        iterate_stone_mem_efficient(stones)

    cache[stone] = stones
    return stones


def split_blinking_one_at_a_time(stones: List[str]) -> int:
    total_sum = 0
    cache = {}
    for index, stone in enumerate(stones):
        print("iteration", index)
        result = do_one_stone_at_a_time(stone, cache, 25)
        for sub_index, stone in enumerate(result):
            result = do_one_stone_at_a_time(stone, cache, 25)
            for stone in result:
                total_sum += len(do_one_stone_at_a_time(stone, cache, 25))

    return total_sum


if __name__ == "__main__":
    print(
        len(keep_blinking(TEST_INPUT, 25))
    )  # should be 55312, but this took a while to calculate...

    print(len(keep_blinking(ACTUAL_INPUT, 25)))  # 213625

    # part 2

    # this runs out of memory
    # print(len(keep_blinking(ACTUAL_INPUT, 75)))

    # this does each 25 at a time.
    # but shouldln't run out of memory
    print(split_blinking_one_at_a_time(ACTUAL_INPUT))
