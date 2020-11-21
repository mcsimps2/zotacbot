from zotacbot import ZotacBot, StockBot


USERNAME = ""
PASSWORD = ""
# List in order of preference - only one will be bought
PRODUCTS = [
    "ZOTAC GAMING GeForce RTX 3070 Twin Edge OC",
    "ZOTAC GAMING GeForce RTX 3070 Twin Edge",
    "ZOTAC GAMING GeForce RTX 3080 Trinity OC",
    "ZOTAC GAMING GeForce RTX 3080 Trinity",
    "ZOTAC GAMING GeForce RTX 3080 AMP Holo",
]
POLL = 60
CLEAR_BASKET = True
SEARCH_PAGE = "https://www.zotacstore.com/us/graphics-cards?cat=494"
# SEARCH_PAGE = "https://www.zotacstore.com/us/graphics-cards"


if __name__ == "__main__":
    checkout_bot = ZotacBot(
        username=USERNAME,
        password=PASSWORD,
        search_page=SEARCH_PAGE,
        products=PRODUCTS,
        poll=POLL,
        clear_basket=CLEAR_BASKET,
    )
    checkout_bot.start()

    # stock_bot = StockBot(
    #     search_page=SEARCH_PAGE,
    #     poll=POLL
    # )
    # stock_bot.start()
    # stock_bot.join()

    checkout_bot.join()
