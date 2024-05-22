import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, features="html.parser")

product_page_url = url
upc = soup.find("th", string="UPC").find_next_sibling("td").text.strip()
title = soup.find("title").text.strip()
price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text.strip()
price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").text.strip()
number_available = soup.find("p", class_="instock availability").find("i").find_next_sibling(string=True).strip()
### product_description = soup.find("h2", string="Product Description").find_next("p").find_next_sibling(string=True).strip() n'affiche rien
product_description = soup.find("h2", string="Product Description").find_next("p").get_text()
category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
review_rating = soup.find("p", class_="star-rating").get("class")[-1]
image_url = soup.find("img")["src"]
image_url = urljoin(url, image_url)

book_info = {
    "product_page_url": product_page_url,
    "upc": upc,
    "title": title,
    "price_excluding_tax": price_excluding_tax,
    "price_including_tax": price_including_tax,
    "number_available": number_available,
    "product_description": product_description,
    "category": category,
    "review_rating": review_rating,
    "image_url": image_url
}


csv_filename = "Projet2.csv"

with open(csv_filename, "w", newline="") as csvfile :
    writer = csv.writer(csvfile)
    writer.writerow(book_info.keys())
    writer.writerow(book_info.values())