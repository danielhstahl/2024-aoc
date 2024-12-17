from typing import List
import re


def extract_true_mult(code: str) -> List[str]:
    return re.findall(r"mul\([\d]+,[\d]+\)", code)


def do_mult(mult_items: List[str]) -> int:
    total_mult = 0
    for item in mult_items:
        num1, num2 = item.replace("mul(", "").replace(")", "").split(",")
        total_mult += int(num1) * int(num2)

    return total_mult


def remove_strings_between_dont(code: str) -> str:
    index = 0
    while index is not None:
        try:
            index = code.index("don't()", index)
            try:
                index_do = code.index("do()", index)
            except:
                index_do = len(code)
            # 4 is length of do()
            code = code[:index] + code[index_do + 4 :]
        except:
            index = None

    return code


if __name__ == "__main__":
    print(
        do_mult(
            extract_true_mult(
                "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
            )
        )
    )  # should be 161

    ## part 1
    result = ""
    with open("day3_input.txt", newline="\n") as file:
        result = file.read()
    print(do_mult(extract_true_mult(result)))

    # part 2

    print(
        do_mult(
            extract_true_mult(
                remove_strings_between_dont(
                    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
                )
            )
        )
    )  # should be 48

    result = ""
    with open("day3_input.txt", newline="\n") as file:
        result = file.read()
    print(do_mult(extract_true_mult(remove_strings_between_dont(result))))
