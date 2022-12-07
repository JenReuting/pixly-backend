"""Seed database with sample data from CSV Files."""

import faker
import random
from csv import DictReader
from app import db
from models import Image
import psycopg2
import datetime

# db.drop_all()
# db.create_all()

with open('generator/images.csv') as images:
    db.session.bulk_insert_mappings(Image, DictReader(images))

db.session.commit()
