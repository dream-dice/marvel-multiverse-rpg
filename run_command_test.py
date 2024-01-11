from run_command import run_command

username = "lukejpreston"

def test(command):
    result = run_command(username, command)
    print('run_command({}) = {}'.format(command, result))

print("=== help ===")
test("!cap     help    ")
test("!cap     h    ")

print("=== random ===")
test("!cap     thing")

print("=== d616 ===")
test("!cap d616")
test("!cap     d        ")
test("!cap d     1    ")
test("!cap d     boop    ")

print("=== view ===")
test("!cap view")
test("!cap    v   ")

print("=== reroll ===")
test("!cap reroll d1")
test("!cap reroll d2 trouble")
test("!cap r dm t")
test("!cap r dX t")
test("!cap r")
