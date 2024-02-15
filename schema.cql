CREATE KEYSPACE IF NOT EXISTS marvel
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

CREATE TABLE IF NOT EXISTS marvel.hero (
    id uuid,
    username text,
    role text,
    token text,
    refresh_token text,
    expires timestamp,
    PRIMARY KEY (id)
);

