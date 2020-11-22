from bs4 import BeautifulSoup
from typing import List

from .client import Client


LOGIN_PAGE = "https://www.zotacstore.com/us/customer/account/login/"
LOGIN_URL = "https://www.zotacstore.com/us/customer/account/loginPost/"
BASKET_PAGE = "https://www.zotacstore.com/us/checkout/cart/"
UPDATE_BASKET_URL = "https://www.zotacstore.com/us/checkout/cart/updatePost/"
PAYPAL_PAGE = "https://www.zotacstore.com/us/paypal/express/start/"


class OperationFailure(Exception):
    pass


def _get_soup(response):
    return BeautifulSoup(response.text, "html.parser")


def _parse_form_key(soup):
    return soup.find("input", {"name": "form_key"})["value"]


def _get_form_key(session: Client, page_url: str):
    response = session.get(page_url)
    soup = _get_soup(response)
    return _parse_form_key(soup)


def login(session: Client, username: str, password: str):
    print(f"Attempting to log in as {username}")
    # Load the login page to get any cookies, etc...
    print("Loading login page")
    form_key = _get_form_key(session, LOGIN_PAGE)
    print(f"Login CSRF form key is {form_key}")
    # Post login credentials
    headers = {
        "authority": "www.zotacstore.com",
        "cache-control": "max-age=0",
        "origin": "https://www.zotacstore.com",
        "upgrade-insecure-requests": "1",
        "dnt": "1",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": LOGIN_PAGE,
        "accept-language": "en-US,en;q=0.9",
    }

    data = {
        "form_key": form_key,
        "login[username]": username,
        "login[password]": password,
        "send": "",
    }
    print("Sending credentials via POST")
    response = session.post(LOGIN_URL, data=data, headers=headers)
    soup = _get_soup(response)
    err_li = soup.find_all(class_="error-msg")
    for child in err_li:
        if child.find_all(text="Invalid login or password."):
            raise OperationFailure("Invalid login credentials")
    if "My Account" not in soup.title.text:
        raise OperationFailure(
            "Did not end up on the My Account page - check login credentials"
        )
    print(f"Successfully logged in")
    return response


def _check_basket(session: Client):
    response = session.get(BASKET_PAGE)
    soup = _get_soup(response)
    empty_p = soup.find("p", {"class": "empty"})
    if empty_p and "You have no items" in empty_p.text:
        return None, None, None
    form_key = _parse_form_key(soup)
    return response, soup, form_key


def clear_basket(session: Client):
    print(f"Loading basket page")
    response, soup, form_key = _check_basket(session)
    print(f"Basket CSRF form key is {form_key}")
    if not response:
        print("Basket is already empty")
        return
    headers = {
        "authority": "www.zotacstore.com",
        "cache-control": "max-age=0",
        "origin": "https://www.zotacstore.com",
        "upgrade-insecure-requests": "1",
        "dnt": "1",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": BASKET_PAGE,
        "accept-language": "en-US,en;q=0.9",
    }

    data = {"form_key": form_key, "update_cart_action": "empty_cart"}
    print("Clearing basket via POST")
    response = session.post(UPDATE_BASKET_URL, headers=headers, data=data)
    soup = _get_soup(response)
    empty_p = soup.find("p", {"class": "empty"})
    if not empty_p or "You have no items" not in empty_p.text:
        raise OperationFailure("Did not clear basket successfully")
    print("Successfully cleared basket")
    return response


def add_one_to_basket(session: Client, search_page, product_titles: List[str]):
    print("Loading product page")
    response = session.get(search_page)
    soup = _get_soup(response)
    details = soup.find_all(class_="product-details")
    link = None
    product = None
    for detail in details:
        for product_title in product_titles:
            if detail.find("a", {"title": product_title}):
                buttons = detail.find_all("button", {"title": "Add to Cart"})
                if buttons:
                    link = buttons[0]["onclick"].split("'")[1]
                    product = product_title
                    break
    if not link:
        raise OperationFailure(f"No add to cart links found")
    print(f"Adding {product} to cart via {link}")
    response = session.get(link)
    print("Successfully added to cart")
    return response


def checkout(session: Client):
    print("Attempting to generate PayPal express checkout")
    response = session.get(PAYPAL_PAGE, allow_redirects=False)
    redirect_url = response.headers["Location"]
    if "paypal.com" not in redirect_url.lower():
        raise OperationFailure(
            "Failed to start PayPal express checkout. "
            "Make sure your shipping address has been saved. "
            "Otherwise, go here to try manually "
            "(Your basket still has your items, but you must log in first.): "
            "https://www.zotacstore.com/us/checkout/onepage/"
        )
    return redirect_url
