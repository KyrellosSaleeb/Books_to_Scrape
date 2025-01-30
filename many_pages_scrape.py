import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import pandas as pd 

# Mapping star ratings to numbers
number_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

url = 'https://books.toscrape.com/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0'}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

page_html = response.text
soup = BeautifulSoup(page_html, 'html.parser')

# Initialize lists for each key in the dictionary
img_link = []
stars = []
title = []
prices = []
book_link = []
Availability_list = []

# Dictionary with empty lists to store book data
keys = ["title", "stars", "price", "Availability", "img_link", "book_link"]
Dict_Books_data = {key: [] for key in keys}

# Get the number of pages to scrape
page_count_str = soup.find('li', class_="current").text.strip()
page_count_str = page_count_str.split()[-1]
page_count = int(page_count_str)

# Create a folder to store images
image_folder = "book_images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)


# Counter for naming images
image_counter = 1


# Loop through pages
for n in range(1, page_count + 1):
    paged_url = f'https://books.toscrape.com/catalogue/page-{n}.html'
    response = requests.get(paged_url, headers=headers)
    response.encoding = 'utf-8'
    page_html = response.text
    soup = BeautifulSoup(page_html, 'html.parser')

    if response.status_code == 200:
        # Find all book containers
        container_tag = soup.find_all('article', class_='product_pod')
        print(f"Found {len(container_tag)} books on page {n}")

        # Extract book details from each container
        for book in container_tag:
            # Get the book link
            book_link_1 = book.find('a')['href']
            book_link = urljoin(url, book_link_1)

            # Get the image link
            img_link_div = book.find('div', class_='image_container').img['src']
            img_link_full = urljoin(url, img_link_div)

            # Get the stars rating (converted to number)
            stars_tag = book.find('p', class_='star-rating')
            stars_class = stars_tag['class'][1]
            stars_value = str(number_dict[stars_class])

            # Get the book title
            title_value = book.find('h3').a.text.strip()

            # Get the price
            price = book.find('p', class_='price_color').text.strip()

            # Get the availability
            availability = book.find('p', class_='instock availability').text.strip()

            # Create a unique image name based on the counter
            image_name = f"{image_counter}.jpg"  # Name images as 1.jpg, 2.jpg, etc.
            image_path = os.path.join(image_folder, image_name)

            # Download the image
            img_response = requests.get(img_link_full, headers=headers)
            if img_response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded image: {image_name}")

             # Increment image counter for the next image
            image_counter += 1
            
                
            # Append each book's data to the respective list in Dict_Books_data
            Dict_Books_data["title"].append(title_value)
            Dict_Books_data["stars"].append(stars_value)
            Dict_Books_data["price"].append(price)
            Dict_Books_data["Availability"].append(availability)
            Dict_Books_data["img_link"].append(img_link_full)
            Dict_Books_data["book_link"].append(book_link)

# Convert dictionary to DataFrame and save as CSV
df = pd.DataFrame(Dict_Books_data)
df.to_csv('books_data.csv', index=False)

print("Data saved to books_data.csv")
