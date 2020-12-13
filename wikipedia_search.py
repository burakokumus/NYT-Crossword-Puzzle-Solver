
import wikipedia

# https://pypi.org/project/Wikipedia-API/

# wiki_wiki = wikipediaapi.Wikipedia('en')

# page_py = wiki_wiki.page('yo-yo ma')
# print(page_py.exists())

# page_py = wiki_wiki.page('Yo-yo Ma')
# print(page_py.exists())

# page_py = wiki_wiki.page('Yo-yo ma')
# print(page_py.exists())

# page_py = wiki_wiki.page('yo-yo Ma')
# print(page_py.exists())

list = wikipedia.search("yo yo ma")
print(list[0])
print(wikipedia.summary("Yo-Yo Ma!"))


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