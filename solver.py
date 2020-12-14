import string
from nltk.corpus import stopwords

def solve(  grid, across, down, grid_numbers):
    answer = [
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
    ]
    return answer

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
