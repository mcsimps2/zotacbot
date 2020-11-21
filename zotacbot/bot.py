import os
import time
from threading import Thread

from requests import RequestException

from . import zotac
from .client import Client
from .stock import fetch_num_in_stock


RETRY_WAIT = 0.25


def try_until_success(f, wait=RETRY_WAIT):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except Exception as e:
                print(f"Exception in {f}: {e}")
                time.sleep(wait)

    return wrapper


class ZotacBot(Thread):
    def __init__(
        self,
        username,
        password,
        search_page,
        products,
        poll,
        clear_basket=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.session = Client()
        self.username = username
        self.password = password
        self.search_page = search_page
        self.products = products
        self.poll = poll
        self.clear_basket = clear_basket

    def run(self) -> None:
        try_until_success(zotac.login)(self.session, self.username, self.password)
        if self.clear_basket:
            try_until_success(zotac.clear_basket)(self.session)
        try_until_success(zotac.add_one_to_basket, wait=self.poll)(
            self.session, self.search_page, self.products
        )
        checkout_url = try_until_success(zotac.checkout)(self.session)
        while True:
            print(checkout_url)
            os.system("say CHECKOUT LINK GENERATED")
            time.sleep(1)


class StockBot(Thread):
    def __init__(self, search_page, poll, *args, **kwargs):
        self.search_page = search_page
        self.poll = poll

    def run_job(self):
        try:
            num_in_stock = fetch_num_in_stock(self.search_page)
            if num_in_stock:
                print(f"FOUND {num_in_stock} IN STOCK")
                while True:
                    os.system("say GRAPHICS CARD IN STOCK")
                    time.sleep(0.5)
            else:
                print("Nothing in stock")
        except RequestException as e:
            print(e)
            os.system("say Webpage under heavy load, possible incoming stock")
        except Exception as e:
            print(e)

    def run(self) -> None:
        while True:
            self.run_job()
            time.sleep(self.poll)

