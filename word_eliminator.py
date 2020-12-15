import string
import nltk
from nltk.corpus import stopwords

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)

def eliminate_duplicates(word_list):
    return list(set(word_list))

def eliminate_punctuation(word_list):
    return [s.translate(str.maketrans('', '', string.punctuation)) for s in word_list]

def eliminate_long_words(word_list):
    return [word for word in word_list if len(word) <= 5 and len(word) > 1] 

def eliminate_numbers(word_list):
    return [word for word in word_list if not has_numbers(word)]

def eliminate_stop_words(word_list):
    return [word for word in word_list if word not in stopwords.words('english')]

def to_upper_case(word_list):
    return [x.upper() for x in word_list]
