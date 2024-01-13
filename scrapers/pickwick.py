from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

base_url = r"https://www.pickwick.nl"

category_url = f"{base_url}/assortiment"
PRODUCER_ID = 6
PRODUCER_NAME = "pickwick"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
}

all_drinks: List[Drink] = []
# Get all drinks from overview
response = requests.get(
    category_url,
    headers=headers,
)
print(response.status_code)

if response.status_code != 200:
    raise ConnectionError(f"Did not get a 200 status from {category_url}")

drinks_soup = BeautifulSoup(response.content, "html.parser")

all_category_url = []
category_items = drinks_soup.find_all("ul", class_="category-names")

for category_item in category_items:
    post_fix = category_item.find("a")["href"]
    url: str = base_url + post_fix
    if url.startswith(category_url):
        all_category_url.append(url)

category_items = drinks_soup.find_all("div", class_="content-buttons")
for category_item in category_items:
    post_fix = category_item.find("a")["href"]
    url: str = base_url + post_fix
    if url.startswith(category_url):
        all_category_url.append(url)

# Populate the drink with specific info
for category_url in tqdm(all_category_url):
    response = requests.get(category_url, headers=headers)

    if response.status_code != 200:
        raise ConnectionError(f"Did not get a 200 status from {category_url}")
    category_soup = BeautifulSoup(response.content, "html.parser")

    all_soup_drinks = category_soup.find_all(
        "div", class_="product-range-product text-center"
    )

    for drink_soup in all_soup_drinks:
        name = drink_soup.find_all("h3")[0].text.strip()
        description = drink_soup.find_all("p", class_="product-name")[0].text.strip()
        href = f"{base_url}{drink_soup.find('a')['href']}"
        image_url = f"{base_url}{drink_soup.find_all('img')[0]['src']}"
        drink = Drink(
            href=href,
            name=name,
            description=description,
            image_url=image_url,
            producer=PRODUCER_ID,
        )
        all_drinks.append(drink)

export_drinks(PRODUCER_NAME, all_drinks)
