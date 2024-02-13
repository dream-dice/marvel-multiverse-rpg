from captain_dice import CaptainDice

hero = "lukejpreston"

cap = CaptainDice()

print('=== set ===')
cap.set(hero, 1, 2, 3)
print(cap.pool(hero))

print('=== trouble ===')
cap.set(hero, 6, 6, 1)
print(cap.pool(hero))
cap.trouble(hero, trouble=100)
print(cap.pool(hero))

print('=== edge ===')
cap.set(hero, 1, 1, 2)
print(cap.pool(hero))
cap.edge(hero, "d1")
print(cap.pool(hero))
cap.edge(hero, "d2")
print(cap.pool(hero))
cap.edge(hero, "dm")
print(cap.pool(hero))

print('=== d616 ===')
cap.set(hero, 6, 6, 1)
print(cap.pool(hero))
cap.d616(hero)
print(cap.pool(hero))
cap.d616(hero, trouble=100)
print(cap.pool(hero))

print('=== init ===')
print(cap.init(hero, 1234))

