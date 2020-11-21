import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def fetch_num_in_stock(search_page):
    response = requests.get(search_page, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    grids = soup.find_all(class_="category-products")
    count = 0
    for grid in grids:
        res = grid.find_all(text="Add to Cart")
        count += len(res)
    return count
