import json
import urllib.request as urllib2
import word_eliminator

def get_data(query, length):
    api_url = 'https://api.datamuse.com/' + query
    result = json.load(urllib2.urlopen(api_url))
    result_list = []
    for res in result:
        result_list.append(res["word"])
    
    return word_eliminator.filter_words(result_list, length)

# word
def get_words_with_similar_meaning(input_word, length):
    input_word = input_word.lower()
    input_word = input_word.replace(" ", "+")
    query = "/words?ml=" + input_word
    return get_data(query, length)

def get_words_with_similar_sound(input_word, length):
    input_word = input_word.lower()
    input_word = input_word.replace(" ", "+")
    query = "/words?sl=" + input_word
    return get_data(query, length)

def get_words_with_similar_spelling(input_word, length):
    input_word = input_word.lower()
    input_word = input_word.replace(" ", "+")
    query = "/words?sp=" + input_word
    return get_data(query, length)

def get_words_that_rhyme_with(input_word, length):
    input_word = input_word.lower()
    input_word = input_word.replace(" ", "+")
    query = "/words?rel_rhy=" + input_word
    return get_data(query, length)

def get_adjectives_to_describe(input_word, length):
    input_word = input_word.lower()
    input_word = input_word.replace(" ", "+")
    query = "/words?rel_jjb=" + input_word
    return get_data(query, length)

def get_nouns_that_are_described_by(input_word, length):
    input_word = input_word.lower()
    input_word = input_word.replace(" ", "+")
    query = "/words?rel_jja=" + input_word
    return get_data(query, length)

def get_words_triggered_by(input_word, length):
    input_word = input_word.lower()
    input_word = input_word.replace(" ", "+")
    query = "/words?rel_trg=" + input_word
    return get_data(query, length)

def get_with_start_end_count(known_letters, length):
    query = "/words?sp=" + known_letters[0] + "?" * (len(known_letters) - 2) + known_letters[-1]
    return get_data(query, length)

def get_letter_completion(letters_so_far, length):
    query = "/sug?s=" + letters_so_far
    return get_data(query, length)

def get_related_starts_with(word, starting_letter, length):
    query = "/words?ml=" + word + "&sp=" + starting_letter + "*"
    return get_data(query, length)

def get_related_ends_with(word, starting_letter, length):
    query = "/words?ml=" + word + "&sp=*" + starting_letter
    return get_data(query, length)

def get_often_follows_starts_with(word, starting_letter, length):
    query = "/words?lc=" + word + "&sp=" + starting_letter + "*"
    return get_data(query, length)