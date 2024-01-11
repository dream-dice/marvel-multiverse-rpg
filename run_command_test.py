from run_command import run_command

username = "lukejpreston"

def test(command):
    result = run_command(username, command)
    print('run_command({}) = {}'.format(command, result))

print("=== HELP ===")
test("!cap     help    ")

print("=== RANDOM ===")
test("!cap     thing")

print("=== d616 ===")
test("!cap d616")
test("!cap     d        ")
test("!cap d     1    ")
test("!cap d     boop    ")

print("=== view ===")
test("!cap view")
test("!cap    v   ")