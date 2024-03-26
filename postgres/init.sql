-- create an empty table for storing scraped appartments metadata
CREATE TABLE IF NOT EXISTS apartments (
    title TEXT,
    price INTEGER,
    img_url TEXT
);