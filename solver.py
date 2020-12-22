import string
import google_search
import wikipedia_search
import word_eliminator
import datamuse

'''
Solve takes information about grid and clues
Utilizes google, wikipedia and wordnet to find candidates to clues
Recursively inserts answers using depth-first approach
Returns solution with maximum filled squares
'''
def solve(  grid, across, down, grid_numbers, trace_mod=False):
    answer = [
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
    ]

    across_clue_lengths = get_clue_lengths(grid, grid_numbers, across, "across")
    down_clue_lengths = get_clue_lengths(grid, grid_numbers, down, "down")

    if trace_mod:
        print("Finding candidate list for across clues")
    across_candidate_lists = find_candidate_lists(across, across_clue_lengths, trace_mod)
    # across_blacklist = [i for i, clue in enumerate(across) if across[i][1][-1] == "?"]
    if trace_mod:
        print("Finding candidate list for down clues")
    down_candidate_lists = find_candidate_lists(down, down_clue_lengths, trace_mod)
    # down_blacklist = [i for i, clue in enumerate(down) if down[i][1][-1] == "?"]

    if trace_mod:
        print("Trying to fit candidates for clues")
    results = rec_insert(grid, grid_numbers, answer, across_candidate_lists, down_candidate_lists, False)

    if trace_mod:
        print("Finding answers with least empty cells")
    min_empty = empty_tile_number(grid, answer)
    for result in results:
        min_current = empty_tile_number(grid, result)
        if min_current < min_empty:
            min_empty = min_current
    count = 0
    best_results = []
    for result in results:
        if empty_tile_number(grid, result) == min_empty:
            best_results.append(result)
            count += 1
            if trace_mod:
                print("This is an alternative best result")
                for row in result:
                    print(row)
                print("------")
    if trace_mod:
        print("Answer found. Reporting...")
    if len(best_results) == 0:
        print(len(results), "answers found")
        return answer
    return best_results[0]

'''
Find and return candidate list for a set of clues
'''
def find_candidate_lists(clues, clue_lengths, trace_mod):
    candidate_lists = []
    for clue in clues:
        candidate_list = find_candidates(clue[1], clue_lengths[str(clue[0])], trace_mod)
        candidate_lists.append( (clue[0], candidate_list) )
        if trace_mod:
            print("Candidates for", clue)
            print(candidate_list)
    return candidate_lists

'''
Find candidates for a single clue with given length
Use google, wikipedia and wordnet
'''
def find_candidates(clue, length, trace_mod=False):
    if trace_mod:
        print("Finding possible candidates for the clue", clue)
    # search clue
    filtered_clue = word_eliminator.remove_escape_sequences(clue)
    filtered_clue = word_eliminator.eliminate_punctuation(filtered_clue.split(" "))
    filtered_clue = ' '.join(filtered_clue)
    if trace_mod:
        print("Searching google")
    google_results = google_search.search_google(filtered_clue, length)
    if len(google_results) > 100:
        google_results = google_results[:100]
    if trace_mod:
        print("Searching wikipedia")
    wikipedia_results = wikipedia_search.wikipedia_search(filtered_clue, length)
    if len(wikipedia_results) > 100:
        wikipedia_results = wikipedia_results[:100]
    if trace_mod:
        print("Searching wordnet")
    datamuse_results = datamuse.get_words_with_similar_meaning(clue, length)
    candidates_list = word_eliminator.stratified_merge(datamuse_results, google_results, wikipedia_results)
    candidates_list = word_eliminator.eliminate_duplicates(candidates_list)
    return candidates_list

'''
Find and return number of empty squares given grid geometry and filled squares
'''
def empty_tile_number(grid, current_grid):
    empty_no = 0
    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            if tile == 0 and current_grid[x][y] == ' ':
                empty_no += 1
    return empty_no

