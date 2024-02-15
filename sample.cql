CREATE KEYSPACE IF NOT EXISTS marvel
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

USE marvel;

CREATE TABLE IF NOT EXISTS hero (
    id uuid,
    username text,
    role text,
    token text,
    refresh_token text,
    expires timestamp,
    PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS hero_stats (
    hero_id uuid,
    name text,
    melee int,
    agility int,
    vigilance int,
    ego int,
    logic int,
    init int,
    powers list<tuple<text, text>>,
    notes list<text>,
    PRIMARY KEY (hero_id)
)

CREATE TABLE IF NOT EXISTS pool (
    hero_id uuid,
    d1 text,
    d2 text,
    dm text,
    trouble int,
    edge int,
    rolls list<text>,
    PRIMARY KEY (hero_id)
)

CREATE TABLE IF NOT EXISTS init (
    init_id uuid,
    hero_ids list<uuid>,
    values <int>,
    turn int,
    PRIMARY KEY (username, server)
)

CREATE TABLE IF NOT EXISTS hero_init (
    hero_id uuid,
    value int,
    PRIMARY KEY (hero, server)
)

INSERT INTO user (
  username
) VALUES (
  'lukejpreston'
);

UPDATE user
SET token = '1234'
WHERE username = 'lukejpreston';

SELECT * FROM user WHERE username = 'bacon';

-- session.execute(query)
