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
    "www.wordfun.ca",
    "chambers.co.uk/puzzles/word-wizard",
    "www.realqunb.com",
    "puzzlepageanswers.org"
]

TAG_RE = re.compile(r'<[^>]+>')


def remove_html_tags(text):
    ''' Remove html tags from the input '''
    return TAG_RE.sub('', text)
    
def google_query(query, length, api_key, cse_id, **kwargs):
    query_service = build("customsearch", 
                        "v1", 
                        developerKey=api_key
                        )  
    query_results = query_service.cse().list(q=query,    # Query
                                            cx=cse_id,  # CSE ID
                                            **kwargs    
                                            ).execute()
    result_words = []
    site_count = 0
    for a_result in query_results['items']:
        if a_result["displayLink"] not in FORBIDDEN_SITES and "crossword" not in a_result["displayLink"]:
            print(a_result["displayLink"])
            snippet = remove_html_tags(a_result["snippet"])
            html_snippet = remove_html_tags(a_result["htmlSnippet"])
            snippet = snippet.split(" ")
            html_snippet = html_snippet.split(" ")
            # remove punctuations, long words
            for x in html_snippet:
                result_words.append(x)
            for x in snippet:
                result_words.append(x)
            site_count += 1
    
    while site_count < 20:
        next_response = query_service.cse().list(
                                        q=query,cx=cse_id,num=10,start=query_results['queries']['nextPage'][0]['startIndex'],).execute() 

        for a_result in next_response['items']:
            if a_result["displayLink"] not in FORBIDDEN_SITES and "crossword" not in a_result["displayLink"]:
                print(a_result["displayLink"])
                snippet = remove_html_tags(a_result["snippet"])
                html_snippet = remove_html_tags(a_result["htmlSnippet"])
                snippet = snippet.split(" ")
                html_snippet = html_snippet.split(" ")
                # remove punctuations, long words
                for x in html_snippet:
                    result_words.append(x)
                for x in snippet:
                    result_words.append(x)
                site_count += 1

    return word_eliminator.filter_words(result_words, length)
    
def search_google(query, length):
    google_query(query, length, api_key, cse_id)

if __name__ == '__main__':
    my_results_list = []
    my_results = google_query("greek k",
                                5,
                            api_key, 
                            cse_id, 
                            num = 10
                            )

    print(my_results)
        
    