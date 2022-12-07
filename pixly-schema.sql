CREATE TABLE images (
    id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(25),
    file_name TEXT NOT NULL,
    image_url TEXT NOT NULL,
    signed_url TEXT
);
