import requests
from bs4 import BeautifulSoup

# from .constants import GUTENBERG_YESTERDAY_100

GUTENBERG_YESTERDAY_100 = "https://www.gutenberg.org/browse/scores/top"
GUTENBERG_FILES = "https://www.gutenberg.org/files"
REMOVE_WORDS = ['BIBLIOGRAPHICAL', 'PREFACE', 'VOLUME', 'BOOK']





def get_top_books_urls(url):
    book_url ={}
    soup =get_html_book(url)
    clasif = soup.findAll('h2')

    e_books_index = -1
    for i, c in enumerate(clasif):
        if c['id'] == 'books-last1':  # the tag for the 100 eBooks
            e_books_index = i
    ol_segment = [] if e_books_index == -1 else soup.findAll('ol')[e_books_index]
    for link in ol_segment.find_all('a', href=True):
        book_url[link.text] = link['href']
    return book_url


def get_html_book(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_beauty_text(url):
    content = get_html_book(url)
    title = content.title
    chapters = []
    contents = content.findAll('table')
    for table in contents:
        for link in table.find_all('a', href=True, text=True):
            chap = link.text
            chapters.append(chap)

    other_contents = content.findAll('blockquote')
    for p in other_contents:
        if "CONTENTS" in p.text:
            for link in p.find_all('a', href=True):
                if not len([i for i in REMOVE_WORDS if link.text.replace(" ", "").startswith(i)]):
                    chapters.append(link.text)

    chapters = [chap for chap in chapters if chap not in REMOVE_WORDS and not chap.lstrip().isdigit()]
    print(chapters)

    return chapters



def test():
    top_books_url = get_top_books_urls(GUTENBERG_YESTERDAY_100)
    for book in top_books_url.keys():
        url = top_books_url[book].replace("ebooks/", "")
        html_url = GUTENBERG_FILES + url + url+"-h" + url+"-h"
        get_beauty_text(html_url)

# get_beauty_text('http://www.gutenberg.org/files/84/84-h/84-h')
test()