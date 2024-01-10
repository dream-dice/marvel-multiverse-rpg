import re

import robot


def help(username, command):
    return """
Hey there, it's Captain Dice here

If you need help run
!cap help

If you want to roll a new set of dice run
!cap d616|d <karma:number>

Examples:
`!cap d616` for normal roll
`!cap d616 1` for normal roll with 1 karma
`!cap d 1` for normal roll with 1 karma, but using the shortcut

!cap reroll| d1|d2|dm edge|e|trouble|t
!cap view|v
!cap init|i start|s
!cap init|i join|j <username|user:string>
!cap init|i next|n
!cap init|i previous|p
!cap init|i display|d
!cap init|i end|e
    """

commands = {
    "help": help
}

def default_fn(username, command):
    return "Captain Dice here, sorry @{} I do not know what `{}` is. Run `!cap help` for me to come to the rescue.".format(username, command)

def run_command(username, content):
    if not content.startswith('!cap'):
        return
    command = re.match("!cap(.*)", content).groups()[0].strip()

    fn = commands.get(command) or default_fn
    return fn(username, command)