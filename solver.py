import ssl
import string
from nltk.corpus import stopwords
from nltk.probability import log_likelihood
import google_search
import wikipedia_search
import word_eliminator
import datamuse

SOLUTION = {
    "date": "Thursday, November 5, 2020", 
    "grid": [   [1, 1, 0, 0, 0], 
                [0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0], 
                [0, 0, 0, 1, 1] ], 
    "grid_numbers": [   [0, 0, "1", "2", "3"], 
                        ["4", "5", 0, 0, 0], 
                        ["6", 0, 0, 0, 0], 
                        ["7", 0, 0, 0, 0], 
                        ["8", 0, 0, 0, 0]  ], 
    "answer": [ [" ", " ", "T", "A", "B"], 
                ["S", "M", "I", "L", "E"], 
                ["K", "A", "P", "P", "A"], 
                ["I", "T", "S", "O", "N"], 
                ["S", "H", "Y", " ", " "]], 
    "across": [ ["1", "Running total at a bar"], 
                ["4", "Photographer's request"],
                ["6", "Greek \"K\""], 
                ["7", "\"Oh, you wanna go? Let's go!\""], 
                ["8", "Bashful"]], 
    "down": [   ["1", "A little drunk"], 
                ["2", "Purina dog food brand"], 
                ["3", "Word after jelly or coffee"], 
                ["4", "Sports equipment with which you can do a \"pizza stop\""], 
                ["5", "Class that has its pluses and minuses"]]
}

def solve(  grid, across, down, grid_numbers, puzzle):
    answer = [
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
    ]
    across_clue_lengths = get_clue_lengths(grid, grid_numbers, across, "across")
    down_clue_lengths = get_clue_lengths(grid, grid_numbers, down, "down")
    across_candidate_lists = find_candidate_lists(across, across_clue_lengths)
    down_candidate_lists = find_candidate_lists(down, down_clue_lengths)

    across_candidates_list = [
            (1, ["TAB"]),
            (4, ["SMILE"]),
            (6, ["KAPPA"]),
            (7, ["ITSON"]),
            (8, ["SHY", "CRY", "BAD"])
            ]
    down_candidates_list = [ 
        (4, ["SKIS"]),
        (5, ["MATH"]),
        (1, ["ABCDY", "1234Y", "ABOUT", "TIPSY"]),
        (2, ["ALPO"]),
        (3, ["BEAN"])
        ]

    results = insert_clues(grid, grid_numbers, answer, across_candidate_lists, down_candidate_lists)
    for result in results:
        for row in result:
            print(row)
        print("------")
    print(len(results))

    return answer

def find_candidate_lists(clues, clue_lengths):
    candidate_lists = []
    for clue in clues:
        print("Finding answers for clue", clue[1], "length", clue_lengths[str(clue[0])])
        candidate_list = find_candidates(clue[1], clue_lengths[str(clue[0])])
        print(candidate_list)
        candidate_lists.append( (clue[0], candidate_list) )
    return candidate_lists

def find_candidates(clue, length):
    candidates_list = []
    # search clue
    filtered_clue = word_eliminator.remove_escape_sequences(clue)
    google_results = google_search.search_google(filtered_clue, length)
    candidates_list.extend(google_results)
    wikipedia_results = wikipedia_search.wikipedia_search(filtered_clue, length)
    candidates_list.extend(wikipedia_results)
    datamuse_results = datamuse.get_words_with_similar_meaning(clue)
    candidates_list.extend(datamuse_results)
    candidates_list = word_eliminator.eliminate_duplicates(candidates_list)
    return candidates_list

def insert_clues(grid, grid_numbers, current_grid, across_candidates_list, down_candidates_list):
    across_count = len(across_candidates_list) - 1
    down_count = len(down_candidates_list) - 1
    possible_answers = [ [row[:] for row in current_grid] ]
    while across_count >= 0 and down_count >= 0:
        next_across = across_candidates_list[across_count]
        start_acc, end_acc = start_and_end(grid, grid_numbers, int(next_across[0]), "across")
        current_findings = []
        for possible_answer in possible_answers:
            append_unique(current_findings, possible_answer)
            for candidate in next_across[1]:
                try_to_insert = insert_to_grid(possible_answer, start_acc, end_acc, candidate)
                if try_to_insert is not None:
                    append_unique(current_findings, try_to_insert)
        across_count -= 1
        possible_answers = current_findings
        current_findings = []
        next_down = down_candidates_list[down_count]
        start_dwn, end_dwn = start_and_end(grid, grid_numbers, int(next_down[0]), "down")
        for possible_answer in possible_answers:
            append_unique(current_findings, possible_answer)
            for candidate in next_down[1]:
                try_to_insert = insert_to_grid(possible_answer, start_dwn, end_dwn, candidate)
                if try_to_insert is not None:
                    append_unique(current_findings, try_to_insert)
        down_count -= 1
        possible_answers = current_findings

    # If left
    while across_count >= 0:
        next_across = across_candidates_list[across_count]
        start_acc, end_acc = start_and_end(grid, grid_numbers, int(next_across[0]), "across")
        current_findings = []
        for possible_answer in possible_answers:
            append_unique(current_findings, possible_answer)
            for candidate in next_across[1]:
                try_to_insert = insert_to_grid(possible_answer, start_acc, end_acc, candidate)
                if try_to_insert is not None:
                    append_unique(current_findings, try_to_insert)
        across_count -= 1
        possible_answers = current_findings

    while down_count >= 0:
        next_across = across_candidates_list[across_count]
        start_acc, end_acc = start_and_end(grid, grid_numbers, int(next_across[0]), "across")
        current_findings = []
        for possible_answer in possible_answers:
            append_unique(current_findings, possible_answer)
            for candidate in next_across[1]:
                try_to_insert = insert_to_grid(possible_answer, start_acc, end_acc, candidate)
                if try_to_insert is not None:
                    append_unique(current_findings, try_to_insert)
        across_count -= 1
        possible_answers = current_findings
    
    return possible_answers

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

def start_and_end(grid, grid_numbers, clue_no, direction):
    starting_pos = start_position(grid_numbers, clue_no)
    ending_pos = end_position(grid, starting_pos, direction) 
    return starting_pos, ending_pos

def start_position(grid_numbers, clue_no):
    for x in range(5):
        for y in range(5):
            if int(grid_numbers[x][y]) == clue_no:
                return (x, y)

def end_position(grid, start_position, direction):
    x = start_position[0]
    y = start_position[1]
    if direction == "across":
        while y < 4 and grid[x][y + 1] != 1:
            y += 1
    elif direction == "down":
        while x < 4 and grid[x + 1][y] != 1:
            x += 1
    return (x, y)    

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def remove_punctuation(inputString):
    return inputString.translate(str.maketrans('', '', string.punctuation))

def process_list(input_list):
    unique_words = set(input_list) # remove duplicates
    words_without_punc = [remove_punctuation(x) for x in unique_words]
    short_words = [x for x in words_without_punc if len(x) <= 5 and len(x) > 1] # find all words with less than or equal to 5 characters
    none_number_words = [x for x in short_words if not has_numbers(x)]
    none_stop_words = [x for x in none_number_words if x not in stopwords.words('english')] # remove stop-words
    result_words = [x.lower() for x in none_stop_words]
    return result_words

def append_unique(append_to, target):
    if target not in append_to:
        append_to.append(target)

#solve(SOLUTION["grid"], SOLUTION["across"], SOLUTION["down"], SOLUTION["grid_numbers"])
