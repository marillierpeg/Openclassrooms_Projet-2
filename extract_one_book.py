
#import des modules nécessaires
import requests
from bs4 import BeautifulSoup
import csv

#url choisie
url = "http://books.toscrape.com/catalogue/the-picture-of-dorian-gray_270/index.html"

#parser la page uniquement si la page répond
page = requests.get(url)
if page.ok:
    soup = BeautifulSoup(page.content, "html.parser")

#récupérer tous les "td" de la page
listetd = soup.find_all("td")

#récupérer chaque information du livre
upc = listetd[0].text
title = soup.find("h1").text
price_excluding_tax = listetd[2].text
price_including_tax = listetd[3].text
number_available = listetd[5].text
product_description = soup.find(id = "product_description").find_next("p").text.replace("...more", "")
category = soup.find("ul", attrs = {"class": "breadcrumb"}).find_all("a")[2].text
review_rating = soup.find("p", class_='star-rating').get('class').pop() + " stars on five"
image_url = soup.find(class_ = "item active").find_next("img").get("src").replace("../..", "http://books.toscrape.com")


#création d'un fichier CSV regroupant les infos du livre
infos = [url, upc, title, price_excluding_tax, price_including_tax, number_available, product_description, category, review_rating, image_url]
en_tete = ["url", "upc", "title", "price excluding_tax", "price including tax", "number available", "product description", "category", "review rating", "image url"]

with open('book.csv', 'w', encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter= ",")
    writer.writerow(en_tete)
    writer.writerow(infos)


