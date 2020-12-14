
import wikipedia
import nltk
from nltk.corpus import stopwords
import datetime
from solver import process_list

def wikipedia_search(input_string):
    list = wikipedia.search(input_string)
    
    page_content = wikipedia.page(list[0] + '.').content
    
    all_words = page_content.split(' ')
    '''
    unique_words = set(all_words) # remove duplicates

    words_without_punc = [remove_punctuation(x) for x in unique_words]
    
    short_words = [x for x in words_without_punc if len(x) <= 5 and len(x) > 1] # find all words with less than or equal to 5 characters

    none_number_words = [x for x in short_words if not has_numbers(x)]

    none_stop_words = [x for x in none_number_words if x not in stopwords.words('english')] # remove stop-words

    lower_case = [x.lower() for x in none_stop_words]
    '''
    return process_list(all_words)

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