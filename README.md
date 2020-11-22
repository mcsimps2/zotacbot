# zotacbot
## Installation
Make sure you have Python3 installed.  Clone the repo.
```
git clone https://github.com/mcsimps2/zotacbot.git
```

Install dependencies.
```
pip3 install pipenv
pipenv install
```

## Setup
1. Make a Zotac account here: [https://www.zotacstore.com/us/customer/account/create/](https://www.zotacstore.com/us/customer/account/create/)
1. Go to your address book and add your shipping and billing addresses: [https://www.zotacstore.com/us/customer/address/](https://www.zotacstore.com/us/customer/address/)
1. Go ahead and add any item to your cart and go through the checkout process, but don't actually buy the item.  This will let you set your default preferences for your shipping address for checkout and allow the bot to skip this step.  After you have gotten to the last step, you will be redirected to PayPal.  Go ahead and cancel the checkout and empty your cart.

## Running the bot
Source your virtual environment.
```
pipenv shell
```

Set your username and password in `main.py`.
```
USERNAME = "john_doe@gmail.com
PASSWORD = "mysecurepassword"
```

Alter the product list in order of which graphics card you want the most.  Remove any graphics cards you don't want.  The bot buy the first available graphics card in your preference list.  It will attempt to buy the graphics cards in the order they are listed in the `PRODUCTS` variable.
```
# Preference list - bot will try to buy the 3070 OC before the 3080s.  It will not buy the 3090.
PRODUCTS = [
    "ZOTAC GAMING GeForce RTX 3070 Twin Edge OC",
    "ZOTAC GAMING GeForce RTX 3070 Twin Edge",
    "ZOTAC GAMING GeForce RTX 3080 Trinity OC",
    "ZOTAC GAMING GeForce RTX 3080 Trinity",
    "ZOTAC GAMING GeForce RTX 3080 AMP Holo",
]
```

Set the `POLL` time to how often you want to check the website.  As you approach 9:40 PM, you may want to change this to every 10 seconds are so.

The `SEARCH_PAGE` page is set to the 3070/3080/3090 search page.  If you want to buy a different graphics card, change the `SEARCH_PAGE` variable.

Run the program.
```
python main.py
```

Use `Ctrl + C` to stop the program from running - you may have to do this several times.

## How the bot works
The bot will start by logging in.
It will then clear your basket to make sure it is empty.
Afterwards, it will keep trying to add graphics cards to the basket.  It will usually stay in this state until graphics card stock is added.  You will probably see print statements saying "No add to cart links found" for a while.  When an "Add to Cart" link finally becomes available, you will receive sound alerts, so make sure your volume is on.
The bot will then generate a PayPal link for you to checkout.  Copy/paste the link in your browser.

## Troubleshooting
The Zotac website often crashes during re-stocks.  In these scenarious, the bot will continue to retry operations.
Sometimes these crashes reset your shopping cart.  In this case, restart the bot.
Sometimes, these crashes will log the bot out.  In this case, restart the bot.
If the PayPal link is not generated correctly, the item will still be in your cart.  Go to the [Zotac Store](https://www.zotacstore.com/us/), login, and checkout manually.
The bot has been tested on Mac.  It should work on Windows as well, but this has not been verified.
