import os
from full_class import textExtractor

"""

-> main app which uses the textExtractor class from full_class.py
-> Works good!

"""


def main():
    while True:
        print("From where do you want to download texts?")
        print("1. Gutenberg")
        print("2. WikisourceRO")
        print("Q. Quit")
        choice = input("Enter choice (1/2/Q): ").strip().lower()

        if choice == "1":
            # gutenberg choice
            author_name = input("Enter the author name to search on Gutenberg: ").strip()
            extractor = textExtractor()
            epub_links = extractor.search_epub(author_name)

            if not epub_links:
                print(f"No EPUB links found for author: {author_name}!!!\n")
                continue

            os.makedirs(author_name, exist_ok=True)
            for i, link in enumerate(epub_links, start=1):
                epub_file_name = f"{author_name}_book{i}.epub"
                epub_file_path = os.path.join(author_name, epub_file_name)
                txt_file_path = os.path.join(author_name, f"{author_name}_book{i}.txt")

                extractor.download_epub(link, epub_file_path)
                extractor.epub_to_txt(epub_file_path, txt_file_path)

            extractor.rename_and_clean_files(author_name)
            extractor.delete_epubs(author_name)
            print()

        elif choice == "2":
            # wikisource(RO) choice
            author_name = input("Enter the author name to search on Wikisource (ro): ").strip()
            extractor = textExtractor()
            text_links = extractor.search_texts(author_name)

            if not text_links:
                print(f"No Wikisource links found for author: {author_name}!!!\n")
                continue

            texts = extractor.get_text_from_html(text_links)
            extractor.transform_texts_to_txt(texts, author_name)
            print()

        elif choice == "q":
            print("Exiting program!!!")
            break

        else:
            print("NO!!! Please enter 1, 2, or Q to quit!!!\n")


if __name__ == "__main__":
    main()
