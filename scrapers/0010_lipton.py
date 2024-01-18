from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 10
PRODUCER_NAME = "Lipton"
BASE_URL = r"https://www.lipton.com/"
headers = {
    "Host": BASE_URL,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
}


drinks_soup = BeautifulSoup(
    Path("downloaded_sites/0010_lipton.html").read_text(), "html.parser"
)

all_drink_items = []
drink_items = drinks_soup.find_all(
    "div",
    class_="products-thumbnail",
)
all_drink_items += drink_items

all_drinks: List[Drink] = []
for drink_item in tqdm(all_drink_items):
    title = drink_item.find(
        "p", class_="reccomendedProductQuickView-module--textBar--157ed"
    ).text.strip()
    href = drink_item.find("a")["href"]
    image_url = "https:" + drink_item.find("img")["src"]
    new_drink = Drink(
        href=f"{BASE_URL}{href}", name=title, producer=PRODUCER_ID, image_url=image_url
    )
    all_drinks.append(new_drink)

for drink in tqdm(all_drinks):
    response = requests.get(drink.href)
    if response.status_code != 200:
        raise ConnectionError(
            f"Did not get a 200 status from {drink.href}. \n {response.content}"
        )
    drink_soup = BeautifulSoup(response.content, "html.parser")

    try:
        description = drink_soup.find(
            "p", class_="product-form-module--sub-title--3f479"
        ).text.strip()
        drink.description = description
    except:
        print(f"Did not find description for {drink.href}")
        drink.description = " "

export_drinks(PRODUCER_NAME, all_drinks)
