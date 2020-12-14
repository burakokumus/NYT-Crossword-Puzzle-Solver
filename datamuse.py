import json
import urllib.request as urllib2

prompt = input("Do you want to search for a complete word, word and a letter or letters? ")

def get_data(query):
    api_url = 'https://api.datamuse.com/' + query
    return json.load(urllib2.urlopen(api_url))

# word
def get_words_with_similar_meaning(input_word):
    query = "/words?ml=" + input_word
    return get_data(query)

def get_words_with_similar_sound(input_word):
    query = "/words?sl=" + input_word
    return get_data(query)

def get_words_with_similar_spelling(input_word):
    query = "/words?sp=" + input_word
    return get_data(query)

def get_words_that_rhyme_with(input_word):
    query = "/words?rel_rhy=" + input_word
    return get_data(query)

def get_adjectives_to_describe(input_word):
    query = "/words?rel_jjb=" + input_word
    return get_data(query)

def get_nouns_that_are_described_by(input_word):
    query = "/words?rel_jja=" + word
    return get_data(query)

def get_words_triggered_by(input_word):
    query = "/words?rel_trg=" + word
    return get_data(query)

if prompt.lower() == "word":
    word = input("What is the word you are searching about? ").lower()
    menu = "Select a query from 1-7\n" + \
            "\n7. words that are triggered by (strongly associated with) the word " + word + "\n"
    choice = int(input(menu))
    if choice == 7:
        query = "/words?rel_trg=" + word
    else:
        print("Invalid choice.. Quting..")
        quit()

def get_with_start_end_count(known_letters):
    query = "/words?sp=" + known_letters[0] + "?" * (len(known_letters) - 2) + known_letters[-1]
    return get_data(query)

def get_letter_completion(letters_so_far):
    query = "/sug?s=" + letters_so_far
    return get_data(query)

def get_related_starts_with(word, starting_letter):
    query = "/words?ml=" + word + "&sp=" + starting_letter + "*"
    return get_data(query)

def get_related_ends_with(word, starting_letter):
    query = "/words?ml=" + word + "&sp=*" + starting_letter
    return get_data(query)

def get_often_follows_starts_with(word, starting_letter):
    query = "/words?lc=" + word + "&sp=" + starting_letter + "*"
    return get_data(query)