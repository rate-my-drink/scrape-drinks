from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

base_url = r"https://www.brandzaak.nl/koffiebonen"
PRODUCER_ID = 5
PRODUCER_NAME = "brandzaak"

all_drinks: List[Drink] = []

# Get all drinks from overview
response = requests.get(base_url)
last_response = response.status_code

if last_response != 200:
    raise ConnectionError(f"Did not get a 200 status from {base_url}")

drinks_soup = BeautifulSoup(response.content, "html.parser")

drink_items = drinks_soup.find_all("div", class_="product-item-info")

for drink_item in drink_items:
    a_tittle = drink_item.find("div", class_="product-item-name").find("p")
    title = a_tittle.text.strip()
    href = drink_item.find("a", class_="product-item-link product")["href"]
    image_url = drink_item.find("img", class_="product-image-photo product-item-photo")[
        "src"
    ]
    new_drink = Drink(href=href, name=title, producer=PRODUCER_ID, image_url=image_url)
    all_drinks.append(new_drink)


# Populate the drink with specific info
for drink in tqdm(all_drinks):
    response = requests.get(drink.href)

    if response.status_code != 200:
        raise ConnectionError(f"Did not get a 200 status from {drink.href}")
    drink_soup = BeautifulSoup(response.content, "html.parser")

    description = (
        drink_soup.find("div", class_="product attribute description")
        .find("p")
        .text.strip()
    )
    drink.description = description

export_drinks(PRODUCER_NAME, all_drinks)
