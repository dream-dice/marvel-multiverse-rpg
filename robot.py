import json
from random import randint


def save(users):
    with open("users.json", "w") as outfile:
        json.dump(users, outfile)


def load():
    with open("users.json", "r") as openfile:
        return json.load(openfile)


def d616(username):
    users = load()
    users[username] = {
        "d1": randint(1, 6),
        "d2": randint(1, 6),
        "dm": randint(1, 6)
    }
    save(users)
    return users


def reroll(username, die, edge):
    users = load()
    user = users[username] or d616(username)[username]
    value = randint(1, 6)
    current = user[die]
    if edge and die == 'dm' and current == 1:
        user[die] = current
    elif edge and die == 'dm' and (value > current or value == 1):
        user[die] = value
    elif edge and die == 'd1' and (value > current):
        user[die] = value
    elif edge and die == 'd2' and (value > current):
        user[die] = value
    elif not edge and die == 'dm' and current == 1:
        user[die] = value
    elif not edge and die == 'dm' and (value < current or value == 1):
        user[die] = current
    elif not edge and die == 'd1' and (value < current):
        user[die] = value
    elif not edge and die == 'd2' and (value < current):
        user[die] = value
    save(users)
    return users


def set(username, value):
    users = load()
    users[username] = value
    users[username]
    save(users)
    return users


dice_emojis = {
    1: "⚀",
    2: "⚁",
    3: "⚂",
    4: "⚃",
    5: "⚃",
    6: "⚅",
    "m": "🇲"
}

def display(username, karma=0):
    users = load()
    user = users[username] or d616(username)
    sum = user["d1"] + user["d2"] + karma
    if user["dm"] == 1:
        sum += 6
    else:
        sum += user["dm"]

    fantastic = ''
    fantastic_roll = user["dm"]
    if user["dm"] == 1:
        fantastic_roll = 'M'
        fantastic = 'Fantastic!'

    karma_value = ''
    if karma > 0:
        karma_value = ', K ({})'.format(karma)

    if sum > 19:
        sum = 19

    return "{}: D1 ({}) {}, D2 ({}) {}, DM ({}) {}{} = {} {}".format(
        username,
        user["d1"],
        dice_emojis[user["d1"]],
        user["d2"],
        dice_emojis[user["d2"]],
        fantastic_roll,
        dice_emojis["m" if user["dm"] == 1 else user["dm"]],
        karma_value,
        sum,
        fantastic
    )
