from typing import List, Tuple, Dict
from functools import cmp_to_key


## Rules maps "after" items to "before" items
def is_order_correct(numbers: List[int], rules: Dict[int, List[int]]) -> bool:
    for index, number in enumerate(numbers):
        if number in rules:
            numbers_to_come_before = rules[number]
            for future_number in numbers[index:]:
                if future_number in numbers_to_come_before:
                    return False

    return True


def _sort_fn(item1: int, item2: int, rules: Dict[int, List[int]]):
    if item2 in rules:
        if item1 in rules[item2]:
            return -1
        else:
            return 1
    return 0


# part 2 function
def correct_out_of_order(numbers: List[int], rules: Dict[int, List[int]]) -> List[int]:
    return sorted(
        numbers, key=cmp_to_key(lambda item1, item2: _sort_fn(item1, item2, rules))
    )


def get_middle_index(numbers: List[int]) -> int:
    return numbers[len(numbers) // 2]


def get_map_of_rules(rule_strings: List[str]) -> Dict[int, List[int]]:
    dict_of_rules: Dict[int, List[int]] = {}
    for rule_string in rule_strings:
        before_str, after_str = rule_string.split("|")
        before = int(before_str)
        after = int(after_str)
        if after in dict_of_rules:
            dict_of_rules[after].append(before)
        else:
            dict_of_rules[after] = [before]

    return dict_of_rules


def get_middle_sum(number_array: List[List[int]], rule_strings: List[str]) -> int:
    rules = get_map_of_rules(rule_strings)

    return sum(
        get_middle_index(numbers)
        for numbers in number_array
        if is_order_correct(numbers, rules)
    )


def get_middle_sum_part_two(
    number_array: List[List[int]], rule_strings: List[str]
) -> int:
    rules = get_map_of_rules(rule_strings)
    return sum(
        get_middle_index(correct_out_of_order(numbers, rules))
        for numbers in number_array
        if not is_order_correct(numbers, rules)
    )


def load_from_file(file_name: str) -> Tuple[List[str], List[List[int]]]:
    rule_strings = []
    number_array = []
    is_rule_section = True
    with open(file_name, newline="\n") as file:
        for row in file.readlines():
            cleaned = row.strip()
            if cleaned == "":
                is_rule_section = False
            elif is_rule_section:
                rule_strings.append(cleaned)
            else:
                number_array.append([int(item) for item in cleaned.split(",")])
    return rule_strings, number_array


if __name__ == "__main__":
    rule_strings_test, number_array_test = load_from_file("day5_input_example.txt")

    print(get_middle_sum(number_array_test, rule_strings_test))  # should be 143

    rule_strings, number_array = load_from_file("day5_input.txt")

    print(get_middle_sum(number_array, rule_strings))

    # Part 2
    print(
        get_middle_sum_part_two(number_array_test, rule_strings_test)
    )  # should be 123

    print(get_middle_sum_part_two(number_array, rule_strings))
