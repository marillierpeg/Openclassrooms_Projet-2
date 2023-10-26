import functions as fs

url = "http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"


if __name__ == "__main__":
    fs.scrape_books(url)