from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 15
PRODUCER_NAME = "Celestial Seasonings"
BASE_URL = r"https://celestialseasonings.com/"


all_catagories = []
drinks_url = BASE_URL
# Get all drinks from overview
response = requests.get(drinks_url)
last_response = response.status_code

if response.status_code != 200:
    raise ConnectionError(
        f"Got {response.status_code} status from {drinks_url}. {response.content}"
    )

drinks_soup = BeautifulSoup(response.content, "html.parser")

catagories = drinks_soup.find_all(
    "div",
    class_="grid__item one-half medium--one-third large--one-third collection-collage__item text-center",
)
all_catagories += catagories

all_drinks: List[Drink] = []
for category_item in tqdm(all_catagories):
    category_href = BASE_URL + category_item.find("a")["href"]

    response = requests.get(category_href)
    if response.status_code != 200:
        raise ConnectionError(
            f"Got {response.status_code} status from {category_href}. {response.content}"
        )
    category_soup = BeautifulSoup(response.content, "html.parser")

    all_drinks_soup = category_soup.find_all("div", class_="grid-product__wrapper")

    for drink_soup in all_drinks_soup:
        title = drink_soup.find("h3", class_="grid-product__title").text.strip()
        href = BASE_URL + drink_soup.find("a")["href"]
        new_drink = Drink(
            href=href,
            name=title,
            producer=PRODUCER_ID,
        )
        all_drinks.append(new_drink)


for drink in tqdm(all_drinks):
    response = requests.get(drink.href)
    if response.status_code != 200:
        raise ConnectionError(
            f"Got {response.status_code} status from {drink.href}. {response.content}"
        )
    drink_soup = BeautifulSoup(response.content, "html.parser")

    image_url = drink_soup.find("img", class_="mfp-image")["src"]

    drink.image_url = "https:" + image_url

    description_ps = drink_soup.find(
        "div", class_="product-single__description rte"
    ).find_all("p")
    description = ""
    for p in description_ps:
        text = p.text.strip()
        if text:
            description += f"{text}\n"

    drink.description = description

export_drinks(PRODUCER_NAME, all_drinks)
