import os
import ebooklib
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import urllib.parse
from bs4.element import Tag
import re

"""

-> class containing all of the functions for Wikisource(ro) and Gutenberg extracting and cleaning
-> this is just a summary of the separate .py file:
    -> author_directory_cleanup.py
    -> author_texts_extraction_epub_to_txt.py
    -> wikisource_RO_texts_extraction.py
-> this class will be used in the main program main.py

"""


class textExtractor():

    ### -> functions for extracting Wikisource texts
    def decode_url_title(self, encoded_html_href):
        decoded_title = urllib.parse.unquote(encoded_html_href).replace("/wiki/", "")
        return decoded_title.replace('_', ' ')

    def search_texts(self, author_name):
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
                        decoded_title = self.decode_url_title(encoded_html_href_title)

                        if decoded_title == text_title:
                            link_to_book = f"https://ro.wikisource.org{html_a_elem['href']}"
                            text_titles.append(link_to_book)
            return text_titles[1:]
        else:
            print(f"Error accessing page: {response.status_code}")
            return []

    def get_text_from_html(self, text_links):
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

    def transform_texts_to_txt(self, texts, author_name):
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




    ### -> functions for extracting Gutenberg texts
    def search_epub(self, author_name):

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

    def download_epub(self, epub_url, output_path):
        # Go to the url and download the .epub file
        response = requests.get(epub_url)
        with open(output_path, 'wb') as epub_file:
            epub_file.write(response.content)
        print(f'Downloaded: {output_path}')

    def epub_to_txt(self, epub_file_path, output_txt_path):
        book = epub.read_epub(epub_file_path)
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_body_content().decode('utf-8')
                    soup = BeautifulSoup(content, 'html.parser')
                    txt_file.write(soup.get_text())
        print(f'Converted {epub_file_path} to {output_txt_path}')



    ### -> functions for cleaning Gutenberg extracted folders
    def get_title_from_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if "Title:" in line:
                    return line.split("Title:")[1].strip()
        return None

    def clean_text_content(self, file_path, output_path):
        start_marker = "*** START OF"
        end_marker = "*** END OF"
        content_started = False

        with open(file_path, 'r', encoding='utf-8') as file, open(output_path, 'w', encoding='utf-8') as out_file:
            for line in file:
                if start_marker in line:
                    content_started = True
                    continue
                if end_marker in line:
                    break
                if content_started:
                    out_file.write(line)
        print(f"Cleaned and saved file: {output_path}")

    def rename_and_clean_files(self, directory):
        for file_name in os.listdir(directory):
            if file_name.endswith('.txt'):
                file_path = os.path.join(directory, file_name)

                title = self.get_title_from_text(file_path)
                if not title:
                    print(f"Could not find title in {file_name}, skipping.")
                    continue

                new_file_name = f"{title}.txt"
                new_file_path = os.path.join(directory, new_file_name)
                self.clean_text_content(file_path, new_file_path)

                os.remove(file_path)
                print(f"Renamed {file_name} to {new_file_name} and cleaned it.")

    def delete_epubs(self, directory):
        for file_name in os.listdir(directory):
            if file_name.endswith('.epub'):
                file_path = os.path.join(directory, file_name)
                os.remove(file_path)
                print(f"Deleted {file_name}")
