import requests
from bs4 import BeautifulSoup
import csv
import time


#scrap toutes les pages d'une catégorie et créé un fichier csv 
def scrape_books(csv_writer, page_number):
    url = f"http://books.toscrape.com/catalogue/category/books/fantasy_19/page-{page_number}.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    books = soup.find_all(class_ = "product_pod")

    for book in books:
        writer.writerow(get_book_info(book))


#récupère toutes les infos d'un livre
def get_book_info(book):
    image_url = book.find("img").get("src").replace("../..", "http://books.toscrape.com")
    title = book.find("h3").find_next("a").get("title")
    book_url = book.find("a").get("href").replace("../../..", "http://books.toscrape.com/catalogue")
    rating = book.find("p", class_='star-rating').get('class').pop()
    price = book.find("p", class_= "price_color").text
    price = float(price[1:])
    availability = book.find(class_ = "instock availability").text.strip()

    return [title, book_url, rating, price, availability, image_url]

if __name__ == "__main__":
    filename = f"fantasy_{time.strftime('%Y_%m_%d_%H_%M_%S')}.csv"

    with open(filename, "a", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "url_book", "rating", "price", "availability", "image_url"])

        for page_number in range(1, 5):
            scrape_books(writer, page_number)