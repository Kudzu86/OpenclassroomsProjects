import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://books.toscrape.com/catalogue/"

# Définition d'une fonction pour obtenir tous les liens des livres appartenant à la catégorie mystery
def get_all_mystery_books(base_url):
    url = f"{base_url}category/books/mystery_3/index.html"
    csv_filename = "Projet2.csv"

    
    # Ouverture d'un fichier CSV en mode écriture
    # newline="" est utilisé pour éviter l'ajout de lignes vides sur Windows
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "product_page_url", "upc", "title", "price_excluding_tax",
            "price_including_tax", "number_available", "product_description",
            "category", "review_rating", "image_url"
        ])

        # Boucle qui va itérer les différentes pages de la catégorie
        while url:
            # Liste pour stocker les différents liens de livre de la catégorie
            links = []

            response = requests.get(url) # On récupère le code HTML
            soup = BeautifulSoup(response.text, features="html.parser")
            
            # Boucle for pour trouver tous les éléments h3 et extraire l'url de la balise a href
            for h3 in soup.find_all("h3"):
                href = h3.find("a")["href"][9:]
                product_page_url = base_url + href
                links.append(product_page_url)
            print(links)
            
            # Boucle for pour extraire le code HTML de chaque page produit
            for product_page_url in links:
                book_response = requests.get(product_page_url)
                book_soup = BeautifulSoup(book_response.text, features="html.parser")

                # Extraction des données de la page produit grace à la fonction get_book_info
                book_info = get_book_info(book_soup, product_page_url)
                if book_info:
                    print("Book Info:", book_info)

                    # Ecriture des informations du livre dans le CSV
                    writer.writerow([book_info[key] for key in book_info])

            # Recherche du bouton next pour aller a la page suivante s'il y en a une
            next_button = soup.find("li", class_="next")
            if next_button and next_button.find("a"):
                # Construction de l'url de la page suivante SANS URL JOIN
                next_url = next_button.find("a")["href"]
                url = url[:-10] + next_url
            else:
                print("Pas d'autres pages.")
                break

# Définition d'une fonction pour récupérer les informations d'un livre depuis sa page produit
def get_book_info(soup, product_page_url):
    try:
        
        upc_element = soup.find("th", string="UPC")
        if upc_element:
            upc = upc_element.find_next_sibling("td").text.strip()
            print("Code UPC:", upc) 
        else:
            print("Code UPC non trouvé pour:", product_page_url)
            return None

        title_element = soup.find("title")
        if not title_element:
            print("Titre non trouvé pour:", product_page_url)
            return None
        title = title_element.text.split("|")[0].strip()
        print("Titre:", title)

        price_excluding_tax_element = soup.find("th", string="Price (excl. tax)")
        if not price_excluding_tax_element:
            print("Prix hors taxe non trouvé pour:", product_page_url)
            return None
        price_excluding_tax = price_excluding_tax_element.find_next_sibling("td").text.strip().replace("Â£", "£")
        print("Prix hors taxe:", price_excluding_tax)  

        price_including_tax_element = soup.find("th", string="Price (incl. tax)")
        if not price_including_tax_element:
            print("Prix incluant la taxe non trouvé pour:", product_page_url)
            return None
        price_including_tax = price_including_tax_element.find_next_sibling("td").text.strip().replace("Â£", "£")
        print("Prix incluant la taxe:", price_including_tax)  

        number_available_element = soup.find("p", class_="instock availability")
        if not number_available_element:
            print("Nombre disponible non trouvé pour:", product_page_url)
            return None
        number_available = number_available_element.find("i").find_next_sibling(string=True).strip()
        print("Nombre disponible:", number_available)  

        product_description_element = soup.find("h2", string="Product Description")
        if not product_description_element:
            print("Description du produit non trouvée pour:", product_page_url)
            return None
        product_description = product_description_element.find_next("p").get_text()
        print("Description du produit:", product_description)  

        category_element = soup.find("ul", class_="breadcrumb").find_all("li")[2]
        if not category_element:
            print("Catégorie non trouvée pour:", product_page_url)
            return None
        category = category_element.text.strip()
        print("Catégorie:", category)  

        review_rating_element = soup.find("p", class_="star-rating")
        if not review_rating_element:
            print("Évaluation de la critique non trouvée pour:", product_page_url)
            return None
        review_rating = review_rating_element.get("class")[-1]
        print("Évaluation de la critique:", review_rating)  

        image_url_element = soup.find("img")
        if not image_url_element:
            print("URL de l'image non trouvée pour:", product_page_url)
            return None
        image_url = base_url + image_url_element["src"].replace('../', '')
        print("URL de l'image:", image_url)  

        return {
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

    except Exception as e:
        print(f"Erreur lors du traitement du livre à {product_page_url}: {e}")
        return None

get_all_mystery_books(base_url)



"""

import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://books.toscrape.com/catalogue/"

def get_all_mystery_books(base_url):
    url = f"{base_url}category/books/mystery_3/index.html"
    csv_filename = "Projet2.csv"

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "product_page_url", "upc", "title", "price_excluding_tax",
            "price_including_tax", "number_available", "product_description",
            "category", "review_rating", "image_url"
        ])

        while url:
            links = []

            response = requests.get(url)
            soup = BeautifulSoup(response.text, features="html.parser")

            for h3 in soup.find_all("h3"):
                href = h3.find("a")["href"][9:]
                product_page_url = base_url + href
                links.append(product_page_url)

            for product_page_url in links:
                book_response = requests.get(product_page_url)
                book_soup = BeautifulSoup(book_response.text, features="html.parser")

                book_info = get_book_info(book_soup, product_page_url)
                writer.writerow([book_info[key] for key in book_info])

            next_button = soup.find("li", class_="next")
            if next_button and next_button.find("a"):
                next_url = next_button.find("a")["href"]
                url = url[:-10] + next_url
            else:
                break
                


def get_book_info(soup, product_page_url):
    upc = soup.find("th", string="UPC").find_next_sibling("td").text.strip()
    title = soup.find("title").text.split("|")[0].strip()
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text.strip().replace("Â£", "£")
    price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").text.strip().replace("Â£", "£")
    number_available = soup.find("p", class_="instock availability").find("i").find_next_sibling(string=True).strip()
    product_description = soup.find("h2", string="Product Description").find_next("p").get_text()
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    review_rating = soup.find("p", class_="star-rating").get("class")[-1]
    image_url = base_url + soup.find("img")["src"].replace('../', '')

    return {
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

    
get_all_mystery_books(base_url)
"""