'''
Recursively insert given candidates using constraint satisfaction
Turn represents input direction (true => across, false => down)
'''
def rec_insert(grid, grid_numbers, current_grid, acro_cand_list, down_cand_list, turn):
    across_count = len(acro_cand_list) 
    down_count = len(down_cand_list)
    add_across = False
    add_down = False
    if across_count <= 0 and down_count <= 0:
        return [ [row[:] for row in current_grid] ]
    elif across_count > 0 and turn:
        add_across = True
    elif down_count > 0 and not turn:
        add_down = True
    elif across_count > 0:
        add_across = True
    elif down_count > 0:
        add_down = True

    possible_outcomes = []
    if add_across:
        next_across_tup = acro_cand_list[0]
        clue_no = next_across_tup[0]
        cand_list = next_across_tup[1]
        start, end = start_and_end(grid, grid_numbers, int(clue_no), "across")
        possible_branches = []
        if  len(cand_list) == 0:
            possible_branches = [ [row[:] for row in current_grid]]
        for candidate in cand_list:
            inserted = insert_to_grid(current_grid, start, end, candidate)
            if inserted is not None:
                if empty_tile_number(grid, inserted) == 0:
                    return [inserted]
                append_unique(possible_branches, inserted)
        
        for branch in possible_branches:
            outcomes = rec_insert(grid, grid_numbers, branch, acro_cand_list[1:], down_cand_list, not turn)
            for outcome in outcomes:
                append_unique(possible_outcomes, outcome)

    elif add_down:
        next_down_tup = down_cand_list[0]
        clue_no = next_down_tup[0]
        cand_list = next_down_tup[1]
        start, end = start_and_end(grid, grid_numbers, int(clue_no), "down")
        possible_branches = []
        if len(cand_list) == 0:
            possible_branches = [ [row[:] for row in current_grid] ]
        for candidate in cand_list:
            inserted = insert_to_grid(current_grid, start, end, candidate)
            if inserted is not None:
                if empty_tile_number(grid, inserted) == 0:
                    return [inserted]
                append_unique(possible_branches, inserted)
        
        for branch in possible_branches:
            outcomes = rec_insert(grid, grid_numbers, branch, acro_cand_list, down_cand_list[1:], not turn)
            for outcome in outcomes:
                append_unique(possible_outcomes, outcome)

    return possible_outcomes

'''
Insert a single word onto a given position
Return resulting grid if insert is succesful, None otherwise
'''
def insert_to_grid(current_grid, start, end, word):
    temp_grid = [row[:] for row in current_grid]
    x = start[0]
    y = start[1]
    while x <= end[0] and y <= end[1]:
        if start[0] == end[0]: # across
            if temp_grid[x][y] == " " or temp_grid[x][y] == word[y - start[1]]:
                temp_grid[x][y] = word[y - start[1]]
                y += 1
            else:
                return # Cannot insert
        elif start[1] == end[1]: # down
            if temp_grid[x][y] == " " or temp_grid[x][y] == word[x - start[0]]:
                temp_grid[x][y] = word[x - start[0]]
                x += 1
            else:
                return # Cannot insert
    return temp_grid

'''
Find and return clue lengths as a dictionary
Uses grid geometry and grid numbers information to determine length
'''
def get_clue_lengths(grid, grid_numbers, clues, direction):
    clue_lengths = {}
    for clue in clues:
        start, end = start_and_end(grid, grid_numbers, int(clue[0]), direction)
        length = 0
        if direction == "down":
            length = end[0] - start[0] + 1
        elif direction == "across":
            length = end[1] - start[1] + 1
        clue_lengths[clue[0]] = length
    return clue_lengths

'''
Find starting and ending position of a word in puzzle given clue no
'''
def start_and_end(grid, grid_numbers, clue_no, direction):
    starting_pos = start_position(grid_numbers, clue_no)
    ending_pos = end_position(grid, starting_pos, direction) 
    return starting_pos, ending_pos

def start_position(grid_numbers, clue_no):
    for x in range(5):
        for y in range(5):
            if int(grid_numbers[x][y]) == int(clue_no):
                return (x, y)

def end_position(grid, start_pos, direction):
    x = start_pos[0]
    y = start_pos[1]
    if direction == "across":
        while y < 4 and grid[x][y + 1] != 1:
            y += 1
    elif direction == "down":
        while x < 4 and grid[x + 1][y] != 1:
            x += 1
    return (x, y)    

'''
Append target element to append_to list only if it is not already in the list 
'''
def append_unique(append_to, target):
    if target not in append_to:
        append_to.append(target)
