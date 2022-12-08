CREATE TABLE images (
    id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    file_name TEXT NOT NULL,
    title VARCHAR(25),
    image_url TEXT NOT NULL,
    bucket_name VARCHAR(25) NOT NULL,
    description VARCHAR(25),
    creation_date TIMESTAMP NOT NULL
);

