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

    def set_cherry_session(self, id, data, expiration_time, timestamp):
        print('set_cherry_session', id, data, expiration_time, timestamp)
        connection = sqlite3.connect('marvel.db')
        data_text = json.dumps(data)
        print(data_text)
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO cherry_session (id, data, expiration_timestamp, timestamp) VALUES ('{}', '{}', '{}', '{}')".format(
                id,
                data_text,
                expiration_time,
                timestamp
            )
            print(insert_query)
            try:
                cursor.execute(insert_query)
                connection.commit()
            except Exception as e:
                print('set_cherry_session:insert', e)
                update_query = "UPDATE cherry_session SET data = '{}' WHERE id = '{}'".format(data_text, id)
                print(update_query)
                cursor.execute(update_query)
        except Exception as e:
            print('set_cherry_session', e)
        finally:
            connection.close()

    def get_cherry_session(self, id):
        connection = sqlite3.connect('marvel.db')
        try:
            query = "SELECT * FROM cherry_session WHERE id = '{}';".format(id)

            print(1)
            cursor = connection.execute(query)
            print(2)
            columns = [column[0] for column in cursor.description]
            print(3)
            results = cursor.fetchall()
            print(4, results)
            cursor_hash = [dict(zip(columns, row)) for row in results]
            print(5, cursor_hash[0]["data"], cursor_hash[0]["expiration_timestamp"])

            if cursor_hash:
                return (json.loads(cursor_hash[0]["data"]), datetime.datetime.strptime(cursor_hash[0]["expiration_timestamp"], '%Y-%m-%d %H:%M:%S.%f'))
            else:
                return None
        except Exception as e:
            print('get_cherry_session', e)
        finally:
            connection.close()

    def delete_cherry_session(self, id):
        connection = sqlite3.connect('marvel.db')
        try:
            query = "DELETE FROM cherry_session WHERE id = '{}';".format(
                id)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except Exception as e:
            print('delete_cherry_session', e)
        finally:
            connection.close()
