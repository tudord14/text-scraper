import os
import ebooklib
import requests
from bs4 import BeautifulSoup
from ebooklib import epub


""""

-> "search_epub" function is made to take in an author name as input and    
    create a list of links of texts that were written by that author
-> The links are for the .epub versions of the books
-> Once a list of links is obtained we use the function "download_epub" 
   that takes as input a link and an output path to download each .epub file
-> By using the "epub_to_text" function we transform an .epub into .txt file
-> The "main" function takes care of everything and requires only an author name

----> When run, the program should ask for an author name, be sure to write it correctly!!!

"""

def search_epub(author_name):

    # The search url for the specific author_name from gutenberg
    search_url = f'https://www.gutenberg.org/ebooks/search/?query={author_name}&submit_search=Go%21'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # By using HTML elements <li> from a <ul> we can extract each book name
    # And by finding the <a> element we can get the LINK
    epub_links = []
    for book in soup.find_all('li', class_='booklink'):
        link_tag = book.find('a', href=True)
        book_url = f'https://www.gutenberg.org{link_tag["href"]}'

        book_page = requests.get(book_url)
        book_soup = BeautifulSoup(book_page.text, 'html.parser')

        # We again search through the HTML elements to find the .epub <a> element LINK
        for link in book_soup.find_all('a', href=True):
            if 'epub.noimages' in link['href']:
                epub_link = f'https://www.gutenberg.org{link["href"]}'
                epub_links.append(epub_link)
                break

    return epub_links


def download_epub(epub_url, output_path):
    # Go to the url and download the .epub file
    response = requests.get(epub_url)
    with open(output_path, 'wb') as epub_file:
        epub_file.write(response.content)
    print(f'Downloaded: {output_path}')


def epub_to_txt(epub_file_path, output_txt_path):
    book = epub.read_epub(epub_file_path)
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content = item.get_body_content().decode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')
                txt_file.write(soup.get_text())
    print(f'Converted {epub_file_path} to {output_txt_path}')


def main(author_name):
    epub_links = search_epub(author_name)

    if not epub_links:
        print(f"No EPUB files found for author {author_name}.")
        return

    if not os.path.exists(author_name):
        os.makedirs(author_name)

    for i, epub_link in enumerate(epub_links):
        epub_file_path = os.path.join(author_name, f'{author_name}_{i}.epub')
        txt_file_path = os.path.join(author_name, f'{author_name}_{i}.txt')

        download_epub(epub_link, epub_file_path)
        epub_to_txt(epub_file_path, txt_file_path)


author = input("Enter author name: ")
main(author)
