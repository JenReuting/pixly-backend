"""Generate CSVs of random data for Pixly.
"""
import csv
from random import choice, randint, sample
from itertools import permutations
import requests
from faker import Faker
from generator.helpers import get_random_datetime

IMAGE_CSV_HEADERS = ['id', 'ext', 'file_name', 'title',
                     'image_url', 'bucket_name', 'description', 'creation_date']
NUM_IMAGES = 10

METADATA_CSV_HEADERS = ['id', 'tag_name', 'value', 'file_name']
NUM_METADATA = 100

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
        file_name = fake.ean(length=13)
        ext = fake.file_extension(category='image')

        images_writer.writerow(dict(
            id=file_name,
            ext=ext,
            file_name=f"{file_name}.{ext}",
            title=fake.city(),
            image_url=url,
            bucket_name='seed-bucket',
            description=fake.sentence(),
            creation_date=fake.get_random_datetime()
        ))


# with open('generator/metadata.csv', 'w') as metadata_csv:
#     metadata_writer = csv.DictWriter(
#         metadata_csv, fieldnames=[METADATA_CSV_HEADERS])
#     metadata_writer.writeheader()

#     for i in range(NUM_METADATA):
#         url = choice(image_urls)
#         file_name = fake.ean(length=13)
#         ext = fake.file_extension(category='image')

#         metadata_writer.writerow(dict(
#             id=file_name,
#             ext=ext,
#             file_name=f"{file_name}.{ext}",
#             title=fake.city(),
#             image_url=url,
#             bucket_name='seed-bucket',
#             description=fake.sentence(),
#             creation_date=fake.date()
#         ))

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )

#     tag_name = db.Column(
#         db.String(50),
#         nullable=False,
#     )
#     value = db.Column(
#         db.String(200),
#         nullable=False,
#     )

#     file_name = db.Column(
#         db.Text,
#         db.ForeignKey('images.id', ondelete='CASCADE'),
#         nullable=False,
#     )
