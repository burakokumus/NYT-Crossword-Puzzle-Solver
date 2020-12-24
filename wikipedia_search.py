
import wikipedia
import nltk
from nltk.corpus import stopwords
import datetime
import string
import word_eliminator

def wikipedia_search(input_string, word_length):
    print("Wikipedia is searching for {} with length {}".format(input_string, word_length))
    try:
        list = wikipedia.search(input_string)
        if len(list) > 0:
            page_content = wikipedia.page(list[0] + '.').content
        else:
            return []
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            return wikipedia_search(e.options[0], word_length)
        except wikipedia.exceptions.PageError as e:
            return []
    
    all_words = page_content.split(' ')
    

    filtered_words = word_eliminator.filter_words(all_words, word_length)
    
    return filtered_words