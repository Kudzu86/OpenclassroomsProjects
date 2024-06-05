import requests
from bs4 import BeautifulSoup
import csv
import os

base_url = "https://books.toscrape.com/"    



# Fonction qui récupère les liens de toutes les catégories
def get_all_category(base_url):
    url = base_url + "index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    categories = []

    for category in soup.find("ul", class_="nav nav-list").find("ul").find_all("li"):
        category_name = category.get_text().strip()
        relative_url = category.find("a")["href"]
        category_url = base_url + relative_url.replace("../", "")
        categories.append({"name": category_name, "url": category_url})

    return categories



# Fonction qui récupère tous les liens des livres dans une catégorie
def get_book_url_from_category(category_url):
    category_books_url = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, features="html.parser")
        for h3 in soup.find_all("h3"):
            href = h3.find("a")["href"]
            product_page_url = base_url + href.replace("../../../" , "catalogue/")               
            category_books_url.append(product_page_url)
        category_url = get_next_page_url(soup, category_url)
    return category_books_url



# Fonction qui recherche du bouton next pour aller à la page suivante s'il y en a une
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
def get_book_info(product_page_url, category_directory):
    response = requests.get(product_page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    upc = soup.find("th", string="UPC").find_next_sibling("td").text.strip()
    title = soup.find("title").text.split("|")[0].strip()
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text.strip().replace("Â£", "£")
    price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").text.strip().replace("Â£", "£")
    number_available = soup.find("p", class_="instock availability").find("i").find_next_sibling(string=True).strip()
    try: 
        product_description = soup.find("h2", string="Product Description").find_next("p").get_text()
    except:
        product_description = "Pas de description pour ce livre"
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    review_rating = soup.find("p", class_="star-rating").get("class")[-1]
    image_url = base_url + soup.find("img")["src"].replace('../', '')
    image_filename = get_img(image_url, title, category_directory)
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




# Fonction qui télécharge l'image de couverture de chaque livre et l'enregistre dans le répertoire de la catégorie correspondante
def get_img(image_url, title, category_directory):
    valid_title = "".join(c for c in title[:50] if c.isalnum() or c in (" ", "-", "_")).rstrip()
    valid_title = valid_title.replace("Ã", "é")
    image_filename = os.path.join(category_directory, f"{valid_title}.jpg")
    with open(image_filename, "wb") as img:
        image_response = requests.get(image_url)
        img.write(image_response.content)
    return image_filename



# Fonction globale qui récupère toutes les infos de tous les livres du site
def get_all_books(base_url):
    categories = get_all_category(base_url)
    all_books_url = []

    for category in categories:
        print(f"Catégorie en cours : {category['name']}")
        category_books = get_book_url_from_category(category['url'])
        category_directory = os.path.join("Books", category['name'])
        os.makedirs(category_directory, exist_ok=True)
        csv_filename = f"{category['name'].replace(' ', '_')}.csv"

        create_csv_file(csv_filename, category_books, category_directory)




# Fonction qui crée un fichier CSV avec écriture des infos extraites
def create_csv_file(csv_filename, all_books_url, category_directory):
    csv_filename = os.path.join(category_directory, csv_filename)

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        if not all_books_url:
            print("Aucun livre trouvé.")
            return

        # Obtenir les clés du premier dictionnaire pour déterminer les fieldnames
        first_book_info = get_book_info(all_books_url[0], category_directory)
        fieldnames = list(first_book_info.keys())

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for product_page_url in all_books_url:
            book_info = get_book_info(product_page_url, category_directory)
            if book_info:
                writer.writerow(book_info)



    
    
get_all_books(base_url)
