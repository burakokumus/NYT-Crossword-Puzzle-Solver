from time import process_time
import requests
import json

DICTIONARY_KEY = "340a0202-dd9f-461a-857b-7a401ca334e8"
THESAURUS_KEY  = "784474a4-5968-45da-8f98-d987d2c4935d"

def get_ants_and_syns(word):
    thes_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + THESAURUS_KEY
    response = requests.get(thes_url)
    r = response.json()
    synonyms = []
    antonyms = []
    for result in r:
        if type(result) == str:
            return [], []
        for fields in result["meta"].items():
            # If result is not the exact match of the word, skip
            if fields[0] == "id":
                if fields[1] != word:
                    break
            # Add synonyms
            if fields[0] == "syns":
                for syn_list in fields[1]:
                    for syn in syn_list: 
                        synonyms.append(syn)
            # Add antonyms
            if fields[0] == "ants":
                for ant_list in fields[1]:
                    for ant in ant_list: 
                        antonyms.append(ant)
    return antonyms, synonyms

def get_dictionary_result(word):
    dict_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + DICTIONARY_KEY
    response = requests.get(dict_url)
    r = response.json()
    definitions = []
    related = False
    for result in r:
        if type(result) == str:
            return []
        related = False
        for meta_items in result["meta"].items():
            # If result is not the exact match of the word, skip
            if meta_items[0] == "id":
                if len(meta_items[1]) == len(word):
                    related = True
                else:
                    words = meta_items[1].split(" ")
                    if len(words) == 1 and words[0][len(word)] == ':': 
                        related = True
                break
        if related:
            # Add each definition
            for definition in result["shortdef"]:
                definitions.append(definition)
    return definitions

if __name__ == '__main__':
    word = input("Enter a word\n").lower()
    choice = int(input("Which one do you need?\n1. Dictionary\n2. Antonyms\n3. Synonyms\n"))
    if choice == 1:
        print(get_dictionary_result(word))
    elif choice == 2 or choice == 3:
        ants, syns = get_ants_and_syns(word)
        if choice == 2:
            print(ants)
        elif choice == 3:
            print(syns)
    else:
        print("Wrong input")