import robot

username = "lukejpreston"
print('==== INIT =====')
print(robot.d616(username))

print('==== EDGE D1 =====')
print(robot.reroll(username, "d1", True))

print('==== EDGE D2 =====')
print(robot.reroll(username, "d2", True))

print('==== EDGE DM =====')
print(robot.reroll(username, "dm", True))

print('==== SET =====')
print(robot.set(username, {"d1": 2, "d2": 2, "dm": 4}))

print('==== DISPLAY =====')
print(robot.display(username, 20))