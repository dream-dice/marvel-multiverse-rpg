CREATE TABLE IF NOT EXISTS heroes (
    username text,
    name text,
    id uuid,
    PRIMARY KEY (username, name)
);
