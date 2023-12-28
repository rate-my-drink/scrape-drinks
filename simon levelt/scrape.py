import csv
import datetime

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

base_url = r"https://www.simonlevelt.nl"
PRODUCER_ID = 1


def get_all_drinks(part_url):
    last_response = 200
    drink_list = []
    p = 1
    while last_response == 200:
        drinks_url = f"{base_url}/{part_url}&p={p}"
        response = requests.get(drinks_url)
        last_response = response.status_code
        if last_response != 200:
            break
        # Parse the HTML content of the drinks page
        drinks_soup = BeautifulSoup(response.content, "html.parser")

        # Find the HTML elements that contain all of the drinks
        drink_items = drinks_soup.find_all("div", class_="product--box")

        # Get the name, and href of each drink
        # Producer is fixed to be 1 (Simon Levelt)
        for item in drink_items:
            try:
                a_tittle = item.find("a", class_="product--title")
                name = a_tittle.text.strip()
                href = a_tittle["href"]
                drink_list.append({"name": name, "producer": PRODUCER_ID, "href": href})
            except:
                pass
        p += 1

    for drink in tqdm(drink_list):
        try:
            response = requests.get(drink["href"])
            last_response = response.status_code
            if last_response != 200:
                continue
            # Parse the HTML content of the drink page
            single_drink_soup = BeautifulSoup(response.content, "html.parser")
            description = (
                single_drink_soup.find(
                    "div", class_="product--origin--information--left-content"
                )
                .find("p")
                .text.strip()
            )
            image_url = single_drink_soup.find(
                "img", class_="orbitvu-gallery-main-image"
            )["src"]
            drink["image_url"] = image_url
            drink["description"] = description
        except:
            pass
    return drink_list


coffee_list = get_all_drinks(part_url="koffie?o=2&n=17&f=10003")
tea_list = get_all_drinks(part_url="thee?o=2&n=17&f=6739|6737")

all_drinks = coffee_list + tea_list


# Get the current date and time
now = datetime.datetime.now()

# Format the date as a string to append to the filename
date_str = now.strftime("%Y-%m-%d_%H-%M-%S")

filename = f"simon_levelt_drinks_{date_str}.csv"

# Open the file in write mode
with open(filename, mode="w", newline="") as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(["name", "producer", "href", "description"])

    # Write each drink to a row in the CSV file
    for drink in all_drinks:
        writer.writerow(
            [
                drink["name"],
                drink["producer"],
                drink["href"],
                drink.get("description", ""),
            ]
        )
