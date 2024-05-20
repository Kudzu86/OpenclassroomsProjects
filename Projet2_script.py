import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Fonction pour extraire les informations d'un livre
def extract_book_data(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text.strip()
    upc = soup.find('th', string='UPC').find_next_sibling('td').text.strip()
    price_including_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text.strip()
    price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text.strip()
    availability = soup.find('th', string='Availability').find_next_sibling('td').text.strip()
    availability = ''.join(filter(str.isdigit, availability))
    description = soup.find('meta', {'name': 'description'})['content'].strip()
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = soup.find('img')['src']
    image_url = urljoin(product_url, image_url)
    return {
        'title': title,
        'upc': upc,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'availability': availability,
        'description': description,
        'category': category,
        'rating': rating,
        'image_url': image_url
    }

# Fonction pour extraire les URLs des pages produits de la catégorie
def extract_product_urls(category_url):
    product_urls = []
    while True:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Trouver tous les liens vers les pages produits sur la page de la catégorie
        links = soup.find_all('h3')
        for link in links:
            product_urls.append(urljoin(category_url, link.a['href']))
        # Trouver le lien vers la page suivante de la catégorie
        next_page = soup.find('li', class_='next')
        if next_page:
            category_url = urljoin(category_url, next_page.a['href'])
        else:
            break
    return product_urls

# Fonction principale pour récupérer les informations de tous les livres d'une catégorie
def scrape_category(category_url):
    product_urls = extract_product_urls(category_url)
    all_book_data = []
    for product_url in product_urls:
        book_data = extract_book_data(product_url)
        all_book_data.append(book_data)
    return all_book_data

# Exemple d'utilisation
if __name__ == "__main__":
    # URL de la catégorie choisie
    category_url = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
    category_book_data = scrape_category(category_url)

    # Nom du fichier CSV
    csv_filename = 'Projet2.csv'

    # Enregistrement des données dans un fichier CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=category_book_data[0].keys())
        writer.writeheader()
        for book_data in category_book_data:
            writer.writerow(book_data)

    print(f"Les informations des livres de la catégorie ont été enregistrées dans {csv_filename}")