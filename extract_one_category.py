#Extrait les données et images de tous les livres d'une catégorie

import functions as fs



if __name__ == "__main__":
    fs.scrape_books(fs.category_choice(fs.root_url))
    print("extraction terminée")