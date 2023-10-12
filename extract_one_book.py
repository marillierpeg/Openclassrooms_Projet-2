
#import des modules nécessaires
import requests
from bs4 import BeautifulSoup
import csv
import time

#url choisie
url = "http://books.toscrape.com/catalogue/the-picture-of-dorian-gray_270/index.html"

#parser la page uniquement si la page répond
page = requests.get(url)
if page.ok:
    soup = BeautifulSoup(page.content, "html.parser")
else:
    print("la page demandée ne répond pas")


#récupérer chaque information du livre
upc = soup.find(string ='UPC').findNext('td').text
title = soup.find("h1").text
number_available = soup.find(string = "Availability").find_next("td").text
product_description = soup.find(id = "product_description").find_next("p").text.replace("...more", "")
book_category = soup.find("ul", attrs = {"class": "breadcrumb"}).find_all("a")[2].text
review_rating = soup.find("p", class_= "star-rating").get("class").pop() + " stars on five"
print(review_rating)
image_url = soup.find(class_ = "item active").find_next("img").get("src").replace("../..", "http://books.toscrape.com")

price_excluding_tax = soup.find(string ="Price (excl. tax)").findNext("td").text
price_including_tax = soup.find(string ="Price (incl. tax)").findNext("td").text
#convertir les prix en float pour éventuellement les utiliser en tant que nombres
price_excluding_tax = float(price_excluding_tax[1:])
price_including_tax = float(price_including_tax[1:]) 


#créer un nom de fichier unique
fichier = f"{title}_{time.strftime('%Y_%m_%d_%H_%M_%S')}.csv"

#création d'un fichier CSV regroupant les informations du livre
infos = [url, upc, title, price_excluding_tax, price_including_tax, number_available, product_description, book_category, review_rating, image_url]
en_tete = ["url", "upc", "title", "price excluding_tax", "price including tax", "number available", "product description", "category", "review rating", "image url"]


with open(fichier, 'w', encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter= ",")
    writer.writerow(en_tete)
    writer.writerow(infos)