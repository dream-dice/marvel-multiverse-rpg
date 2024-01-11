import re

import robot


def help(username, command):
    return """
Hey there, it's Captain Dice here

If you need help run
!cap help

If you want to roll a new set of dice
`!cap d616|d <karma:number>`

Examples:
`!cap d616` for normal roll
`!cap d616 1` for normal roll with 1 karma
`!cap d 1` for normal roll with 1 karma, but using the shortcut

If you want to see your current dice
`!cap view|v`

If you want to reroll a dice
`!cap reroll|r d1|d2|dm trouble|t`

Examples
`!cap reroll d1` to reroll your d1
`!cap reroll d2 trouble` to reroll your d1 with trouble
`!cap r dm t` to reroll your dm with trouble

!cap init|i start|s
!cap init|i join|j <username|user:string>
!cap init|i next|n
!cap init|i previous|p
!cap init|i display|d
!cap init|i end|e
    """

def d616(username, command):
    robot.d616(username)

    command_params = split_command(command)
    if len(command_params) > 1:
        try:
            karma = int(command_params[1])
            return robot.display(username, karma)
        except:
            pass

    return robot.display(username)

def view(username, command):
    return robot.display(username)

def reroll(username, command):
    command_params = split_command(command)
    if len(command_params) <= 1:
        return "Captain Dice here, you need to at least specify a d1, d2, dm and you said '{}'. Captain Dice to the rescue `!cap help`!.".format(command)

    die = command_params[1].lower()

    valid_die = die in ["d1", "d2", "dm"]
    if not valid_die:
        return "Captain Dice here, '{}' is not a dice I know. Captain Dice to the rescue `!cap help`!.".format(command_params[1])

    new_value = robot.reroll(username, die, len(command_params) == 2)
    return "rolled: {}, {}".format(new_value, robot.display(username))

def split_command(command):
    command_params = re.split("\W", command)
    return [param for param in command_params if param]

commands = {
    "h": help,
    "d": d616,
    "v": view,
    "r": reroll
}

def default_fn(username, command):
    return "Captain Dice here, sorry @{} I do not know what `{}` is. Run `!cap help` for me to come to the rescue.".format(username, command)

def run_command(username, content):
    if not content.startswith('!cap'):
        return
    command = re.match("!cap(.*)", content).groups()[0].strip()

    fn = commands.get(command[0]) or default_fn
    return fn(username, command)