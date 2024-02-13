import datetime
import json
import string
from random import randint, choice


TOKEN_LENGTH = 20


def save(heros):
    with open("heros.json", "w") as file:
        json.dump(heros, file)


def load():
    with open("heros.json", "r") as file:
        return json.load(file)


def max_dice(pool):
    d1 = pool["d1"]
    d2 = pool["d2"]
    dm = pool["dm"]
    if dm == 1:
        dm = 7

    if dm >= d1 and dm >= d2 and dm > 2:
        return "dm"
    if d1 >= d2 and d1 >= dm:
        return "d1"
    if d2 >= d1 and d2 >= dm:
        return "d2"
    return "dm"


def random_token(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))


def d6():
    return randint(1, 6)


def roll_trouble(pool, trouble=0):
    rolled = []
    for _ in range(trouble):
        highest_die = max_dice(pool)
        current = pool[highest_die]
        new_value = d6()
        if highest_die == 'dm' and new_value == 1:
            current_str = current
            if current == 1:
                current_str = 'M'
            rolled.append(
                "**{}** `{}` -> `{}`".format(highest_die, current_str, current_str))
            pool["dm"] = current
        elif highest_die == 'dm' and current == 1:
            current_str = current
            if current == 1:
                current_str = 'M'
            new_str = new_value
            if new_value == 1:
                new_str = 'M'
            rolled.append(
                "**{}** `{}` -> `{}`".format(highest_die, current_str, new_str))
            pool["dm"] = new_value
        elif new_value < current:
            rolled.append(
                "**{}** `{}` -> `{}`".format(highest_die, current, new_value))
            pool[highest_die] = new_value
        else:
            rolled.append("`{}` is not lower than **D1** `{}`, **D2** `{}`, **DM** `{}`".format(
                new_value, pool["d1"], pool["d2"], pool["dm"]))

    return pool, rolled


class CaptainDice:
    def __init__(self) -> None:
        self.heros = load()

    def d616(self, hero, trouble=0):
        pool = {
            "d1": d6(),
            "d2": d6(),
            "dm": d6()
        }
        pool, trouble_rolled = roll_trouble(pool, trouble)
        self.set_pool(hero, pool)
        return trouble_rolled

    def trouble(self, hero, trouble=0):
        pool, rolled = roll_trouble(self.pool(hero), trouble)
        self.set_pool(hero, pool)
        return rolled

    def edge(self, hero, dice):
        pool = self.pool(hero)
        current = pool[dice]
        new_value = d6()
        if dice == "dm" and new_value == 1:
            pool[dice] = new_value
        elif dice == "dm" and current == 1:
            pool[dice] = current
        elif new_value > current:
            pool[dice] = new_value
        self.set_pool(hero, pool)
        return new_value

    def set_pool(self, hero, pool):
        self.heros[hero] = self.heros.get(hero) or {}
        self.heros[hero]["pool"] = pool
        save(self.heros)

    def set(self, hero, d1, d2, dm):
        pool = {}
        pool["d1"] = d1
        pool["d2"] = d2
        pool["dm"] = 1 if dm == 'm' else dm
        self.set_pool(hero, pool)

    def pool(self, hero):
        hero_data = self.heros.get(hero) or {}
        return hero_data.get("pool") or {}

    def init(self, hero, multiverse_id):
        token = random_token(TOKEN_LENGTH)
        current_time = datetime.datetime.now()
        three_hours_from_now = current_time + datetime.timedelta(hours=3)
        epoch_time = three_hours_from_now.timestamp()
        self.heros[hero] = self.heros.get(hero) or {}
        self.heros[hero]["token"] = token
        self.heros[hero]["multiverse_id"] = multiverse_id
        self.heros[hero]["expires"] = epoch_time
        save(self.heros)
        return {"token": token, "multiverse_id": multiverse_id, "expires": epoch_time}
