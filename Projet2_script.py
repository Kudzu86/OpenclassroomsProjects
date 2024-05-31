import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://books.toscrape.com/"    

# Fonction chef d'orchestre
def get_all_mystery_books(base_url):
    url = f"{base_url}catalogue/category/books/mystery_3/index.html"
    csv_filename = "Projet2.csv"
    book_links = get_book_links_from_category(url)
    create_csv_file(csv_filename, book_links)

# Fonction qui récupère tous les liens de la catégorie
def get_book_links_from_category(url):
    links = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")
        for h3 in soup.find_all("h3"):
            href = h3.find("a")["href"]
            product_page_url = base_url + href.replace("../../../" , "catalogue/")               
            links.append(product_page_url)
        url = get_next_page_url(soup, url)
    return links

# Création d'un fichier CSV avec écriture des infos extraites
def create_csv_file(csv_filename, book_links):
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        if not book_links:
            print("Aucun livre trouvé.")
            return

        # Obtenir les clés du dictionnaire pour déterminer les fieldnames
        fieldnames = list(get_book_info(book_links[0]).keys())

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for product_page_url in book_links:
            book_info = get_book_info(product_page_url)
            if book_info:
                writer.writerow(book_info)


# Recherche du bouton next pour aller à la page suivante s'il y en a une
def get_next_page_url(soup, current_url):
    next_button = soup.find("li", class_="next")
    if next_button and next_button.find("a"):
        next_url = next_button.find("a")["href"]
        current_url = current_url.replace("index.html", "") + next_url
        return current_url
    else:
        print("Pas d'autres pages.")
        return None


# Fonction pour extraire les informations d'un livre à partir de sa page produit
def get_book_info(product_page_url):
    response = requests.get(product_page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    upc = soup.find("th", string="UPC").find_next_sibling("td").text.strip()
    title = soup.find("title").text.split("|")[0].strip()
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text.strip().replace("Â£", "£")
    price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").text.strip().replace("Â£", "£")
    number_available = soup.find("p", class_="instock availability").find("i").find_next_sibling(string=True).strip()
    product_description = soup.find("h2", string="Product Description").find_next("p").get_text()
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    review_rating = soup.find("p", class_="star-rating").get("class")[-1]
    image_url = base_url + soup.find("img")["src"].replace('../', '')
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
    return book_info

get_all_mystery_books(base_url)
