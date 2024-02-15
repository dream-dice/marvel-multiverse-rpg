CREATE TABLE IF NOT EXISTS marvel.users (
    username text,
    "token" text,
    refresh_token text,
    expires timestamp,
    PRIMARY KEY (username)
);