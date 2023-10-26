import requests
from bs4 import BeautifulSoup
import csv
import time


#variables et constantes
root_url = "http://books.toscrape.com/"
catalogue_url = "/index.html"
books_url = "/catalogue/category/books/{category_name}/{page}.html"
book_detail_url = "/catalogue/{book_id}/index.html"
list_categories = []
list_url_categories = []
en_tete = ["url", "upc", "title", "price excluding_tax", "price including tax", "number available", "product description", "category", "review rating", "image url"]

#parse la page si elle répond
def jolie_soupe(url):
    try:
        page = requests.get(url)    
    except IOError:
        print("Invalid URL")
    page = requests.get(url)    
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


#créé une liste des url de chaque catégorie
def get_url_categories(soup):
    list_url_categories = []
    url_category = soup.find(class_ = "nav-list").findAll("a")
    for link in url_category:
        links = root_url + link.get("href")
        list_url_categories.append(links)
    del(list_url_categories[0])
    return list_url_categories


#créé une liste des catégories
def get_categories(soup):
    list_categories = soup.find(class_ = "nav-list").find_next("li").text.replace(" ", "").replace("\n", " ").split()
    del(list_categories[0])
    return list_categories


#créé une liste des url de chaque livre pour une catégorie
def url_books(url_category):
    soup = jolie_soupe(url_category)
    next_page = soup.find("li", class_ = "next")
    list_url_books = []

    if not next_page:
        url_book = soup.find(class_ = "row").findAllNext("h3")
        for link in url_book:
            links = url_category[:27] + link.find("a").get("href").replace("../../..", "")
            list_url_books.append(links)
    else:
        page_number = soup.find('li', class_='current').text.replace("\n", "").replace("  ","").split().pop(3)
        page_number = int(page_number)

        for i in range(0, page_number):
            new_url = url_category.replace("index", "page-" + str(i+1))
            soup = jolie_soupe(new_url)
            url_book = soup.find(class_ = "row").findAllNext("h3")
            for link in url_book:
                links = new_url[:26] + link.find("a").get("href").replace("../../..", "catalogue")
                list_url_books.append(links)
    return list_url_books


#récupère toutes les information d'un livre
def scrape_one_book(soup, url_book):
    upc_element = soup.find(string='UPC')
    if upc_element:
        upc = upc_element.findNext('td').text
    else:
        upc = "Not available"    
    title = soup.find("h1").text
    number_available = soup.find(string = "Availability").find_next("td").text.removeprefix('In stock (').removesuffix(' available)')
    product_description = soup.find(id = "product_description").find_next("p").text.replace("...more", "")
    if product_description is not None:
        product_description = product_description
    else:
        product_description = "pas de description"
    book_category = soup.find(class_ = "breadcrumb").findAll("a")[-1].text
    review_rating = soup.find("p", class_= "star-rating").get("class").pop() + " stars on five"
    image_url = soup.find(class_ = "item active").find_next("img").get("src").replace("../..", "http://books.toscrape.com")
    price_excluding_tax = soup.find(string ="Price (excl. tax)").findNext("td").text
    price_including_tax = soup.find(string ="Price (incl. tax)").findNext("td").text
    #convertir les prix en float pour éventuellement les utiliser en tant que nombres
    price_excluding_tax = float(price_excluding_tax[1:])
    price_including_tax = float(price_including_tax[1:]) 
    infos_book = [upc,title, price_excluding_tax,price_including_tax, number_available, product_description, book_category, review_rating, url_book, image_url]
    return infos_book


#récupère les infos de chaque livre d'une catégorie et les stock dans un fichier CSV
def scrape_books(url_category):
    category_name = url_category.split("/").pop(6).split("_").pop(0)
    filename = f"{category_name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}.csv"
    with open(filename, "a", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["upc", "title", "price excluding_tax", "price including tax", "number available", "product description", "category", "review rating", "url", "image url"])
        soup = jolie_soupe(url_category)
        list_url_books = url_books(url_category)
        for url_book in list_url_books:
            soup = jolie_soupe(url_book)
            writer.writerow(scrape_one_book(soup, url_book))


