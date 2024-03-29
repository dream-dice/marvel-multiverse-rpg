import os

import bcrypt

import powers

from dotenv import load_dotenv

load_dotenv()

hero = "lukejpreston"

hero_server = 'My Server'
hero_name = 'lukejpreston'
salt = bytes(os.environ['SALT'], 'utf8')
hero = str(bcrypt.hashpw("{}.{}".format(hero_server, hero_name).encode(), salt))

power = powers.Power()


def test(hero_request):
    result = power.power(hero, hero_name, hero_request)
    print('power({})\n{}'.format(hero_request, result))


test("!cap x")

print("=== help ===")
test("!cap h")
test("!cap     help    d616   ")
test("!cap     h    d   ")
test("!cap     h    1 2 x 3 d")
test("!cap h h")
test("!cap h d")
test("!cap h p")
test("!cap h t")
test("!cap h e")
test("!cap h s")

print("=== d616 ===")
test("!cap set d1 1 d2 5 dm 6")
test("!cap pool ability 3 vs_target 12")
test("!cap d")
test("!cap d trouble 10")
test("!cap d t 10")

print("=== edge ===")
test("!cap p")
test("!cap edge D1")
test("!cap edge d2")
test("!cap edge m")
test("!cap edge random")

print("=== pool ===")
test("!cap pool")
test("!cap p")

print("=== set ===")
test("!cap set d1 1 d2 2 dm 3")
test("!cap set 1 2 2 3 m 4")
test("!cap s 1 3 2 4 m 5")
test("!cap s 1 3 2 4 m M")
test("!cap s 1 3 2 4 m m")
test("!cap s 1 3 2 4")
test("!cap s 1 x 2 4 m m")
test("!cap s 1 3 2 x m m")
test("!cap s 1 3 2 4 m x")

test("!cap s d1 6 d2 6 dm m")


test("!cap set d1 6 d2 6 dm m")
test("!cap trouble 20")
test("!cap set d1 6 d2 6 dm m")
test("!cap trouble 20 thing a dine")
test("!cap set d1 6 d2 6 dm m")
test("!cap trouble")
