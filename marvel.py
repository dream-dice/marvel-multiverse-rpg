import json
import os
import datetime
import time

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class Marvel():
    def __init__(self):
        auth_provider = PlainTextAuthProvider(
            username='cassandra',
            password='cassandra'
        )
        self.cluster = Cluster(
            auth_provider=auth_provider,
            contact_points=['cassandra'],
            port=9042
        )

    def run_schema(self):
        session = self.cluster.connect()
        schema_folder = '/app/schema'
        for filename in sorted(os.listdir(schema_folder)):
            print("Ran {}".format(filename))
            if filename.endswith('.cql'):
                with open(os.path.join(schema_folder, filename)) as f:
                    session.execute(f.read())

        session.shutdown()

    def session(self):
        return self.cluster.connect()

    def add_user(self, id, username, access_token, refresh_token, expires_in):
        session = self.cluster.connect()
        try:
            now = datetime.datetime.now()
            expires = now + datetime.timedelta(seconds=expires_in)
            unix_timestamp = int(time.mktime(expires.timetuple()) * 1000)

            query = """INSERT INTO marvel.users (
                id,
                username,
                access_token,
                refresh_token,
                expires
            )
            VALUES (
                '{}',
                '{}',
                '{}',
                '{}',
                '{}'
            )
            IF NOT EXISTS;
            """.format(
                id,
                username,
                access_token,
                refresh_token,
                unix_timestamp
            )
            return session.execute(query)
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def get_user(self, id):
        session = self.cluster.connect()
        try:
            query = "SELECT * FROM marvel.users WHERE id = '{}';".format(id)
            return session.execute(query).one()
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def add_hero(self, username, hero):
        session = self.cluster.connect()
        try:
            query = "INSERT INTO marvel.heroes (username, name, id) VALUES ('{}', '{}', uuid()) IF NOT EXISTS;".format(
                username, hero)
            return session.execute(query)
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def get_heroes(self, username):
        session = self.cluster.connect()
        try:
            query = "SELECT * FROM marvel.heroes WHERE username = '{}';".format(
                username)
            return session.execute(query).all()
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def get_hero(self, username, name):
        session = self.cluster.connect()
        try:
            query = "SELECT * FROM marvel.heroes WHERE username = '{}' and name = '{}';".format(
                username, name)
            return session.execute(query).one()
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def add_pool(self, hero_id):
        session = self.cluster.connect()
        try:
            query = "INSERT INTO marvel.pools (hero_id, d1, d2, dm) VALUES ('{}', '{}', '{}', '{}');".format(
                hero_id, 0, 0, 0)
            return session.execute(query)
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def get_pool(self, hero_id):
        session = self.cluster.connect()
        try:
            query = "SELECT * FROM marvel.pools WHERE hero_id = '{}';".format(
                hero_id)
            return session.execute(query).one()
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def set_cherry_session(self, id, data, expiration_time, timestamp):
        session = self.cluster.connect()
        data_text = json.dumps(data)
        print("THE ID", id)
        try:
            insert_query = "INSERT INTO marvel.cherry_session (id, data, expiration_timestamp, timestamp) VALUES ('{}', '{}', '{}', '{}') IF NOT EXISTS;".format(
                id,
                data_text,
                expiration_time,
                timestamp
            )
            session.execute(insert_query)
            update_query = "UPDATE marvel.cherry_session SET data = '{}' WHERE id = '{}' IF EXISTS;".format(data_text, id)
            session.execute(update_query)
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def get_cherry_session(self, id):
        print("THE ID", id)
        session = self.cluster.connect()
        try:
            query = "SELECT * FROM marvel.cherry_session WHERE id = '{}';".format(id)
            result_set = session.execute(query).one()
            print("GET", result_set.data, result_set.expiration_timestamp, result_set.timestamp)
            return (json.loads(result_set.data), datetime.datetime.strptime(result_set.expiration_timestamp, '%Y-%m-%d %H:%M:%S.%f'))
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def delete_cherry_session(self, id):
        session = self.cluster.connect()
        try:
            query = "DELETE FROM marvel.cherry_session WHERE id = '{}';".format(
                id)
            session.execute(query)
        except Exception as e:
            print(e)
        finally:
            session.shutdown()
