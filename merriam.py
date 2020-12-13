import requests

DICTIONARY_KEY = "340a0202-dd9f-461a-857b-7a401ca334e8"
THESAURUS_KEY  = "784474a4-5968-45da-8f98-d987d2c4935d"

def get_dictionary_result(word):
    dict_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + DICTIONARY_KEY
    r = requests.get(dict_url)
    # process the .json file
    return r.json()

def get_thesaurus_result(word):
    thes_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + THESAURUS_KEY
    r = requests.get(thes_url)
    # process the .json file
    return r.json()

if __name__ == '__main__':
    word = input("Enter a word\n").lower()
    choice = int(input("Which one do you need?\n1. Dictionary\n2. Thesaurus\n"))
    if choice == 1:
        print(get_dictionary_result(word))
    elif choice == 2:
        print(get_thesaurus_result(word))
    else:
        print("Wrong input")
    