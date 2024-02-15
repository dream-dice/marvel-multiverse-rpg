import marvel

mdb = marvel.Marvel()

# session = mdb.session()
# session.execute("DROP TABLE marvel.users")
# session.execute("DROP TABLE marvel.heroes")
# session.execute("DROP TABLE marvel.pools")
# mdb.run_schema()

session.execute("select * from marvel.users").all()

id = 82764823764237846
username = 'user'
access_token = 'an_access_token'
refresh_token = 'a_refresh_token'
expires_in = 604800

mdb.add_user(id, username, access_token, refresh_token, expires_in)
user = mdb.get_user(id)
print(user)



# mdb.add_hero('user', 'hero')
# mdb.add_hero('user', 'hero')
# mdb.add_hero('user', 'hero')
# mdb.add_hero('user', 'hero')
# mdb.add_hero('user', 'hero1')
# mdb.add_hero('user', 'hero2')
# heroes = mdb.get_heroes('user')
# print(heroes)
# hero = mdb.get_hero('user', 'hero')
# print(hero)
# mdb.add_pool(hero.id)
# pool = mdb.get_pool(hero.id)
# print(pool)
