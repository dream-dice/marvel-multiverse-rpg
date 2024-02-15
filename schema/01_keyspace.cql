CREATE KEYSPACE IF NOT EXISTS marvel
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};