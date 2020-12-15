import string
from nltk.corpus import stopwords

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

def solve(  grid, across, down, grid_numbers):
    answer = [
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
    ]
    across_clue_lengths = get_clue_lengths(grid, grid_numbers, across, "across")
    down_clue_lengths = get_clue_lengths(grid, grid_numbers, down, "down")

    print(across_clue_lengths)
    print(down_clue_lengths)

    return answer

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

solve(SOLUTION["grid"], SOLUTION["across"], SOLUTION["down"], SOLUTION["grid_numbers"])
