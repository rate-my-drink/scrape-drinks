from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 13
PRODUCER_NAME = "Bean Brothers"
BASE_URL = r"https://www.beanbrothers.nl/"


all_drink_items = []
drinks_url = r"https://www.beanbrothers.nl/product-category/espresso/"
# Get all drinks from overview
response = requests.get(drinks_url)
last_response = response.status_code

if response.status_code != 200:
    raise ConnectionError(
        f"Got {response.status_code} status from {drinks_url}. {response.content}"
    )

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
