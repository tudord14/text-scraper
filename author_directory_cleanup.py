import os
from tkinter import Tk, filedialog, messagebox

"""
-> because each gutenberg file contains other elements besides the text we would like
   to clean each file a little bit before starting our analysis
-> first of all we should change the .txt file title by finding it in the file
-> then we would like to only extract the text from the whole file
-> optional: we can delete the .epub files so that at the end we have a clean folder
    --> "get_title_from_text" function reads the text and searches for the gutenberg tag 
    that indicates the texts Title
    --> "clean_text_content" function looks for the gutenberg tags that declare the start and end of a text
    and save only the text part that is delimited by those tags
    --> "rename_and_clean_files" assigns each text the correct title that the
    author gave it and makes sure that the file contains only the text
    --> "delete_epubs" is a function that takes care of the remaining .epub files
    and deletes them from the directory 
    --> "select_and_process_multiple_folders" function allows us to clean multiple
    directories at the same time (users choice)

                                        !!!
    ------> even though this process "cleans" the directory as much as possible,
            a lot of gutenberg authors have assigned to their name a lot of texts
            that may or may not really be their work
    ------> that being said, the user is advised to take a look at the resulted texts
            so that he can ensure data quality ;)
                                        !!!

"""


def get_title_from_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if "Title:" in line:
                return line.split("Title:")[1].strip()
    return None


def clean_text_content(file_path, output_path):
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


def rename_and_clean_files(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            file_path = os.path.join(directory, file_name)

            title = get_title_from_text(file_path)
            if not title:
                print(f"Could not find title in {file_name}, skipping.")
                continue

            new_file_name = f"{title}.txt"
            new_file_path = os.path.join(directory, new_file_name)
            clean_text_content(file_path, new_file_path)

            os.remove(file_path)
            print(f"Renamed {file_name} to {new_file_name} and cleaned it.")


def delete_epubs(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.epub'):
            file_path = os.path.join(directory, file_name)
            os.remove(file_path)
            print(f"Deleted {file_name}")


def select_and_process_multiple_folders():
    Tk().withdraw()
    folders = []

    while True:
        folder_path = filedialog.askdirectory(title="Select a folder containing text files")
        if folder_path:
            folders.append(folder_path)
        else:
            break
        if not messagebox.askyesno("Select More?", "Do you want to select another folder?"):
            break

    for directory_path in folders:
        rename_and_clean_files(directory_path)
        delete_epubs(directory_path)

select_and_process_multiple_folders()