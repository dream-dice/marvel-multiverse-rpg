import json
import os
import datetime
import time
import sqlite3


class Marvel():
    def run_schema(self):
        connection = sqlite3.connect('marvel.db')
        try:
            cursor = connection.cursor()
            schema_folder = './schema'
            for filename in sorted(os.listdir(schema_folder)):
                print("Ran {}".format(filename))
                if filename.endswith('.cql'):
                    with open(os.path.join(schema_folder, filename)) as f:
                        cursor.execute(f.read())
            connection.commit()
        except Exception as e:
            print('run_schema', e)
        finally:
            connection.close()

    def update_user(self, id, username, access_token, refresh_token, expires_in):
        connection = sqlite3.connect('marvel.db')
        try:
            now = datetime.datetime.now()
            expires = now + datetime.timedelta(seconds=expires_in)
            unix_timestamp = int(time.mktime(expires.timetuple()) * 1000)

            query = """UPDATE marvel.users
            SET
                username = '{}',
                access_token = '{}',
                refresh_token = '{}',
                expires = '{}'
            WHERE
                id = '{}';
            """.format(
                username,
                access_token,
                refresh_token,
                unix_timestamp,
                id
            )
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except Exception as e:
            print('update_user', e)
        finally:
            connection.close()

    def add_user(self, id, username, access_token, refresh_token, expires_in):
        connection = sqlite3.connect('marvel.db')
        try:
            now = datetime.datetime.now()
            expires = now + datetime.timedelta(seconds=expires_in)
            unix_timestamp = int(time.mktime(expires.timetuple()) * 1000)

            query = """INSERT INTO users (
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
            """.format(
                id,
                username,
                access_token,
                refresh_token,
                unix_timestamp
            )
            connection.execute(query)
            connection.commit()
        except Exception as e:
            print('add_user', e)
        finally:
            connection.close()

    def get_user(self, id):
        connection = sqlite3.connect('marvel.db')
        try:
            query = "SELECT * FROM users WHERE id = '{}';".format(id)
            cursor = connection.execute(query)
            columns = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            cursor_hash = [dict(zip(columns, row)) for row in results]
            return cursor_hash[0]
        except Exception as e:
            print('get_user', e)
        finally:
            connection.close()
