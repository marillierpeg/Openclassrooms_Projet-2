#Extrait les données et images de tous les livres de toutes les categories


import functions as fs
    

if __name__ == "__main__":
    fs.scrape_all(fs.jolie_soupe(fs.root_url))