import numpy as np
import numpy.typing as npt
import sys

from pathlib import Path
from itertools import product, groupby

#for debugging
np.set_printoptions(threshold=sys.maxsize)

input_shape = (140, 140)

def calculate_neighbours(iy: int, ix: int)-> list:
    # crop the boarders
    if iy == 0:
        range_y = [iy, iy+1]
    elif iy == input_shape[1]-1:
        range_y = [iy-1, iy]
    else:
        range_y = [iy-1, iy ,iy+1]
        
    if ix == 0:
        range_x = [ix, ix+1]
    elif ix == input_shape[0]-1:
        range_x = [ix-1, ix]
    else:
        range_x = [ix-1, ix ,ix+1]
    
    return product(range_y,range_x)

def parse_input(file_path: Path) -> npt.NDArray:
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append([None if cell == '.' else cell for cell in line.rstrip()])
            
    return np.array(data)
            
def create_mask(data: npt.NDArray)-> npt.NDArray:
    mask = np.copy(data)
    mask.fill(0)
    for iy, ix in np.ndindex(data.shape):
        # mark neighbours for every cell which hasn't a value
        if data[iy][ix] is not None and not data[iy][ix].isnumeric():
            neighbours = calculate_neighbours(iy, ix)
            for x in neighbours:
                mask[x] = 1
                
    return mask
    
def create_numbers(schema: npt.NDArray)-> npt.NDArray:
    values = np.zeros(schema.shape, dtype=int)
    number_digits=0
    for iy, ix in np.ndindex(schema.shape):
        
        # the number has already encountered in some previous digit.
        if number_digits > 0:
            number_digits -= 1
            # set every digit of the original to its number value
            values[iy][ix] = int(number)
            continue
        
        # get number
        if schema[iy][ix] and schema[iy][ix].isnumeric():
            number = ''
            while schema[iy][ix+number_digits] and schema[iy][ix+number_digits].isnumeric():
                number += schema[iy][ix+number_digits]
                if ix+number_digits < input_shape[1]-1:
                    number_digits += 1
                else:
                    # end of line
                    number_digits += 1
                    break
                
            #store number in first digit cell
            values[iy][ix] = int(number)
            
            number_digits -= 1

    return values

def correct_parts(parts: npt.NDArray) ->npt.NDArray:
    previous_number = 0
    for iy, ix in np.ndindex(parts.shape):
        if ix == 0:
            #reset each line
            previous_number = 0
            
        if parts[iy][ix] == previous_number:
            parts[iy][ix] = 0
        else:
            previous_number = parts[iy][ix]
    return parts


if __name__ ==  '__main__':
    engine_schematic = parse_input(Path("day3/input.txt"))
    mask = create_mask(engine_schematic)
    numbers = create_numbers(engine_schematic)
    parts = np.multiply(mask, numbers)
    # correction if character hit multiple digits
    parts = correct_parts(parts)
    #print(engine_schematic)
    #print(mask)
    #print(numbers)
    print(np.sum(parts))
    
    