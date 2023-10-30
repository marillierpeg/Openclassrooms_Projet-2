import requests
from bs4 import BeautifulSoup
import csv
import time
import functions as fs
import urllib.request

url = "https://books.toscrape.com/"
soup = fs.jolie_soupe(url)



list_url_categories = fs.get_url_categories(soup)
for url_category in list_url_categories:
    print(f"url catégorie: {url_category}")
    fs.scrape_books(url_category)
       
    





# if __name__ == "__main__":
#     scrape_all_books(url)