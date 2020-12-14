
import wikipedia
import nltk
from nltk.corpus import stopwords
import datetime
import string
import word_eliminator

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def remove_punctuation(inputString):
    return inputString.translate(str.maketrans('', '', string.punctuation))

def wikipedia_search(input_string):
    list = wikipedia.search(input_string)
    
    page_content = wikipedia.page(list[0] + '.').content
    
    all_words = page_content.split(' ')

    unique_words = word_eliminator.eliminate_duplicates(all_words)

    words_without_punc = word_eliminator.eliminate_punctuation(unique_words)
    
    short_words = word_eliminator.eliminate_long_words(words_without_punc)

    nonnumber_words = word_eliminator.eliminate_numbers(short_words)

    nonstop_words = word_eliminator.eliminate_stop_words(nonnumber_words)

    lower_case = word_eliminator.to_lower_case(nonstop_words)
    
    return lower_case

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    words = wikipedia_search("Barrack Obama")
    print(words)
    print("Found {} words".format(len(words)))
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds()
    print("Exec time: {}".format(execution_time))
    pass






'''
# Plan B
# start from <li class='mw-search-result'><div class='mw-search-result-heading'><a href=" end at "
word = "yo+yo+ma"
str = "https://en.wikipedia.org/w/index.php?search=" + word + "&title=Special:Search&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1"
r = requests.get(str)
f = open("page.txt", "w", encoding="utf-8")
f.write(r.text)
f.close()
quit()
'''