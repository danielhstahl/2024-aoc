from typing import List


def compute_sum_of_distance(list1: List[int], list2: List[int]) -> int:
    list1.sort()
    list2.sort()
    total_distance = 0
    for item1, item2 in zip(list1, list2):
        total_distance += abs(item1 - item2)
    return total_distance


def compute_similarity_score(list1: List[int], list2: List[int]) -> int:
    frequency_map = {}
    for element in list2:
        if element in frequency_map:
            frequency_map[element] += 1
        else:
            frequency_map[element] = 1
    total_similarity = 0
    for element in list1:
        if element in frequency_map:
            total_similarity += element * frequency_map[element]

    return total_similarity


#
# 3   4
# 4   3
# 2   5
# 1   3
# 3   9
# 3   3


if __name__ == "__main__":
    list1 = [3, 4, 2, 1, 3, 3]
    list2 = [4, 3, 5, 3, 9, 3]
    print(compute_sum_of_distance(list1, list2))  ## should be 11
    print(compute_similarity_score(list1, list2))  ## should be 31
    import csv

    list1 = []
    list2 = []
    with open("day1_1_input.txt", newline="\n") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in spamreader:
            list1.append(int(row[0]))
            list2.append(int(row[3]))

    print(compute_sum_of_distance(list1, list2))
    print(compute_similarity_score(list1, list2))
