# Présentation
Ce projet a pour but d'extraire les données et images de tous les livres présents sur le site [books to scrape](https://books.toscrape.com/)
Le programme **"main"** va créer une arborescence à la racine du dossier depuis lequel vous lancez le programme. Le dossier books_to_scrape est créé, il contiendra un dossier par catégorie. Dans chacun de ces dossiers vous trouverez le fichier csv contenant toutes les informations extraites telles que les titres, les prix, les descriptions,... ainsi qu'un dossier "images" contenant toutes les couvertures de livres de la catégorie.

Le programme **"extract_one_category"**, une fois lancé, demandera à l'utilisateur de choisir quelle catégorie il souhaite extraire parmi la liste affichée. Il créera alors une arborescence sur le même modèle que le programme "main".

Et enfin le programme **"extract_one_book"**, demandera à l'utilisateur de saisir l'url du livre dont il souhaite extraire les informations.

# Instructions
## Prérequis
Avoir installé une version de Python égale ou supérieure à la 3.11.5

## Récupérer le programme

Téléchargement du dossier zip:
[en cliquant ici](https://github.com/marillierpeg/Openclassrooms_Projet-2.git)

Choisissez l'endroit où vous souhaitez le dézipper. C'est dans ce dossier que le programme stockera les fichiers extraits après lancement.

## Environnement virtuel
Principalement pour des raisons de compatibilité de versions et ainsi éviter tout bug du à des conflits de versions des librairies/packages utilisés, il est fortement conseillé de travailler au sein d'un environnement virtuel.

Commencez par utiliser votre terminal pour vous place dans le dossier que vous avez choisi pour dézipper.

#### Créer l'environnement virtuel

saisir la commande  suivante :
```
python -m venv env
```

#### Lancer l'environnement virtuel :

* saisir la commande  suivante  **sous Windows** :
```
env\Scripts\activate.bat
```

* saisir cette commande sous **Linux / Mac** :

```
source env/bin/activate
```

#### Installation des librairies/packages nécessaires :
```
pip install -r requirements.txt
```
Vous pouvez contrôler lesquels se sont installés avec la commande suivante : 
```
pip freeze
```


### Lancement des programmes

1. Pour l'extraction de données d'un seul livre :
Rendez-vous sur le site [books to scrape](https://books.toscrape.com/) et copier l'url du livre souhaité puis dans votre terminal saisir la commande suivante :
   ```
   python extract_one_book.py
    ```
2. Pour l'extraction de données d'une catégorie entière de livres, saisissez la commande suivante :
   ```
   python extract_one_category.py
   ```
3. Pour l'extraction de toutes les données du site, saisissez la commande suivante :
   ```
   python main.py
   ```