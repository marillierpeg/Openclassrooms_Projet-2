#import des packages / modules nécessaires
import functions as fs



print("Entrer l'url du livre dont vous souhaitez extraire les informations")
url = input()


if __name__ == "__main__":
#création d'un fichier CSV regroupant les informations du livre
    print("début de l'extraction")
    fs.make_csv(url)
#récupère l'image associée au livre    
    fs.download_image(url)
    print("Extraction terminée")
