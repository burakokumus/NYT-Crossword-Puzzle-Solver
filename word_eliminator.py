import string
import nltk
from nltk.corpus import stopwords

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)

def eliminate_duplicates(word_list):
    return list(set(word_list))

def eliminate_punctuation(word_list):
    return [s.translate(str.maketrans('', '', string.punctuation)) for s in word_list]

def eliminate_long_or_short_words(word_list, word_length):
    return [word for word in word_list if len(word) == word_length] 

def eliminate_numbers(word_list):
    return [word for word in word_list if not has_numbers(word)]

def eliminate_stop_words(word_list):
    return [word for word in word_list if word not in stopwords.words('english')]

def to_upper_case(word_list):
    return [x.upper() for x in word_list]

def filter_words(word_list, word_length):
    unique_words = eliminate_duplicates(word_list)
    words_without_punc = eliminate_punctuation(unique_words)
    words_with_correct_length = eliminate_long_or_short_words(words_without_punc, word_length)
    words_without_number = eliminate_numbers(words_with_correct_length)
    words_without_stop_words = eliminate_stop_words(words_without_number)
    words_with_lower_case = to_upper_case(words_without_stop_words)
    
    return words_with_lower_case