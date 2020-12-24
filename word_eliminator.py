import string
import nltk
from nltk.corpus import stopwords

USER_DEFINED=[
    "ANBSP",
    "NBSP"

]

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)

def stratified_merge(list_a, list_b, list_c):
    lena = len(list_a)
    lenb = len(list_b)
    lenc = len(list_c)
    stratified = []
    while len(list_a) > 0 or len(list_b) > 0 or len(list_c) > 0:
        if len(list_a) > lena // 10 and len(list_a) > 10:
            stratified.extend( list_a[:lena // 10])
            list_a = list_a[lena // 10:]
        else:
            stratified.extend(list_a)
            list_a = []

        if len(list_b) > lenb // 10 and len(list_b) > 10:
            stratified.extend( list_b[:lenb // 10])
            list_b = list_b[lenb // 10:]
        else:
            stratified.extend(list_b)
            list_b = []

        if len(list_c) > lenc // 10 and len(list_c) > 10:
            stratified.extend( list_c[:lenc // 10])
            list_c = list_c[lenc // 10:]
        else:
            stratified.extend(list_c)
            list_c = []

    return stratified

def eliminate_duplicates(word_list):
    duplicates = [x for x in word_list if word_list.count(x) > 1]
    eliminated_list = [x for x in word_list if word_list.count(x) == 1]
    duplicates = [i for j, i in enumerate(duplicates) if i not in duplicates[:j]] 
    return duplicates + eliminated_list

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
    is_single_word = len(query) == 1
    for word in query:
        filtered = filter(str.isalpha, word)
        words_without_escape += "".join(filtered) + " "
    return words_without_escape[:-1] if not is_single_word else words_without_escape

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