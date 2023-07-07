import os
import requests
import csv
from lxml import html

# Set the URL and headers
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
}

# Get the path of the current script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the CSV file path
csv_path = os.path.join(script_dir, "product_data.csv")

# Create a CSV file to store the scraped data
csv_file = open(csv_path, "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])

# Function to scrape product information
def scrape_product_info(product):
    product_url = product.xpath(".//a[@class='a-link-normal s-no-outline']/@href")[0]
    product_name = product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()")[0].strip()
    product_price = product.xpath(".//span[@class='a-offscreen']/text()")[0].strip()
    rating = product.xpath(".//span[@class='a-icon-alt']/text()")[0].strip().split()[0]
    num_reviews_elements = product.xpath(".//span[@class='a-size-base']/text()")
    num_reviews = num_reviews_elements[0].strip() if num_reviews_elements else "N/A"
    return product_url, product_name, product_price, rating, num_reviews

# Scrape the product listings
product_count = 0
page_number = 1
while product_count < 200:  # Scrape at least 200 products
    page_url = url + str(page_number)
    response = requests.get(page_url, headers=headers)
    tree = html.fromstring(response.content)
    products = tree.xpath("//div[@data-component-type='s-search-result']")
    for product in products:
        product_url, product_name, product_price, rating, num_reviews = scrape_product_info(product)
        csv_writer.writerow([product_url, product_name, product_price, rating, num_reviews])
        product_count += 1
        if product_count >= 200:
            break
    page_number += 1

# Close the CSV file
csv_file.close()

print("Scraping completed. The product data has been saved in 'product_data.csv'.")
