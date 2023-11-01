#import des modules/packages nécessaires
import requests
from bs4 import BeautifulSoup
import csv
import time
import os


#variables et constantes
root_url = "https://books.toscrape.com/"
category_url = "https://books.toscrape.com/catalogue/"
en_tete = ["upc", "title", "price excluding_tax", "price including tax", "number available", "product description", "category", "review rating", "url", "image url"]

#parse une URL si celle-ci est correcte et accessible
def jolie_soupe(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        print ("L'URL saisie n'existe pas, merci de relancer le programme avec une URL valide")
        time.sleep(5)
        exit()  
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


#créé une liste des url de chaque livre pour une catégorie quel que soit le nombre de page de la catégorie
def url_books(url_category):
    soup = jolie_soupe(url_category)
    next_page = soup.find("li", class_ = "next")
    list_url_books = []

    if not next_page:
        url_book = soup.find(class_ = "row").findAllNext("h3")
        for link in url_book:
            links = category_url + link.find("a").get("href").replace("../../../", "")
            list_url_books.append(links)
    else:
        page_number = soup.find('li', class_='current').text.replace("\n", "").replace("  ","").split().pop(3)
        page_number = int(page_number)

        for i in range(0, page_number):
            new_url = url_category.replace("index", "page-" + str(i+1))
            soup = jolie_soupe(new_url)
            url_book = soup.find(class_ = "row").findAllNext("h3")
            for link in url_book:
                links = category_url + link.find("a").get("href").replace("../../../", "")
                list_url_books.append(links)
    return list_url_books


#récupère toutes les information d'un livre
def scrape_one_book(soup, url_book):
    upc= soup.find(string='UPC').findNext('td').text  
    title = soup.find("h1").text
    number_available = soup.find(string = "Availability").find_next("td").text.removeprefix('In stock (').removesuffix(' available)')
    product_description = soup.find(id = "product_description")
    if product_description is not None:
        product_description = product_description.find_next("p").text.replace("...more", "")
    else:
        product_description = "pas de description"
    book_category = soup.find(class_ = "breadcrumb").findAll("a")[-1].text
    review_rating = soup.find("p", class_= "star-rating").get("class").pop() + " stars on five"
    image_url = soup.find(class_ = "item active").find_next("img").get("src").replace("../../", root_url)
    price_excluding_tax = soup.find(string ="Price (excl. tax)").findNext("td").text
    price_including_tax = soup.find(string ="Price (incl. tax)").findNext("td").text
    #convertir les prix en float pour éventuellement les utiliser en tant que nombres
    price_excluding_tax = float(price_excluding_tax[1:])
    price_including_tax = float(price_including_tax[1:])
    infos_book = [upc,title, price_excluding_tax,price_including_tax, number_available, product_description, book_category, review_rating, url_book, image_url]
    return infos_book


#récupère les infos de chaque livre d'une catégorie, les stocke dans un fichier CSV
#télécharge l'image associée à chaque livre
#créé une arborescence de dossiers
def scrape_books(url_category):
    category_name = url_category.split("/").pop(6).split("_").pop(0)
    filename = f"{category_name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}.csv"
    path = os. getcwd() #renvoie le dossier courant comme chemin
    if not os.path.exists(f"{path}/books_to_scrape/{category_name}"):
        os.makedirs(f"{path}/books_to_scrape/{category_name}")
    with open(f"{path}/books_to_scrape/{category_name}/{filename}", "a", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(en_tete)
        soup = jolie_soupe(url_category)
        list_url_books = url_books(url_category)
        for url_book in list_url_books:
            soup = jolie_soupe(url_book)
            writer.writerow(scrape_one_book(soup, url_book))
            book_name = soup.find("h1").text[:10].replace(":","").replace("/","").replace("?","").replace('"',"")
            image_name = book_name + ".jpg"
            image_url = soup.find(class_ = "item active").find_next("img").get("src").replace("../../", root_url)
            load_image = requests.get(image_url)
            path = os. getcwd() #renvoie le dossier courant comme chemin
            if not os.path.exists(f"{path}/books_to_scrape/{category_name}/images"):
                    os.makedirs(f"{path}/books_to_scrape/{category_name}/images")#créé le dossier si il n'existe pas
            with open(f"{path}/books_to_scrape/{category_name}/images/{image_name}", "wb") as f:
                f.write(load_image.content)
                os.chdir(f'{path}/')

#télécharge l'image d'un livre et la nomme avec le titre du livre (10 premiers caractères)
def download_image(url_book):
    soup = jolie_soupe(url_book)
    book_name = soup.find("h1").text[:10].replace(":","").replace("/","").replace("?","").replace('"',"").replace(" ","")
    image_name = book_name + ".jpg"
    image_url = soup.find(class_ = "item active").find_next("img").get("src").replace("../../", root_url)
    load_image = requests.get(image_url)
    path = os. getcwd() #renvoie le dossier courant comme chemin
    if not os.path.exists(f"{path}/{book_name}"):
            os.makedirs(f"{path}/{book_name}")#créé le dossier si il n'existe pas
    with open(f"{path}/{book_name}/{image_name}", "wb") as f:
        f.write(load_image.content)
        os.chdir(f'{path}/')

#créé fichier csv et arborescence dossiers
def make_csv(url_book):
    soup = jolie_soupe(url_book)
    book_name = soup.find("h1").text[:10].replace(":","").replace("/","").replace("?","").replace('"',"").replace("-","").replace(" ","")
    filename = f"{book_name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}.csv"
    path = os. getcwd() #renvoie le dossier courant comme chemin
    if not os.path.exists(f"{path}/{book_name}"):
            os.makedirs(f"{path}/{book_name}")#créé le dossier si il n'existe pas
    with open(f"{path}/{book_name}/{filename}", "w", encoding="utf-8-sig",) as file:
        writer = csv.writer(file, delimiter= ",")
        writer.writerow(en_tete)
        writer.writerow(scrape_one_book(soup, url_book))



#demande à l'utilisateur de choisir parmi la liste de catégories, celle dont il souhaite extraire les données
def category_choice(root_url):
    dict_cat = {}
    soup = jolie_soupe(root_url)

    list_url_cat = get_url_categories(soup)
    for url in list_url_cat:
        category_name = url.split("/").pop(6).split("_").pop(0)
        dict_cat[category_name] = url
    categories = list(dict_cat.keys())

    try:
        while True:
            for i, categorie in enumerate(categories, start=1):
                print(f"{i}.{categorie}")
            choice = input("Merci d'entrer le numéro de la catégorie que vous souhaitez extraire : ")

            user_choice = int(choice) - 1
            if 1 <= user_choice <= len(categories):
                break
            else:
                print("numéro invalide")
    except ValueError:
        print("Veuillez entrer un numéro valide")
    except requests.exceptions.HTTPError:
        print("Le site Web est en panne ou le HTML est modifié.")

    category_chosen = categories[user_choice]
    print(f"vous avez choisi la catégorie :  {category_chosen}")
    url_category = list(dict_cat.values())
    url_to_scrape = url_category[user_choice]
    print("début de l'extraction")

    return url_to_scrape

#extrait les données de tous les livres de toutes les catégories
def scrape_all(soup):
    list_url_categories = get_url_categories(soup)
    print("Début de l'extraction de données")
    for url_category in list_url_categories:
        category_name = url_category.split("/").pop(6).split("_").pop(0)
        print(f"Extraction en cours de la catégorie {category_name} ({list_url_categories.index(url_category)+1}/{len(list_url_categories)})")
        scrape_books(url_category)

