from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os


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

    def add_user(self, username):
        try:
            session = self.cluster.connect()
            query = "INSERT INTO marvel.users (username) VALUES ('{}') IF NOT EXISTS;".format(username)
            return session.execute(query)
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def get_user(self, username):
        try:
            session = self.cluster.connect()
            query = "SELECT * FROM marvel.users WHERE username = '{}';".format(username)
            return session.execute(query).one()
        except Exception as e:
            print(e)
        finally:
            session.shutdown()
    
    def add_hero(self, username, hero):
        try:
            session = self.cluster.connect()
            query = "INSERT INTO marvel.heroes (username, name, id) VALUES ('{}', '{}', uuid()) IF NOT EXISTS;".format(username, hero)
            return session.execute(query)
        except Exception as e:
            print(e)
        finally:
            session.shutdown()
    
    def get_heroes(self, username):
        try:
            session = self.cluster.connect()
            query = "SELECT * FROM marvel.heroes WHERE username = '{}';".format(username)
            return session.execute(query).all()
        except Exception as e:
            print(e)
        finally:
            session.shutdown()
    
    def get_hero(self, username, name):
        try:
            session = self.cluster.connect()
            query = "SELECT * FROM marvel.heroes WHERE username = '{}' and name = '{}';".format(username, name)
            return session.execute(query).one()
        except Exception as e:
            print(e)
        finally:
            session.shutdown()

    def add_pool(self, hero_id):
        try:
            session = self.cluster.connect()
            query = "INSERT INTO marvel.pools (hero_id, d1, d2, dm) VALUES ('{}', '{}', '{}', '{}');".format(hero_id, 0, 0, 0)
            return session.execute(query)
        except Exception as e:
            print(e)
        finally:
            session.shutdown()
    
    def get_pool(self, hero_id):
        try:
            session = self.cluster.connect()
            query = "SELECT * FROM marvel.pools WHERE hero_id = '{}';".format(hero_id)
            return session.execute(query).one()
        except Exception as e:
            print(e)
        finally:
            session.shutdown()