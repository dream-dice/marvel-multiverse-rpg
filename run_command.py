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

!cap reroll|r d1|d2|dm edge|e|trouble|t

!cap init|i start|s
!cap init|i join|j <username|user:string>
!cap init|i next|n
!cap init|i previous|p
!cap init|i display|d
!cap init|i end|e
    """

def d616(username, command):
    robot.d616(username)

    command_params = re.split("\W", command)
    command_params = [param for param in command_params if param]
    if len(command_params) > 1:
        try:
            karma = int(command_params[1])
            return robot.display(username, karma)
        except:
            pass

    return robot.display(username)

def view(username, command):
    return robot.display(username)

commands = {
    "h": help,
    "d": d616,
    "v": view
}

def default_fn(username, command):
    return "Captain Dice here, sorry @{} I do not know what `{}` is. Run `!cap help` for me to come to the rescue.".format(username, command)

def run_command(username, content):
    if not content.startswith('!cap'):
        return
    command = re.match("!cap(.*)", content).groups()[0].strip()

    fn = commands.get(command[0]) or default_fn
    return fn(username, command)