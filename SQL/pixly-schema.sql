CREATE TABLE images (
    id TEXT PRIMARY KEY,
    file_name TEXT NOT NULL,
    ext VARCHAR(5) NOT NULL,
    title VARCHAR(25),
    image_url TEXT NOT NULL,
    bucket_name VARCHAR(25) NOT NULL,
    description VARCHAR(25),
    creation_date TIMESTAMP NOT NULL
);


CREATE TABLE metadata (
    id INTEGER PRIMARY KEY AUTO
)

