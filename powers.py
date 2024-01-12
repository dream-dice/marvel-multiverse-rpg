import re
import collections
import numbers

import captain_dice
from power_descriptions import DESCRIPTIONS


VALID_D6_VALUES = [1, 2, 3, 4, 5, 6]
VALID_DM_VALUES = VALID_D6_VALUES + ["m", "M"]
DICE = ["d1", "d2", "dm"]


def friendly_reply(cap: captain_dice.CaptainDice, hero, command, params):
    pool = cap.heros[hero]
    d1 = pool["d1"]
    d2 = pool["d2"]
    dm = pool["dm"]

    fantastic = dm == 1
    friendly_dm = "M" if fantastic else dm
    fantastic_message = " **Fantastic!**" if fantastic else ""
    dm_value = 6 if fantastic else dm

    extra_message = ""

    ability = params.get("a") or 0
    extra_message = extra_message + \
        ("**Ability** `{}`".format(ability) if ability != 0 else "")

    total = d1 + d2 + dm_value + ability

    vs_target = params.get("v") or 0
    extra_message = extra_message + \
        ("**Target** `{}`".format(vs_target) if vs_target != 0 else "")

    if extra_message != "":
        extra_message = "\n__Extra__ {}".format(extra_message)

    target_message = ""
    if vs_target == 0:
        target_message = ""
    elif d1 == 6 and d2 == 6 and dm_value == 6:
        target_message = "\nYour target was `{}` and your score is `{}`, CRITICAL SUCCESS!".format(
            vs_target, total)
    elif d1 == 1 and d2 == 1 and dm_value == 2:
        target_message = "\nYour target was `{}` and your score is `{}`, critical failure!".format(
            vs_target, total)
    elif fantastic and total >= vs_target:
        target_message = "\nYour target was `{}` and your score is `{}`, that is a FANTASTIC success!".format(
            vs_target, total)
    elif fantastic and total < vs_target:
        target_message = "\nYour target was `{}` and your score is `{}`, that is a FANTASTIC failure.".format(
            vs_target, total)
    elif total >= vs_target:
        target_message = "\nYour target was `{}` and your score is `{}`, you succeeded!".format(
            vs_target, total)
    elif total < vs_target:
        target_message = "\nYour target was `{}` and your score is `{}`, you failed.".format(
            vs_target, total)

    return """__Hero__ @{hero}
__Pool__ **D1** `{d1}` **D2** `{d2}` **DM** `{dm}` **Total** `{total}`{fantastic_message}{extra_message}{target_message}""".format(
        hero=hero,
        d1=d1,
        d2=d2,
        dm=friendly_dm,
        total=total,
        fantastic_message=fantastic_message,
        extra_message=extra_message,
        target_message=target_message
    )


def params(command):
    command_params = re.split(" ", command)
    command_params = [param for param in command_params if param]
    command_params = command_params[1:]
    params = {}
    if len(command_params) == 1:
        param = command_params[0].lower()
        if param in DICE:
            param = param[1]
        elif param.isdigit():
            param = int(param)
        else:
            param = param[0]
        params[param] = True
    else:
        current_param = None
        is_key = True
        for i, param in enumerate(command_params):
            param = param.lower()
            if is_key:
                if param in DICE:
                    is_key = False
                    current_param = param[1]
                elif param.isdigit():
                    is_key = True
                    current_param = param
                else:
                    is_key = False
                    current_param = param[0]

                params[current_param] = True
            else:
                is_key = True
                try:
                    params[current_param] = int(param)
                except:
                    params[current_param] = param

    return collections.OrderedDict(sorted(params.items()))


def d616(cap: captain_dice.CaptainDice, hero, command, params):
    cap.d616(hero, params.get("t") or 0)
    return friendly_reply(cap, hero, command, params)


def edge(cap: captain_dice.CaptainDice, hero, command, params):
    try:
        if params.get("1"):
            cap.edge(hero, "d1")
        elif params.get("2"):
            cap.edge(hero, "d2")
        elif params.get("m"):
            cap.edge(hero, "dm")
        else:
            return "Captain Dice here, you need to specify either `d1, d2, dm` for more help ask `!cap help edge`"
        return friendly_reply(cap, hero, command, params)
    except KeyError:
        return "Captain Dice here, looks like @{} doesn't have a Pool yet, you need to run `!cap d616` first, for more help ask `!cap help edge` or `!cap help d616`".format(hero)


def help(cap: captain_dice.CaptainDice, hero, command, params):
    for key in params:
        if key in commands:
            return DESCRIPTIONS.get(key)
    return "Captain Dice here, I do not know how to help with `{}`. I can help with `help d616|d|pool|p|trouble|t|edge|e|set|s|init|i` commands.".format(command)


def init(cap: captain_dice.CaptainDice, hero, command, params):
    pass


def pool(cap: captain_dice.CaptainDice, hero, command, params):
    return friendly_reply(cap, hero, command, params)


def set(cap: captain_dice.CaptainDice, hero, command, params):
    d1 = params.get("1")
    d2 = params.get("2")
    dm = params.get("m")
    if None in [d1, d2, dm]:
        return "Captain Dice here, if you are wanting to set dice you need to specify all dice for the pool, you have provided me with `D1: {}, D2: {}, DM: {}`. Ask for help `!cap help set`".format(d1, d2, dm)

    if not dm in VALID_DM_VALUES:
        return "Captain Dice here, your DM value can be one of `1, 2, 3, 4, 5, 6, M` and you shared `DM: {}`. Ask for help `!cap help set`".format(dm)
    elif not d1 in VALID_D6_VALUES:
        return "Captain Dice here, your D1 value can be one of `1, 2, 3, 4, 5, 6` and you shared `D1: {}`. Ask for help `!cap help set`".format(d1)
    elif not d2 in VALID_D6_VALUES:
        return "Captain Dice here, your D2 value can be one of `1, 2, 3, 4, 5, 6` and you shared `D2: {}`. Ask for help `!cap help set`".format(d2)

    try:
        dm = dm.lower()
    except:
        pass
    cap.set(hero, d1, d2, dm)

    return friendly_reply(cap, hero, command, params)


def trouble(cap: captain_dice.CaptainDice, hero, command, params):
    trouble_applied = False
    for param in params:
        if isinstance(param, numbers.Number) or param.isdigit():
            cap.trouble(hero, int(param))
            trouble_applied = True
            break
    if not trouble_applied:
        cap.trouble(hero, 1)
    return friendly_reply(cap, hero, command, params)


commands = {
    "d": d616,
    "e": edge,
    "h": help,
    "i": init,
    "p": pool,
    "s": set,
    "t": trouble
}


def default_fn(hero, command, _):
    return "Captain Dice here, sorry @{} I do not know what `{}` is. Run `!cap help` for me to come to the rescue.".format(hero, command)


class Power:
    def __init__(self):
        self.cap = captain_dice.CaptainDice()

    def power(self, hero, hero_request):
        if not hero_request.startswith('!cap'):
            return
        command = re.match("!cap(.*)", hero_request).groups()[0].strip()

        if command == '':
            return default_fn(hero, command)

        fn = commands.get(command[0]) or default_fn
        return fn(self.cap, hero, command, params(command))
