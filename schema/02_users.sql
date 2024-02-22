CREATE TABLE IF NOT EXISTS users (
    id text,
    username text,
    access_token text,
    refresh_token text,
    expires timestamp,
    PRIMARY KEY (id)
);
