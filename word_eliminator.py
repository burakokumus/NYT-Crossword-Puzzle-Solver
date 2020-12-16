import string
import nltk
from nltk.corpus import stopwords

USER_DEFINED=[
    "ANBSP",
    "NBSP"

]

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)

def eliminate_duplicates(word_list):
    return list(set(word_list))

def eliminate_user_defined(word_list):
    return [word for word in word_list if word not in USER_DEFINED]

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

def remove_escape_sequences(input_str):
    query = input_str.split(" ")
    words_without_escape = ""
    for word in query:
        filtered = filter(str.isalpha, word)
        words_without_escape += "".join(filtered) + " "
    return words_without_escape

def filter_words(word_list, word_length):
    words_without_escape = []
    for word in word_list:
        filtered = filter(str.isalpha, word)
        words_without_escape.append("".join(filtered))

    words_with_upper_case = to_upper_case(words_without_escape)
    words_without_user_defined = eliminate_user_defined(words_with_upper_case)
    unique_words = eliminate_duplicates(words_without_user_defined)
    words_without_punc = eliminate_punctuation(unique_words)
    words_with_correct_length = eliminate_long_or_short_words(words_without_punc, word_length)
    words_without_number = eliminate_numbers(words_with_correct_length)
    words_without_stop_words = eliminate_stop_words(words_without_number)
    result = eliminate_duplicates(words_without_stop_words)


    return result