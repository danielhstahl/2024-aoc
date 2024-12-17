## This is my favorite answer...the python code is super clean
## The "correctness" of the code is obvious
## the creation of wrapper functions made it easy to swap
## operators in and out
from typing import List, Tuple
from itertools import product


def load_from_file(file_name: str) -> List[Tuple[int, List[int]]]:
    values = []
    with open(file_name, newline="\n") as file:
        for row in file.readlines():
            cleaned = row.strip()
            answer, numbers = cleaned.split(":")
            values.append(
                (int(answer), [int(number) for number in numbers.strip().split(" ")])
            )
    return values


def _local_sum(a: int, b: int) -> int:
    return a + b


def _local_mult(a: int, b: int) -> int:
    return a * b


def _local_concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def get_all_permutations_of_mult_and_add(n: int):
    return product([_local_sum, _local_mult], repeat=n)  # this should be a generator


def get_all_permutations_of_mult_and_add_and_combine(n: int):
    return product(
        [_local_sum, _local_mult, _local_concat], repeat=n
    )  # this should be a generator


def can_equal_answer(
    equation: Tuple[int, List[int]],
    permutation_generator=get_all_permutations_of_mult_and_add,
) -> bool:
    answer, values = equation
    for permutation in permutation_generator(len(values) - 1):
        possible_answer = values[0]
        for index, v in enumerate(values[1:]):
            possible_answer = permutation[index](possible_answer, v)
        if answer == possible_answer:
            return True

    return False


def get_all_answers(
    equations: List[Tuple[int, List[int]]],
    permutation_generator=get_all_permutations_of_mult_and_add,
) -> int:
    return sum(
        equation[0]
        for equation in equations
        if can_equal_answer(equation, permutation_generator)
    )


if __name__ == "__main__":
    test_inputs = load_from_file("day7_input_example.txt")
    print(get_all_answers(test_inputs))  # should equal 3749

    inputs = load_from_file("day7_input.txt")
    print(get_all_answers(inputs))  #

    # part 2
    print(
        get_all_answers(test_inputs, get_all_permutations_of_mult_and_add_and_combine)
    )  # should equal 11387
    print(get_all_answers(inputs, get_all_permutations_of_mult_and_add_and_combine))
