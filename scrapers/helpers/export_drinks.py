import csv
import datetime
from typing import List

from helpers import Drink


def export_drinks(producer_name: str, all_drinks: List[Drink]):
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date as a string to append to the filename
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"{producer_name}_{date_str}.csv"

    # Open the file in write mode
    with open(filename, mode="w", newline="") as csv_file:
        # Create a CSV writer object
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow(["name", "producer", "href", "image_url", "description"])

        # Write each drink to a row in the CSV file
        for drink in all_drinks:
            writer.writerow(
                [
                    drink.name,
                    drink.producer,
                    drink.href,
                    drink.image_url,
                    drink.description,
                ]
            )
