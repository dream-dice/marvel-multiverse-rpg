CREATE TABLE IF NOT EXISTS marvel.heroes (
    username text,
    name text,
    id uuid,
    PRIMARY KEY (username, name)
);
