
import wikipedia
import nltk
from nltk.corpus import stopwords
import datetime
import string
import word_eliminator

def wikipedia_search(input_string, word_length):
    list = wikipedia.search(input_string)
    
    page_content = wikipedia.page(list[0] + '.').content
    
    all_words = page_content.split(' ')

    filtered_words = word_eliminator.filter_words(all_words, word_length)
    
    return filtered_words