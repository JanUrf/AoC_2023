from pathlib import Path
# array indices
src_start = 0
src_end = 1
dest_start = 2
dest_end = 3
offset = 4

def parse_input(file_path: Path) -> (list, dict):

    with open(file_path, 'r') as f:
        data = f.read().split("\n\n")
        seeds = [int(x) for x in data[0].split(":")[1].split()]
        maps = {}
        
        # create maps 
        # [source_start source_end dest_start dest_end offset]
        for map in data[1:]:
            parsed_rules = []
            
            map = map.split(" map:\n")
            name = map[0]
            rules = map[1].split("\n")
            
            for rule in rules:
                tmp_rule = [int(x) for x in rule.split()]
                new_rule = [# source
                            tmp_rule[1], 
                            tmp_rule[1]+tmp_rule[2]-1,
                            # destination # not needed necessarily
                            tmp_rule[0],
                            tmp_rule[0]+tmp_rule[2]-1,
                            # offset
                            tmp_rule[0]-tmp_rule[1]]
                
                parsed_rules.append(new_rule)
                
            maps[name] = parsed_rules
            
    
    return (seeds, maps)

def calculate_dependency(src: int, knowledge: list)-> int:
    # calculate which destination value belongs to the source
    dest = src
    
    for rule in knowledge:
        if rule[src_start] <= src <= rule[src_end]:
            dest += rule[offset]
            break
    
    return dest

if __name__ ==  '__main__':
    seeds, knowledge_base = parse_input(Path("day5/input.txt"))
    locations = []
    result = []
    for seed in seeds:
        information_per_seed = {"seed": seed}
        # compute every information for a seed.
        # assumes correct order of maps
        for map_name in knowledge_base.keys():
            information_per_seed[map_name.split("-")[-1]] = calculate_dependency(information_per_seed[map_name.split("-")[0]], knowledge_base[map_name])
            pass
        result.append(information_per_seed)
        locations.append(information_per_seed["location"])
    print(min(locations))