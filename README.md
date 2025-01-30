# Books Scraper - Scrape Book Data from Books to Scrape

A Python script that scrapes book data from [books.toscrape.com](https://books.toscrape.com/) and downloads book images.

## Features
- Scrapes book titles, ratings, prices, availability, and links
- Downloads book images
- Handles pagination (all pages)
- Saves data to CSV format
- Stores images in organized folders

## Installation
1. Clone this repository
2. Install required packages:
```bash
pip install requests beautifulsoup4 pandas lxml
```
## Usage

Run the script:
``` bash
python books_scraper.py
```

The script will:
  1. Create a book_images folder for downloaded images

  2. Generate books_data.csv with all scraped data

## Code Overview
### Key components:
- Star rating conversion dictionary
- Pagination handling
- CSS selector-based data extraction
- Image downloading system
- Data storage in Pandas DataFrame
- CSV export functionality

## File Structure

.
├── books_scraper.py        # Main scraping script
├── books_data.csv          # Output data file
├── book_images/            # Folder for downloaded images
└── README.md               # This documentation

## Data Collected

| Column        | Description                          | Example                 |
|---------------|--------------------------------------|-------------------------|
| **title**     | Book title                           | "A Light in the..."     |
| **stars**     | Rating (1-5)                         | "4"                     |
| **price**     | Book price                           | "£51.77"                |
| **Availability** | Stock status                      | "In stock"              |
| **img_link**  | Full URL to book cover image         | `https://example.com/image.jpg` |
| **book_link** | Full URL to book detail page         | `https://example.com/book-detail` |
