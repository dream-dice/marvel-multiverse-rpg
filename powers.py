import re
import collections
import numbers

import captain_dice
from power_descriptions import DESCRIPTIONS


VALID_D6_VALUES = [1, 2, 3, 4, 5, 6]
VALID_DM_VALUES = VALID_D6_VALUES + ["m", "M"]
DICE = ["d1", "d2", "dm"]


def friendly_reply(cap: captain_dice.CaptainDice, hero, hero_name, command, params, message=''):
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

    if message:
        message = "{}\n".format(message)

    return """{message}__Hero__ @{hero}
__Pool__ **D1** `{d1}` **D2** `{d2}` **DM** `{dm}` **Total** `{total}`{fantastic_message}{extra_message}{target_message}""".format(
        message=message,
        hero=hero_name,
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


def trouble_message(rolled):
    return "Captain Dice here, I have rolled a trouble for you, the results are:\n{}".format("\n".join(map(str, rolled)))

def d616(cap: captain_dice.CaptainDice, hero, hero_name, command, params):
    trouble_rolled = cap.d616(hero, params.get("t") or 0)
    if trouble_rolled and len(trouble_rolled) > 0:
        message = trouble_message(trouble_rolled)
        return friendly_reply(cap, hero, hero_name, command, params, message)
    return friendly_reply(cap, hero, hero_name, command, params)


def edge(cap: captain_dice.CaptainDice, hero, hero_name, command, params):
    try:
        new_value = ''
        original_value = ''
        if params.get("1"):
            original_value = cap.pool(hero).get("d1")
            new_value = cap.edge(hero, "d1")
        elif params.get("2"):
            original_value = cap.pool(hero).get("d2")
            new_value = cap.edge(hero, "d2")
        elif params.get("m"):
            original_value = cap.pool(hero).get("dm")
            new_value = cap.edge(hero, "dm")
        else:
            return "Captain Dice here, you need to specify either `d1, d2, dm` for more help ask `!cap help edge`"

        message = "Captain Dice here, your value is still `{}` as I rolled a `{}`".format(original_value, new_value)

        if (params.get("m") and new_value == 1 and original_value != 1):
            message = "Captain Dice here, your new value is `{}` replacing `{}`".format('M', original_value)
        elif (new_value > original_value):
            message = "Captain Dice here, your new value is `{}` replacing `{}`".format(new_value, original_value)
            
        return friendly_reply(cap, hero, hero_name, command, params, message)

    except KeyError:
        return "Captain Dice here, looks like @{} doesn't have a Pool yet, you need to run `!cap d616` first, for more help ask `!cap help edge` or `!cap help d616`".format(hero)


def help(cap: captain_dice.CaptainDice, hero, hero_name, command, params):
    for key in params:
        if key in commands:
            return DESCRIPTIONS.get(key)
    if len(params) == 0:
        return "Captain Dice here, I can help with `d616|d|pool|p|trouble|t|edge|e|set|s|init|i` commands."
    return "Captain Dice here, I do not know how to help with `{}`. I can help with `help d616|d|pool|p|trouble|t|edge|e|set|s|init|i` commands.".format(command)


def init(cap: captain_dice.CaptainDice, hero, hero_name, command, params):
    pass


def pool(cap: captain_dice.CaptainDice, hero, hero_name, command, params):
    return friendly_reply(cap, hero, hero_name, command, params)


def set(cap: captain_dice.CaptainDice, hero, hero_name, command, params):
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

    return friendly_reply(cap, hero, hero_name, command, params)


def trouble(cap: captain_dice.CaptainDice, hero, hero_name, command, params):
    trouble_applied = False
    rolled = []
    for param in params:
        if isinstance(param, numbers.Number) or param.isdigit():
            rolled = cap.trouble(hero, int(param))
            trouble_applied = True
            break
    if not trouble_applied:
        rolled = cap.trouble(hero, 1)

    return friendly_reply(cap, hero, hero_name, command, params, trouble_message(rolled))


commands = {
    "d": d616,
    "e": edge,
    "h": help,
    "i": init,
    "p": pool,
    "s": set,
    "t": trouble
}


def default_fn(self, hero, hero_name, command, _):
    return "Captain Dice here, sorry @{} I do not know what `{}` is. Run `!cap help` for me to come to the rescue.".format(hero_name, command)


class Power:
    def __init__(self):
        self.cap = captain_dice.CaptainDice()

    def power(self, hero, hero_name, hero_request):
        if not hero_request.startswith('!cap'):
            return
        command = re.match("!cap(.*)", hero_request).groups()[0].strip()

        if command == '':
            return default_fn(hero, hero_name, command)

        fn = commands.get(command[0]) or default_fn
        return fn(self.cap, hero, hero_name, command, params(command))
