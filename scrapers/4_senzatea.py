import csv
import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

base_url = r"https://shop.senzatea.nl/product-categorie/selected-teas/"
PRODUCER_ID = 4

all_drinks: List[Drink] = []

# Get all drinks from overview
response = requests.get(base_url)
last_response = response.status_code

if last_response != 200:
    raise ConnectionError(f"Did not get a 200 status from {base_url}")

drinks_soup = BeautifulSoup(response.content, "html.parser")

drink_items = drinks_soup.find_all("div", class_="product-small box")

for drink_item in drink_items:
    a_tittle = drink_item.find("p", class_="product-title").find("a")
    title = a_tittle.text.strip()
    href = a_tittle["href"]
    new_drink = Drink(href=href, name=title, producer=PRODUCER_ID)
    all_drinks.append(new_drink)

# Populate the drink with specific info
for drink in tqdm(all_drinks):
    response = requests.get(drink.href)

    if response.status_code != 200:
        raise ConnectionError(f"Did not get a 200 status from {drink.href}")
    drink_soup = BeautifulSoup(response.content, "html.parser")

    description = (
        drink_soup.find("div", class_="product-short-description")
        .find("p")
        .text.strip()
    )
    image_url = drink_soup.find("img", class_="wp-post-image skip-lazy")["src"]
    drink.description = description
    drink.image_url = image_url

export_drinks("senzatea", all_drinks)
