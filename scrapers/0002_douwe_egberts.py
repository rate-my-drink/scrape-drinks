from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 2
PRODUCER_NAME = "Douwe Egberts"
BASE_URL = r"https://www.de.nl/"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
}


all_catagories = []
drinks_url = r"https://www.de.nl/producten/"
# Get all drinks from overview
response = requests.get(
    drinks_url,
    headers=headers,
)

if response.status_code != 200:
    raise ConnectionError(
        f"Got {response.status_code} status from {drinks_url}. {response.content}"
    )

catagories_soup = BeautifulSoup(response.content, "html.parser")

catagories = catagories_soup.find_all(
    "div",
    class_="product-range-category text-left",
)
all_catagories += catagories

all_drinks: List[Drink] = []
for category_item in tqdm(all_catagories):
    category_href = BASE_URL + category_item.find("a")["href"]

    response = requests.get(
        category_href,
        headers=headers,
    )
    if response.status_code != 200:
        raise ConnectionError(
            f"Got {response.status_code} status from {category_href}. {response.content}"
        )
    category_soup = BeautifulSoup(response.content, "html.parser")

    all_drinks_soup = category_soup.find_all(
        "div", class_="product-main-section__wrapper"
    )

    for drink_soup in all_drinks_soup:
        title = drink_soup.find("h3", class_="product-name").text.strip()
        href = BASE_URL + drink_soup.find("a")["href"]
        new_drink = Drink(
            href=href,
            name=title,
            producer=PRODUCER_ID,
        )
        all_drinks.append(new_drink)


for drink in tqdm(all_drinks):
    response = requests.get(drink.href, headers=headers)
    if response.status_code != 200:
        raise ConnectionError(
            f"Got {response.status_code} status from {drink.href}. {response.content}"
        )
    drink_soup = BeautifulSoup(response.content, "html.parser")

    image_url = drink_soup.find("div", class_="image-content").find("img")["src"]

    drink.image_url = BASE_URL + image_url

    description_ps = drink_soup.find(
        "div", class_="product-detail__description"
    ).find_all("p")
    description = ""
    for p in description_ps:
        text = p.text.strip()
        if text:
            description += f"{text}\n"

    drink.description = description

export_drinks(PRODUCER_NAME, all_drinks)
