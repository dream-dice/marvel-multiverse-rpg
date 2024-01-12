import json
from random import randint


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


def d6():
    return randint(1, 6)


def roll_trouble(pool, trouble=0):
    for _ in range(trouble):
        highest_die = max_dice(pool)
        current = pool[highest_die]
        new_value = d6()
        if highest_die == 'dm' and new_value == 1:
            pool["dm"] = current
        elif highest_die == 'dm' and current == 1:
            pool["dm"] = new_value
        elif new_value < current:
            pool[highest_die] = new_value

    return pool


class CaptainDice:
    def __init__(self) -> None:
        self.heros = load()

    def d616(self, hero, trouble=0):
        pool = {
            "d1": d6(),
            "d2": d6(),
            "dm": d6()
        }
        self.heros[hero] = roll_trouble(pool, trouble)
        save(self.heros)

    def trouble(self, hero, trouble=0):
        pool = self.heros[hero]
        self.heros[hero] = roll_trouble(pool, trouble)
        save(self.heros)

    def edge(self, hero, dice):
        pool = self.heros[hero]
        current = pool[dice]
        new_value = d6()
        if dice == "dm" and new_value == 1:
            pool[dice] = new_value
        elif dice == "dm" and current == 1:
            pool[dice] = current
        elif new_value > current:
            pool[dice] = new_value
        self.heros[hero] = pool
        save(self.heros)

    def set(self, hero, d1, d2, dm):
        pool = self.heros.get(hero) or {}
        pool["d1"] = d1
        pool["d2"] = d2
        pool["dm"] = 1 if dm == 'm' else dm
        self.heros[hero] = pool
        save(self.heros)

    def pool(self, hero):
        return self.heros[hero]

    def init(self, hero):
        pass
