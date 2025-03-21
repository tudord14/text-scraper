import os
import ebooklib
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import urllib.parse
from bs4.element import Tag
import re

"""
UPDATE 1: ->
    -> The code obtains the texts from a specific Romanian author
    but the folder is not really "clean"
    -> A follow-up program for cleaning the folder will be created
    -> (I hope it will happen soon)
    
UPDATE 2: ->
    -> The folder is a little cleaner now
    -> I have added a list of the most notable romanian authors
    -> This list can be used to generate all the folders at once later
    
UPDATE 3:  -> 
    -> The text files now don't contain the text title and the authors name
    -> Works good!
    
"""


authors = [
    "Mihai Eminescu",
    "Ion Creangă",
    "Ion Luca Caragiale",
    "Vasile Alecsandri",
    "George Coșbuc",
    "Lucian Blaga",
    "George Bacovia",
    "Tudor Arghezi",
    "Nicolae Bălcescu",
    "Octavian Goga",
    "Dimitrie Cantemir",
    "Alexandru Macedonski",
    "Barbu Ștefănescu Delavrancea",
    "Liviu Rebreanu",
    "Ioan Slavici",
    "Gala Galaction",
    "Constantin Negruzzi",
    "Alexandru Vlahuță",
    "George Topîrceanu",
    "Nicolae Filimon",
    "Mateiu Caragiale",
    "Camil Petrescu",
    "Mircea Eliade",
    "Eugen Lovinescu",
    "Ion Barbu",
    "Panait Istrati",
    "Ion Agârbiceanu",
    "Grigore Alexandrescu",
    "Vasile Voiculescu",
    "Ștefan Octavian Iosif",
    "Mihail Sadoveanu",
    "Ion Pillat",
    "Zaharia Stancu",
    "Nicolae Iorga",
    "Vasile Pârvan",
    "Bogdan Petriceicu Hasdeu",
    "Costache Negruzzi",
    "Alecu Russo",
    "Dimitrie Bolintineanu",
    "Ion Heliade Rădulescu",
    "Cezar Bolliac",
    "Traian Demetrescu",
    "Mihail Kogălniceanu",
    "Iacob Negruzzi",
    "Nicolae Gane",
    "Emanoil Bucuța",
    "Ovid Densusianu",
    "Ioan Alexandru Brătescu-Voinești",
    "Alexandru Odobescu",
    "Ion Minulescu"
]




def decode_url_title(encoded_html_href):
    decoded_title = urllib.parse.unquote(encoded_html_href).replace("/wiki/", "")
    return decoded_title.replace('_', ' ')


def search_texts(author_name):
    author_page = f"https://ro.wikisource.org/wiki/Autor:{author_name}"
    response = requests.get(author_page)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_titles = []

        for html_ul_elem in soup.find_all('ul'):
            for html_li_elem in html_ul_elem.find_all('li'):
                html_a_elem = html_li_elem.find('a')
                if html_a_elem:
                    # Skip <a> elements with color #D73333
                    style = html_a_elem.get('style', '')
                    if 'color: #D73333' in style.replace(' ', ''):
                        continue

                    text_title = html_a_elem.text.strip()
                    encoded_html_href_title = html_a_elem['href']
                    decoded_title = decode_url_title(encoded_html_href_title)

                    if decoded_title == text_title:
                        link_to_book = f"https://ro.wikisource.org{html_a_elem['href']}"
                        text_titles.append(link_to_book)
        return text_titles[1:]
    else:
        print(f"Error accessing page: {response.status_code}")
        return []


def get_text_from_html(text_links):
    texts = []
    for link in text_links:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_title = link.replace("https://ro.wikisource.org/wiki/", "")
            # Decode the title to handle URL-encoded characters
            text_title = urllib.parse.unquote(text_title).replace('_', ' ')

            # The text is usually contained in the <div class="mw-parser-output">
            content_div = soup.find('div', class_='mw-parser-output')
            if content_div:
                # Remove all <span> elements
                for span in content_div.find_all('span'):
                    span.decompose()

                # Remove the <td class="titlu_titlu">
                titlu = content_div.find('td', class_='titlu_titlu')
                if titlu:
                    titlu.decompose()

                # Check for and remove the <a href="#top"> element
                a_tag = content_div.find('a', href='#top')
                if a_tag:
                    a_tag.decompose()

                # Remove any <div> with id="toc" (Table of Contents)
                toc_div = content_div.find('div', id='toc')
                if toc_div:
                    toc_div.decompose()

                text_content = ""
                for child in content_div.children:
                    if isinstance(child, Tag) and child.name != 'span':
                        text_content += child.get_text(separator="\n", strip=True) + "\n"

                texts.append({'title': text_title, 'content': text_content})
            else:
                print(f"Content div not found {link}")
        else:
            print(f"Error when trying to access page: {response.status_code}")
    return texts


def transform_texts_to_txt(texts, author_name):
    os.makedirs(author_name, exist_ok=True)

    for text in texts:
        # Decode the title to handle URL-encoded characters
        title = urllib.parse.unquote(text['title'])
        content = text['content']
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", title)
        file_path = os.path.join(author_name, f"{sanitized_title}.txt")

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Saved '{title}' to '{file_path}'")


name = input("Author name: ")
all_text_titles = search_texts(name)
texts = get_text_from_html(all_text_titles)
transform_texts_to_txt(texts, name)

files_in_folder = os.listdir(name)
num_files = len([f for f in files_in_folder if os.path.isfile(os.path.join(name, f))])
print(f"\nTotal number of files in the folder '{name}': {num_files}")