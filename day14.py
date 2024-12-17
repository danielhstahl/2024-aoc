from typing import List, Tuple, Optional, Dict

def load_from_file(file_name: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    values = []
    with open(file_name, newline="\n") as file:
        for row in file.readlines():
            cleaned = row.strip()
            p, v=cleaned.split(" ")
            p=p.replace("p=", "")
            start=p.split(",")
            start_point=(int(start[0]), int(start[1]))
            v=v.replace("v=", "")
            vel=v.split(",")
            velocity=(int(vel[0]), int(vel[1]))
            values.append((start_point, velocity))

    return values

def get_single_dimension_modulo(start: int, velocity: int, dimension:int, steps:int)->int:
    return (start+steps*velocity) % dimension

def get_position_after_n_steps(init_pos_and_vel:Tuple[Tuple[int, int], Tuple[int, int]], dimensions: Tuple[int, int], num_steps:int)->Tuple[int, int]:
    start, velocity=init_pos_and_vel
    return (get_single_dimension_modulo(start[0], velocity[0], dimensions[0], num_steps), get_single_dimension_modulo(start[1], velocity[1], dimensions[1], num_steps))

def get_all_final_positions(all_guards: List[Tuple[Tuple[int, int], Tuple[int, int]]], dimensions:Tuple[int, int], num_steps:int)->List[Tuple[int, int]]:
    results=[]
    for guard in all_guards:
        results.append(get_position_after_n_steps(guard, dimensions, num_steps))
    return results

def get_final_score(final_positions: List[Tuple[int, int]], dimensions: Tuple[int, int])->int:
    midpoint_row=dimensions[0]//2
    midpoint_col=dimensions[1]//2
    quadrant=[0, 0, 0, 0]
    for position in final_positions:
        row, col=position
        if row<midpoint_row and col<midpoint_col:
            quadrant[0]+=1
        elif row>midpoint_row and col>midpoint_col:
            quadrant[3]+=1
        elif row>midpoint_row and col<midpoint_col:
            quadrant[2]+=1  
        elif row<midpoint_row and col>midpoint_col:
            quadrant[1]+=1  
    total_prod=1
    for quad in quadrant:
        total_prod*=quad

    return total_prod 


def variance(x:List[int])->float:
    v=0
    for item in x:
        v+=item*item
    return v/len(x)

def get_variance_of_coordinates(positions:List[Tuple[int, int]])->Tuple[float, float]:
    x_positions=[pos[0] for pos in positions]
    y_positions=[pos[1] for pos in positions]
    return variance(x_positions), variance(y_positions)

def print_ascii_art(positions: List[Tuple[int, int]], dimensions:Tuple[int, int]):
    string_pos=[f"{pos[0]}_{pos[1]}" for pos in positions]
    for i in range(dimensions[0]):
        str_to_print=""
        for j in range(dimensions[1]):
            if f"{i}_{j}" in string_pos:
                str_to_print+="*"
            else:
                str_to_print+="."
        print(str_to_print)

def get_cluster_of_coordinates(positions: List[Tuple[int, int]], dimensions:Tuple[int, int])->int:
    string_pos=[f"{pos[0]}_{pos[1]}" for pos in positions]
    cluster=0
    for i in range(dimensions[0]//2-10, dimensions[0]//2+10):
        for j in range(dimensions[1]//2-10, dimensions[1]//2+10):
            if f"{i}_{j}" in string_pos:
                cluster+=1
    return cluster

def get_christmas_tree(all_guards: List[Tuple[Tuple[int, int], Tuple[int, int]]], dimensions:Tuple[int, int])->int:
    i=1
    total_cluster=0
    while total_cluster<65:
        positions=get_all_final_positions(all_guards, dimensions, i)
        total_cluster=get_cluster_of_coordinates(positions, dimensions)
        
        i+=1
    print(total_cluster)
    print_ascii_art(positions, dimensions)
    return i-1

if __name__=="__main__":
    test_values=load_from_file("day14_input_example.txt")
    test_dimensions=(11, 7)
    test_positions=get_all_final_positions(test_values,test_dimensions, 100)
    print(get_final_score(test_positions, test_dimensions)) # should be 12

    values=load_from_file("day14_input.txt")
    dimensions=(101, 103)
    positions=get_all_final_positions(values,dimensions, 100)
    print(get_final_score(positions, dimensions)) # 231782040

    # part 2...WHAT
    print(get_christmas_tree(values, dimensions))