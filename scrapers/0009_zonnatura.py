from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 9
PRODUCER_NAME = "Zonnatura"
BASE_URL = r"https://www.zonnatura.nl/"
headers = {
    "Host": "www.zonnatura.nl",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,nl;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
}


all_drink_items = []
drinks_url = r"https://www.zonnatura.nl/onze-producten/thee-categorie/"
# Get all drinks from overview
response = requests.get(drinks_url, headers=headers)
last_response = response.status_code

if last_response != 200:
    raise ConnectionError(f"Did not get a 200 status from {drinks_url}")

drinks_soup = BeautifulSoup(response.content, "html.parser")

drink_items = drinks_soup.find_all(
    "div",
    class_="item item-hover-view-cart",
)
all_drink_items += drink_items

all_drinks: List[Drink] = []
for drink_item in tqdm(all_drink_items):
    title = drink_item.find("h4", class_="product-name").text.strip()
    href = drink_item.find("a")["href"]
    image_url = drink_item.find("img")["src"]
    new_drink = Drink(
        href=f"{BASE_URL}{href}", name=title, producer=PRODUCER_ID, image_url=image_url
    )
    all_drinks.append(new_drink)

for drink in tqdm(all_drinks):
    response = requests.get(drink.href, headers=headers)
    if response.status_code != 200:
        raise ConnectionError(f"Did not get a 200 status from {drink.href}")
    drink_soup = BeautifulSoup(response.content, "html.parser")

    description = drink_soup.find("div", class_="product-description").text.strip()
    drink.description = description

export_drinks(PRODUCER_NAME, all_drinks)
