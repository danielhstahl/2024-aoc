from typing import List, Tuple, Optional

BUTTON_A_COST = 3
BUTTON_B_COST = 1


def load_from_file(file_name: str) -> List[Tuple[List[int], List[int], List[int]]]:
    values = []
    with open(file_name, newline="\n") as file:
        button_a = []
        button_b = []
        prize = []
        for row in file.readlines():
            cleaned = row.strip()
            if "Button A: " in cleaned:
                record = cleaned.replace("Button A: ", "")
                record = record.replace("X+", "")
                record = record.replace("Y+", "").strip()
                result = record.split(",")
                button_a = [int(result[0]), int(result[1])]
            elif "Button B: " in cleaned:
                record = cleaned.replace("Button B: ", "")
                record = record.replace("X+", "")
                record = record.replace("Y+", "").strip()
                result = record.split(",")
                button_b = [int(result[0]), int(result[1])]
            elif "Prize: " in cleaned:
                record = cleaned.replace("Prize: ", "")
                record = record.replace("X=", "")
                record = record.replace("Y=", "").strip()
                result = record.split(",")
                prize = [int(result[0]), int(result[1])]
            else:
                values.append((button_a, button_b, prize))
                button_a = []
                button_b = []
                prize = []
        values.append((button_a, button_b, prize))

    return values


def find_a_solution(
    button_a: List[int], button_b: List[int], prize: List[int]
) -> List[int]:
    c = button_a[0] / button_a[1]
    x2 = (prize[0] - prize[1] * c) / (button_b[0] - button_b[1] * c)
    x1 = (prize[0] - button_b[0] * x2) / button_a[0]
    return [x1, x2]


def is_int_the_same_result(
    button_a: List[int], button_b: List[int], solution: List[int], prize: List[int]
) -> bool:
    result = [
        button_a[0] * solution[0] + button_b[0] * solution[1],
        button_b[1] * solution[1] + button_a[1] * solution[0],
    ]
    return result[0] == prize[0] and result[1] == prize[1]


def is_solution_viable(
    button_a: List[int], button_b: List[int], solution: List[int], prize: List[int]
) -> Optional[List[int]]:
    result = []
    for item in solution:
        rounded = round(item)
        result.append(rounded)
        if item < 0:
            return None

    if not is_int_the_same_result(button_a, button_b, result, prize):
        return None
    return result


def get_cost(solution: List[int]) -> int:
    return solution[0] * BUTTON_A_COST + solution[1] * BUTTON_B_COST


def total_cost(games: List[Tuple[List[int], List[int], List[int]]]) -> int:
    cost = 0
    for game in games:
        result = is_solution_viable(
            game[0], game[1], find_a_solution(game[0], game[1], game[2]), game[2]
        )
        if result is not None:
            cost += get_cost(result)
    return cost


def adjust_games(
    games: List[Tuple[List[int], List[int], List[int]]]
) -> List[Tuple[List[int], List[int], List[int]]]:
    result = []
    for game in games:
        result.append(
            (
                game[0],
                game[1],
                [10000000000000 + game[2][0], 10000000000000 + game[2][1]],
            )
        )
    return result


if __name__ == "__main__":

    test_games = load_from_file("day13_input_example.txt")

    print(total_cost(test_games))

    games = load_from_file("day13_input.txt")

    print(total_cost(games))  # 34393

    ## Part 2

    test_games_altered = adjust_games(test_games)

    print(total_cost(test_games_altered))

    games_altered = adjust_games(games)
    print(
        total_cost(games_altered)
    )  # 157129151042201 is too high.  152358926517456 is too high.  83923072196853 is too high.  43318609967763 is "not right" 83551068361379
