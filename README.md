# text-scraper

Fast python scraper to download texts from [Project Gutenberg](https://www.gutenberg.org/) or [Wikisource (Romanian only)](https://ro.wikisource.org)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tudord14/text-scraper
   cd text-scraper
   ```
2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
   
### Main App =>
Fully working cli app where the user chooses between Gutenberg or Wikisource(RO), then desired author name should be written... easy!
```bash
python main.py
```

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
