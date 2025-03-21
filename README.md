# text-scraper

Fast python scraper to download texts from [Project Gutenberg](https://www.gutenberg.org/) or [Wikisource (Romanian only)](https://ro.wikisource.org)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tudord14/text-scraper.git
   cd text-scraper
   ```
2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
   
### Main App =>
Fully working cli app where the user chooses between Gutenberg or Wikisource(RO), then desired author name should be written... easy! The user should be really careful when writing authors names as the program is *really* sensitive to diacritics, especially for romanian authors. Even for swedish authors for example one should copy the name from the internet!!! I will include a txt file in the project which will have a lot of romanian authors names!!! For example...
```
Ion Creanga ❌
Ion Creangă ✅
```
If noted then do:
```bash
python main.py
```
![WhatsApp Image 2025-03-21 at 14 05 45](https://github.com/user-attachments/assets/71965973-e2db-4017-8afe-2c3e9d9a6b14)

### Individual scripts =>
If the user (for some reason) wants to independently run the wikisource or gutenberg process he can...
1. Wikisource(RO)
   ```bash
   python wikisource_RO_texts_extraction.py
   ```
2. Gutenberg
   ```bash
   python author_texts_extraction_epub_to_txt.py
   ```
   Then cleanup...
   ```bash
   python author_directory_cleanup.py
   ```

### Disclaimer

This tool directly scrapes publicly available text from the respective websites it does **not** use any official API!!!!!!
By using this scraper, **you assume full responsibility for your actions** and compliance with all relevant legal and ethical obligations!!!!!
The author of this repository(me!) bears **no liability** for any misuse or resulting issues!!!!

**Have fun!!!!**
