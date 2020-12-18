import json
from bs4 import BeautifulSoup
from googleapiclient.discovery import build 
import re
import word_eliminator



credentials_file = open('./GoogleCredentials/credentials15.json', "r")
credentials_data = json.load(credentials_file)

api_key = credentials_data["api_key"]
cse_id = credentials_data["cse_id"]

FORBIDDEN_SITES = [
    "www.wordplays.com",
    "www.wordfun.ca",
    "chambers.co.uk/puzzles/word-wizard",
    "www.realqunb.com",
    "puzzlepageanswers.org",
    "www.danword.com",
    "ultimatesuccesspuzzle.com",
    "www.cluest.net",
    "nytimesanswers.com",
    "jumbleanswers.com",
    "unscramblex.com",
    "www.word-grabber.com",
    "www.globalclue.com"
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
        if a_result["displayLink"] not in FORBIDDEN_SITES and "crossword" not in a_result["displayLink"] and "puzzle" not in a_result["displayLink"]:
            snippet = remove_html_tags(a_result["snippet"])
            html_snippet = remove_html_tags(a_result["htmlSnippet"])
            snippet = snippet.split(" ")
            html_snippet = html_snippet.split(" ")
            # remove punctuations, long words
            for x in html_snippet:
                filtered = filter(str.isalpha, x)
                result_words.append("".join(filtered))
            for x in snippet:
                filtered = filter(str.isalpha, x)
                result_words.append("".join(filtered))
            site_count += 1
            
    
    next_response = query_service.cse().list(
                                q=query,cx=cse_id,num=10,start=query_results['queries']['nextPage'][0]['startIndex'],).execute() 
    print
    if query == "\"Oh, you wanna go? Let's go!\"":
        f = open("results.txt", "w")
        f.write(next_response)
    for a_result in next_response['items']:
        if a_result["displayLink"] not in FORBIDDEN_SITES and "crossword" not in a_result["displayLink"]:
            snippet = remove_html_tags(a_result["snippet"])
            html_snippet = remove_html_tags(a_result["htmlSnippet"])
            snippet = snippet.split(" ")
            html_snippet = html_snippet.split(" ")
            # remove punctuations, long words
            for x in html_snippet:
                filtered = filter(str.isalpha, x)
                result_words.append("".join(filtered))
            for x in snippet:
                filtered = filter(str.isalpha, x)
                result_words.append("".join(filtered))
            site_count += 1

    return word_eliminator.filter_words(result_words, length)
    
def search_google(query, length):
    return google_query(query, length, api_key, cse_id, num=10)
