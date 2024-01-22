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
    class_="product-small box",
)
all_drink_items += drink_items

all_drinks: List[Drink] = []
for drink_item in tqdm(all_drink_items):
    title_div = drink_item.find("div", class_="title-wrapper")
    title = title_div.text.strip()
    href = title_div.find("a")["href"]
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

    image_url = drink_soup.find("img", class_="wp-post-image skip-lazy")["src"]

    drink.image_url = image_url

    description_ps = drink_soup.find(
        "div", class_="product-short-description"
    ).find_all("p")
    description = ""
    for p in description_ps:
        text = p.text.strip()
        if text:
            description += f"{text}\n"

    drink.description = description

export_drinks(PRODUCER_NAME, all_drinks)
