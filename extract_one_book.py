#import des modules nécessaires
import csv
import time
import functions as fs

url = "http://books.toscrape.com/catalogue/the-picture-of-dorian-gray_270/index.html"


if __name__ == "__main__":
#créer un nom de fichier unique
    soup = fs.jolie_soupe(url)
    book_name = url.split("/").pop(4)[:20]
    filename = f"{book_name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}.csv"
#création d'un fichier CSV regroupant les informations du livre
    en_tete = ["upc", "title", "price excluding_tax", "price including tax", "number available", "product description", "category", "review rating", "url", "image url"]
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter= ",")
        writer.writerow(en_tete)
        writer.writerow(fs.scrape_one_book(soup, url))
    
