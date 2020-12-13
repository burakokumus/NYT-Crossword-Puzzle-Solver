'''
-----For words-----
words with a meaning similar to engineering big data	/words?ml=engineering+big+data  ****Added
words that sound like pithon	/words?sl=pithon ****Added
words that are spelled similarly to cali	/words?sp=california ****Added
words that rhyme with big	/words?rel_rhy=big ****Added
adjectives that are often used to describe software	/words?rel_jjb=software ****Added
words that are triggered by (strongly associated with) the word “code”	/words?rel_trg=code ****Added
nouns that are often described by the adjective tough	/words?rel_jja=tough ****Added

-----For letters----
words that start with d, end in a, and have two letters in between	/words?sp=d??a
suggestions for the user if they have typed in softw so far	/sug?s=softw 

-----For words and letters-----
words related to data that start with the letter i	/words?ml=data&sp=i*
words related to python that end with the letter a	/words?ml=python&sp=*a
words that often follow “drink” in a sentence, that start with the letter c	/words?lc=software&sp=c*

words that rhyme with coding that are related to software	/words?ml=software&rel_rhy=code  **** I dont think we will use it
adjectives describing software sorted by how related they are to code	/words?rel_jjb=software&topics=code  **** I dont think we will use it
'''
import json
import urllib.request as urllib2

prompt = input("Do you want to search for a complete word, word and a letter or letters? ")

if prompt.lower() == "word":
    word = input("What is the word you are searching about? ").lower()
    menu = "Select a query from 1-7\n" + \
            "\n1. words with a meaning similar to " + word + \
            "\n2. words that sound like " + word + \
            "\n3. words that are spelled similarly to " + word + \
            "\n4. words that rhyme with " + word + \
            "\n5. adjectives that are often used to describe " + word + \
            "\n6. nouns that are often described by the adjective " + word + \
            "\n7. words that are triggered by (strongly associated with) the word " + word + "\n"
    choice = int(input(menu))
    if choice == 1:
        query = "/words?ml=" + word
    elif choice == 2:
        query = "/words?sl=" + word
    elif choice == 3:
        query = "/words?sp=" + word
    elif choice == 4:
        query = "/words?rel_rhy=" + word
    elif choice == 5:
        query = "/words?rel_jjb=" + word
    elif choice == 6:
        query = "/words?rel_jja=" + word
    elif choice == 7:
        query = "/words?rel_trg=" + word
    else:
        print("Invalid choice.. Quting..")
        quit()

if prompt.lower() == "letters":
    letters = input("What are the letters you are searching about? ")
    menu = "Select a query from 1-7\n" + \
        "\n1. words that start with " + letters[0] + ", end in " + letters[-1] + ", and have " + str((len(letters) - 2)) + " letters in between " + \
        "\n2. suggestions if they have typed in " + letters + " so far " + "\n"

    choice = int(input(menu))
    if choice == 1:
        query = "/words?sp=" + letters[0] + "?" * (len(letters) - 2) + letters[-1]
    elif choice == 2:
        query = "/sug?s=" + letters
    else:
        print("Invalid choice.. Quting..")
        quit()


if prompt.lower() == "word and a letter":
    word_and_letter = input("What is the word and the letter you are searching about? ")
    word_and_letter = word_and_letter.split(" ")
    menu = "Select a query from 1-7\n" + \
    "\n1. words related to " + word_and_letter[0] + " that start with the letter " + word_and_letter[1] + \
    "\n2. words related to " + word_and_letter[0] + " that end with the letter " + word_and_letter[1] + \
    "\n3. words that often follow “" + word_and_letter[0] + "” in a sentence, that start with the letter " + word_and_letter[1] + "\n"

    choice = int(input(menu))

    if choice == 1:
        query = "/words?ml=" + word_and_letter[0] + "&sp=" + word_and_letter[1] + "*"
    elif choice == 2:
        query = "/words?ml=" + word_and_letter[0] + "&sp=*" + word_and_letter[1]
    elif choice == 3:
        query = "/words?lc=" + word_and_letter[0] + "&sp=" + word_and_letter[1] + "*"
    else:
        print("Invalid choice.. Quting..")
        quit()

print()

api_url = 'https://api.datamuse.com/' + query
data = json.load(urllib2.urlopen(api_url))
 
def datamuse_api():
    print(data)
 
datamuse_api()