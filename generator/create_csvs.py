"""Generate CSVs of random data for Pixly.
"""

import csv
from random import choice, randint, sample
from itertools import permutations
import requests
from faker import Faker
from generator.helpers import get_random_datetime

IMAGE_CSV_HEADERS = ['file_name', 'image_url']
NUM_IMAGES = 10

fake = Faker()

# # Generate random  image URLs to use for seeded images

image_urls = [
    f"https://randomuser.me/api/portraits/{kind}/{i}.jpg"
    for kind, count in [("lego", 10), ("men", 100), ("women", 100)]
    for i in range(count)
]


with open('generator/images.csv', 'w') as images_csv:
    images_writer = csv.DictWriter(images_csv, fieldnames=IMAGE_CSV_HEADERS)
    images_writer.writeheader()

    for i in range(NUM_IMAGES):
        url = choice(image_urls)
        images_writer.writerow(dict(
            file_name=url,
            image_url=url,
        ))
