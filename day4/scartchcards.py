from pathlib import Path

def parse_input(file_path: Path) -> (list,list):
    winning_numbers = []
    my_numbers =  []
    with open(file_path, 'r') as f:
        for line in f:
            #removes the "Card x:"
            data = line.rstrip().split(":")[1]
            
            numbers = data.split("|")
            winning_numbers.append(set([int(x) for x in numbers[0].split()]))
            my_numbers.append(set([int(x) for x in numbers[1].split()]))
            
    return (winning_numbers, my_numbers)

def calculate_points(winning_numbers: list[set], my_numbers: list[set]) -> list:
    points = []
    for card_i in range(len(winning_numbers)):
        # calculate intersection
        matches = winning_numbers[card_i].intersection(my_numbers[card_i])
        # double the points depending on number of matches
        if len(matches) == 0:
            points.append(0)
        else:
            points.append(2 ** (len(matches)-1))

    return points

if __name__ ==  '__main__':
    (winning_numbers, my_numbers) = parse_input(Path("day4/input.txt"))
    points = calculate_points(winning_numbers, my_numbers)
    print("points: ", sum(points))