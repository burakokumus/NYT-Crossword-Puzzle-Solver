import requests
import json
from bs4 import BeautifulSoup
from googleapiclient.discovery import build   #Import the library
import re
import word_eliminator



credentials_file = open('credentials.json', "r")
credentials_data = json.load(credentials_file)

api_key = credentials_data["api_key"]
cse_id = credentials_data["cse_id"]

FORBIDDEN_SITES = [
    "www.wordplays.com",
    "www.crosswordsolver.org",
    "www.the-crossword-solver.com",
    "crossword-solver.io",
    "www.crosswordsolver.com",
    "crossword-solver.org",
    "crosswordmonkey.com",
    "www.crosswordclues.com",
    "www.wordfun.ca",
    "chambers.co.uk/puzzles/word-wizard",
    "www.realqunb.com",
    "puzzlepageanswers.org"
]

TAG_RE = re.compile(r'<[^>]+>')


def remove_html_tags(text):
    ''' Remove html tags from the input '''
    return TAG_RE.sub('', text)
    
def google_query(query, api_key, cse_id, **kwargs):
    query_service = build("customsearch", 
                        "v1", 
                        developerKey=api_key
                        )  
    query_results = query_service.cse().list(q=query,    # Query
                                            cx=cse_id,  # CSE ID
                                            **kwargs    
                                            ).execute()
    result_words = []
    for a_result in query_results['items']:
        if a_result["displayLink"] not in FORBIDDEN_SITES:
            snippet = remove_html_tags(a_result["snippet"])
            html_snippet = remove_html_tags(a_result["htmlSnippet"])
            snippet = snippet.split(" ")
            html_snippet = html_snippet.split(" ")
            # remove punctuations, long words
            for x in html_snippet:
                result_words.append(x)
            for x in snippet:
                result_words.append(x)

            unique_words = word_eliminator.eliminate_duplicates(result_words)

            words_without_punc = word_eliminator.eliminate_punctuation(unique_words)
            
            short_words = word_eliminator.eliminate_long_words(words_without_punc)

            nonnumber_words = word_eliminator.eliminate_numbers(short_words)

            nonstop_words = word_eliminator.eliminate_stop_words(nonnumber_words)

            result_words = word_eliminator.to_upper_case(nonstop_words)

    return result_words
    


if __name__ == '__main__':
    my_results_list = []
    my_results = google_query("logitech mouse",
                            api_key, 
                            cse_id, 
                            num = 10
                            )
    f = open("result.json", "w")
    print(my_results)
        
    