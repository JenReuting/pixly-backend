# Pixly

Pixly is a full stack web-application to upload, edit, and browse image files.

# Table of Contents
1. [Features](#Features)
2. [Tech stack](#Tech-stack)
3. [Install](#Install)
4. [Testing](#Testing)
6. [Future features](#Future-features)

## Features<a name="Features"></a>:
* Utilizes RESTful API
* JPEG storage
* Image gallery
* Light image editing

## Tech stack<a name="Tech-stack"></a>:

### Backend:
![alt text](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white&style=for-the-badge)
![alt text](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=for-the-badge)

### Frontend:
![alt text](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![alt text](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![alt text](https://img.shields.io/badge/-Bootstrap-7952B3?logo=bootstrap&logoColor=white&style=for-the-badge)

### Database Management:
![alt text](https://img.shields.io/badge/-PostgresSQL-4169E1?logo=postgresql&logoColor=white&style=for-the-badge)
![alt text](https://img.shields.io/badge/-SQLAlchemy-F40D12?logo=sqlalchemy&logoColor=white&style=for-the-badge)

## Install<a name="Install"></a>:
Create Python virtual environment and activate:

    python3 -m venv venv
    source venv/bin/activate

Install dependences from requirements.txt:

    pip install -r requirements.txt

Setup the database:

    createdb pixly
    python seed.py

Create an .env file to hold configurations:

    SECRET_KEY=abc123
    DATABASE_URL=postgresql:///pixly

Start the server:

    flask run

## Testing<a name="Testing"></a>:
There are four test files: two for testing the models, and two for testing the routes/view-functions:

    FLASK_DEBUG=False python -m unittest <name-of-python-file>

Note: We set FLASK_DEBUG=False for this command, so it doesn’t use debug mode, and therefore won’t use the Debug Toolbar during our tests. If you are having an error running tests (comment out the line in your app.py that uses the Debug Toolbar).

## Future features<a name="Future-features"></a>:
* Live image search
* Expanded image editing features
* Versioning - retrieve previous image versions.

