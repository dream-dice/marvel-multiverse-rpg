CREATE TABLE IF NOT EXISTS cherry_session (
    id text,
    data text,
    expiration_timestamp timestamp,
    timestamp int,
    PRIMARY KEY (id)
);